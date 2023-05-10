from flask import request, jsonify
from flask import Blueprint
from .models import Book, db
from .utils import dict_helper, CustomException


book_bp = Blueprint('book', __name__, url_prefix='/books')

@book_bp.errorhandler(CustomException)
def handle_scheduler_exception(e):
    return {"success": False, "error": e.message}, e.code


@book_bp.route('', methods=['POST'])
def create_author():
    title = request.json.get("title")
    author_id = request.json.get("author_id")
    year_published = request.json.get("year_published")
    params = request.json.get("params")
    book = Book(title=title, author_id=author_id, year_published=year_published, params=params)
    db.session.add(book)
    db.session.commit()
    response = {'message': 'Book created successfully', "data": book.serialize}
    return jsonify(response)


@book_bp.route('/<int:book_id>', methods=['PUT'])
def update_book(book_id):
    data = request.get_json()
    book = Book.query.get(book_id)

    if book is None:
        raise CustomException(f'Book {book_id} not found', 404)

    for field in book.get_editable_fields:
        if field in data:
            setattr(book, field, data[field])

    db.session.add(book)
    db.session.commit()
    response = {
        'message': 'Book updated successfully',
        "data": book.serialize
    }
    return jsonify(response)


@book_bp.route('/<int:book_id>', methods=['GET'])
@book_bp.route('', methods=['GET'])
def get_books(book_id=None):
    book = Book.query
    if book_id:
        book = book.filter(Book.id == book_id).first()
        if book is None:
            raise CustomException(f'Book {book_id} not found', 404)
        response = {'message': 'Book retrieved successfully', "data": book.serialize}
        return jsonify(response)
    book_list_dict = dict_helper(book.all())
    response = jsonify(book_list_dict)
    return response

@book_bp.route('/<int:book_id>', methods=['DELETE'])
def delete_book(book_id):
    book = Book.query.get(book_id)
    if book is None:
        raise CustomException(f'Book {book_id} not found', 404)
    db.session.delete(book)
    db.session.commit()
    response = {
        'message': 'Book deleted successfully',
        "data": book.serialize
    }
    return jsonify(response)