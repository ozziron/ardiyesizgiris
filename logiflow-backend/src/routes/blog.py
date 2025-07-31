from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from src.models.blog_post import db, BlogPost
from src.models.user import User

blog_bp = Blueprint('blog', __name__)

@blog_bp.route('', methods=['GET'])
def get_blog_posts():
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 10, type=int)
    
    posts = BlogPost.query.filter_by(status='published').order_by(BlogPost.published_at.desc()).paginate(
        page=page, per_page=per_page, error_out=False
    )
    
    return jsonify({
        'success': True,
        'data': [post.to_summary_dict() for post in posts.items],
        'pagination': {
            'page': page,
            'per_page': per_page,
            'total': posts.total,
            'pages': posts.pages
        }
    })

@blog_bp.route('/<slug>', methods=['GET'])
def get_blog_post(slug):
    post = BlogPost.query.filter_by(slug=slug, status='published').first_or_404()
    post.increment_view_count()
    
    return jsonify({
        'success': True,
        'data': post.to_dict()
    })

@blog_bp.route('/featured', methods=['GET'])
def get_featured_posts():
    posts = BlogPost.query.filter_by(status='published', is_featured=True).order_by(BlogPost.published_at.desc()).limit(3).all()
    
    return jsonify({
        'success': True,
        'data': [post.to_summary_dict() for post in posts]
    })
