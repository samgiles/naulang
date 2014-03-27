let f = fn(x) {
    return fn(y) {
        return y * x
    }
}

let a = f(10)
print a(30)
