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
    posts = []
    for filename in os.listdir(POSTS_DIR):
        if not filename.endswith('.mdx'):
            continue
        meta = {'filename': filename, 'title': '', 'date': '', 'tags': [], 'image': '', 'excerpt': ''}
        with open(os.path.join(POSTS_DIR, filename)) as f:
            for line in f:
                if line.startswith('title:'):
                    meta['title'] = line[len('title:'):].strip()
                elif line.startswith('date:'):
                    meta['date'] = line[len('date:'):].strip()
                elif line.startswith('tags:'):
                    tags = line[len('tags:'):].strip().replace('[','').replace(']','').replace('"','').replace("'",'')
                    meta['tags'] = [t.strip() for t in tags.split(',') if t.strip()]
                elif line.startswith('image:'):
                    meta['image'] = line[len('image:'):].strip()
                elif line.startswith('excerpt:'):
                    meta['excerpt'] = line[len('excerpt:'):].strip()
                elif line.strip() == '---':
                    continue
                # Stop reading after frontmatter
                elif line.strip().startswith('#'):
                    break
        posts.append(meta)
    # Sort posts by date descending
    posts.sort(key=lambda x: x['date'], reverse=True)
    return render_template('blog_home.html', posts=posts)

@app.route('/post/<post>')
def view_post(post):
    post_path = os.path.join(POSTS_DIR, post)
    if not os.path.exists(post_path):
        abort(404)
    meta = {'title': '', 'date': '', 'tags': [], 'image': '', 'excerpt': ''}
    content_lines = []
    with open(post_path) as f:
        in_frontmatter = True
        for line in f:
            if in_frontmatter:
                if line.startswith('title:'):
                    meta['title'] = line[len('title:'):].strip()
                elif line.startswith('date:'):
                    meta['date'] = line[len('date:'):].strip()
                elif line.startswith('tags:'):
                    tags = line[len('tags:'):].strip().replace('[','').replace(']','').replace('"','').replace("'",'')
                    meta['tags'] = [t.strip() for t in tags.split(',') if t.strip()]
                elif line.startswith('image:'):
                    meta['image'] = line[len('image:'):].strip()
                elif line.startswith('excerpt:'):
                    meta['excerpt'] = line[len('excerpt:'):].strip()
                elif line.strip() == '---':
                    continue
                elif line.strip().startswith('#') or not line.strip():
                    in_frontmatter = False
                    if line.strip():
                        content_lines.append(line)
                else:
                    continue
            else:
                content_lines.append(line)
    html = markdown.markdown(''.join(content_lines))
    return render_template('view_post.html', meta=meta, content=html)

@app.route('/about')
def about():
    return 'About'