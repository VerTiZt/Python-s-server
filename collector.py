import imaplib
import email
from email.header import decode_header
import time
import configparser

config = configparser.ConfigParser()
config.read("config.ini")

email_login = config["EMAIL"]["EMAIL_LOGIN"]
password = config["EMAIL"]["EMAIL_PASSWORD"]
imap_host = config["EMAIL"]["IMAP_HOST"]
imap_port = int(config["EMAIL"]["IMAP_PORT"])
period_check = int(config["EMAIL"]["PERIOD_CHECK"])


def check_mail():
    with imaplib.IMAP4_SSL(imap_host, imap_port) as mail:
        # Попытка входа
        try:
            mail.login(email_login, password)

            # Запись успешного входа в аккаунт с уведомлением от сервера
            with open("success_request.log", "a") as log:
                log.write(f"Успешный вход в аккаунт: {email_login}\n")

            # Получение уведомления от сервера (если доступно)
            server_message = mail.noop()[1]  # Здесь вы можете получить сообщение от сервера
            if server_message:
                with open("success_request.log", "a") as log:
                    log.write(f"Уведомление от сервера: {server_message}\n")

            mail.select("inbox")

            status, messages = mail.search(None, 'ALL')
            messages = messages[0].split()

            for msg_num in messages[-5:]:
                status, msg_data = mail.fetch(msg_num, "(RFC822)")
                for response_part in msg_data:
                    if isinstance(response_part, tuple):
                        msg = email.message_from_bytes(response_part[1])
                        subject, encoding = decode_header(msg["Subject"])[0]
                        if isinstance(subject, bytes):
                            subject = subject.decode(encoding or "utf-8")

                        if "[Ticket #" in subject:
                            with open("success_request.log", "a") as log:
                                log.write(f"Успешно обработано: {subject}\n")
                        else:
                            with open("error_request.log", "a") as log:
                                log.write(f"Ошибка обработки: {subject}\n")

        except Exception as e:
            with open("error_request.log", "a") as log:
                log.write(f"Ошибка при входе: {str(e)}\n")

        mail.logout()


if __name__ == "__main__":
    while True:
        check_mail()
        time.sleep(period_check)
