from flask import Flask, render_template, request, redirect, url_for, flash
from flask_wtf import FlaskForm
from wtforms import IntegerField, SubmitField
from wtforms.validators import DataRequired, NumberRange
from flask_bootstrap import Bootstrap
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

bootstrap = Bootstrap(app)
app.config['SECRET_KEY'] = "top secret password don't tell anyone this"
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///equipment.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

class Equipment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    price = db.Column(db.String(20), nullable=False)
    description = db.Column(db.String(200))
    image_path = db.Column(db.String(120))

    def __repr__(self):
        return '<Equipment %r>' % self.name

class AddToBasketForm(FlaskForm):
    quantity = IntegerField('Quantity', validators=[DataRequired(), NumberRange(min=1)])
    submit = SubmitField('Add to Basket')

@app.route('/', methods=['GET', 'POST'])
def galleryPage():
    equipment = Equipment.query.all() 
    return render_template('index.html',title = "index", equipment=equipment)

@app.route('/equipment/<int:itemId>', methods=['GET', 'POST'])
def singleProductPage(itemId):
    form = AddToBasketForm()
    items = Equipment.query.all()
    if form.validate_on_submit() and items:
        quantity = int(form.quantity.data)
        flash(f"You added {quantity} {items[itemId].name}(s) to the basket")
        return redirect(url_for('singleProductPage', item=items[itemId], itemId = itemId))
    if items:
         return render_template('SingleTech.html', item=items[itemId],itemId = itemId, form=form)
    else:
        return "item not found", 404

    
    

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True,port=5000)