''' route handlers for treasures api '''
from fastapi.responses import HTMLResponse
from fastapi import APIRouter, Request
from fastapi.templating import Jinja2Templates
from ..dependencies import root_dir

router = APIRouter()
templates = Jinja2Templates(directory=f'{root_dir}/views')

# Add treasure item to a shop
@router.get('/add-to-treasures', response_class=HTMLResponse)
def add_to_treasure_page(request: Request) -> HTMLResponse:
    ''' add treasure item to treasures '''
    return templates.TemplateResponse(request, name='add-treasure.html')
