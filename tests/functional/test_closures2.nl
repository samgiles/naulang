let f = fn(b, x) {
	return b(fn(y) {
		return x + y
	})
}

print f(fn(x) {
	return x(10)
}, 15)
