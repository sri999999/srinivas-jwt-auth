from flask import request, jsonify
from flask import Blueprint
from .models import Author, db
from .utils import dict_helper, CustomException


author_bp = Blueprint('author', __name__, url_prefix='/author')


@author_bp.errorhandler(CustomException)
def handle_scheduler_exception(e):
    return {"success": False, "error": e.message}, e.code

@author_bp.route('', methods=['POST'])
def create_author():
    name = request.json.get("name")
    author = Author(name=name)
    db.session.add(author)
    db.session.commit()
    response = {'message': 'Author created successfully', "data": author.serialize}
    return jsonify(response)


@author_bp.route('/<int:author_id>', methods=['PUT'])
def update_author(author_id):
    data = request.get_json()
    author = Author.query.get(author_id)
    if author is None:
        raise CustomException(f'author {author_id} not found', 404)

    for field in author.get_editable_fields:
        if field in data:
            setattr(author, field, data[field])

    db.session.add(author)
    db.session.commit()
    response = {
        'message': 'Author updated successfully',
        "data": author.serialize
    }
    return jsonify(response)


# @author_bp.route('/author/<int:author_id>', methods=['GET'])
@author_bp.route('', methods=['GET'])
def get_authors(author_id=None):
    author = Author.query
    if author_id:
        author = author.filter(Author.id == author_id).first()
        if author is None:
            raise CustomException(f'author {author_id} not found', 404)
        response = {'message': 'Author retrieved successfully', "data": author.serialize}
        return jsonify(response)
    author_list_dict = dict_helper(author.all())
    response = jsonify(author_list_dict)
    return response


@author_bp.route('/<int:author_id>', methods=['DELETE'])
def delete_author(author_id):
    author = Author.query.filter(Author.id == author_id).first()
    if author is None:
        raise CustomException(f'author {author_id} not found', 404)
    db.session.delete(author)
    db.session.commit()
    response = {
        'message': 'Author deleted successfully',
        "data": author.serialize
    }
    return jsonify(response)