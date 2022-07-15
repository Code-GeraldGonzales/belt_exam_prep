from flask import render_template, redirect, request, session, flash
from flask_app import app
from flask_app.models.review import Review
from flask_app.models.user import User
from flask_bcrypt import Bcrypt
bcrypt = Bcrypt(app)

@app.route('/dashboard')
def user_dashboard():
    user_data = {
        'id': session['user_id']
    }
    user = User.get_user_by_id(user_data)
    reviews = Review.get_all()
    return render_template('dashboard.html', user=user, reviews=reviews)

@app.route('/reviews/new')
def new_review_form():
    user_data = {
        'id': session['user_id']
    }
    user = User.get_user_by_id(user_data)
    return render_template("create_review.html", user=user)

@app.route('/reviews/create', methods=['POST'])
def create_review():
    if not Review.validate_create(request.form):
        return redirect('reviews/new')
    Review.create(request.form)
    return redirect('/dashboard')

@app.route('/reviews/<int:id>')
def show_review(id):
    user_data = {
        'id': session['user_id']
    }
    user = User.get_user_by_id(user_data)
    review_data = {
        'id': id
    }
    review = Review.get_one(review_data)
    return render_template('show_review.html', review=review, user=user)

@app.route('/reviews/<int:id>/edit')
def show_edit_form(id):
    user_data = {
        'id': session['user_id']
    }
    user = User.get_user_by_id(user_data)
    review_data = {
        'id': id
    }
    review = Review.get_one(review_data)
    if(review.user_id != user.id):
        flash(f"Unathorized access to the edit review with id {id}")
    return render_template('edit_review.html', user=user, review=review)

@app.route('/reviews/<int:id>/update', methods=['POST'])
def update_review(id):
    Review.update(request.form)
    return redirect('/dashboard')

@app.route('/reviews/<int:id>/delete', methods=['POST'])
def delete(id):
    review_data = {
        'id': id
    }
    review = Review.get_one(review_data)
    if(review.user_id != session['user_id']):
        flash(f"Unauthorized access to edit review with id {id}")
        return redirect('/dashboard')
    Review.delete(request.form)
    return redirect('/dashboard')