"""Functions for creating Elm types from swagger-to def types.
"""
import logging
from functools import singledispatch

import swagger_to.intermediate

log = logging.getLogger(__name__)


@singledispatch
def def_to_elm_type(deftype):
    raise TypeError("No elm-type converter for {}".format(type(deftype)))


@def_to_elm_type.register(swagger_to.intermediate.AnyValuedef)
def _(anyvalue):
    log.warning("No implementation of _def_to_elm_type for AnyValue")


@def_to_elm_type.register(swagger_to.intermediate.Propertydef)
def _(propertydef):
    typename = def_to_elm_type(propertydef.typedef)
    if not propertydef.required:
        typename = "Maybe ({})".format(typename)
    return typename


@def_to_elm_type.register(swagger_to.intermediate.Parameter)
def _(parameter):
    typename = def_to_elm_type(parameter.typedef)
    if not parameter.required:
        typename = "Maybe ({})".format(typename)
    return typename


@def_to_elm_type.register(swagger_to.intermediate.Primitivedef)
def _(primitivedef):
    return {"string": "String", "integer": "Int", "float": "Float", "number": "Float"}[
        primitivedef.type
    ]


@def_to_elm_type.register(swagger_to.intermediate.Arraydef)
def _(arraydef: swagger_to.intermediate.Arraydef):
    return "List {}".format(def_to_elm_type(arraydef.items))


@def_to_elm_type.register(swagger_to.intermediate.Objectdef)
def _(objectdef: swagger_to.intermediate.Objectdef):
    if objectdef.identifier:
        return objectdef.identifier

    properties = (
        f"{property.name}: {def_to_elm_type(property)}"
        for property in objectdef.properties.values()
    )

    properties = ", ".join(properties)

    return "{" + properties + "}"
