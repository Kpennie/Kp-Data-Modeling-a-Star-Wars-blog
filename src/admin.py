import os


def setup_admin(app):
    """
    Set up Flask admin interface - imports moved inside function to avoid circular imports
    """
    app.secret_key = os.environ.get('FLASK_APP_KEY', 'sample key')
    app.config['FLASK_ADMIN_SWATCH'] = 'cerulean'

    # Import Flask-Admin inside the function
    from flask_admin import Admin
    from flask_admin.contrib.sqla import ModelView

    admin = Admin(app, name='4Geeks Admin', template_mode='bootstrap3')

    # Import models inside the function to avoid circular imports
    from models import db, User, Character, Planet, BlogPost

    # Add your models here
    admin.add_view(ModelView(User, db.session))
    admin.add_view(ModelView(Character, db.session))
    admin.add_view(ModelView(Planet, db.session))
    admin.add_view(ModelView(BlogPost, db.session))

    return admin
