from flask_sqlalchemy import SQLAlchemy

"""Models for Blogly."""
db = SQLAlchemy()

def connect_db(app):
    db.app = app
    db.init_app(app)


    __tablename__ = 'users'

class User(db.Model):
    """create users schema"""

    id = db.Column(db.Integer,
                   primary_key=True,
                   autoincrement=True)
    
    first_name = db.Column(db.String(25), 
                           nullable=False)
    
    last_name = db.Column(db.String(20),
                          nullable=False)
    
    img_url = db.Column(db.String(50),
                        nullable=True,
                        default="https://www.google.com/url?sa=i&url=https%3A%2F%2Fwww.vecteezy.com%2Ffree-vector%2Fdefault-profile-picture&psig=AOvVaw1cSE6VukWBYfPTIRBVikNn&ust=1719591855681000&source=images&cd=vfe&opi=89978449&ved=0CBEQjRxqFwoTCPC5g_-Y_IYDFQAAAAAdAAAAABAE")
    

    def __repr__(self):
        """Shows self instance"""
        u = self
        return f"User id={u.id}, {u.first_name} {u.last_name}, {u.img_url}."
    
