let func_a = fn(chan_in, chan_out) {
	chan_in <-<: chan_out
}

let i = 1000000

let chan_start = chan()
chan_start <- 200

let chan_in = chan_start
let chan_out = chan()
let chan_end = chan_out

while i > 0 {
	async func_a(chan_in, chan_out)
	chan_in = chan_out
	chan_end = chan_out
	chan_out = chan()
	i = i - 1
}

print <: chan_end
