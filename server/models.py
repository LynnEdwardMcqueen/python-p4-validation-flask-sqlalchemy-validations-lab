from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import validates
from sqlalchemy.exc import IntegrityError
from math import log10

db = SQLAlchemy()

debug_list = []
class Author(db.Model):
    __tablename__ = 'authors'
    # Add validations and constraints 

    id = db.Column(db.Integer, primary_key=True)
    name= db.Column(db.String, unique=True, nullable=False)
    phone_number = db.Column(db.String)
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    updated_at = db.Column(db.DateTime, onupdate=db.func.now())

    def __repr__(self):
        return f'Author(id={self.id}, name={self.name} phone = {self.phone_number})'

    @validates('name')
    def validate_email(self, key, author_name):
        # Check to make sure a name was included
        if not author_name:
            raise ValueError("no author name given.")
        
        # Check to see that the given name is unique in the database.
        existing_authors = Author.query.all()
        debug_list.append(author_name)
        for author in existing_authors:
            debug_list.append(f"author.name = {author.name}")
            if (author.name == author_name):
                raise IntegrityError("All author names are unique.")
        return author_name
    
    @validates('phone_number')
    def validate_phone_number(self, key, author_phone_number):
        debug_list.append(author_phone_number)
        phone = int(author_phone_number)
        debug_list.append(phone)
        if not (11 >= log10(phone) or log10(phone) < 10):
            raise ValueError("Phone number is not 10 digits")

class Post(db.Model):
    __tablename__ = 'posts'
    # Add validations and constraints 

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String, nullable=False)
    content = db.Column(db.String)
    category = db.Column(db.String)
    summary = db.Column(db.String)
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    updated_at = db.Column(db.DateTime, onupdate=db.func.now())

    @validates('title')
    def validate_post_title(self, key, post_title):
        if not post_title:
            raise ValueError("no title given.")
        if post_title == "Why I love programming.":
            raise ValueError("NERD LEVEL ACTIVATE!")
        return post_title
        
    @validates('content')
    def validate_post_content(self, key, post_content):
        if len(post_content) < 250:
            raise ValueError("Post content less than 250 characters")
        return post_content

    @validates('summary')
    def validate_post_summary(self, key, post_summary):
        if len(post_summary) >= 250:
            raise ValueError("Post Summary content greater than 250 characters")
        return post_summary
    
    @validates('category')
    def validate_post_category(self, key, post_category):
        if post_category not in ("Fiction", "Non-Fiction"):
            raise ValueError("Either Fiction or Non-Fiction")
        return post_category

    def __repr__(self):
        return f'Post(id={self.id}, title={self.title} content={self.content}, summary={self.summary})'
