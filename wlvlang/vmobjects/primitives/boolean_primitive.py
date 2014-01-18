from wlvlang.vmobjects.boolean import Boolean

def _eq(invokable, activation_record, interpreter):
    right = activation_record.pop()
    left = activation_record.pop()

    result = left.get_value() == right.get_value()
    activation_record.push(Boolean(result))

def _or(invokable, activation_record, interpreter):
    right = activation_record.pop()
    left = activation_record.pop()

    result = left.get_value() or right.get_value()
    activation_record.push(Boolean(result))
