"""Functions for generating JSON encoders and decoders.
"""

import logging
from functools import singledispatch

import swagger_to.intermediate

from .common import convert_to_camel_case

log = logging.getLogger(__name__)


@singledispatch
def typedef_to_encoder(typedef):
    """Generate a JSON encoder for a typedef. 

    This could be either a type name (i.e. for a generated encoder) or just standalone encoding code.
    """
    raise ValueError('No JSON encoder generator for {}'.format(type(typedef)))


@typedef_to_encoder.register(swagger_to.intermediate.Primitivedef)
def _(primitivedef):
    return {
        'string': 'Json.Encode.string',
        'integer': 'Json.Encode.int',
        'float': 'Json.Encode.float',
        'number': 'Json.Encode.float',
    }[primitivedef.type]


@typedef_to_encoder.register(swagger_to.intermediate.Objectdef)
def _(objectdef):
    def make_properties():
        for property in objectdef.properties.values():
            if property.required:
                yield f'Just ("{property.name}", {typedef_to_encoder(property.typedef)} obj.{convert_to_camel_case(property.name)})'
            else:
                yield f"""case obj.{convert_to_camel_case(property.name)} of
                    Just val -> Just ("{property.name}", {typedef_to_encoder(property.typedef)} obj.{convert_to_camel_case(property.name)})
                    Nothing -> Nothing"""

    properties = ',\n'.join(make_properties())
    
    return f"""[
        {properties}
    ] |> Maybe.Extra.values |> Json.Encode.object
    """


def _encoder_name(identifier):
    return convert_to_camel_case("{}Encoder".format(identifier))


@singledispatch
def typedef_to_decoder(deftype):
    """Generate a JSON decoder for a def. 

    This could be either a type name (i.e. for a generated decoder) or just standalone decoding code.
    """
    raise ValueError('No JSON decoder generator for {}'.format(type(deftype)))


@typedef_to_decoder.register(swagger_to.intermediate.AnyValuedef)
def _(anyvalue):
    log.warning('No _def_to_json_decoder_type for AnyValuedef')


@typedef_to_decoder.register(swagger_to.intermediate.Primitivedef)
def _(primitivedef):
    return {
        'string': 'Json.Decode.string',
        'integer': 'Json.Decode.int',
        'float': 'Json.Decode.float',
        'number': 'Json.Decode.float',
    }[primitivedef.type]


def _decoder_name(identifier):
    return convert_to_camel_case("{}Decoder".format(identifier))


@typedef_to_decoder.register(swagger_to.intermediate.Arraydef)
def _(arraydef):
    return "(Json.Decode.list {})".format(typedef_to_decoder(arraydef.items))


@typedef_to_decoder.register(swagger_to.intermediate.Objectdef)
def _(objectdef):
    return _decoder_name(objectdef.json_schema.identifier)
