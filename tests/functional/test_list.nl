let x = list(10)

let i = 0

while i < 10 {
    x[i] = i
    i = i + 1
}

i = 0

while i < 10 {
    print x[i]
    i = i + 1
}
