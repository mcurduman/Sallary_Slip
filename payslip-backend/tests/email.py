from app.utils.email import mail
from flask_mail import Message

users = {
    {"name":"Miruna", "email":"curduman.miruna@gmail.com"},
    {"name":"Miruna", "email":"curduman.miruna02@gmail.com"}
}
with mail.connect() as conn:
    for user in users:
        msg = Message(
            subject=f"hello, {user.name}",
            body="...",
            recipients=[user.email],
        )
        conn.send(msg)