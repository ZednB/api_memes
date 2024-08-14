import pytest
from sqlalchemy.orm import Session

from memes import schemas, crud
from tests.test_main import TestingSessionLocal


def test_create_meme_in_crud():
    db: Session = TestingSessionLocal()
    meme_data = schemas.MemeCreate(title="CRUD test meme", description="CRUD test")
    meme = crud.create_meme(db=db, meme=meme_data)
    assert meme.title == "CRUD test meme"
    assert meme.description == "CRUD test"
    assert meme.id is not None
    db.close()


def test_read_memes_in_crud():
    db: Session = TestingSessionLocal()
    memes = crud.get_memes(db)
    assert len(memes) > 0
    db.close()
