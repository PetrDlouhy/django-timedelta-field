__version__ = "0.5.1"

try:
    from fields import TimedeltaField
    from helpers import divide, multiply, modulo, parse, nice_repr, percentage
except ImportError:
    pass