from getpass import getpass
from gptblog.models import db, User, BlogPost, Visit
from gptblog.views import app

def init_database():
    db.create_all()
    print("Creating test user...")
    username = input("Enter a username for the test user: ")
    password = getpass("Enter a password for the test user: ")

    test_user = User(username=username)
    test_user.set_password((password))
    db.session.add(test_user)
    db.session.commit()

    print("Creating test post...")
    test_post = BlogPost(title='Test Post', content='This is a test post.', teaser='A teaser for the test post.', author=test_user)
    db.session.add(test_post)
    db.session.commit()

    print('Initializing view counter')
    visit = Visit(views=0)
    db.session.add(visit)
    db.session.commit()

    print("Database initialized successfully!")

if __name__ == "__main__":
    with app.app_context():
        init_database()

