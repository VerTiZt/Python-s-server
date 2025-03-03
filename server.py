import socket
import smtplib
import configparser
import random

config = configparser.ConfigParser()
config.read("config.ini")

smtp_host = config["EMAIL"]["SMTP_HOST"]
smtp_port = int(config["EMAIL"]["SMTP_PORT"])
from_email = config["EMAIL"]["EMAIL_LOGIN"]
password = config["EMAIL"]["EMAIL_PASSWORD"]

host = "127.0.0.1"
port = 50005


def is_valid_email(email):
    return "@" in email and "." in email


def send_email(email_to, subject, message):
    try:
        with smtplib.SMTP_SSL(smtp_host, smtp_port) as smtp:
            smtp.login(from_email, password)
            email_message = f"Subject: {subject}\n {message}"
            smtp.sendmail(from_email, email_to, email_message)
        return True
    except Exception as e:
        print(f"Ошибка при отправке письма: {e}")
        return False


def main():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:
        server_socket.bind((host, port))
        server_socket.listen()
        print("Сервер запущен и ожидает соединения...")

        while True:
            conn, addr = server_socket.accept()
            with conn:
                print(f"Соединение установлено: {addr}")
                try:
                    data = conn.recv(1024).decode()
                    email, message = data.split('|', 1)

                    if not is_valid_email(email):
                        conn.sendall("Некорректный email".encode())
                        continue

                    unique_id = random.randint(10000, 100000)
                    subject = f"[Ticket #{unique_id}] Mailer"

                    if send_email(email, subject, message):
                        conn.sendall("OK".encode())
                    else:
                        conn.sendall("Ошибка отправки письма".encode())
                except Exception as e:
                    print(f"Ошибка при обработке данных: {e}")
                    conn.sendall("Ошибка при обработке данных".encode())


if __name__ == "__main__":
    main()
