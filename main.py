from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.exceptions import RequestValidationError
from fastapi.templating import Jinja2Templates
from api.routers import file
from web.routers import web
from settings import settings


app = FastAPI(**settings.fastapi_kwargs)
app.mount('/static', StaticFiles(directory='static'), name='static')
app.include_router(file.router)
app.include_router(web.router)
templates = Jinja2Templates(directory='templates')


@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request, e):
    return templates.TemplateResponse(
        'message.html',
        {
            'request': request,
            'title': settings.page_title,
            'message': str(e)
        },
        status_code=422
    )


if __name__ == '__main__':
    import uvicorn
    uvicorn.run(app, host='0.0.0.0', port=8080)
