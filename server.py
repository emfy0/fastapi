from fastapi import FastAPI, Request
from fastapi.responses import FileResponse, RedirectResponse, HTMLResponse
import uvicorn
from os.path import isfile
from fastapi.templating import Jinja2Templates

app = FastAPI()

templates = Jinja2Templates(directory = "templates")

@app.exception_handler(404)
def redirect_error(request, exc):
    return RedirectResponse("/404")

@app.get("/404", response_class = HTMLResponse)
def notfound(request: Request):
    return templates.TemplateResponse("404template.html", {"request": request, "error_message": "Не удалось найти данную страницу"})

@app.get("/")
def redirect():
    return RedirectResponse("/library")

@app.get("/library")
def writers():
    return FileResponse("pages/writers.html")

@app.get("/library/{author}", response_class = HTMLResponse)
def work_list(request: Request, author):
    file_path = "pages/" + author + ".html"
    return FileResponse(file_path) if isfile(file_path) > 0 else templates.TemplateResponse("404template.html", {"request": request, "error_message": "Не удалось найти данного автора"})

@app.get("/library/{author}/{work}", response_class = HTMLResponse)
def work_choose(request: Request, work, author, begin: int = 0, end: int = -1):
    if isfile("pages/" + author + ".html") == 0:
        return templates.TemplateResponse("404template.html", {"request": request, "error_message": "Не удалось найти автора с данным произведением"})
    if isfile("works/" + work + ".txt") == 0:
        return templates.TemplateResponse("404template.html", {"request": request, "error_message": "Не удалось найти данное произведение у автора"})
    file = open("works/" + work + ".txt", encoding='utf-8')
    string = file.read()
    string = string.replace('\n', '<br>')
    return templates.TemplateResponse("worktemplate.html", {"request": request, "text": string[begin:end]})

if __name__ == "__main__":
    uvicorn.run(app)