''' This module is the entrypoint for the `Cat's Rare Treasures` FastAPI app. '''
from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
from fastapi.exceptions import RequestValidationError
from fastapi.templating import Jinja2Templates

from .dependencies import root_dir
from .controllers import treasures_router, admin_router
templates = Jinja2Templates(directory=f'{root_dir}/views')

app = FastAPI()
app.include_router(treasures_router)
app.include_router(admin_router)

# Global Error handling

ERROR_MSGS = {
    400: '400 Bad Request: invalid query parameters',
    404: '404 Not Found: The requested page could not be found'
}

@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, __):
    ''' Redirect to the Error page if bad request '''
    return templates.TemplateResponse(
        request, 'error.html', context={'status_code': 400, 'message': ERROR_MSGS[400]}
    )

@app.exception_handler(404)
async def handler_404(request: Request, __):
    ''' Redirect to the Error page if the page is not found '''
    return templates.TemplateResponse(
        request, 'error.html', context={'status_code': 404, 'message': ERROR_MSGS[404]}
    )

# Serve static files
app.mount('/public', StaticFiles(directory=f'{root_dir}/public', html=True), name='public')
