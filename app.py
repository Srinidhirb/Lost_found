from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime, timezone

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///LostDb.db"
db = SQLAlchemy(app)


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    item_name = db.Column(db.String(50), nullable=False)  # Fixed type to String
    item_desc = db.Column(db.String(100), nullable=False)  # Increased length
    owner_name = db.Column(db.String(50), nullable=False)
    owner_number = db.Column(db.String(15), nullable=False)  # String for phone numbers
    lost_date = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))
    location = db.Column(db.String(50), nullable=False)

    def __repr__(self) -> str:
        return f"{self.owner_name} - {self.item_name}"

class FoundItem(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    item_name = db.Column(db.String(50), nullable=False)
    item_desc = db.Column(db.String(100), nullable=False)
    owner_name = db.Column(db.String(50), nullable=False)
    owner_number = db.Column(db.String(15), nullable=False)
    found_date = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))
    lost_date = db.Column(db.DateTime)
    location = db.Column(db.String(50), nullable=False)

    def __repr__(self) -> str:
        return f"{self.owner_name} - {self.item_name}"
@app.route("/")
def index():
    users = User.query.all()
    return render_template("index.html", users=users)




@app.route("/add", methods=["GET", "POST"])
def add():
    if request.method == "POST":
        item_name = request.form.get("item_name")
        item_desc = request.form.get("item_desc")
        owner_name = request.form.get("owner_name")
        owner_number = request.form.get("owner_number")
        location = request.form.get("location")

        new_user = User(
            item_name=item_name,
            item_desc=item_desc,
            owner_name=owner_name,
            owner_number=owner_number,
            location=location
        )
        db.session.add(new_user)
        db.session.commit()
        return redirect(url_for("index"))
    
    return render_template("add.html")


@app.route("/list")
def list_items():
    users = User.query.all()
    return render_template("list.html", users=users)

@app.route("/update/<int:id>", methods=["GET", "POST"])
def update(id):
    user = User.query.get_or_404(id)
    if request.method == "POST":
        user.item_name = request.form.get("item_name")
        user.item_desc = request.form.get("item_desc")
        user.owner_name = request.form.get("owner_name")
        user.owner_number = request.form.get("owner_number")
        user.location = request.form.get("location")

        db.session.commit()
        return redirect(url_for("index"))
    
    return render_template("add.html", user=user)

@app.route("/delete/<int:id>")
def delete(id):
    user = User.query.get_or_404(id)
    db.session.delete(user)
    db.session.commit()
    return redirect(url_for("index"))

@app.route("/search", methods=["GET", "POST"])
def search():
    query = request.args.get("query", "")
    users = User.query.filter(
        (User.item_name.ilike(f"%{query}%")) |
        (User.item_desc.ilike(f"%{query}%")) |
        (User.owner_name.ilike(f"%{query}%")) |
        (User.location.ilike(f"%{query}%"))
    ).all()
    return render_template("search.html", users=users, query=query)
@app.route("/mark_as_found/<int:id>")
def mark_as_found(id):
    user = User.query.get_or_404(id)
    
    # Add the item to the found items database
    found_item = FoundItem(
        item_name=user.item_name,
        item_desc=user.item_desc,
        owner_name=user.owner_name,
        owner_number=user.owner_number,
        found_date=datetime.now(timezone.utc),
        lost_date=user.lost_date,
        location=user.location
    )
    db.session.add(found_item)
    
    # Remove the item from the lost items database
    db.session.delete(user)
    db.session.commit()
    
    return redirect(url_for("found_items"))


@app.route("/found_items")
def found_items():
    found_items = FoundItem.query.all()
    return render_template("found_items.html", found_items=found_items)

if __name__ == "__main__":
 # In your Flask app
    with app.app_context():
        # Drop the old table
         db.create_all()
        # Create all tables with the new schema
     

    app.run(debug=True)
