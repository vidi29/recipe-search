import pandas as pd
from sqlalchemy import create_engine
import os
from app.models import Recipe, Base
from app.db import engine

# contoh CSV format: id,title,ingredients,steps,calories,vegetarian,halal,image_url
df = pd.read_csv("dataset/recipes.csv")

# create tables
Base.metadata.create_all(bind=engine)
conn = engine.connect()
for _, row in df.iterrows():
    ingredients = "||".join(str(row['ingredients']).split(";"))  # normalize
    conn.execute(Recipe.__table__.insert().values(
        title=row['title'],
        ingredients=ingredients,
        steps=row.get('steps',''),
        calories=row.get('calories',None),
        vegetarian=int(row.get('vegetarian',0)),
        halal=int(row.get('halal',0)),
        image_path=row.get('image_path', None)
    ))
conn.close()
print("import done")
