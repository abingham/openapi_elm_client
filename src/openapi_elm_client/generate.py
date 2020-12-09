import logging
from functools import singledispatch, wraps

import swagger_to.intermediate
from jinja2 import Environment, PackageLoader

log = logging.getLogger(__name__)


def generate_elm_client(spec_file, module_name):
    swagger, errs = swagger_to.swagger.parse_yaml_file(path=spec_file)
    if errs:
        raise ValueError('Error parsing spec: {}'.format(errs))

    intermediate_typedefs = swagger_to.intermediate.to_typedefs(
        swagger=swagger)
    intermediate_params = swagger_to.intermediate.to_parameters(
        swagger=swagger, typedefs=intermediate_typedefs)
    intermediate_endpoints = swagger_to.intermediate.to_endpoints(
        swagger=swagger,
        typedefs=intermediate_typedefs,
        params=intermediate_params)

    env = Environment(
        loader=PackageLoader('openapi_elm_client', 'templates'),
        trim_blocks=True,
    )
    env.filters['pascal_case'] = _convert_to_pascal_case
    env.filters['camel_case'] = _convert_to_camel_case
    env.filters['alias_name'] = lambda objdef: _convert_to_pascal_case(
        objdef.identifier)
    env.filters['property_name'] = lambda propertydef: _convert_to_camel_case(
        propertydef.name)
    env.filters['elm_type'] = _def_to_elm_type
    env.filters['function_name'] = lambda d: _convert_to_camel_case(
        _def_to_function_name(d))
    # env.filters['elm_identifier'] = _def_to_identifier
    env.filters['json_decoder'] = _def_to_json_decoder_type

    template = env.get_template('Client.elm.j2')
    client_code = template.render(
        module_name=module_name,
        typedefs=intermediate_typedefs,
        endpoints=intermediate_endpoints)
    return client_code


@singledispatch
def _def_to_elm_type(deftype):
    raise TypeError('No elm-type converter for {}'.format(type(deftype)))


@_def_to_elm_type.register(swagger_to.intermediate.AnyValuedef)
def _(anyvalue):
    log.warning('No implementation of _def_to_elm_type for AnyValue')


@_def_to_elm_type.register(swagger_to.intermediate.Propertydef)
def _(propertydef):
    typename = _def_to_elm_type(propertydef.typedef)
    if not propertydef.required:
        typename = 'Maybe ({})'.format(typename)
    return typename


@_def_to_elm_type.register(swagger_to.intermediate.Primitivedef)
def _(primitivedef):
    return {
        'string': 'String',
        'integer': 'Int',
        'float': 'Float',
        'number': 'Float'
    }[primitivedef.type]


@_def_to_elm_type.register(swagger_to.intermediate.Arraydef)
def _(arraydef: swagger_to.intermediate.Arraydef):
    return "List {}".format(_def_to_elm_type(arraydef.items))


@_def_to_elm_type.register(swagger_to.intermediate.Objectdef)
def _(objectdef: swagger_to.intermediate.Objectdef):
    return objectdef.identifier


@singledispatch
def _def_to_json_decoder_type(deftype):
    raise ValueError('No JSON typename generator for {}'.format(type(deftype)))


@_def_to_json_decoder_type.register(swagger_to.intermediate.AnyValuedef)
def _(anyvalue):
    log.warning('No _def_to_json_decoder_type for AnyValuedef')


@_def_to_json_decoder_type.register(swagger_to.intermediate.Primitivedef)
def _(typedef):
    return {
        'string': 'Json.Decode.string',
        'integer': 'Json.Decode.int',
        'float': 'Json.Decode.float',
        'number': 'Json.Decode.float',
    }[typedef.type]


def _decoder_name(identifier):
    return _convert_to_camel_case("{}Decoder".format(identifier))


@_def_to_json_decoder_type.register(swagger_to.intermediate.Arraydef)
def _(arraydef):
    return "(Json.Decode.list {})".format(_def_to_json_decoder_type(arraydef.items))


@_def_to_json_decoder_type.register(swagger_to.intermediate.Objectdef)
def _(objectdef):
    return _decoder_name(objectdef.identifier)


@singledispatch
def _def_to_function_name(typedef):
    raise ValueError(
        'No function name generator for {}'.format(type(typedef)))


@_def_to_function_name.register(swagger_to.intermediate.Primitivedef)
def _(primitivedef):
    return primitivedef.identifier


# @_def_to_identifier.register(swagger_to.intermediate.Arraydef)
# def _(arraydef):
#     return "List {}".format(arraydef.items.identifier)


@_def_to_function_name.register(swagger_to.intermediate.Objectdef)
def _(objectdef: swagger_to.intermediate.Objectdef):
    return objectdef.identifier


def _valid_elm(f):
    """Attempt to create a valid Elm identifier from a string.
    
    This replaces illegal characters with legal onces. 
    """
    @wraps(f)
    def wrapper(*args, **kwargs):
        result = f(*args, **kwargs)
        # TODO: More replacements.
        result = result.replace('@', 'atsign_')
        if result == 'type':
            result = 'type_'
        return result
    return wrapper


@_valid_elm
def _convert_to_pascal_case(value):
    for separator in {'-', '.'}:
        value = value.replace(separator, '_')
    elements = value.split('_')
    return ''.join(map(_upper_first_letter, elements))


@_valid_elm
def _convert_to_camel_case(value):
    pc = _convert_to_pascal_case(value)
    return _lower_first_letter(pc)


def _upper_first_letter(value):
    return ''.join([c.upper() for c in value[:1]]) + value[1:]


def _lower_first_letter(value):
    return ''.join([c.lower() for c in value[:1]]) + value[1:]
