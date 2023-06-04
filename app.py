from flask import  Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy
from main import main

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///mbt.sqlite3'
db = SQLAlchemy(app)
db.app = app

@app.route('/')
def index():
    db.create_all()

    create_test_data()

    not_exist = request.args['ne'] if 'ne' in  request.args else None
    return render_template('login.html', ne=not_exist)

def create_test_data():
    import models
    
    is_superadmin_existing = models.Users.query.filter_by(name='superadmin').first()
    if is_superadmin_existing is None:
        # Insert User
        _superadmin = models.Users(
            name='superadmin',
            password='Super123!',
            email='super@email.com'
        )
        db.session.add(_superadmin)

    
    

app.register_blueprint(main)
   
if __name__ == '__main__':
    app.run(debug=True)