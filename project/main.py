from flask import Blueprint, render_template, request
from . import db
from flask_login import login_required, current_user
from project.models import Post, Subreddit, User, Comment
from datetime import datetime

main = Blueprint('main', __name__)

@main.route('/')
def index():
    all_posts = Post.query.all()
    subreddits = Subreddit.query.all()
    return render_template('index.html', all_posts=all_posts, subreddits=subreddits, profile=False)

@main.route('/upvote_post/<post_id>')
def upvote_post(post_id):
    subreddits = Subreddit.query.all()
    post = Post.query.filter_by(id=post_id).first_or_404()
    post.votes = post.votes + 1
    db.session.commit()
    all_posts = Post.query.all()
    return render_template('index.html', all_posts=all_posts, subreddits=subreddits, profile=False)

@main.route('/downvote_post/<post_id>')
def downvote_post(post_id):
    post = Post.query.filter_by(id=post_id).first_or_404()
    subreddits = Subreddit.query.all()
    post.votes = post.votes - 1
    db.session.commit()
    all_posts = Post.query.all()
    return render_template('index.html', all_posts=all_posts, subreddits=subreddits)

@main.route('/', methods=['POST'])
def create_post():
    title = request.form['post-title']
    content = request.form['post-content'] 
    subreddit = request.form['subreddit']
    if subreddit == 'Music':
        subreddit_id = 0
    elif subreddit == 'Funny':
        subreddit_id = 1
    elif subreddit == 'Programming':
        subreddit_id = 2
    elif subreddit == 'News':
        subreddit_id = 3
    elif subreddit == 'Design':
        subreddit_id = 4
    else:
        subreddit_id = 5 

    time = datetime.now()
    newtime = datetime.strftime(time, '%d/%m/%Y')
    print('newtime: ', newtime)
    print('time: ', time)
    print('newtime: ', type(newtime))
    subreddits = Subreddit.query.all()
    sub = subreddit
    newPost = Post(title=title, description=content, sub=sub, votes=0, user=current_user, subreddit_id=subreddit_id, timestamp=newtime)
    db.session.add(newPost)
    db.session.commit()
    all_posts = Post.query.all()
    return render_template('index.html', name=current_user.name, all_posts=all_posts, subreddits=subreddits, profile=False)    

@main.route('/delete_post/<post_id>/<user_id>', methods=['GET'])
def delete_post(post_id, user_id):
    target_post = Post.query.filter_by(id=post_id).first_or_404()    
    print('post: ', target_post)
    db.session.delete(target_post)
    db.session.commit()
    subreddits = Subreddit.query.all()
    user_posts = Post.query.filter_by(user_id=user_id)
    current_user = User.query.filter_by(id=user_id).first_or_404()
    return render_template('profile.html', user_posts=user_posts, name=current_user.name, subreddits=subreddits)

@main.route('/subreddits/<sub_name>')
def get_posts_for_subreddit(sub_name):
    subreddits = Subreddit.query.all()
    music_posts = Post.query.filter_by(sub=sub_name)
    return render_template('subreddit_details.html', music_posts=music_posts, subreddits=subreddits, sub_name=sub_name)

@main.route('/all')
def get_all_posts():
    subreddits = Subreddit.query.all()
    all_posts = Post.query.all()
    return render_template('index.html', all_posts=all_posts, subreddits=subreddits)

@main.route('/upvote_post_subreddit/<sub_name>/<post_id>')
def upvote_post_subreddit(post_id, sub_name):
    subreddits = Subreddit.query.all()
    post = Post.query.filter_by(id=post_id).first_or_404()
    post.votes = post.votes + 1
    db.session.commit()
    music_posts = Post.query.filter_by(sub=sub_name)
    return render_template('subreddit_details.html', music_posts=music_posts, subreddits=subreddits, sub_name=sub_name)

@main.route('/downvote_post_subreddit/<sub_name>/<post_id>')
def downvote_post_subreddit(post_id, sub_name):
    subreddits = Subreddit.query.all()
    post = Post.query.filter_by(id=post_id).first_or_404()
    post.votes = post.votes - 1
    db.session.commit()
    music_posts = Post.query.filter_by(sub=sub_name)
    return render_template('subreddit_details.html', music_posts=music_posts, subreddits=subreddits, sub_name=sub_name)

@main.route('/profile<user_id>', methods=['GET', 'POST'])
@login_required
def profile(user_id):
    subreddits = Subreddit.query.all()
    user_posts = Post.query.filter_by(user_id=user_id)
    current_user = User.query.filter_by(id=user_id).first_or_404()
    return render_template('profile.html', user_posts=user_posts, name=current_user.name, subreddits=subreddits, profile=True)

@main.route('/user/<user_id>', methods=['GET', 'POST'])
def user_profile(user_id):
    subreddits = Subreddit.query.all()
    user_posts = Post.query.filter_by(user_id=user_id)
    current_user = User.query.filter_by(id=user_id).first_or_404()
    return render_template('user.html', user_posts=user_posts, name=current_user.name, subreddits=subreddits)

@main.route('/upvote_post_user/<user_id>/<post_id>')
def upvote_post_user(post_id, user_id):
    subreddits = Subreddit.query.all()
    current_user = User.query.filter_by(id=user_id).first_or_404()
    post = Post.query.filter_by(id=post_id).first_or_404()
    post.votes = post.votes + 1
    db.session.commit()
    user_posts = Post.query.filter_by(user_id=user_id)
    return render_template('user.html', user_posts=user_posts, subreddits=subreddits, name=current_user.name)

