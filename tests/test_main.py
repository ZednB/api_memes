import pytest
from fastapi.testclient import TestClient
from memes.main import app
from memes.database import Base, get_db
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

# Настройка тестовой базы данных
SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"  # Используем SQLite для тестов
engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base.metadata.create_all(bind=engine)

# Создание тестового клиента
client = TestClient(app)


# Функция для зависимостей, которая будет использовать тестовую базу данных
def override_get_db():
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()


app.dependency_overrides[get_db] = override_get_db


def test_create_meme():
    response = client.post(
        "/memes",
        json={"title": "Test Meme", "description": "This is a test meme."}
    )
    assert response.status_code == 201
    data = response.json()
    assert data["title"] == "Test Meme"
    assert data["description"] == "This is a test meme."
    assert data["id"] is not None


def test_read_memes():
    response = client.get("/memes")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert len(data) > 0


# def test_create_meme_validation_error():
#     response = client.post(
#         "/memes",
#         json={"title": "", "description": "This meme has no title."}
#     )
#     assert response.status_code == 400
#     assert response.json() == {
#         "detail": "Title is required and must not be empty."
#     }


def test_read_nonexistent_meme():
    response = client.get("/memes/999")
    assert response.status_code == 404
    assert response.json() == {'detail': 'Мем не найден'}
