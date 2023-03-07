from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///reviews.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class Review(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    content = db.Column(db.Text, nullable=False)
    rating = db.Column(db.Integer, nullable=False)

@app.route('/')
def index():
    reviews = Review.query.all()
    return render_template('index.html', reviews=reviews)

@app.route('/add', methods=['GET', 'POST'])
def add_review():
    if request.method == 'POST':
        title = request.form['title']
        content = request.form['content']
        rating = request.form['rating']
        review = Review(title=title, content=content, rating=rating)
        db.session.add(review)
        db.session.commit()
        return redirect(url_for('index'))
    return render_template('add_review.html')

if __name__ == '__main__':
    app.run(debug=True)