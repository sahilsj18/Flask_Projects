from flask import Blueprint, render_template, request, redirect, jsonify
from models import Blog

# Define a Blueprint
blog_blueprint = Blueprint('blog', __name__)

@blog_blueprint.route('/create', methods=['POST'])
def create_post():
    try:
        if request.is_json:
            data = request.get_json()
            title = data.get('title')
            content = data.get('content')
        else:
            title = request.form.get('title')
            content = request.form.get('content')

        if not title or not content:
            return jsonify({"error": "Title and Content are required"}), 400
        
        Blog.create_post(title, content)
        return jsonify({"message": "Blog post created successfully"}), 201

    except Exception as e:
        return jsonify({"error": str(e)}), 500

@blog_blueprint.route('/',methods=['GET'])
def index():
    
    try:
        posts = Blog.get_all_posts()
        return jsonify(posts), 200  # Return JSON response
    except Exception as e:
        return jsonify({"error": str(e)}), 500
@blog_blueprint.route('/post/<int:post_id>')
def get_post(post_id):
    post = Blog.get_post(post_id)
    return render_template('post.html', post=post)

@blog_blueprint.route('/update/<int:post_id>', methods=['PUT'])
def update_post(post_id):
    try:
        post = Blog.get_post(post_id)
        if not post:
            return jsonify({"error": "Post not found"}), 404  # If post does not exist
        
        # Check if the request is JSON
        if not request.is_json:
            return jsonify({"error": "Request must be JSON"}), 400

        data = request.get_json()
        title = data.get('title')
        content = data.get('content')

        if not title or not content:
            return jsonify({"error": "Title and Content are required"}), 400
        
        Blog.update_post(post_id, title, content)
        return jsonify({"message": "Blog post updated successfully"}), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500

@blog_blueprint.route('/delete/<int:post_id>', methods=['DELETE'])
def delete_post(post_id):
    try:
        post = Blog.get_post(post_id)
        if not post:
            return jsonify({"error": "Post not found"}), 404  # If post does not exist
        
        Blog.delete_post(post_id)
        return jsonify({"message": f"Blog post with ID {post_id} deleted successfully"}), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500
