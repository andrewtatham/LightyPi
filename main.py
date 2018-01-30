from lighty_pi import LightyPi

if __name__ == '__main__':
    pi = LightyPi()
    pi.at_midnight_get_sun_data()
    pi.piglow_clock()

    # pi.cheerlights_subscribe()
    #
    # pi.aws_iot_button_subscribe()
    #
    # pi.aws_foobar_subscribe()
    # pi.aws_foobar_publish()

    pi.larsson_scanner()

    try:
        pi.run()
    except KeyboardInterrupt:
        pass
    finally:
        pi.shutdown()