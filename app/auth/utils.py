
import os
import secrets
from PIL import Image
from flask import url_for, current_app
from flask_mail import Message
from app import mail
from functools import wraps
from datetime import datetime
from flask_login import current_user


def save_picture(form_picture):
    random_hex = secrets.token_hex(8)
    _, f_ext = os.path.splitext(form_picture.filename)
    picture_fn = random_hex + f_ext
    picture_path = os.path.join(current_app.root_path, 'static/profile_pics', picture_fn)

    output_size = (125, 125)
    i = Image.open(form_picture)
    i.thumbnail(output_size)
    i.save(picture_path)

    return picture_fn


def send_reset_email(conta):
    token = conta.get_reset_token()
    msg = Message('Password Reset Request',
                  sender='noreply@demo.com',
                  recipients=[conta.email])
    msg.body = f'''Para renovar a sua senha, acesse o sequinte link:
{url_for('auth.reset_token', token=token, _external=True)}

Se voce não realizou esta solicitação, então ignore este email e nenhuma mudança será feita.
'''
    mail.send(msg)

# def check_expired(func):
#     @wraps(func)
#     def decorated_function(*args, **kwargs):
#         # if datetime.utcnow() > current_user.account_expires:
#         if datetime.utcnow() > 1800: # 30 minutos
#             flash("Your account has expired. Update your billing info.")
#             return redirect(url_for('account_billing'))
#         return func(*args, **kwargs)

#     return decorated_function
