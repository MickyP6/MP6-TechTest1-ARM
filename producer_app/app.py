from fastapi import FastAPI, Request, Response
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

import data_cleanser
from get_google_data import GoogleApiRequest

app = FastAPI()

app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")


@app.get("/", response_class=HTMLResponse)
async def index(request: Request):
    return templates.TemplateResponse(name="index.html", context={"request": request})


@app.get("/grab_data")
def grab_data() -> Response:
    """
    This is the main entrypoint for d3 to request data.
    """
    data = GoogleApiRequest().request_data()
    data = data_cleanser.jsonify_data(data)

    return Response(data)
