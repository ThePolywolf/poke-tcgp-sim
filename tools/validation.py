
def validate_type(obj, required_type) -> None:
    """
    Validates that the object is of type required_type. Throws an exception if not.
    :param obj: object to check
    :param required_type: object must be this type
    :return: None | Raises TypeError
    """
    if not isinstance(obj, required_type):
        raise TypeError(f"Obj must be a {required_type.__name__}")
