	.file	"vuln_template.c"
	.intel_syntax noprefix
	.text
	.section	.rodata
.LC0:
	.string	"/bin/sh"
	.text
	.globl	_start
	.type	_start, @function
_start:
.LFB0:
	.cfi_startproc
	push	rbp
	.cfi_def_cfa_offset 16
	.cfi_offset 6, -16
	mov	rbp, rsp
	.cfi_def_cfa_register 6
	sub	rsp, 32
	mov	rax, QWORD PTR execve@GOTPCREL[rip]
	mov	QWORD PTR -24[rbp], rax
	lea	rax, -32[rbp]
	mov	edx, 32
	mov	rsi, rax
	mov	edi, 0
	//call	[QWORD PTR read@GOTPCREL[rip]]
	mov     eax, 0
	syscall
	mov	rax, QWORD PTR -24[rbp]
	mov	edx, 0
	mov	esi, 0
	lea	rdi, .LC0[rip]
	call	rax
	nop
	leave
	.cfi_def_cfa 7, 8
	ret
	.cfi_endproc
.LFE0:
	.size	_start, .-_start
	.ident	"GCC: (Debian 8.3.0-6) 8.3.0"
	.section	.note.GNU-stack,"",@progbits
