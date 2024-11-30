from flask import Flask, render_template, request, redirect, url_for, flash, session, jsonify
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime
import os
from functools import wraps
from flask_migrate import Migrate

app = Flask(__name__)
app.secret_key = os.getenv('SECRET_KEY', 'not-set')

# Database configuration
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialize SQLAlchemy with app
db = SQLAlchemy()
db.init_app(app)

migrate = Migrate(app, db)

# Models
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(200), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    projects = db.relationship('Project', backref='author', lazy=True)
    comments = db.relationship('Comment', backref='author', lazy=True)
    is_admin = db.Column(db.Boolean, default=False)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

class Project(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=False)
    image_url = db.Column(db.String(200))
    github_url = db.Column(db.String(200))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    comments = db.relationship('Comment', backref='project', lazy=True)
    likes = db.relationship('Like', backref='project', lazy=True)

class Comment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    project_id = db.Column(db.Integer, db.ForeignKey('project.id'), nullable=False)

class Like(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    project_id = db.Column(db.Integer, db.ForeignKey('project.id'), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

class Skill(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    category = db.Column(db.String(50))
    proficiency = db.Column(db.Integer)  # 1-5

class Contact(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), nullable=False)
    message = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

# Login required decorator
def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            flash('Please login first.')
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function

# Routes
@app.route('/')
def home():
    return render_template('home.html')

@app.route('/projects')
def projects():
    projects = Project.query.order_by(Project.created_at.desc()).all()
    return render_template('projects.html', projects=projects, is_admin=is_admin)

@app.route('/projects/add', methods=['GET', 'POST'])
@login_required
def add_project():
    if request.method == 'POST':
        project = Project(
            title=request.form['title'],
            description=request.form['description'],
            image_url=request.form['image_url'],
            github_url=request.form['github_url'],
            user_id=session['user_id']
        )
        db.session.add(project)
        db.session.commit()
        flash('Project added successfully!')
        return redirect(url_for('projects'))
    return render_template('add_project.html')

#### original from init_test
def init_test_data():
    # Create test user
    test_user = User(
        username='testuser',
        email='test@example.com'
    )
    test_user.set_password('123')
    db.session.add(test_user)
    db.session.commit()

    # Create admin user
    admin_user = User(
        username='admin',
        email='admin@example.com',
        is_admin=True
    )
    admin_user.set_password('123')
    db.session.add(admin_user)
    db.session.commit()

    # Add projects
    projects = [
        Project(
            title='Portfolio Website',
            description='A personal portfolio website built with Flask and PostgreSQL. Features include project showcase, skills display, and contact form.',
            image_url='https://raw.githubusercontent.com/github/explore/80688e429a7d4ef2fca1e82350fe8e3517d3494d/topics/flask/flask.png',
            github_url='https://github.com/username/portfolio',
            user_id=test_user.id
        ),
        Project(
            title='E-commerce Platform',
            description='Full-stack e-commerce platform built with Python and React. Includes user authentication, product management, and payment integration.',
            image_url='https://raw.githubusercontent.com/github/explore/80688e429a7d4ef2fca1e82350fe8e3517d3494d/topics/react/react.png',
            github_url='https://github.com/username/ecommerce',
            user_id=test_user.id
        ),
        Project(
            title='Task Management System',
            description='A collaborative task management system with real-time updates using WebSocket. Built with Flask and Vue.js.',
            image_url='https://raw.githubusercontent.com/github/explore/80688e429a7d4ef2fca1e82350fe8e3517d3494d/topics/vue/vue.png',
            github_url='https://github.com/username/taskmanager',
            user_id=test_user.id
        ),
        Project(
            title='Weather Dashboard',
            description='Real-time weather dashboard using OpenWeatherMap API. Features include location search, 5-day forecast, and weather alerts.',
            image_url='https://openweathermap.org/themes/openweathermap/assets/img/logo_white_cropped.png',
            github_url='https://github.com/username/weather-dashboard',
            user_id=test_user.id
        )
    ]
    
    # Add skills by category
    programming_skills = [
        Skill(name='Python', category='Programming Languages', proficiency=5),
        Skill(name='JavaScript', category='Programming Languages', proficiency=4),
        Skill(name='Java', category='Programming Languages', proficiency=4),
        Skill(name='SQL', category='Programming Languages', proficiency=4)
    ]
    
    framework_skills = [
        Skill(name='Flask', category='Frameworks', proficiency=5),
        Skill(name='Django', category='Frameworks', proficiency=4),
        Skill(name='React', category='Frameworks', proficiency=4),
        Skill(name='Vue.js', category='Frameworks', proficiency=3)
    ]
    
    database_skills = [
        Skill(name='PostgreSQL', category='Databases', proficiency=4),
        Skill(name='MongoDB', category='Databases', proficiency=3),
        Skill(name='Redis', category='Databases', proficiency=3)
    ]
    
    devops_skills = [
        Skill(name='Docker', category='DevOps', proficiency=4),
        Skill(name='Git', category='DevOps', proficiency=5),
        Skill(name='CI/CD', category='DevOps', proficiency=3),
        Skill(name='AWS', category='DevOps', proficiency=3)
    ]

    # Add all projects
    for project in projects:
        db.session.add(project)
    
    # Add all skills
    for skills in [programming_skills, framework_skills, database_skills, devops_skills]:
        for skill in skills:
            db.session.add(skill)
    
    # Commit all changes
    db.session.commit()
    print("Test data initialized successfully!")

if __name__ == '__main__':
    with app.app_context():
        # Clear existing data
        db.session.query(Project).delete()
        db.session.query(Skill).delete()
        db.session.query(User).delete()
        db.session.commit()
        
        # Initialize new data
        init_test_data() 
#### original from init_test

@app.route('/skills')
def skills():
    skills = Skill.query.all()
    return render_template('skills.html', skills=skills)

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/contact', methods=['GET', 'POST'])
def contact():
    if request.method == 'POST':
        contact = Contact(
            name=request.form['name'],
            email=request.form['email'],
            message=request.form['message']
        )
        db.session.add(contact)
        db.session.commit()
        flash('Message sent successfully!')
        return redirect(url_for('contact'))
    return render_template('contact.html')

@app.route('/projects/<int:project_id>/comment', methods=['POST'])
@login_required
def add_comment(project_id):
    content = request.form['content']
    comment = Comment(
        content=content,
        user_id=session['user_id'],
        project_id=project_id
    )
    db.session.add(comment)
    db.session.commit()
    flash('Comment added successfully!')
    return redirect(url_for('projects'))

@app.route('/projects/<int:project_id>/like', methods=['POST'])
@login_required
def like_project(project_id):
    existing_like = Like.query.filter_by(
        user_id=session['user_id'],
        project_id=project_id
    ).first()
    
    if existing_like:
        db.session.delete(existing_like)
        db.session.commit()
        return jsonify({'status': 'unliked'})
    
    like = Like(user_id=session['user_id'], project_id=project_id)
    db.session.add(like)
    db.session.commit()
    return jsonify({'status': 'liked'})

@app.cli.command('init-db')
def init_db():
    """Initialize the database."""
    with app.app_context():
        db.drop_all()
        db.create_all()
        print('Database initialized!')

# Routes for authentication
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']
        
        if User.query.filter_by(username=username).first():
            flash('Username already exists')
            return redirect(url_for('register'))
            
        if User.query.filter_by(email=email).first():
            flash('Email already registered')
            return redirect(url_for('register'))
            
        user = User(username=username, email=email)
        user.set_password(password)
        db.session.add(user)
        db.session.commit()
        
        flash('Registration successful!')
        return redirect(url_for('login'))
        
    return render_template('auth/register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = User.query.filter_by(username=username).first()
        
        if user and user.check_password(password):
            session['user_id'] = user.id
            flash('Logged in successfully!')
            return redirect(url_for('home'))
            
        flash('Invalid username or password')
        
    return render_template('auth/login.html')

@app.route('/logout')
def logout():
    session.pop('user_id', None)
    flash('Logged out successfully!')
    return redirect(url_for('home'))

# check if admin
def is_admin():
    if 'user_id' not in session:
        return False
    user = User.query.get(session['user_id'])
    return user and user.is_admin

# modify comment
@app.route('/comment/<int:comment_id>/edit', methods=['GET', 'POST'])
@login_required
def edit_comment(comment_id):
    comment = Comment.query.get_or_404(comment_id)
    if comment.user_id != session['user_id'] and not is_admin():
        flash('You do not have permission to edit this comment.')
        return redirect(url_for('projects'))
    
    if request.method == 'POST':
        comment.content = request.form['content']
        db.session.commit()
        flash('Comment updated successfully!')
        return redirect(url_for('projects'))
    
    return render_template('edit_comment.html', comment=comment)

# delete comment
@app.route('/comment/<int:comment_id>/delete', methods=['POST'])
@login_required
def delete_comment(comment_id):
    comment = Comment.query.get_or_404(comment_id)
    if comment.user_id != session['user_id'] and not is_admin():
        flash('You do not have permission to delete this comment.')
        return redirect(url_for('projects'))
    
    db.session.delete(comment)
    db.session.commit()
    flash('Comment deleted successfully!')
    return redirect(url_for('projects'))

# admin management
@app.route('/admin/comments')
@login_required
def admin_comments():
    if not is_admin():
        flash('Access denied.')
        return redirect(url_for('home'))
    
    comments = Comment.query.order_by(Comment.created_at.desc()).all()
    return render_template('admin/comments.html', comments=comments)

# add message
@app.context_processor
def utility_processor():
    return {
        'is_admin': is_admin
    }

if __name__ == '__main__':
    app.run(debug=True)
