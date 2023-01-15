from flask_sqlalchemy import SQLAlchemy
import datetime


db = SQLAlchemy()

def connect_db(app):
    """Connect to database."""
    db.app = app
    db.init_app(app)


"""Models for Blogly."""


class User(db.Model):
    """Contains all user information related to a user"""
    def __repr__(self):
        return f"User: {self.id} {self.first_name} {self.last_name}"
    
    __tablename__ = "users"
    
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    first_name = db.Column(db.String(50), nullable=False)
    last_name = db.Column(db.String(50), nullable=False)
    image_url = db.Column(db.String(100), default = "https://www.pngitem.com/pimgs/m/146-1468479_my-profile-icon-blank-profile-picture-circle-hd.png", nullable=False)
    posts = db.relationship("Post", backref="user", cascade="all, delete-orphan")
    
    @property
    def full_name(self):
        """Can be called with 'example.full_name' """
        return f"{self.first_name} {self.last_name}"
    
    
    
class Post(db.Model):
    """Post created by a user"""
    def __repr__(self):
        return f"Post: ID{self.id} UserID {self.user_id} Title {self.title} {self.created_at}"
    
    default_time= datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    __tablename__ = "posts"
    
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String(50), nullable=False)
    content = db.Column(db.String(50), nullable=False)
    created_at = db.Column(db.DateTime, default=default_time, onupdate=default_time, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"))
    
    
class Tag(db.Model):
    """Tag created for describing a post"""
    def __repr__(self):
        return f"Tag {self.id} {self.name}"

    __tablename__ = "tags"
    
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(20), nullable=False, unique=True)
    
    posts_tags = db.relationship('Post',secondary='posts_tags', backref='tags')

    
class PostTag(db.Model):
    """Mapping a post to a tag"""
    
    def __repr__(self):
        return f"Tag: Post {self.post_id} Tag {self.tag_id}"
    __tablename__ = "posts_tags"
    
    post_id = db.Column(db.Integer, db.ForeignKey("posts.id"), primary_key=True)
    tag_id = db.Column(db.Integer, db.ForeignKey("tags.id"), primary_key=True)
    
    __table_args__ = (db.PrimaryKeyConstraint(post_id, tag_id),)