let ELEMENTS = 256
let cycles = 1000
let tokens = 150


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

    print "start"

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

    print "end"
    print sum
    next <- 0
    token = <:this
}

let ring = fn(cycles, tokens) {
    let head = chan()
    let this = head
    let next = 0
    let i = 0
    let elems = ELEMENTS - 1
    while i < elems {
        i = i + 1
        next = chan()
        async element(this, next)
        this = next
    }

    let t = root(cycles, tokens, this, head)
}

ring(cycles, tokens)
