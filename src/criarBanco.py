from src import app, database
from src.models import User, Posts

with app.app_context():
    database.create_all()