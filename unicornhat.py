from lighty_pi import LightyPi

if __name__ == '__main__':
    pi = LightyPi()
    pi.at_midnight_get_sun_data()
    pi.unicornhat_job()
    try:
        pi.run()
    except KeyboardInterrupt:
        pass
    finally:
        pi.shutdown()