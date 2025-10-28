from flask_mail import Message
from flask import current_app
from app.utils import mail

class Email_Service:
    def send_bulk_with_attachments(users,files):
        with mail.connect() as conn:
            for user in users:
                msg = Message(
                    subject=f"hello, {user["name"]}",
                    body="...",
                    recipients=[user["email"]],
                )
                # with current_app.open_resource("image.png") as fp:
                #    msg.attach("image.png", "image/png", fp.read())
                conn.send(msg)
