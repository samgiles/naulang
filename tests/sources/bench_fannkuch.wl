n = 12
fact = list(n+1)

fact[0] = 1

i = 1

while i < n + 1 {
    fact[i] = fact[i - 1] * i
    i = i + 1
}

chunksz = (fact[n] + nchunks - 1) / NCHUNKS
chunksz = chunksz + (chunksz % 2)

fannkuch = fn(idxMin) {

    idxMax = idxMin + chunks

    if idxMax < fact[n] {
        fannkuch(idxMax)
    } else {
        idxMax = fact[n]
    }

    p = list(n)
    pp = list(n)
    count = list(n)

    # First permutation
    i = 0
    while i < n {
        p[i] = i
        i = i + 1
    }

    i = n - 1
    idx = idxMin

    while i > 0 {
        d = idx / fact[i]
        count[i] = d
        idx = idx % fact[i]

        copy(pp, p)

        j = 0

        while j <= i {

            if j + d <= i {
                p[j] = pp[j + d]
            } else {
               p[j] = pp[j + d - i - 1]
            }

            j = j + 1
        }

        i = i - 1
    }

    maxFlips = 1
    checkSum = 0

    idx = idxMin
    sign = true

    while true {

        # Count flips
        first = p[0]

        if first != 0 {
            flips = 1
            if p[first] != 0 {
                copy(pp, p)
                p0 = first

                while true {
                    flips = flips + 1
                    i = 1
                    j = p0 - 1

                    while i < j {
                        tmp = pp[i]
                        pp[i] = pp[j]
                        pp[j] = tmp
                        i = i + 1
                        j = j - 1
                    }

                    t = pp[p0]
                    pp[p0] = p0
                    p0 = t
                    if pp[p0] == 0 {
                        break
                    }
                }
            }

            if maxFlips < flips {
                maxFlips = flips
            }

            if sign {
                checkSum = checkSum + flips
            } else {
                checksum = checksum - flips
            }
        }

        idx = idx + 1

        if idx == idxMax {
            break
        }

        if sign {
            p[0] = p[1]
            p[1] = first
        } else {
            tmp = p[1]
            p[1] = p[2]
            p[2] = tmp

            k = 2

            while true {
                count[k] = count[k] + 1
                if count[k] <= k {
                    break
                }

                count[k] = 0

                j = 0
                while j <= k {
                    p[j] = p[j + 1]
                    j = j + 1
                }

                p[k + 1] = first
                k = k + 1
            }
        }
        sign = not sign
    }

    print maxFlips
    print checkSum
}

fannkuch(0)
