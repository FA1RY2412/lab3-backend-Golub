
from ..db import db

class Category(db.Model):
    __tablename__ = "categories"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False, index=True)
    # If True -> visible to all users; if False -> only to the owner (user_id)
    is_global = db.Column(db.Boolean, default=False, nullable=False)

    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=True)
    user = db.relationship("User", back_populates="categories")

    expenses = db.relationship("Expense", back_populates="category")

    __table_args__ = (
        db.UniqueConstraint("name", "user_id", name="uq_cat_name_per_user"),
    )

    def __repr__(self):
        scope = "global" if self.is_global else f"user:{self.user_id}"
        return f"<Category {self.name} ({scope})>"
