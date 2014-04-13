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

let i = 0
while i < 1000 {
    i = i + 1
    let prime = <:channel
    print prime
    let ch1 = chan()
    async sieve(channel, ch1, prime)
    channel = ch1
}
