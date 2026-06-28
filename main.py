# main entry point for the dataplotter app

from pathlib import Path

import uvicorn
from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from services.grapher import graphdata
from services.parser import cleandata

app = FastAPI()
templates = Jinja2Templates(directory=Path(__file__).parent / "frontend")
app.mount("/static", StaticFiles(directory=Path(__file__).parent / "frontend"), name="static")


@app.get("/")
async def home(request: Request):
    # render the upload page
    return templates.TemplateResponse(request, "index.html")


@app.post("/plot")
async def sort_data(request: Request):
    # process the uploaded file and render the selected plot
    formcontent = await request.form()

    plotdiv, traces, plot_stats = graphdata(
        cleandata(formcontent),
        formcontent["plot_type"].lower(),
    )

    return templates.TemplateResponse(
        request,
        "graph.html",
        {
            "plotdiv": plotdiv,
            "traces": traces,
            "plot_stats": plot_stats,
        },
    )


if __name__ == "__main__":
    # run the app locally
    uvicorn.run(app="main:app", host="0.0.0.0", port=8000, reload=True)


