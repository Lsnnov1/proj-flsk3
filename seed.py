from models import db, User
from app import app


db.drop_all()
db.create_all()


river=User(first_name="River", last_name="Bottom", img_url="")
mac=User(first_name="Mac", last_name="Book", img_url="")
bob=User(first_name="Bob", last_name="Bobbins", img_url="")
kurt=User(first_name="Kurt", last_name="Cobain", img_url="")
cat=User(first_name="Tabby", last_name="Cat", img_url="")

db.session.add(river)
db.session.add(mac)
db.session.add(bob)
db.session.add(kurt)
db.session.add(cat)


db.session.commit()