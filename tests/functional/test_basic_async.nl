let a_function = fn(channela, channelb) {
    print <: channela
    print <: channelb
}

let chana = chan()
let chanb = chan()

async a_function(chana, chanb)

chana <- 10
chanb <- 100
