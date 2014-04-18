from wlvlang.interpreter.objectspace.primitive_object import PrimitiveObject

class String(PrimitiveObject):

    _immutable_fields_ = ['string']
    def __init__(self, value):
        self.string = value

    def get_string_value(self):
        return self.string

    def get_as_string(self):
        return self.string

    def __str__(self):
        return "\"" + self.string + "\""

    def w_add(self, activation_record, space):
        left = activation_record.pop()
        right = activation_record.pop()

        result = space.new_string(left.get_as_string() + right.get_as_string())
        activation_record.push(result)

    def w_print(self, activation_record, space):
        top = activation_record.pop()
        print top.get_as_string()
