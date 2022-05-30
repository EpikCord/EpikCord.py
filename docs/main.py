from inspect import isclass, isfunction, iscoroutine, signature, _empty, getdoc
import EpikCord


def document_method(method):
    method_name = method.__name__
    to_append = "\n"

    if iscoroutine(method):
        to_append += "async "

    def type_of(annotation):
        if isclass(annotation) and annotation != _empty:
            return annotation.__name__
        return "Any"

    sig = signature(method)
    to_append += f"def {method_name}({', '.join([f'{param.name}: {type_of(param.annotation)}' for param in sig.parameters.values()])}) -> {sig.return_annotation if sig.return_annotation != _empty else 'None'}"
    

    if getdoc(method):
        to_append += f"{getdoc(method)}\n"

    return f"{to_append}\n"


def document_class(cls):
    m = ""

    m += f"\n\n{cls.__name__}\n{''.join(['-' for _ in range(len(cls.__name__))]) }\n"

    try:
        to_append += f"Is a subclass of {cls.__bases__[-1].__name__}\n"
    except:
        ...

    for method_name in list(
        filter(
            lambda member: isfunction(getattr(cls, member))
            and not member.startswith("_"),
            dir(cls),
        )
    ):
        method = getattr(cls, method_name)
        m += document_method(method)
    return m


def recursive_document(cls):
    m = ""
    members = filter(
        lambda member: isclass(member) and not member.__name__.startswith("_"),
        [getattr(cls, member) for member in dir(cls)],
    )
    for member in list(members):

        m += document_class(member)
    return m


message = recursive_document(EpikCord)

print(message)
with open("docs.rst", "w") as f:
    f.write(message)
