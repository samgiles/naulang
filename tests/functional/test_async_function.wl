let ring_node = fn(in, out) {
	out <-<: in
}

let i = 5

let start = chan()
start <- 200

let in = start
let out = chan()
let end = out

while i > 0 {
	async ring_node(in, out)
	in = out
	end = out
	out = chan()
	i = i - 1
}

print <: end
