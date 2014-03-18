let func_a = fn(channela, channelb) {
    print <: channela
    print <: channelb
}

let chana = chan()
let chanb = chan()
async func_a(chana, chanb)

chana <- 10
chanb <- 100
