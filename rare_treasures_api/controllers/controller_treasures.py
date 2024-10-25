''' route handlers for treasures api '''
from typing import Dict
from fastapi import APIRouter, HTTPException, Depends, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

from ..dependencies import ROOT_PATH
from ..models.model_treasures import (
    TreasureFields,
    TreasureQueryParams,
    fetch_treasures,
    insert_treasure,
    fetch_colours
)


router = APIRouter()
templates = Jinja2Templates(directory=f'{ROOT_PATH}/views')


# Homepage
@router.get('/', response_class=HTMLResponse)
def homepage(request: Request) -> HTMLResponse:
    ''' return the home page '''
    colours = fetch_colours()
    return templates.TemplateResponse(
        request, name='index.html', context={'colours': colours}
    )


# Initial healthcheck
@router.get('/api/healthcheck')
def get_healthcheck() -> Dict:
    ''' Check that we are all up and running! '''
    return {'message': 'application is healthy'}


# Fetch all treasures
# Returns an HTML table of all treasures
@router.get('/api/treasures', response_class=HTMLResponse)
def get_treasures(request: Request, params=Depends(TreasureQueryParams)) -> HTMLResponse:
    ''' return all treasures and their shop details '''

    if (treasures := fetch_treasures(params)):
        return templates.TemplateResponse(
            request, name='partials/treasures_table.html', context=treasures
        )

    raise HTTPException(status_code=422, detail='Bad Request: unsuccessful query')


# Add a treasure
@router.post('/api/treasures')
def add_treasure(treasure: TreasureFields) -> Dict:
    ''' Add a treasure to the treasures table '''
    if (inserted_treasure := insert_treasure(treasure)):
        return inserted_treasure

    raise HTTPException(status_code=400, detail='Bad Request: treasure not added')
