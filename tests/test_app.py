import pytest
from app import app, db

@pytest.fixture
def client():
    app.config['TESTING'] = True
    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://localhost:5432/test_portfolio'
    
    with app.test_client() as client:
        with app.app_context():
            db.create_all()
        yield client
        with app.app_context():
            db.drop_all()

def test_home_page(client):
    rv = client.get('/')
    assert rv.status_code == 200

def test_add_project(client):
    rv = client.post('/projects/add', data={
        'title': 'Test Project',
        'description': 'Test Description',
        'image_url': 'http://example.com/image.jpg',
        'github_url': 'http://github.com/test'
    }, follow_redirects=True)
    assert rv.status_code == 200 