let n = 10

let f = fn(x) {
    return fn(y) {
        return x + y + n
    }
}

let a = f(100)
let b = f(200)

print a(2)
print a(4)
print b(8)
print b(16)
