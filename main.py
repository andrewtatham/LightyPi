from lighty_pi import LightyPi

if __name__ == '__main__':
    pi = LightyPi()
    pi.at_midnight_get_sun_data()
    # pi.ping_andrewdesktop()
    pi.piglow_clock()

    # pi.cheerlights_subscribe()
    #
    # pi.aws_iot_button_subscribe()
    #
    # pi.aws_foobar_subscribe()
    # pi.aws_foobar_publish()

    pi.larsson_scanner()
    pi.hue_colour_loop()

    try:
        pi.run()
    except KeyboardInterrupt:
        pass
    finally:
        pi.shutdown()