import json

from fastapi import Depends, FastAPI, Request, Form
from fastapi.responses import HTMLResponse, JSONResponse
from starlette.responses import RedirectResponse
from sqlalchemy.orm import Session
from fastapi import Form
from fastapi.encoders import jsonable_encoder
from fastapi.middleware.cors import CORSMiddleware

from model import Books
import schema
from database import SessionLocal, engine
import model

from datetime import datetime

app = FastAPI()

model.Base.metadata.create_all(bind=engine)

app.add_middleware(
    CORSMiddleware,
    allow_origins=['http://localhost:3000'],
    allow_methods=['*'],
    allow_headers=['*']
)


def get_database_session():
    try:
        db = SessionLocal()
        yield db
    finally:
        db.close()


@app.get("/books")
async def read_orders(request: Request, db: Session = Depends(get_database_session)):
    orders = db.query(Books).all()
    return orders

@app.post("/books")
async def create_order(request: Request, db: Session = Depends(get_database_session)):
    data = await request.json()
    print(data)
    books = Books(book_id=data["book_id"], book_name=data["book_name"], price=data["price"], quantity=data["quantity"])
    db.add(books)
    db.commit()
    db.refresh(books)
    response = RedirectResponse('/books', status_code=303)
    return response

@app.delete("/books/{id}")
async def delete_book(request: Request, id: int, db: Session = Depends(get_database_session)):
    book = db.query(Books).get(id)
    db.delete(book)
    db.commit()
    return JSONResponse(status_code=200, content={
        "status_code": 200,
        "message": "success",
        "book": None
    })

@app.patch("/books/{id}")
async def update_book(request: Request, id: int, db: Session = Depends(get_database_session)):
    requestBody = await request.json()
    book = db.query(Books).get(id)
    book.quantity = requestBody['update_num']
    db.commit()
    db.refresh(book)
    newBook = jsonable_encoder(book)
    return JSONResponse(status_code=200, content={
        "status_code": 200,
        "message": "success",
        "book": newBook
    })

# @app.put("/books/{book_id}")
# def create_or_update_book(Book_id: int) -> Books:
#     book = Books[Book_id]
#     Books[Book_id] = Books{
#         book_id=Book_id,
#         book_
#     }
#     return book

# @app.put("/books/{book_id}", response_model=Books)
# async def update_item(book_id: str, item: Books):
#     update_item_encoded = jsonable_encoder(item)
#     Books[book_id] = update_item_encoded
#     return update_item_encoded

# @app.get("/", response_class=HTMLResponse)
# async def read_item(request: Request, db: Session = Depends(get_database_session)):
#     records = db.query(Order).all()
#     return templates.TemplateResponse("index.html", {"request": request, "data": records})
#

# @app.get("/books/{book_id}", response_class=HTMLResponse)
# def read_item(request: Request, book_id: schema.Books.book_name, db: Session = Depends(get_database_session)):
#     item = db.query(Books).filter(Books.id == book_id).first()
#     return templates.TemplateResponse("overview.html", {"request": request, "movie": item})
#
#
# @app.post("/movie/")
# async def create_movie(db: Session = Depends(get_database_session), name: schema.Movie.name = Form(...), url: schema.Movie.url = Form(...), rate: schema.Movie.rating = Form(...), type: schema.Movie.type = Form(...), desc: schema.Movie.desc = Form(...)):
#     movie = Order(name=name, url=url, rating=rate, type=type, desc=desc)
#     db.add(movie)
#     db.commit()
#     db.refresh(movie)
#     response = RedirectResponse('/movie', status_code=303)
#     return response
#
#
# @app.patch("/movie/{id}")
# async def update_movie(request: Request, id: int, db: Session = Depends(get_database_session)):
#     requestBody = await request.json()
#     movie = db.query(Order).get(id)
#     movie.name = requestBody['name']
#     movie.desc = requestBody['desc']
#     db.commit()
#     db.refresh(movie)
#     newMovie = jsonable_encoder(movie)
#     return JSONResponse(status_code=200, content={
#         "status_code": 200,
#         "message": "success",
#         "movie": newMovie
#     })
#
#

