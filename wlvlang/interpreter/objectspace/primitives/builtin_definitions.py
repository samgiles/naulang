import time

from rpython.rlib.rarithmetic import ovfcheck_float_to_int

def builtin_functions():
    """ Returns a map of builtin function definitions with values:

        "function_name" -> (_invokable_function, unique_index)

        unique index identifies this method instead of its name
    """
    return {
        "list": (_list_primitive, 0),
        "time": (_time_primitive, 1),
        "int" : (_int_primitive,  2),
        "chan": (_channel_primitive, 3),
    }

def _time_primitive(primitive, activation_record):
    # Returns an integer representing a point in time. Should be used for benching
    activation_record.push(primitive.space.new_integer(ovfcheck_float_to_int(time.time() * 1000000)))

def _int_primitive(primitive, activation_record):
    # Parse a value into an integer
    string = activation_record.pop()
    activation_record.push(primitive.space.new_integer(int(string.get_as_string())))

def _list_primitive(primitive, activation_record):
    """ Creates a new array/list object and pushes onto stack """
    size = activation_record.pop()
    activation_record.push(primitive.space.new_array((size.get_integer_value())))

def _channel_primitive(primitive, activation_record):
    """ Creates a new channel object """
    activation_record.push(primitive.space.new_channel())
