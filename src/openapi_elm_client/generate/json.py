"""Functions for generating JSON encoders and decoders.
"""

import logging
from functools import singledispatch

import swagger_to.intermediate

from .common import convert_to_camel_case

log = logging.getLogger(__name__)


@singledispatch
def def_to_json_encoder_type(deftype):
    """Generate a JSON encoder for a def. 

    This could be either a type name (i.e. for a generated encoder) or just standalone encoding code.
    """
    raise ValueError('No JSON encoder generator for {}'.format(type(deftype)))


@def_to_json_encoder_type.register(swagger_to.intermediate.Primitivedef)
def _(primitivedef):
    return {
        'string': 'Json.Encode.string',
        'integer': 'Json.Encode.int',
        'float': 'Json.Encode.float',
        'number': 'Json.Encode.float',
    }[primitivedef.type]


@def_to_json_encoder_type.register(swagger_to.intermediate.Objectdef)
def _(objectdef):
    return _encoder_name(objectdef.json_schema.identifier)


def _encoder_name(identifier):
    return convert_to_camel_case("{}Encoder".format(identifier))


@singledispatch
def def_to_json_decoder_type(deftype):
    """Generate a JSON decoder for a def. 

    This could be either a type name (i.e. for a generated decoder) or just standalone decoding code.
    """
    raise ValueError('No JSON decoder generator for {}'.format(type(deftype)))


@def_to_json_decoder_type.register(swagger_to.intermediate.AnyValuedef)
def _(anyvalue):
    log.warning('No _def_to_json_decoder_type for AnyValuedef')


@def_to_json_decoder_type.register(swagger_to.intermediate.Primitivedef)
def _(primitivedef):
    return {
        'string': 'Json.Decode.string',
        'integer': 'Json.Decode.int',
        'float': 'Json.Decode.float',
        'number': 'Json.Decode.float',
    }[primitivedef.type]


def _decoder_name(identifier):
    return convert_to_camel_case("{}Decoder".format(identifier))


@def_to_json_decoder_type.register(swagger_to.intermediate.Arraydef)
def _(arraydef):
    return "(Json.Decode.list {})".format(def_to_json_decoder_type(arraydef.items))


@def_to_json_decoder_type.register(swagger_to.intermediate.Objectdef)
def _(objectdef):
    return _decoder_name(objectdef.json_schema.identifier)
