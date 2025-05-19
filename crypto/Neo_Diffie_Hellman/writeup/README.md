# Neo Diffie Hellman

This challenge implements the Diffie–Hellman key exchange protocol over a matrix group, where matrices have entries in a finite field. You are provided with the generator matrix G, the modulus p, and two public key components: pub_a and pub_b.

Your goal is to solve the discrete logarithm problem in the given matrix group. Since this type of DLP is not natively supported in SageMath, you are expected to implement a suitable algorithm yourself. One such algorithm is described as Algorithm 3.3 in the paper [The Discrete Logarithm Problem in Matrix Groups](http://theory.stanford.edu/~dfreeman/papers/discretelogs.pdf)

Note: Due to the specific structure of the matrices used in this challenge, Step 5 of Algorithm 3.3 will never be reached during execution, so it does not need to be implemented correctly for this challenge.

By solving the matrix DLP, you can recover the secret exponent `secret_a` such that:

```
G^secret_a = pub_a
```

Once secret_a is known, you can compute the shared secret by evaluating:

```
shared_secret = pub_b^secret_a
```

This shared secret can then be used to decrypt the flag.

A reference script is provided in [healthcheck.sage](./healthcheck.sage)