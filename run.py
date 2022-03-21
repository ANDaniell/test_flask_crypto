from flask_admin import Admin

from server import create_app, resset_db,create_user, db
from server.admin.routes import create_admin

app = create_app()



if __name__ == '__main__':
    from flask_admin.contrib.sqla import ModelView
    create_user()
    #resset_db()
    create_admin(app,db)
    app.run(debug=True)