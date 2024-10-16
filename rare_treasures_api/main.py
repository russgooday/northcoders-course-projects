''' This module is the entrypoint for the `Cat's Rare Treasures` FastAPI app. '''
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.responses import RedirectResponse

from .dependencies import root_dir
from .controllers import treasures_router, admin_router

app = FastAPI()
app.include_router(treasures_router)
app.include_router(admin_router)

@app.exception_handler(404)
async def handler_404(_, __):
    ''' Redirect to the homepage if the page is not found '''
    return RedirectResponse("/?error=404")

# Serve static files
app.mount('/public', StaticFiles(directory=f'{root_dir}/public', html=True), name='public')
