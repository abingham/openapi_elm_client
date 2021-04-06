"""Functions for generating endpoint Elm functions.
"""
import logging
from functools import singledispatch

from swagger_to.intermediate import Primitivedef

from .common import convert_to_camel_case
from .elm_types import def_to_elm_type

log = logging.getLogger(__name__)


def endpoint_arg_types(endpoint):
    def make_type_specs():
        for parameter in endpoint.parameters:
            yield def_to_elm_type(parameter)
            yield "->"

    return " ".join(make_type_specs())


def endpoint_arg_names(endpoint):
    names = (convert_to_camel_case(p.name) for p in endpoint.parameters)
    return " ".join(names)


def endpoint_url(endpoint):
    path_parameters = [p for p in endpoint.parameters if p.in_what == "path"]

    def resolve_component(component):
        for param in path_parameters:
            if component == "{" + param.name + "}":
                return (
                    to_string_converter(param.typedef)
                    + " "
                    + convert_to_camel_case(param.name)
                )

        return f'"{component}"'

    components = [c for c in endpoint.path.split("/")[1:]]
    return ", ".join(resolve_component(c) for c in components)


@singledispatch
def to_string_converter(typedef):
    "Returns an Elm value-to-string conversion function for the typedef"
    raise TypeError(f"No to-string converter for {typedef}")


@to_string_converter.register(Primitivedef)
def _(primitivedef):
    return {
        "string": "",
        "integer": "String.fromInt",
        "number": "String.fromFloat",
        "float": "String.fromFloat",
    }[primitivedef.type]


def primitivedef_to_url_query_type(primitivedef):
    try:
        return {
            "string": "Url.Builder.string",
            "integer": "Url.Builder.int",
        }[primitivedef.type]
    except KeyError:
        raise KeyError(
            f"parameters of type {primitivedef.type} are not supported as query parameters"
        )
