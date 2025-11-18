from fastapi import FastAPI, HTTPException, UploadFile, File
from typing import List
from .db import SessionLocal, init_db
from .models import Recipe
from .search import RecipeSearch
import os

app = FastAPI(title="Recipe Search API")
init_db()
searcher = RecipeSearch()

def load_all_to_search():
    db = SessionLocal()
    rows = db.query(Recipe).all()
    recipes = []
    for r in rows:
        recipes.append({
            'id': r.id,
            'title': r.title,
            'ingredients': r.ingredients,
            'steps': r.steps
        })
    db.close()
    searcher.fit(recipes)

@app.on_event("startup")
def startup_event():
    load_all_to_search()

@app.get("/health")
def health():
    return {"status": "ok"}

@app.get("/search")
def search(q: str, topk: int = 10, vegetarian: int = None, halal: int = None):
    # naive filtering: search over corpus, then filter results by metadata
    results = searcher.query(q, topk=100)
    db = SessionLocal()
    out = []
    for rid, score in results:
        r = db.query(Recipe).filter(Recipe.id==rid).first()
        if not r:
            continue
        if vegetarian is not None and r.vegetarian != vegetarian:
            continue
        if halal is not None and r.halal != halal:
            continue
        out.append({
            'id': r.id,
            'title': r.title,
            'score': score,
            'image': r.image_path
        })
        if len(out) >= topk:
            break
    db.close()
    return out

@app.get("/recipe/{recipe_id}")
def get_recipe(recipe_id: int):
    db = SessionLocal()
    r = db.query(Recipe).filter(Recipe.id==recipe_id).first()
    db.close()
    if not r:
        raise HTTPException(status_code=404, detail="Recipe not found")
    return {
        'id': r.id,
        'title': r.title,
        'ingredients': r.ingredients.split("||"),
        'steps': r.steps,
        'calories': r.calories,
        'image': r.image_path
    }

# optional endpoint to upload image (for admin)
@app.post("/recipe/{recipe_id}/upload-image")
async def upload_image(recipe_id: int, file: UploadFile = File(...)):
    os.makedirs("images", exist_ok=True)
    path = f"images/{recipe_id}_{file.filename}"
    with open(path, "wb") as f:
        content = await file.read()
        f.write(content)
    db = SessionLocal()
    r = db.query(Recipe).filter(Recipe.id==recipe_id).first()
    if r:
        r.image_path = path
        db.commit()
    db.close()
    load_all_to_search()
    return {"path": path}
