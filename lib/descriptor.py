import os
import yaml

PORT_MIN = 9080
services_file_name = "./devops/services.yaml" 
template_file_name = services_file_name.replace('services', 'template')


def get_services():
        global services
        return [*services['networks'].keys()]


def create_services(id):
    global services
    services['networks'][id] = {"driver": "bridge"}

    with open(template_file_name, 'r') as stream:
        new_services = yaml.safe_load(stream)['services']
        old_services = services['services']

        next_port = len(get_services()) * 100 + PORT_MIN
        new_services['nextcloud']['ports'].append(f'{next_port}:80')    
        new_services['openldap']['volumes'].append(f'openldap_data:/{id}/openldap')

        for key, service in new_services.items():
            old_services[f'{key}_{id}'] = service
            service['networks'].append(id)
        dump()


def load():

    fn = services_file_name if os.path.isfile(services_file_name) \
        else template_file_name

    with open(fn, 'r') as stream:
        global services
        services = yaml.safe_load(stream)


def dump():
    global services, file_name
    all_services = services['services']
    for key in ['openldap', 'nextcloud']:
        if all_services.get(key):
            del all_services[key]
    with open(services_file_name, 'w', encoding='utf8') as outfile:
        yaml.dump(services, outfile, default_flow_style=False, \
            allow_unicode=True)
    return


load()
