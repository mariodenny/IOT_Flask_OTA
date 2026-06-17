# Lesson 6: Adding Login / Auth

We don't want just anyone uploading firmware to our server! We need to protect the upload page with a login screen.

## Flask-Login
We use a library called `Flask-Login`. It helps us manage user sessions.

1. When the teacher logs in with a username and password, Flask remembers who they are using a "cookie".
2. We add a `@login_required` decorator to the upload route.

```python
from flask_login import login_required

@bp.route('/upload', methods=['GET', 'POST'])
@login_required
def upload():
    # Only logged-in users can run this code!
    ...
```

## How to check passwords?
In our simple app, we use raw SQL to check the password against the database.

```python
cursor.execute(
    "SELECT * FROM users WHERE username = %s AND password = %s", 
    (username, password)
)
user_data = cursor.fetchone()

if user_data:
    # Password is correct, log them in!
    login_user(user)
```

*Security Warning: In a real app on the internet, you should NEVER store passwords as plain text. You should "hash" them. But for this local learning project, plain text makes it easier to understand.*
