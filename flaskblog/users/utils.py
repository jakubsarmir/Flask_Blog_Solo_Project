import secrets
import os
from PIL import Image
from flask import url_for, current_app
from flaskblog import mail
from flask_mail import Message



def save_picture(pic):
    rand_hex = secrets.token_hex(8)
    _, ext = os.path.splitext(pic.filename)
    pic_fn = rand_hex + ext
    pic_path = os.path.join(current_app.root_path, 'static/profile_pics', pic_fn)

    output_size = (125, 125)
    i = Image.open(pic)
    i.thumbnail(output_size)

    i.save(pic_path)

    return pic_fn


def send_reset_email(user):
    token = user.get_reset_token()
    msg = Message('Password message request', sender='noreply@demo.com', recipients=[user.email])
    msg.body = f''' To reset your password, visit the following link:
    {url_for('reset_token', token=token, _external=True)}

    If you did  not make this request, simply ignore this email and no changes will be made.
    '''
    mail.send(msg)