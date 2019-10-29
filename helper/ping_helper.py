import ping3


def ping(host):
    delay = ping3.ping(host)
    return not delay is None


def ping_andrewdesktop():
    return ping('andrewdesktop.home')


if __name__ == '__main__':
    print(ping('picube.home'))
    print(ping('scrollbot.home'))