@main.route('/downvote_post_user/<user_id>/<post_id>')
def downvote_post_user(post_id, user_id):
    subreddits = Subreddit.query.all()
    current_user = User.query.filter_by(id=user_id).first_or_404()
    post = Post.query.filter_by(id=post_id).first_or_404()
    post.votes = post.votes - 1
    db.session.commit()
    user_posts = Post.query.filter_by(user_id=user_id)
    return render_template('user.html', user_posts=user_posts, subreddits=subreddits, name=current_user.name)

@main.route('/upvote_post_profile/<user_id>/<post_id>')
def upvote_post_profile(post_id, user_id):
    subreddits = Subreddit.query.all()
    current_user = User.query.filter_by(id=user_id).first_or_404()
    post = Post.query.filter_by(id=post_id).first_or_404()
    post.votes = post.votes + 1
    db.session.commit()
    user_posts = Post.query.filter_by(user_id=user_id)
    return render_template('profile.html', user_posts=user_posts, subreddits=subreddits, name=current_user.name, profile=True)

@main.route('/downvote_post_profile/<user_id>/<post_id>')
def downvote_post_profile(post_id, user_id):
    subreddits = Subreddit.query.all()
    current_user = User.query.filter_by(id=user_id).first_or_404()
    post = Post.query.filter_by(id=post_id).first_or_404()
    post.votes = post.votes - 1
    db.session.commit()
    user_posts = Post.query.filter_by(user_id=user_id)
    return render_template('profile.html', user_posts=user_posts, subreddits=subreddits, name=current_user.name, profile=True)

@main.route('/post_details/<post_id>', methods=['GET', 'POST'])
def post_details(post_id):
    subreddits = Subreddit.query.all()
    target_post = Post.query.filter_by(id=post_id).first_or_404()
    comments = Comment.query.filter_by(post_id=post_id)
    print('target_post: ', target_post)
    return render_template('post_details.html', post=target_post, name=current_user.name, subreddits=subreddits, comments=comments)

@main.route('/upvote_post_details/<user_id>/<post_id>')
def upvote_post_details(post_id, user_id):
    subreddits = Subreddit.query.all()
    current_user = User.query.filter_by(id=user_id).first_or_404()
    target_post = Post.query.filter_by(id=post_id).first_or_404()
    comments = Comment.query.filter_by(post_id=post_id)
    target_post.votes = target_post.votes + 1
    db.session.commit()
    user_posts = Post.query.filter_by(user_id=user_id)
    return render_template('post_details.html', post=target_post, subreddits=subreddits, comments=comments)

@main.route('/downvote_post_details/<user_id>/<post_id>')
def downvote_post_details(post_id, user_id):
    subreddits = Subreddit.query.all()
    current_user = User.query.filter_by(id=user_id).first_or_404()
    target_post = Post.query.filter_by(id=post_id).first_or_404()
    comments = Comment.query.filter_by(post_id=post_id)
    target_post.votes = target_post.votes - 1
    db.session.commit()
    user_posts = Post.query.filter_by(user_id=user_id)
    return render_template('post_details.html', post=target_post, subreddits=subreddits, comments=comments)

@main.route('/create_comment/<post_id>/<user_id>', methods=['POST'])
def create_comment(post_id, user_id):
    target_post = Post.query.filter_by(id=post_id).first_or_404()
    subreddits = Subreddit.query.all()
    text = request.form['comment-text']
    post_id = post_id
    user_id = user_id
    author_id = User.query.filter_by(name=current_user.name).first_or_404().id
    author = User.query.filter_by(id=user_id).first_or_404().name
    print('author: ', author)
    time = datetime.strptime('01/01/2010', '%d/%m/%Y')
    newtime = datetime.strftime(time, '%d/%m/%Y')
    new_comment = Comment(text=text, post_id=post_id, user_id=user_id, author=author, votes=0, timestamp=newtime)
    comments = Comment.query.filter_by(post_id=post_id)
    db.session.add(new_comment)
    db.session.commit()
    return render_template('post_details.html', post=target_post, name=current_user.name, subreddits=subreddits, comments=comments)

@main.route('/upvote_comment/<user_id>/<post_id>/<comment_id>')
def upvote_comment(post_id, user_id, comment_id):
    subreddits = Subreddit.query.all()
    current_user = User.query.filter_by(id=user_id).first_or_404()
    target_post = Post.query.filter_by(id=post_id).first_or_404()
    target_comment = Comment.query.filter_by(id=comment_id).first_or_404()
    print('target_comment: ', target_comment)
    comments = Comment.query.filter_by(post_id=post_id)
    target_comment.votes = target_comment.votes + 1
    db.session.commit()
    user_posts = Post.query.filter_by(user_id=user_id)
    return render_template('post_details.html', post=target_post, subreddits=subreddits, comments=comments)

@main.route('/downvote_comment/<user_id>/<post_id>/<comment_id>')
def downvote_comment(post_id, user_id, comment_id):
    subreddits = Subreddit.query.all()
    current_user = User.query.filter_by(id=user_id).first_or_404()
    target_post = Post.query.filter_by(id=post_id).first_or_404()
    target_comment = Comment.query.filter_by(id=comment_id).first_or_404()
    comments = Comment.query.filter_by(post_id=post_id)
    target_comment.votes = target_comment.votes - 1
    db.session.commit()
    user_posts = Post.query.filter_by(user_id=user_id)
    return render_template('post_details.html', post=target_post, subreddits=subreddits, comments=comments)

@main.route('/create_post_form', methods=['GET'])
def create_post_form():
    return render_template('form.html')
