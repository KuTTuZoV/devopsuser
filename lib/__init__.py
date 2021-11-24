from aiohttp import web
from aiohttp.web import Application, RouteTableDef
from .descriptor import create_services, get_services

routes = RouteTableDef()
api_service = '/api/service'


@routes.get('/')
async def index_handler(_):
    return web.FileResponse('./public/index.html')


@routes.get(api_service)
async def get_services_str(_):
    srv = get_services()
    return web.Response(text='\n'.join(srv))


@routes.post(api_service)
async def yaml_handler(request):
    data = await request.post()
    service_id = data['service_id']
    try:
        create_services(service_id)
        return web.Response(text='OK')
    except ValueError as v_err:
        print(f'Ошибка в имени сервиса - "{service_id}". {v_err}')
        return web.HTTPInternalServerError(text=str(v_err))
    except FileNotFoundError:
        return web.HTTPInternalServerError(text='Ошибка файловой системы')


def create_app():
    global routes
    app = Application()
    app.add_routes(routes)
    app.router.add_static('/', './public', show_index=True)
    return web, app
