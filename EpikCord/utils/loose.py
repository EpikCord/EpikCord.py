def clear_none_values(d: dict):
    """
    Clears all the values in a dictionary that are None.
    """
    return {k: v for k, v in d.items() if v is not None}