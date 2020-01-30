class InvalidAliasException(BaseException):
    """Invalid Alias found in metadata, raised when duplicate alias is found"""
    pass


class DuplicateAliasException(BaseException):
    """Duplicate Alias has been detected, this is a serious error. Notify the developer immediately."""
    pass
