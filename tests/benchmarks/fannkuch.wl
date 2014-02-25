let fannkuch = fn(n) {

    let perm = list(n)
    let perm1 = list(n)
    let count = list(n)

    let maxflipscount = 0
    let permcount = 0
    let checksum = 0

    let i = n

    while i > 0 {
       i = i - 1
       perm[i] = i
       perm1[i] = i
       count[i] = i
    }

    let r = n

    while true {
        while r != 1 {
            count[r - 1] = r
            r = r - 1
        }

        i = 0
        while i < n {
            perm[i] = perm1[i]
            i = i + 1
        }

        let flipscount = 0
        let k = perm[0]

        while k != 0 {
            let k2 = (k + 1) / 2

            i = 0
            while i < k2 {
                let temp = perm[i]
                perm[i] = perm[k - i]
                perm[k - i] = temp
                i = i + 1
            }
            flipscount = flipscount + 1
            k = perm[0]
        }

        if flipscount > maxflipscount {
            maxflipscount = flipscount
        }

        checksum = checksum + -flipscount

        if (permcount % 2) == 0 {
            checksum = checksum + (flipscount + flipscount)
        }

        while true {
            if r == n {
                return maxflipscount
            }

            let perm0 = perm1[0]
            i = 0

            while i < r {
                let j = i + 1
                perm1[i] = perm1[j]
                i = j
            }

            perm1[r] = perm0

            count[r] = count[r] - 1

            if count[r] > 0 {
                break
            }

            r = r + 1
        }

        permcount = permcount + 1
    }
}

let n = int(args[1])

let i = 0
let warmup = 5

while i < warmup {
    fannkuch(n)
    i = i + 1
}

let runs = 10
let t0 = 0
let t1 = 0
i = 0

let total = 0

while runs >= 0 {
    runs = runs - 1
    t0 = time()
    fannkuch(n)
    t1 = time()
    total = total + (t1 - t0)
}

print "fannkuch(" + n + "): total: iterations=10 runtime: " + total + "us"
