let n = 1000
let x = list(n)
let y = list(n)
let i = 0

while i < n {
    x[i] = i
    i = i + 1
}

i = n
while i > 0 {
    i = i - 1
    y[i] = x[i]
}

i = 0

while i < n {
    print x[i]
    i = i + 1
}

i = 0
while i < n {
    print y[i]
    i = i + 1
}
