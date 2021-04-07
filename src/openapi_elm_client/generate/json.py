"""Functions for generating JSON encoders and decoders.
"""


import logging
from functools import singledispatch

import swagger_to.intermediate

from .common import convert_to_camel_case, convert_to_pascal_case
from .unique_names import unique_name

log = logging.getLogger(__name__)


@singledispatch
def typedef_to_encoder(typedef):
    """Generate a JSON encoder for a typedef.

    This could be either a type name (i.e. for a generated encoder) or just standalone encoding code.
    """
    raise ValueError("No JSON encoder generator for {}".format(type(typedef)))


@typedef_to_encoder.register(swagger_to.intermediate.Parameter)
def _(parameter):
    if parameter.required:
        return typedef_to_encoder(parameter.typedef)

    obj_name = unique_name()

    return (
        f"Maybe.andThen (\\{obj_name} -> Just ({typedef_to_encoder(parameter.typedef)} {obj_name})) |> "
        "Maybe.withDefault Json.Encode.null"
    )


@typedef_to_encoder.register(swagger_to.intermediate.Primitivedef)
def _(primitivedef):
    return {
        "string": "Json.Encode.string",
        "integer": "Json.Encode.int",
        "float": "Json.Encode.float",
        "number": "Json.Encode.float",
    }[primitivedef.type]


@typedef_to_encoder.register(swagger_to.intermediate.Objectdef)
def _(objectdef):
    obj_name = unique_name()

    def make_properties():
        for property in objectdef.properties.values():
            if property.required:
                yield f'Just ("{property.name}", {typedef_to_encoder(property.typedef)} {obj_name}.{convert_to_camel_case(property.name)})'
            else:
                val_name = unique_name()
                yield f"""case {obj_name}.{convert_to_camel_case(property.name)} of
                    Just {val_name} -> Just ("{property.name}", {typedef_to_encoder(property.typedef)} {val_name})
                    Nothing -> Nothing"""

    properties = ", ".join(make_properties())

    return f"(\\{obj_name} -> [ {properties} ] |> Maybe.Extra.values |> Json.Encode.object)"


def _encoder_name(identifier):
    return convert_to_camel_case("{}Encoder".format(identifier))


@singledispatch
def typedef_to_decoder(deftype):
    """Generate a JSON decoder for a def.

    This could be either a type name (i.e. for a generated decoder) or just standalone decoding code.
    """
    raise ValueError("No JSON decoder generator for {}".format(type(deftype)))


@typedef_to_decoder.register(swagger_to.intermediate.AnyValuedef)
def _(anyvalue):
    log.warning("No _def_to_json_decoder_type for AnyValuedef")


@typedef_to_decoder.register(swagger_to.intermediate.Primitivedef)
def _(primitivedef):
    return {
        "string": "Json.Decode.string",
        "integer": "Json.Decode.int",
        "float": "Json.Decode.float",
        "number": "Json.Decode.float",
    }[primitivedef.type]


def _decoder_name(identifier):
    return convert_to_camel_case("{}Decoder".format(identifier))


@typedef_to_decoder.register(swagger_to.intermediate.Arraydef)
def _(arraydef):
    return "({} |> Json.Decode.list)".format(typedef_to_decoder(arraydef.items))


@typedef_to_decoder.register(swagger_to.intermediate.Objectdef)
def _(objectdef):
    def make_parameters():
        for property in objectdef.properties.values():
            if property.required:
                yield f'|> Json.Decode.Pipeline.required "{property.name}" {typedef_to_decoder(property.typedef)}'
            else:
                yield f'|> Json.Decode.Pipeline.optional "{property.name}" (Json.Decode.nullable {typedef_to_decoder(property.typedef)}) Nothing'

    parameters = " ".join(make_parameters())

    return f"(Json.Decode.succeed {convert_to_pascal_case(objectdef.identifier)} {parameters})"
