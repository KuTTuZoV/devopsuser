from .yaml_util import get_next_yaml

class Handlers:

    def __init__(self, web):
        self.web = web

    def service_handler(self, request):
        return self.web.Response(text='ok')

    async def yaml_handler(self, request):
        data = await request.post()
        service_id = data['service_id']
        try:
            get_next_yaml(service_id)
            return self.web.Response(text='ok')
        except ValueError as v_err:
            return self.web.HTTPInternalServerError(text=str(v_err))
        except FileNotFoundError as fnf:
            return self.web.HTTPInternalServerError(text='Ошибка файловой системы')
