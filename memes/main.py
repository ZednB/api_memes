from typing import Generator, List
from fastapi import FastAPI, Depends, Query, HTTPException
from sqlalchemy.orm import Session
from . import crud, models, schemas
from .database import SessionLocal, engine, get_db

app = FastAPI()


@app.get("/memes", response_model=List[schemas.Meme])
def read_memes(skip: int = Query(0, ge=0), limit: int = Query(10, le=10), db: Session = Depends(get_db)):
    return crud.get_memes(db, skip=skip, limit=limit)


@app.get("/memes/{id}", response_model=schemas.Meme)
def read_meme(id: int, db: Session = Depends(get_db)):
    db_meme = crud.get_meme(db, meme_id=id)
    if db_meme is None:
        raise HTTPException(status_code=404, detail='Мем не найден')
    return db_meme


@app.post("/memes", response_model=schemas.Meme, status_code=201)
def create_meme(meme: schemas.MemeCreate, db: Session = Depends(get_db)):
    return crud.create_meme(db, meme=meme)


@app.put("/memes/{id}", response_model=schemas.Meme)
def update_meme(id: int, meme: schemas.MemeUpdate, db: Session = Depends(get_db)):
    db_meme = crud.update_meme(db, meme_id=id, meme=meme)
    if db_meme is None:
        raise HTTPException(status_code=404, detail='Мем не найден')
    return db_meme


@app.delete("/memes/{id}", status_code=204)
def delete_meme(id: int, db: Session = Depends(get_db)):
    if not crud.delete_meme(db, meme_id=id):
        raise HTTPException(status_code=404, detail='Мем не найден')
    return None


# @app.get("/")
# async def root():
#     return {"message": "Hello World"}