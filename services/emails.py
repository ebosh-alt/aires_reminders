import smtplib
from email.message import EmailMessage

from data.config import Config


class MailService:
    def __init__(self, sender, password):
        self.sender = sender
        self.password = password

    def send(self, theme, message):
        config = Config()
        msg = EmailMessage()
        msg.set_content(message)
        msg['Subject'] = theme
        msg['From'] = self.sender
        msg['To'] = config.emails

        with smtplib.SMTP('smtp.gmail.com', 587) as server:
            server.starttls()  # Защищенное соединение
            server.login(self.sender, self.password)
            server.send_message(msg)


if __name__ == '__main__':
    mail = MailService("isakovn2005@gmail.com", "ppca spzv qseg jhen")
    mail.send("Обновление", "Сделки")
