# File: backend/app/main.py

from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from .api import router as brand_router
import os

# Get the absolute path to the directory containing this file
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
# Define the path to the static directory, which is one level up from app/
STATIC_DIR = os.path.join(BASE_DIR, "..", "static")


app = FastAPI(
    title="AI Brand Strategist API",
    description="An API to analyze brand voice and generate on-brand content.",
    version="1.0.0"
)

# --- API Routes ---
# All your API logic is under the /api/v1 prefix
app.include_router(brand_router, prefix="/api/v1", tags=["Brand Analysis"])


# --- Frontend Serving ---
# This part serves the static frontend files (HTML, CSS, JS)

# Mount the static directory to the '/static' path.
# This is useful if you have CSS or JS files you want to link in your HTML.
app.mount("/static", StaticFiles(directory=STATIC_DIR), name="static")

# Set up a route for the root URL ("/") to serve your index.html file.
# include_in_schema=False prevents this from showing up in your API docs.
@app.get("/", response_class=FileResponse, include_in_schema=False)
async def read_index():
    """
    Serves the main index.html file for the frontend application.
    """
    return FileResponse(os.path.join(STATIC_DIR, "index.html"))