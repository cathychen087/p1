from app import app, db, User, Project, Skill
from datetime import datetime

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