let run_prime_sieve = fn(n) {
    let sieve = fn(left, right, prime) {
        while true {
            let i =<: left
            if (i % prime) != 0 {
                right <- i
            }
        }
    }

    let generate = fn(channel) {
        let i = 2
        while true {
            channel <- i
            i = i + 1
        }
    }
    let channel = chan()
    async generate(channel)

    let sum = 0
    let i = 0
    while i < n {
        i = i + 1
        let prime = <:channel
        sum = sum + prime
        let ch1 = chan()
        async sieve(channel, ch1, prime)
        channel = ch1
    }

    return sum
}


let primes_to = 100

let warmup = 100
let i = 0
while i < warmup {
	i = i + 1
	let checksum = run_prime_sieve(100)
}

let totaltime = 0
let iterations = 1
let i = 0
while i < iterations {
	i = i + 1
	let t0 = time()
	let checksum = run_prime_sieve(primes_to)
	let t1 = time()
	totaltime = totaltime + (t1 - t0)
}


print "nau-primeseive(" + primes_to + "): total: iterations=" + iterations + " runtime: " + totaltime +"us"
