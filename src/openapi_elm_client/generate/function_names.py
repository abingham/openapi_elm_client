from functools import singledispatch
from .common import convert_to_camel_case

import swagger_to.intermediate


def def_to_function_name(typedef):
    return convert_to_camel_case(_def_to_function_name(typedef))


@singledispatch
def _def_to_function_name(typedef):
    raise ValueError("No function name generator for {}".format(type(typedef)))


@_def_to_function_name.register(swagger_to.intermediate.Primitivedef)
def _(primitivedef):
    return primitivedef.identifier


@_def_to_function_name.register(swagger_to.intermediate.Objectdef)
def _(objectdef: swagger_to.intermediate.Objectdef):
    return objectdef.identifier
