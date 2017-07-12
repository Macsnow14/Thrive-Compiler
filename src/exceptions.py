"""
this module contains thrilang compiler's exception.
"""
class ParseException(Exception):
    """
    raise when detect an invalid token.
    """
    pass


class InvalidTokenException(Exception):
    """
    raise when detect an invalid symbol.
    """
    pass


class TransformException(Exception):
    """
    raise when detect an invalid node.
    """
    pass
