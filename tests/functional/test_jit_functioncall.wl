
let i = 1

let m = fn(x) {
    return x * 2
}

while i < 100000000 {
    i = m(i) + i
}
print i
