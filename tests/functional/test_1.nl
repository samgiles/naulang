
let f = fn(x) {
    let n = 50
    return fn(y) {
        return y * x + n
    }
}

let a = f(10)
let b = f(20)

print a(2)
print a(4)
print b(2)
print b(4)
