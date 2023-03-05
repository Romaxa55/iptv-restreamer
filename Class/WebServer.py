import aiohttp_jinja2
import jinja2
import time
from cryptography import fernet
from aiohttp import web
from aiohttp_session import setup, get_session
from aiohttp_session.cookie_storage import EncryptedCookieStorage
from Class.Streamer import Streamer


class WebServer:
    routes = web.RouteTableDef()

    def __init__(self, **kwargs: dict):
        self.app = web.Application()
        self.host = kwargs['webserver']['host']
        self.port = kwargs['webserver']['port']
        self.iptv = {'host': kwargs['iptv']['host']}

    async def startStream(self, request: web.Request) -> web.Response:
        session = await get_session(request)
        session['last_visit'] = time.time()
        iptv = {
            **self.iptv,
            'id': request.match_info.get("id", ""),
            'key': request.match_info.get("key", ""),
            'path': request.path
        }
        headers = {
            "Content-Type": "application/x-mpegURL"
        }
        await Streamer(**iptv).runStream()
        with open(f"{self.tmp}hls_out.m3u8", 'rb') as f:
            s = f.read().decode("utf-8")
        return web.Response(text=s,
                            headers=headers)

    @staticmethod
    async def videoFiles(request: web.Request) -> web.FileResponse:
        headers = {
            "Content-Type": "video/mp2t",
            "Connection": "keep-alive"
            }
        return web.FileResponse(f"tmp{request.path}")

    @staticmethod
    async def handle_404(request):
        context = {'name': '404', 'text': 'PAGE NOT FOUND'}
        return aiohttp_jinja2.render_template('error.html', request, context)

    @staticmethod
    async def handle_500(request):
        context = {'name': '500', 'text': 'SERVICE UNAVAILABLE'}
        return aiohttp_jinja2.render_template('error.html', request, context)

    def create_error_middleware(self, overrides):

        @web.middleware
        async def error_middleware(request, handler):

            try:
                response = await handler(request)

                override = self.app.get(response.status)
                if override:
                    return await override(request)

                return response
            except web.HTTPException as ex:
                override = overrides.get(ex.status)
                if override:
                    return await override(request)

                raise

        return error_middleware

    async def initializer(self) -> web.Application:
        # Setup routes and handlers
        error_middleware = self.create_error_middleware({
            404: self.handle_404,
            400: self.handle_404,
            500: self.handle_500,
            501: self.handle_500,
            502: self.handle_500,
            503: self.handle_500,
        })
        self.app.middlewares.append(error_middleware)
        self.app.router.add_get('/iptv/{key}/{id}/index.m3u8', self.startStream)
        self.app.router.add_get('/iptv/{key}/{id}/chunk-stream-{num_video:\d+}.ts', self.videoFiles)

        aiohttp_jinja2.setup(self.app,
                             loader=jinja2.FileSystemLoader('html/'))
        fernet_key = fernet.Fernet.generate_key()
        f = fernet.Fernet(fernet_key)
        setup(self.app, EncryptedCookieStorage(f))
        return self.app

    def run(self):
        web.run_app(self.initializer(), host=self.host, port=self.port)
