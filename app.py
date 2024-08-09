from flask import Flask , render_template ,request,redirect
from flask_sqlalchemy import SQLAlchemy

from datetime import datetime , timezone

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///project.db"
db = SQLAlchemy(app)
class User(db.Model):
    id = db.Column(db.Integer , primary_key = True)
    Item_name = db.Column(db.Integer , primary_key = True)
    Item_desc = db.Column(db.String(20), nullable = False)
    Owner_name = db.Column(db.String(20), nullable = False)
    Owner_number = db.Column(db.Integer, nullable = False)
    

    Lost_date = db.Column(db.DateTime , default = lambda: datetime.now(timezone.utc))
    Location =  db.Column(db.String(20), nullable = False)
    
    def __repr__(self) -> str:
        return f"{self.Name} - {self.Pass}"
    
    
    
    
# @app.route('/' ,methods=['Get','Post'])
# def home():
#     if request.method=="POST":
#         name = request.form['mail']
#         pas = request.form['pass']
       
#         obj = User(Name=name , Pass =pas, ePass=ep)
#         db.session.add(obj)
#         db.session.commit()
#     users = User.query.all()
#     return render_template('index.html' , all_users = users )
#     # return 'hello word'
    
# @app.route('/delete/<int:id>')
# def delete(id):
#     user = User.query.filter_by(id = id).first()
#     db.session.delete(user)
#     db.session.commit()
#     return redirect("/")


# @app.route('/update/<int:id>', methods=["Get","Post"])
# def update(id):
#     if request.method=="POST":
#         mail=request.form['mail']
#         pa=request.form['pass']
#         user = User.query.filter_by(id = id).first()
#         user.Name = mail
#         user.Pass = pa
#         db.session.add(user)
#         db.session.commit()
#         return redirect("/")
    
    
#     user = User.query.filter_by(id = id).first()
#     return render_template('update.html' , all_users = user )
    
if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=True)