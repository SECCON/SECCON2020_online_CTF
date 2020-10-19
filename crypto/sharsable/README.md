# sharsable (257pt, 12 solves)
## Overview
Low private exponent attack for original RSA variant

## Problem
You must collect exponents from Alice and Bob.

## Algorithm
### Key Generation
```
e1 * d1 + e2 * d2 = 1 mod phi(n)
```

### Encryption
```
c1 = m^e1 mod n
c2 = m^e2 mod n
```

### Decryption
```
m = c1^d1 * c2^d2 mod n
```

# Solution
[solve.sage](solver/solve.sage)
