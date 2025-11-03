
from ..db import db

class User(db.Model):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)

    categories = db.relationship("Category", back_populates="user", cascade="all,delete")
    expenses = db.relationship("Expense", back_populates="user", cascade="all,delete")

    def __repr__(self):
        return f"<User {self.username}>"
