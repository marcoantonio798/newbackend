from app import app, db  # Substitua 'your_flask_app' pelo nome do seu arquivo Flask  
with app.app_context():  
    db.create_all()