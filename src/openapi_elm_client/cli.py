import click
import swagger_to.intermediate
from jinja2 import Environment, PackageLoader
import logging
from functools import singledispatch

from swagger_to.intermediate import Primitivedef

log = logging.getLogger(__name__)


@click.command()
@click.argument('spec-file', type=click.Path(exists=True, dir_okay=False, readable=True, file_okay=True))
def main(spec_file):
    write_elm_client(spec_file)
    return 0


def write_elm_client(spec_file):
    swagger, errs = swagger_to.swagger.parse_yaml_file(path=spec_file)
    if errs:
        raise ValueError('Error parsing spec: {}'.format(errs))

    intermediate_typedefs = swagger_to.intermediate.to_typedefs(
        swagger=swagger)
    intermediate_params = swagger_to.intermediate.to_parameters(
        swagger=swagger, typedefs=intermediate_typedefs)

    env = Environment(
        loader=PackageLoader('openapi_elm_client', 'templates'),
        trim_blocks=True,
    )
    env.filters['type_name'] = _propertydef_to_elm_type
    env.filters['json_decoder'] = _typedef_to_json_decoder_type

    template = env.get_template('Client.elm.j2')
    output = template.render(typedefs=intermediate_typedefs)
    print(output)


@singledispatch
def _typedef_to_json_decoder_type(typedef: swagger_to.intermediate.Typedef):
    raise ValueError('No JSON typename generator for {}'.format(type(typedef)))


JSON_TYPE_MAP = {
    'string': 'Json.Decode.string',
    'integer': 'Json.Decode.int',
    'float': 'Json.Decode.float',
    'number': 'Json.Decode.float',
}


@_typedef_to_json_decoder_type.register(swagger_to.intermediate.Primitivedef)
def _(typedef):
    return JSON_TYPE_MAP[typedef.type]


@_typedef_to_json_decoder_type.register(swagger_to.intermediate.Arraydef)
def _(arraydef):
    return "(Json.Decode.list {}Decoder)".format(arraydef.items.identifier)


def _propertydef_to_elm_type(property_def: swagger_to.intermediate.Propertydef):
    typename = _typedef_to_elm_type(property_def.typedef)
    if not property_def.required:
        typename = 'Maybe ({})'.format(typename)
    return typename


@singledispatch
def _typedef_to_elm_type(typedef):
    raise ValueError(
        'No typename generator for {}'.format(type(typedef)))


TYPE_MAP = {
    'string': 'String',
    'integer': 'Int',
    'float': 'Float',
    'number': 'Float'
}


@_typedef_to_elm_type.register(swagger_to.intermediate.Primitivedef)
def _(primitivedef):
    return TYPE_MAP[primitivedef.type]


@_typedef_to_elm_type.register(swagger_to.intermediate.Arraydef)
def _(arraydef):
    return "List {}".format(arraydef.items.identifier)
