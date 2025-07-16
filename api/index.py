from flask import Flask, render_template, send_from_directory, abort
import os
import markdown
from admin import admin_bp

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Needed for flash messages
app.register_blueprint(admin_bp)

POSTS_DIR = os.path.join(os.path.dirname(__file__), '../posts')

@app.route('/')
def home():
    posts = [f for f in os.listdir(POSTS_DIR) if f.endswith('.mdx')]
    return render_template('blog_home.html', posts=posts)

@app.route('/post/<post>')
def view_post(post):
    post_path = os.path.join(POSTS_DIR, post)
    if not os.path.exists(post_path):
        abort(404)
    with open(post_path) as f:
        content = f.read()
    html = markdown.markdown(content)
    return render_template('view_post.html', post=post, content=html)

@app.route('/about')
def about():
    return 'About'