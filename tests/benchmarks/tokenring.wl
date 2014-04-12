let ELEMENTS = 256
let cycles = int(args[1])
let tokens = int(args[2])


let element = fn(this, next) {
    while true {
        let token = <:this
        if token > 0 {
            next <- token + 1
            continue
        }

        next <- token
        break
    }
}

let root = fn(cycles, tokens, this, next) {
    next <- 1
    let token = <:this

    let i = 0
    while i < tokens {
        i = i + 1
        next <- i
    }

    while cycles > 0 {
        let i = 0
        while i < tokens {
            i = i + 1
            token = <:this
            next <- token + 1
        }
        cycles = cycles - 1
    }

    let sum = 0
    i = 0
    while i < tokens {
        i = i + 1
        sum = sum + <:this
    }

    next <- 0
    token = <:this
}

let ring = fn(cycles, tokens) {
    let head = chan()
    let this = head
    let next = 0
    let i = 0
    let elems = ELEMENTS
    while i < elems {
        i = i + 1
        next = chan()
        async element(this, next)
        this = next
    }

    root(cycles, tokens, this, head)
}


let warmup = 5
let i = warmup

while i >= 0 {
    i = i - 1
    ring(cycles, tokens)
}

let sum = 0
let tries = 10
i = tries
while i > 0 {
    i = i - 1
    let start = time()
    ring(cycles, tokens)
    let end = time()
    sum = sum + (end - start)
}

print "nau-tokenring(" + cycles + ", " + tokens + "): total: iterations=" + tries + " runtime: " + sum +"us"
