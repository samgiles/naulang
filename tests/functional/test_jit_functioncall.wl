
let i = 1

let m = fn(x) {
    return x * 2
}

while i < 100000 {
    i = (m(i) - i) + 1
}
print i
