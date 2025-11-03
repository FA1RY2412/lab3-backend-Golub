
from ..db import db
from sqlalchemy import CheckConstraint

class Expense(db.Model):
    __tablename__ = "expenses"

    id = db.Column(db.Integer, primary_key=True)
    amount = db.Column(db.Numeric(12, 2), nullable=False)
    description = db.Column(db.String(255), nullable=True)

    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False, index=True)
    user = db.relationship("User", back_populates="expenses")

    category_id = db.Column(db.Integer, db.ForeignKey("categories.id"), nullable=True)
    category = db.relationship("Category", back_populates="expenses")

    __table_args__ = (
        CheckConstraint("amount >= 0", name="ck_expense_amount_nonnegative"),
    )

    def __repr__(self):
        return f"<Expense {self.id} {self.amount}>"
