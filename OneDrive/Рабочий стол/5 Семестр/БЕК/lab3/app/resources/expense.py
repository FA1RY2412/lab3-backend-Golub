
from flask.views import MethodView
from flask import request
from flask_smorest import Blueprint, abort
from ..db import db
from ..models import Expense, Category, User
from ..schemas.expense import ExpenseCreateSchema, ExpensePatchSchema, ExpenseOutSchema

blp = Blueprint("expenses", __name__, description="Expense endpoints")

def _require_user():
    uid = request.headers.get("X-User-Id")
    if not uid:
        abort(400, message="X-User-Id header is required")
    try:
        uid = int(uid)
    except ValueError:
        abort(400, message="X-User-Id must be integer")
    user = db.session.get(User, uid)
    if not user:
        user = User(id=uid, username=f"user{uid}")
        db.session.add(user)
        db.session.commit()
    return user

def _user_can_use_category(user, category: Category | None) -> bool:
    if category is None:
        return True
    if category.is_global:
        return True
    return category.user_id == user.id

@blp.route("")
class ExpenseList(MethodView):
    @blp.response(200, ExpenseOutSchema(many=True))
    def get(self):
        user = _require_user()
        return Expense.query.filter_by(user_id=user.id).order_by(Expense.id.desc()).all()

    @blp.arguments(ExpenseCreateSchema)
    @blp.response(201, ExpenseOutSchema)
    def post(self, payload):
        user = _require_user()

        category = None
        if payload.get("category_id") is not None:
            category = db.session.get(Category, payload["category_id"])
            if not category:
                abort(400, message="category_id does not exist")
            if not _user_can_use_category(user, category):
                abort(403, message="You cannot use this category")

        exp = Expense(
            amount=payload["amount"],
            description=payload.get("description"),
            user_id=user.id,
            category_id=category.id if category else None
        )
        db.session.add(exp)
        db.session.commit()
        return exp

@blp.route("/<int:expense_id>")
class ExpenseItem(MethodView):
    @blp.response(200, ExpenseOutSchema)
    def get(self, expense_id):
        user = _require_user()
        exp = db.session.get(Expense, expense_id)
        if not exp or exp.user_id != user.id:
            abort(404, message="Expense not found")
        return exp

    @blp.arguments(ExpensePatchSchema)
    @blp.response(200, ExpenseOutSchema)
    def patch(self, payload, expense_id):
        user = _require_user()
        exp = db.session.get(Expense, expense_id)
        if not exp or exp.user_id != user.id:
            abort(404, message="Expense not found")

        if "amount" in payload:
            exp.amount = payload["amount"]
        if "description" in payload:
            exp.description = payload["description"]
        if "category_id" in payload:
            if payload["category_id"] is None:
                exp.category_id = None
            else:
                category = db.session.get(Category, payload["category_id"])
                if not category:
                    abort(400, message="category_id does not exist")
                # ensure user can use this category
                if category.is_global or category.user_id == user.id:
                    exp.category_id = category.id
                else:
                    abort(403, message="You cannot use this category")
        db.session.commit()
        return exp

    def delete(self, expense_id):
        user = _require_user()
        exp = db.session.get(Expense, expense_id)
        if not exp or exp.user_id != user.id:
            abort(404, message="Expense not found")
        db.session.delete(exp)
        db.session.commit()
        return {"status": "deleted", "id": expense_id}, 200
