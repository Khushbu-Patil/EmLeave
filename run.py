from app import create_app, db  # from the app package __init__
from app.auth.models import Registration, Office, Admin


if __name__ == '__main__':
    flask_app = create_app('dev')
    with flask_app.app_context():
        db.create_all()

    flask_app.run(debug=True,host='localhost', port=4000)