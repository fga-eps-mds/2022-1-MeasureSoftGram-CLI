import json

from tabulate import tabulate
from src.cli.commands.parse_get_entity import utils

from src.cli.utils import check_host_url
from src.clients.service_client import ServiceClient
from src.config.settings import SUPPORTED_FORMATS


def get_sqc(response, entity_id, history):
    if entity_id:
        extracted_data, headers, data = \
            utils.get_entity_id(response, 'sqc', history)
    else:
        extracted_data, headers, data = \
            utils.get_without_entity_id(response, 'sqc', history)

    return extracted_data, headers, data


def parse_get_sqc(
    repository_id,
    host_url,
    organization_id,
    product_id,
    output_format,
    history,
):
    host_url = check_host_url(host_url)
    host_url += (
        f'api/v1/organizations/{organization_id}/products/{product_id}/'
    )

    if history:
        host_url += 'repositories-sqc-historical-values/'
    else:
        host_url += 'repositories-sqc-latest-values/'

    # /api/v1/organizations/1/products/3/repositories/6/latest-values/sqc/
    response = ServiceClient.make_get_request(host_url)

    extracted_data, headers, data = get_sqc(
        response,
        repository_id,
        history,
    )

    if output_format == 'tabular':
        print(tabulate(extracted_data, headers=headers))
    elif output_format == 'json':
        print(json.dumps(data))

    return

def parse_get_entity(
    entity_name,
    entity_id,
    host_url,
    organization_id,
    repository_id,
    product_id,
    output_format,
    history,
):
    if entity_name == 'sqc':
        parse_get_sqc(entity_id,
                        host_url,
                        organization_id,
                        product_id,
                        output_format,
                        history)

    if output_format not in SUPPORTED_FORMATS:
        print((
            "Output format not supported. "
            f"Supported formats: {SUPPORTED_FORMATS}"
        ))
        return

    host_url = check_host_url(host_url)
    host_url += (
        'api/v1/'
        f'organizations/{organization_id}/'
        f'products/{product_id}/'
        f'repositories/{repository_id}/'
        f'{"historical-values/" if history else "latest-values/"}'
        f'{entity_name}/'
        f'{entity_id if entity_id else ""}'
    )
    response = ServiceClient.get_entity(host_url)

    extracted_data, headers, data = utils.get_entity(
        response,
        entity_name,
        entity_id,
        history
    )

    if output_format == 'tabular':
        print(tabulate(extracted_data, headers=headers))
    elif output_format == 'json':
        print(json.dumps(data))

if __name__ == '__main__':
    parse_get_entity(
        entity_name = 'sqc',
        entity_id = None,
        host_url='https://measuresoftgram-service.herokuapp.com/',
        organization_id = 1,
        repository_id = 6,
        product_id = 3,
        output_format = 'tabular',
        history = False,
)