from flask import Blueprint, render_template, request, redirect, url_for, flash
import os

admin_bp = Blueprint('admin', __name__, template_folder='templates')

POSTS_DIR = os.path.join(os.path.dirname(__file__), '../posts')

@admin_bp.route('/admin')
def admin_home():
    posts = [f for f in os.listdir(POSTS_DIR) if f.endswith('.mdx')]
    return render_template('admin_home.html', posts=posts)

@admin_bp.route('/admin/new', methods=['GET', 'POST'])
def new_post():
    if request.method == 'POST':
        title = request.form['title']
        content = request.form['content']
        filename = f"{title.replace(' ', '_').lower()}.mdx"
        with open(os.path.join(POSTS_DIR, filename), 'w') as f:
            f.write(content)
        flash('Post created!')
        return redirect(url_for('admin.admin_home'))
    return render_template('new_post.html')

@admin_bp.route('/admin/edit/<post>', methods=['GET', 'POST'])
def edit_post(post):
    post_path = os.path.join(POSTS_DIR, post)
    if request.method == 'POST':
        content = request.form['content']
        with open(post_path, 'w') as f:
            f.write(content)
        flash('Post updated!')
        return redirect(url_for('admin.admin_home'))
    with open(post_path) as f:
        content = f.read()
    return render_template('edit_post.html', post=post, content=content)

@admin_bp.route('/admin/delete/<post>', methods=['POST'])
def delete_post(post):
    post_path = os.path.join(POSTS_DIR, post)
    os.remove(post_path)
    flash('Post deleted!')
    return redirect(url_for('admin.admin_home'))
