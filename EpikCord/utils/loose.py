def clear_none_values(d: dict):
    """
    Clears all the values in a dictionary that are None.
    """
    for key in list(d.keys()):
        if d[key] is None:
            del d[key]
    return d
