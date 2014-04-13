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

let checksum = run_prime_sieve(1000)
print checksum
