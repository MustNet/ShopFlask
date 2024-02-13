from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import os

database_path = os.path.join('C:\\', 'Users', 'musta', 'Verpackungsmodul', 'db.db')


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + database_path
app.config['SQLALCHEMY_TRACK_MODIFICATIONS']= False
db = SQLAlchemy(app)

class Message(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user = db.Column(db.String(200), nullable=True)
    article = db.Column(db.String(500), nullable=True)
    stk = db.Column(db.Integer, nullable=False)
    created_at = db.Column(db.DateTime(), default=datetime.utcnow)

class PurchasedItem(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user = db.Column(db.String(200), nullable=True)
    article = db.Column(db.String(500), nullable=True)
    stk = db.Column(db.Integer, nullable=False)
    purchased_at = db.Column(db.DateTime(), default=datetime.utcnow)


@app.route("/")
def home():
    messages = Message.query.all()  # Alle Datensätze aus der Datenbank holen
    return render_template('index2.html', messages=messages)


# Hier fügen Sie die neue Route hinzu
@app.route("/add-message", methods=["POST"])
def add_message():
    user = request.form.get('user')
    article = request.form.get('article')
    stk = request.form.get('stk')
    if not stk.isdigit():  # Einfache Validierung
        return "Quantity must be a number", 400
    stk = int(stk)
    new_message = Message(user=user, article=article, stk=stk)
    db.session.add(new_message)
    db.session.commit()
    return redirect("/")

@app.route("/purchase-item/<int:item_id>", methods=["POST"])
def purchase_item(item_id):
    item = Message.query.get(item_id)
    if item:
        purchased_item = PurchasedItem(user=item.user, article=item.article, stk=item.stk)
        db.session.add(purchased_item)
        db.session.delete(item)
        db.session.commit()
        return redirect("/")
    return "Item not found", 404


# Fügen Sie dies temporär am Ende Ihrer Flask-Datei hinzu
if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=True)


