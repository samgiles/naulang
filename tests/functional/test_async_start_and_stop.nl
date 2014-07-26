let i = 4
let sum = 0

let function_async = fn(channel, next, value) {
    while true {
        let n = <:channel

        if n is 0 {
            next <- 0
            return
        }

        next <- n + value
    }
}

let starter = fn(seed) {
    let counter = 0
    let head = chan()
    let this = head
    while counter < i  {
        counter = counter + 1
        let next = chan()
        async function_async(this, next, 10)
        this = next
    }

    head <- seed

    sum = sum + <:this

    print sum

    head <- 0

    <:this
}

let counter = 1
while counter <= i {
    starter(counter)
    counter = counter + 1
}

print sum
