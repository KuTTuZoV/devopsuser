import re
import os
from glob import glob

MIN_ID_LENGTH = 3
MAX_ID_LENGTH = 30
NETWORK_STUB_NAME = 'MY-NETWORK'
PORT_STUB_NUMBER = 'MY-PORT'

re_service_id = re.compile(r'^[a-z][a-z0-9\-]{'
        f'{MIN_ID_LENGTH},{MAX_ID_LENGTH}' r'}$')
re_fn = re.compile(r'.*\/([^\/]+).yaml$')

fn_matches = services = set([re.match(re_fn, fn) for fn 
    in glob('./devops/*.yaml')])

services = set([fnm.group(1) for fnm in fn_matches if fnm])
current_free_port = len(services) * 1000 + 8000


def get_next_yaml(service_id):
    if len(service_id) < MIN_ID_LENGTH:
        raise ValueError('Имя сервиса слишком короткое.')
    if len(service_id) > MAX_ID_LENGTH:
        raise ValueError('Имя сервиса слишком длинное.')
    if not re.match(re_service_id, service_id):
        raise ValueError('Имя сервиса не соответствует шаблону.')
    if service_id in services:
        raise ValueError('Сервис с таким именем уже зарегистрирован.')
    services.add(service_id)
    global current_free_port
    yaml_tmp = yaml_str\
        .replace(NETWORK_STUB_NAME, service_id)\
        .replace(PORT_STUB_NUMBER, str(current_free_port))
    current_free_port += 1000
    with open(f'devops/{service_id}.yaml', 'w') as yaml_file:
        yaml_file.write(yaml_tmp)


def get_services():
    return sorted(services)

yaml_str = f"""
version: '2'

networks:
  {NETWORK_STUB_NAME}:
    driver: bridge
services:
  openldap:
    image: bitnami/openldap:2
    ports:
      - '1389:1389'
      - '1636:1636'
    environment:
      - LDAP_ADMIN_USERNAME=admin
      - LDAP_ADMIN_PASSWORD=adminpassword
      - LDAP_USERS=user01,user02
      - LDAP_PASSWORDS=password1,password2
    networks:
      - {NETWORK_STUB_NAME}
    volumes:
      - 'openldap_data:/bitnami/openldap'
  myapp:
    image: nextcloud
    ports:
      - {PORT_STUB_NUMBER}
    networks:
      - {NETWORK_STUB_NAME}
volumes:
  openldap_data:
    driver: local

""".strip()

