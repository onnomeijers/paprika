import smtplib
from email.mime.text import MIMEText


class Smtp:
    def __init__(self):
        pass

    @staticmethod
    def send(host, recipients, subject, text):

        me = "apple@peer.com"  # needs to be implemented by user

        # Create a text/plain message
        msg = MIMEText(text)
        msg['Subject'] = subject
        msg['From'] = me
        msg['To'] = recipients

        s = smtplib.SMTP(host)
        s.sendmail(me, recipients, msg.as_string())
        s.quit()
