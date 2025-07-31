import os
import sys
# DON'T CHANGE THIS !!!
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

from flask import Flask, send_from_directory
from flask_cors import CORS
from flask_jwt_extended import JWTManager
from src.models.user import db, User
from src.models.port import Port
from src.models.container_type import ContainerType
from src.models.shipping_line import ShippingLine
from src.models.calculation import Calculation
from src.models.container_tracking import ContainerTracking, TrackingHistory
from src.models.blog_post import BlogPost

# Route imports
from src.routes.user import user_bp
from src.routes.auth import auth_bp
from src.routes.port import port_bp
from src.routes.container_type import container_type_bp
from src.routes.shipping_line import shipping_line_bp
from src.routes.calculation import calculation_bp
from src.routes.container_tracking import tracking_bp
from src.routes.blog import blog_bp
from src.routes.admin import admin_bp

app = Flask(__name__, static_folder=os.path.join(os.path.dirname(__file__), 'static'))

# Configuration
app.config['SECRET_KEY'] = 'LogiFlow2025SecretKey!@#$%'
app.config['JWT_SECRET_KEY'] = 'LogiFlow2025JWTSecretKey!@#$%'
app.config['JWT_ACCESS_TOKEN_EXPIRES'] = False  # Token süresi sınırsız (geliştirme için)

# CORS configuration
CORS(app, origins="*", allow_headers=["Content-Type", "Authorization"])

# JWT configuration
jwt = JWTManager(app)

# Database configuration
app.config['SQLALCHEMY_DATABASE_URI'] = f"sqlite:///{os.path.join(os.path.dirname(__file__), 'database', 'app.db')}"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialize database
db.init_app(app)

# Register blueprints
app.register_blueprint(auth_bp, url_prefix='/api/auth')
app.register_blueprint(user_bp, url_prefix='/api/users')
app.register_blueprint(port_bp, url_prefix='/api/ports')
app.register_blueprint(container_type_bp, url_prefix='/api/container-types')
app.register_blueprint(shipping_line_bp, url_prefix='/api/shipping-lines')
app.register_blueprint(calculation_bp, url_prefix='/api/calculations')
app.register_blueprint(tracking_bp, url_prefix='/api/tracking')
app.register_blueprint(blog_bp, url_prefix='/api/blog')
app.register_blueprint(admin_bp, url_prefix='/api/admin')

# Create tables and default data
with app.app_context():
    db.create_all()
    
    # Create default data
    User.create_default_users()
    Port.create_default_ports()
    ContainerType.create_default_container_types()
    ShippingLine.create_default_shipping_lines()
    BlogPost.create_default_posts()

@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def serve(path):
    static_folder_path = app.static_folder
    if static_folder_path is None:
        return "Static folder not configured", 404

    if path != "" and os.path.exists(os.path.join(static_folder_path, path)):
        return send_from_directory(static_folder_path, path)
    else:
        index_path = os.path.join(static_folder_path, 'index.html')
        if os.path.exists(index_path):
            return send_from_directory(static_folder_path, 'index.html')
        else:
            return "LogiFlow Backend API is running! Frontend not found.", 200

@app.route('/api/health')
def health_check():
    return {
        'status': 'healthy',
        'message': 'LogiFlow API is running',
        'version': '1.0.0'
    }

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
