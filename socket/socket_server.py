import socket
from server.commands import ServerCommands
from helpers.switch import Switch

UDP_MAX_SIZE = 65535


def check_command(command: str, connection: socket, address: str):
    socket_commands = ServerCommands(connection=connection, address=address)
    shortcut = command.split("run_")[-1]
    volume = command.split("volume_")[-1]
    brightness = command.split("brightness_")[-1]
    key = command.split("key_")[-1]

    Switch(command.split("_")[0])\
        .case("shortcuts", lambda: socket_commands.list_shortcuts())\
        .case("run", lambda: socket_commands.run_shortcut(shortcut))\
        .case("system", lambda: socket_commands.system())\
        .case("volume", lambda: socket_commands.set_volume(volume))\
        .case("brightness", lambda: socket_commands.set_brightness(brightness))\
        .case("key", lambda: socket_commands.press_key(key))


def listen(host: str = "127.0.0.1", port: int = 9000):
# def listen(host: str = "192.168.0.1", port: int = 3000):
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    s.bind((host, port))
    print(f"Listening at {host}:{port}")

    while True:
        msg, addr = s.recvfrom(UDP_MAX_SIZE)

        decoded_msg = msg.decode('utf-8')
        print(f"addr {addr} message: {decoded_msg}")
        check_command(decoded_msg, s, addr)

        # a = {'key': 'value', 'key1': 'value1'}
        # data = json.dumps(a)

        # s.sendto(f"test 1".encode('ascii'), addr)
        # s.sendto(bytes(data, encoding="utf-8"), addr)
        # print("send ok")


if __name__ == '__main__':
    listen()
