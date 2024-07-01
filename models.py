from flask_sqlalchemy import SQLAlchemy

"""Models for Blogly."""
db = SQLAlchemy()

def connect_db(app):
    db.app = app
    db.init_app(app)




class User(db.Model):
    """create users schema"""
    __tablename__ = 'users'

    id = db.Column(db.Integer,
                   primary_key=True,
                   autoincrement=True)
    
    first_name = db.Column(db.String(25), 
                           nullable=False)
    
    last_name = db.Column(db.String(20),
                          nullable=False)
    
    img_url = db.Column(db.String(50),
                        nullable=True,
                        default="https://www.vecteezy.com/free-vector/default-profile-picture")
    
    
    def __repr__(self):
        """Shows self instance"""
        u = self
        return f"User id={u.id}, {u.first_name} {u.last_name}, {u.img_url}."
    
class Post(db.Model):
    """Shows user posts"""
    __tablename__ = 'posts'

    id = db.Column(db.Integer, 
                   primary_key=True, 
                   autoincrement=True)
    title = db.Column(db.String(20), 
                      nullable=False)
    content = db.Column(db.String(100),
                        nullable=False)
    created_at = db.Column(db.DateTime, 
                           nullable=False, 
                           default=db.func.current_timestamp())
    
    user_id = db.Column(db.Integer, 
                        db.ForeignKey("users.id"), 
                        nullable=False)

    user = db.relationship('User', backref=db.backref('posts'))