
from flask.views import MethodView
from flask import request
from flask_smorest import Blueprint, abort
from ..db import db
from ..models import Category, User
from ..schemas.category import CategoryCreateSchema, CategoryOutSchema

blp = Blueprint("categories", __name__, description="Category endpoints")

def _require_user():
    # For lab simplicity: we emulate auth via header
    uid = request.headers.get("X-User-Id")
    if not uid:
        abort(400, message="X-User-Id header is required")
    try:
        uid = int(uid)
    except ValueError:
        abort(400, message="X-User-Id must be integer")
    user = db.session.get(User, uid)
    if not user:
        # auto-create user to simplify manual testing
        user = User(id=uid, username=f"user{uid}")
        db.session.add(user)
        db.session.commit()
    return user

@blp.route("")
class CategoryList(MethodView):
    @blp.response(200, CategoryOutSchema(many=True))
    def get(self):
        user = _require_user()
        # global OR owned by user
        q = Category.query.filter((Category.is_global == True) | (Category.user_id == user.id))
        return q.order_by(Category.is_global.desc(), Category.name.asc()).all()

    @blp.arguments(CategoryCreateSchema)
    @blp.response(201, CategoryOutSchema)
    def post(self, payload):
        user = _require_user()
        # Only user-scoped categories are allowed in this lab (is_global forced False)
        cat = Category(
            name=payload["name"],
            is_global=False,
            user_id=user.id
        )
        db.session.add(cat)
        try:
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            abort(409, message="Category with this name already exists for this user")
        return cat

@blp.route("/<int:cat_id>")
class CategoryItem(MethodView):
    @blp.response(200, CategoryOutSchema)
    def get(self, cat_id):
        user = _require_user()
        cat = db.session.get(Category, cat_id)
        if not cat or (not cat.is_global and cat.user_id != user.id):
            abort(404, message="Category not found")
        return cat

    def delete(self, cat_id):
        user = _require_user()
        cat = db.session.get(Category, cat_id)
        if not cat or (not cat.is_global and cat.user_id != user.id):
            abort(404, message="Category not found or not owned")
        if cat.is_global:
            abort(403, message="Global categories cannot be deleted")
        db.session.delete(cat)
        db.session.commit()
        return {"status": "deleted", "id": cat_id}, 200
