from fastapi import APIRouter, Request, Path
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from settings import settings


router = APIRouter(
    tags=['Web']
)
templates = Jinja2Templates(directory='templates')


@router.get('/', response_class=HTMLResponse)
async def main(request: Request):
    """メイン画面"""
    return templates.TemplateResponse('main.html', {
        'request': request,
        'page_title': settings.page_title,
        'expiration_days': settings.expiration_days
    })


@router.get('/files/{file_id}')
async def get_file_info(
    request: Request,
    file_id: str = Path(..., min_length=26, max_length=26, regex='^[A-Z0-9]{26}$')
):
    """ファイル情報画面"""
    return templates.TemplateResponse('file_info.html', {
        'request': request,
        'page_title': settings.page_title,
        'file_id': file_id
    })
