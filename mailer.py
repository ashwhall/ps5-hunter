import smtplib, ssl
from getpass import getpass
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText


SENDER_EMAIL = EMAIL_PWD = RECEIVER_EMAIL = None


def set_login_credentials():
    global SENDER_EMAIL, EMAIL_PWD, RECEIVER_EMAIL
    print('Enter Email credentials:')
    SENDER_EMAIL = input('Sender email: ')
    RECEIVER_EMAIL = input('Receiver email: ')
    EMAIL_PWD = getpass()


def _send(message_body, receiver_email):
    global SENDER_EMAIL, EMAIL_PWD
    assert SENDER_EMAIL is not None and EMAIL_PWD is not None, 'mailer.set_login_credentials must be called prior to mailer.send'

    port = 465  # For SSL
    smtp_server = 'smtp.gmail.com'
    sender_email = SENDER_EMAIL

    message = MIMEMultipart()
    message['From'] = sender_email
    message['To'] = receiver_email
    message['Subject'] = 'PS5 Stock Found!'
    message.attach(MIMEText(f'{message_body}\nxoxo', 'plain'))

    context = ssl.create_default_context()
    with smtplib.SMTP_SSL(smtp_server, port, context=context) as server:
        server.login(sender_email, EMAIL_PWD)
        server.sendmail(sender_email, receiver_email, message.as_string())


def send(message_body):
    _send(message_body, RECEIVER_EMAIL)
    _send(message_body, SENDER_EMAIL)


if __name__ == '__main__':
    set_login_credentials()
    send('abc')
