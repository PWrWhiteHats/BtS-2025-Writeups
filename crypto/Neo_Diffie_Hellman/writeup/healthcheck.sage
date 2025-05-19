from hashlib import sha256
from Crypto.Cipher import AES
from Crypto.Util.Padding import unpad

# Algorithm 3.3 from paper
def find_exponent(A, B, q):
    n = A.nrows()
    p = Integer(q).prime_factors()[0]

    # Step 1: Compute characteristic polynomial of A
    fA = A.charpoly()

    # Step 2: Factor into irreducible polynomials
    factors = fA.factor()
    factors = [g for (g, _) in factors]

    # Initialize variables
    xis = []
    moduli = []
    x0 = None

    # Iterate over each irreducible factor
    for g_i in factors:
        d_i = g_i.degree()
        if d_i == 0:
            continue

        # Step 4.1: Construct field extension K with a root alpha_i of g_i
        K = GF(q**d_i, 'a', modulus=g_i)
        alpha_i = K.gen()

        A_K = A.change_ring(K)
        B_K = B.change_ring(K)

        # Step 4.2: Find eigenvector for alpha_i
        M = A_K - alpha_i * matrix.identity(K, n)
        V = M.right_kernel()
        if V.dimension() == 0:
            raise ValueError("No eigenvectors found for eigenvalue alpha_i")
        v = V.basis()[0]

        # Step 4.3: Compute beta as eigenvalue of B corresponding to v
        Bv = B_K * v
        non_zero_indices = [i for i in range(n) if v[i] != 0]
        if not non_zero_indices:
            raise ValueError("Eigenvector is zero vector")
        k = non_zero_indices[0]
        beta = Bv[k] / v[k]

        # Step 4.4: Compute x_i = log_alpha_i(beta)
        try:
            x_i = beta.log(alpha_i)
        except ValueError:
            raise ValueError(
                f"Discrete log failed for beta={beta}, alpha_i={alpha_i}")
        order_alpha = alpha_i.multiplicative_order()
        xis.append(x_i)
        moduli.append(order_alpha)

        # Step 4.5: Check if eigenspaces dimensions equal multiplicities
        fA_K = fA.change_ring(K)
        factors_K = fA_K.factor()
        all_ok = True
        lambda_bad = None
        for (poly, exp) in factors_K:
            if poly.degree() == 1:
                mu = -poly.constant_coefficient()
                M_mu = A_K - mu * matrix.identity(K, n)
                geo_mult = M_mu.right_kernel().dimension()
                if geo_mult < exp:
                    all_ok = False
                    lambda_bad = mu
                    break
        if all_ok:
            continue

        # non-diagonalizable case doesn't occur

    # Apply Chinese Remainder Theorem
    if not xis:
        raise ValueError("No congruences found")

    try:
        y = CRT(xis, moduli)
    except ValueError:
        raise ValueError("CRT failed for xis and moduli")

    if x0 is None:
        x = y
    else:
        M = LCM(moduli)
        if M % p == 0:
            raise ValueError("Moduli and p are not coprime")
        x = CRT([Integer(x0), Integer(y)], [Integer(p), Integer(M)])

    return x


p = 1000117
Fq = GF(p)
G = matrix(Fq, [[8544, 7125, 942, 1054, 2338, 8223, 1149, 3981],
                [7803, 9243, 6830, 8788, 9576, 1916, 7762, 5861],
                [9026, 9381, 9235, 994, 6194, 508, 7351, 1406],
                [6410, 6445, 6086, 653, 1783, 4564, 8874, 4739],
                [2797, 8921, 113, 1078, 6810, 7392, 3659, 1316],
                [1688, 1010, 631, 6495, 7379, 5804, 7237, 527],
                [2211, 4452, 1519, 498, 9284, 3282, 9628, 4355],
                [1267, 9413, 3340, 2316, 8627, 1310, 4481, 4808]])

A = matrix(Fq, [[535437, 436702, 226549,  36181, 121389, 153630, 731259, 540567],
                [907971, 938518, 894603, 755768, 216225, 593672, 741423,  23476],
                [722305, 647423, 326338, 242088, 488457, 728979, 922735, 747889],
                [297685, 306919, 290639,  27509,   2322, 325140, 477421, 280920],
                [29774, 527786, 611495, 899899, 521717, 533020, 146923, 228648],
                [220169, 473019, 557359, 889119, 915468, 309429, 426937, 289970],
                [353297, 925012, 273876, 541080, 490035, 332930, 328121, 278415],
                [486511, 551604, 110330, 675237,  32977, 360728, 468534, 470750]])

B = matrix(Fq, [[278458,  53534, 847067, 639466, 299135, 226889,  76846, 630318],
                [389389, 394186, 698985, 793202, 290495, 837646, 870685, 718848],
                [758075, 979002, 904988, 856135, 697027, 565219, 562831, 586066],
                [610508, 496282, 719959, 310184, 841117, 700200, 225924, 938975],
                [553891, 268611,  42248, 348624, 769549, 609875, 442900, 984258],
                [397633, 478352, 880372, 982228, 238901,  18500, 192661, 872537],
                [927550, 649966, 414777, 456967, 907846, 112230, 445766, 510641],
                [554075, 858774, 422448, 789101, 664939, 373076, 823091, 439356]])



secret_a = find_exponent(G, A, p)

iv = bytes.fromhex('dd389f38c4980b66ac5fd4c9cd5a7484')
flag = bytes.fromhex('a514a4defc7a3c6a1024641231b6fb8b255f234ff6100aff911ff4b5b6a7990f5210c1768977d0dd900e323ab320ed67')

key = B ^ secret_a
flattened = key.list()
matrix_bytes = ",".join(map(str, flattened)).encode('utf-8')

key = sha256(matrix_bytes).digest()

cipher = AES.new(key, AES.MODE_CBC, iv)
flag = unpad(cipher.decrypt(flag), 16)
print(flag)
