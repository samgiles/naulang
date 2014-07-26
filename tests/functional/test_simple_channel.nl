let chan_x = async_chan()
let chan_y = async_chan()

chan_x <- 10 * 10
chan_y <-<: chan_x
print <: chan_y
