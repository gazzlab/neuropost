import sys
from main import db, User
if len(sys.argv) > 1 and raw_input('Drop tables? [yes/N] ') == 'yes':
  db.drop_all()
db.create_all()
ed_user = User('ed', 'Ed Jones', 'ed@example.com', 'password')
db.session.add(ed_user)
db.session.commit()
print User.query.all()
