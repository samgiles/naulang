from naulang.interpreter.objectspace.object import Object
class PrimitiveObject(Object):

    def w_eq(self, frame, space):
        raise NotImplementedError()

    def w_or(self, frame, space):
        raise NotImplementedError()

    def w_and(self, frame, space):
        raise NotImplementedError()

    def w_print(self, frame, space):
        raise NotImplementedError()

    def w_mul(self, frame, space):
        raise NotImplementedError()

    def w_add(self, frame, space):
        raise NotImplementedError()

    def w_sub(self, frame, space):
        raise NotImplementedError()

    def w_div(self, frame, space):
        raise NotImplementedError()

    def w_mod(self, frame, space):
        raise NotImplementedError()

    def w_neg(self, frame, space):
        raise NotImplementedError()

    def w_not(self, frame, space):
        raise NotImplementedError()

    def w_lt(self, frame, space):
        raise NotImplementedError()

    def w_lteq(self, frame, space):
        raise NotImplementedError()

    def w_gt(self, frame, space):
        raise NotImplementedError()

    def w_gteq(self, frame, space):
        raise NotImplementedError()
