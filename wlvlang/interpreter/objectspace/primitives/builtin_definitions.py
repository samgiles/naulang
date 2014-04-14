import time

from wlvlang.interpreter.objectspace.string import String
from wlvlang.interpreter.objectspace.float import Float
from wlvlang.interpreter.objectspace.integer import Integer

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
        "async_chan": (_async_channel_primitive, 4),
    }

def _time_primitive(primitive, activation_record, interpreter):
    # Returns an integer representing a point in time. Should be used for benching
    activation_record.push(interpreter.space.new_integer(ovfcheck_float_to_int(time.time() * 1000000)))

def _int_primitive(primitive, activation_record, interpreter):
    # Parse a value into an integer
    value = activation_record.pop()
    if isinstance(value, String):
        activation_record.push(interpreter.space.new_integer(int(value.get_as_string())))
    elif isinstance(value, Float):
        activation_record.push(interpreter.space.new_integer(int(value.get_float_value())))
    elif isinstance(value, Integer):
        activation_record.push(value)
    else:
        activation_record.push(interpreter.space.new_integer(int(value.get_as_string())))

def _list_primitive(primitive, activation_record, interpreter):
    """ Creates a new array/list object and pushes onto stack """
    size = activation_record.pop()
    activation_record.push(interpreter.space.new_array((size.get_integer_value())))

def _channel_primitive(primitive, activation_record, interpreter):
    """ Creates a new channel object """
    activation_record.push(interpreter.space.new_channel())

def _async_channel_primitive(primitive, frame, interpreter):
    """ Creates a new buffered channel object """
    frame.push(interpreter.space.new_asyncchannel())
