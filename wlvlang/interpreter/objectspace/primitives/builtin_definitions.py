import time

def builtin_functions():
    """ Returns a map of builtin function definitions with values:

        "function_name" -> (_invokable_function, unique_index)

        unique index identifies this method instead of its name
    """
    return {
        "list": (_list_primitive, 0),
        "time": (_time_primitive, 1),
        "int" : (_int_primitive,  2),
    }

def _time_primitive(primitive, activation_record, interpreter):
    # Returns an integer representing a point in time. Should be used for benching
    activation_record.push(interpreter.universe.new_integer(int(time.time() * 1000000)))

def _int_primitive(primitive, activation_record, interpreter):
    # Parse a value into an integer
    string = activation_record.pop()
    activation_record.push(interpreter.universe.new_integer(int(string.get_as_string())))

def _list_primitive(primitive, activation_record, interpreter):
    """ Creates a new array/list object and pushes onto stack """
    size = activation_record.pop()
    activation_record.push(interpreter.universe.new_array((size.get_integer_value())))
