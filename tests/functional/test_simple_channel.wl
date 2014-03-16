let chan_x = chan()
let chan_y = chan()

chan_x <- 10 * 10
chan_y <-<: chan_x
print <: chan_y
