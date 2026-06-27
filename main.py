# libraries
from fastapi import staticfiles
import uvicorn
from fastapi import FastAPI, Request
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from pathlib import Path

# python files
from services.grapher import graphdata
from services.parser import cleandata
app = FastAPI()
templates = Jinja2Templates(directory=Path(__file__).parent /"frontend")
app.mount("/static", StaticFiles(directory=Path(__file__).parent /"frontend"), name="static")

@app.get("/")
async def home(request: Request):
    return templates.TemplateResponse(request, "index.html")


@app.post("/plot")
async def sort_data(request: Request):
    formcontent = await request.form()
    print(f"{formcontent['file']}\n")
    print(f"{formcontent['plot_type']}\n")

    plotdiv, traces, plot_stats = graphdata(cleandata(formcontent), formcontent["plot_type"].lower())

    return templates.TemplateResponse(request, "graph.html", {
        "plotdiv": plotdiv,
        "traces": traces,
        "plot_stats": plot_stats,
    })

if __name__ == "__main__":
	uvicorn.run(app="main:app", host="0.0.0.0", port=8000, reload=True)
	
	





