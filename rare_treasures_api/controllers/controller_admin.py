''' route handlers for treasures api '''
from fastapi.responses import HTMLResponse
from fastapi import APIRouter, Request
from fastapi.templating import Jinja2Templates
from ..dependencies import ROOT_PATH

router = APIRouter()
templates = Jinja2Templates(directory=f'{ROOT_PATH}/views')

# Add treasure item to a shop
@router.get('/add-treasure', response_class=HTMLResponse)
def add_to_treasure_page(request: Request) -> HTMLResponse:
    ''' add treasure item to treasures '''
    return templates.TemplateResponse(request, name='add-treasure.html')
