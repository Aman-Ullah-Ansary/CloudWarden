import smtplib
from email.mime.text import MIMEText


class Alert:

    def send(self, subject, body):

        sender = "YOUR_EMAIL@gmail.com"
        password = "YOUR_APP_PASSWORD"

        receiver = "YOUR_EMAIL@gmail.com"

        msg = MIMEText(body)

        msg["Subject"] = subject
        msg["From"] = sender
        msg["To"] = receiver

        server = smtplib.SMTP("smtp.gmail.com",587)

        server.starttls()

        server.login(sender,password)

        server.sendmail(sender,receiver,msg.as_string())

        server.quit()

        print("Email Alert Sent")