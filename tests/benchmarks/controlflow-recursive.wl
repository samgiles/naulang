let ack = fn(m, n) {
    if m == 0 {
        return n + 1
    }

    if n == 0 {
        return ack(m - 1, 1)
    }

    return ack(m - 1, ack(m, n - 1))
}

let fib = fn(n) {
    if n < 2 {
        return 1
    }

    return fib(n - 2) + fib(n - 1)
}

let tak = fn(x, y, z) {
    if y >= x {
        return z
    }

    return tak(tak(x-1, y, z), tak(y-1, z, x), tak(z-1, x, y))
}

let i = 3

while i <= 5 {
    ack(3, i)
    fib(17 + i)
    tak(3*i+3, 2*i+2, i+1)

    i = i + 1
}

