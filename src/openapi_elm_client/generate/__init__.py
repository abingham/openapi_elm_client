import logging
from .elm_types import def_to_elm_type
from .common import convert_to_camel_case, convert_to_pascal_case
from .function_names import def_to_function_name
from .endpoints import endpoint_arg_names, endpoint_arg_types, endpoint_url, primitivedef_to_url_query_type
from .json import typedef_to_encoder, typedef_to_decoder

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
    env.filters['pascal_case'] = convert_to_pascal_case
    env.filters['camel_case'] = convert_to_camel_case
    env.filters['alias_name'] = lambda objdef: convert_to_pascal_case(
        objdef.identifier)
    env.filters['property_name'] = lambda propertydef: convert_to_camel_case(
        propertydef.name)
    env.filters['elm_type'] = def_to_elm_type
    env.filters['function_name'] = def_to_function_name
    # env.filters['elm_identifier'] = _def_to_identifier
    env.filters['json_decoder'] = typedef_to_decoder
    env.filters['json_encoder'] = typedef_to_encoder
    env.filters['endpoint_arg_types'] = endpoint_arg_types
    env.filters['endpoint_arg_names'] = endpoint_arg_names
    env.filters['endpoint_url'] = endpoint_url
    env.filters['endpoint_query_type'] = primitivedef_to_url_query_type

    template = env.get_template('Client.elm.j2')
    client_code = template.render(
        module_name=module_name,
        typedefs=intermediate_typedefs,
        endpoints=intermediate_endpoints)
    return client_code

