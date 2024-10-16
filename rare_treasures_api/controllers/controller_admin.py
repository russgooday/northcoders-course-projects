''' route handlers for treasures api '''
from fastapi.responses import HTMLResponse
from fastapi import APIRouter
from jinja2 import Environment, FileSystemLoader


router = APIRouter()
environment = Environment(loader=FileSystemLoader('views/'))
add_to_shop_template = environment.get_template('add_treasure.html')


# Add treasure item to a shop
@router.get('/add-to-treasures')
def add_to_treasure_page():
    ''' add treasure item to treasures '''
    return HTMLResponse(add_to_shop_template.render())
