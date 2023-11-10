import fastapi
from starlette.templating import Jinja2Templates
from starlette.requests import Request

router = fastapi.APIRouter()
templates = Jinja2Templates("templates")


@router.get("/", include_in_schema=False, response_model=None)
def index(request: Request) -> Jinja2Templates.TemplateResponse:
    """
    Render the home page.
    :param request: request object.
    :return: rendered html template of home page.
    """
    return templates.TemplateResponse("home/index.html", {"request": request})


@router.get("/favicon.ico", include_in_schema=False, response_model=None)
def favicon() -> fastapi.responses.RedirectResponse:
    """
    Redirect to the favicon.
    :return: redirect to favicon url.
    """
    return fastapi.responses.RedirectResponse(url="/static/img/favicon.ico")


#
