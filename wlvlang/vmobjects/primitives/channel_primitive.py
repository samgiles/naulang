def _push(activation_record, interpreter):
    channel = activation_record.pop()
    value = activation_record.pop()
    channel.queue.push(value)

def _pop(activation_record, interpreter):
    channel = activation_record.pop()
    value = channel.queue.pop()
    activation_record.push(value)


def init_channel_prims(universe):
    primitives = {
        "->": _push,
        "<-": _pop
    }
    universe.channelClass.add_primitives(primitives)
