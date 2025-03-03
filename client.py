import socket

host = "127.0.0.1"
port = 50005


def get_input_data():
    email_to = input("Введите адрес электронной почты для отправки сообщения: ")
    message_text = input("Введите текст сообщения: ")
    return email_to, message_text


while True:
    email_to, message_text = get_input_data()
    data_string = f"{email_to} | {message_text}"

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((host, port))
        s.sendall(data_string.encode("utf-8"))

        data = s.recv(1024)
        if data.decode("utf-8") == "OK":
            print("Сервер прислал данные: ", data.decode("utf-8"))
            break
        else:
            print("Ошибка на сервере: ", data.decode("utf-8"))
            print("Попробуйте ввести данные снова.")
