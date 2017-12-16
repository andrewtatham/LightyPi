from lighty_pi import LightyPi

if __name__ == '__main__':
    pi = LightyPi()
    pi.xmas()
    try:
        pi.run()
    except KeyboardInterrupt:
        pass
    finally:
        pi.shutdown()
