from pdb import post_mortem
from flask import Blueprint, render_template, request, flash, redirect, url_for, jsonify
from flask_login import login_required, current_user
from .models import Post, User, Comment, Like, SearchForm
from . import db
# import flask_whooshalchemy as wa 

views = Blueprint("views", __name__)


@views.route("/")
@views.route("/home")
@login_required
def home():
    posts = Post.query.all()
    return render_template("home.html", user=current_user, posts=posts)

# Create Search Function for Navbar
@views.route("/search", methods=['GET', 'POST'])
@login_required
def search():
    posts = Post.query.whoosh_search(request.args.get('query')).all()

    return render_template("home.html", user=current_user, posts=posts)

@views.route("/create-post", methods=['GET', 'POST'])
@login_required
def create_post():
    if request.method == "POST":
        text = request.form.get('text')

        if not text:
            flash('Post cannot be empty', category='error')
        else:
            post = Post(text=text, author=current_user.id)
            db.session.add(post)
            db.session.commit()
            flash('Post created!', category='success')
            return redirect(url_for('views.home'))

    return render_template('create_post.html', user=current_user)

@views.route("/edit-post/<id>", methods=['GET', 'POST'])
@login_required
def edit_post(id):
    post_edit = Post.query.filter_by(id=id).first()
    # post_edit = request.form.get(id)
    if request.method == "POST":
        post_edit.text = request.form['text']
        try:
            db.session.commit()
            return redirect(url_for('views.home'))
        except:
            return flash('There was a problem updating that post!', category='error')
    else:
        # if not text:
        #     flash('Post cannot be edited', category='error')
        # else:
        #     post = Post(text=text, author=current_user.id)
        #     db.session.add(post)
        #     db.session.commit()
        #     flash('Post created!', category='success')
        #     return redirect(url_for('views.home'))
        return render_template('edit_post.html', user=current_user, post_edit=post_edit )

@views.route("/delete-post/<id>")
@login_required
def delete_post(id):
    post = Post.query.filter_by(id=id).first()

    if not post:
        flash("Post does not exist.", category='error')
    elif current_user.id != post.id:
        flash('You do not have permission to delete this post.', category='error')
    else:
        db.session.delete(post)
        db.session.commit()
        flash('Post deleted.', category='success')

    return redirect(url_for('views.home'))


@views.route("/posts/<username>")
@login_required
def posts(username):
    user = User.query.filter_by(username=username).first()

    if not user:
        flash('No user with that username exists.', category='error')
        return redirect(url_for('views.home'))

    posts = user.posts
    return render_template("posts.html", user=current_user, posts=posts, username=username)


@views.route("/create-comment/<post_id>", methods=['POST'])
@login_required
def create_comment(post_id):
    text = request.form.get('text')

    if not text:
        flash('Comment cannot be empty.', category='error')
    else:
        post = Post.query.filter_by(id=post_id)
        if post:
            comment = Comment(
                text=text, author=current_user.id, post_id=post_id)
            db.session.add(comment)
            db.session.commit()
        else:
            flash('Post does not exist.', category='error')

    return redirect(url_for('views.home'))

@views.route("/edit-comment/<id>", methods=['GET', 'POST'])
@login_required
def edit_comment(id):
    comment_edit = Comment.query.filter_by(id=id).first()
    # comment_edit = request.form.get(id)
    # in posts_div.html i had to remove {% or user.id == post.author %} from the condition
    if request.method == "POST":
        comment_edit.text = request.form['text']
        try:
            db.session.commit()
            return redirect(url_for('views.home'))
        except:
            return flash('There was a problem updating that comment!', category='error')
    else:
        # if not text:
        #     flash('Post cannot be edited', category='error')
        # else:
        #     post = Post(text=text, author=current_user.id)
        #     db.session.add(post)
        #     db.session.commit()
        #     flash('Post created!', category='success')
        #     return redirect(url_for('views.home'))
        return render_template('edit_comment.html', user=current_user, comment_edit=comment_edit )

@views.route("/delete-comment/<comment_id>")
@login_required
def delete_comment(comment_id):
    comment = Comment.query.filter_by(id=comment_id).first()

    if not comment:
        flash('Comment does not exist.', category='error')
    elif current_user.id != comment.author and current_user.id != comment.post.author:
        flash('You do not have permission to delete this comment.', category='error')
    else:
        db.session.delete(comment)
        db.session.commit()

    return redirect(url_for('views.home'))


@views.route("/like-post/<post_id>", methods=['GET', 'POST'])
@login_required
def like(post_id):
    post = Post.query.filter_by(id=post_id).first()
    like = Like.query.filter_by(
        author=current_user.id, post_id=post_id).first()

    if not post:
        return jsonify({'error': 'Post does not exist.'}, 400)
    elif like:
        db.session.delete(like)
        db.session.commit()
    else:
        like = Like(author=current_user.id, post_id=post_id)
        db.session.add(like)
        db.session.commit()

    return jsonify({"likes": len(post.likes), "liked": current_user.id in map(lambda x: x.author, post.likes)})

# Pass Data to Navbar
# @views.context_processor
# def base():
#     form = SearchForm()
#     return dict(form=form)

# Create Search Function for Navbar
# @views.route("/search", methods=['GET', 'POST'])
# @login_required
# def search():
#     posts = Post.query.whoosh
    # form = SearchForm()
    # posts = Post.query
    # if form.is_submitted() and form.validate():
    #     # Get data from submitted form
    #     post_searched = form.searched.data
    #     # Query the database
    #     posts = posts.filter(Post.text.like('%' + post_searched + '%'))
    #     posts = posts.order_by(Post.text).all()
    # else:
    #     flash('Cannot be searched', category='error')
    
    # return render_template('search.html', form=form, searched=post_searched, posts=posts)
