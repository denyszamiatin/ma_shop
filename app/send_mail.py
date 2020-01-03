"""email sending module"""

import smtplib
from email.message import EmailMessage

from app import app


def send_mail(sender, receiver, subject, message):
    """
    :param sender: from whom the email "admin@ma_shop.org"
    :param receiver: for whom the email "client@gmail.com"
    :param subject: email topic
    :param message: email text
    """
    smtpObj = smtplib.SMTP(app.config['SMTP_SERVER'])
    # smtpObj.starttls()  #SSL/TLS cryptographic protocol
    # smtpObj.login('admin@ma_shop.org','password')  #autentification to SMPT server
    msg = EmailMessage()
    msg['Subject'] = subject
    msg['From'] = sender
    msg['To'] = receiver
    msg.set_content(message)
    smtpObj.send_message(msg)
    smtpObj.quit()
