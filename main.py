from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
import uvicorn
from pymongo import MongoClient

app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

# MongoDB connection
conn = MongoClient("mongodb+srv://bhagyesh:Bhagyesh20@cluster0.dtgb6.mongodb.net")

@app.get("/", response_class=HTMLResponse)
async def read_item(request: Request):
    doc = conn.notes.notes.find_one({})  
    newDocs = []
    
    # Ensure doc is not None
    if doc:
        newDocs.append({
            "id": str(doc["_id"]), 
            "notes": doc.get("notes", "") 
              })
    
    return templates.TemplateResponse("index.html", {"request": request, "newDocs": newDocs})

if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)
