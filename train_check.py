import json
import pprint

import requests

prod = "http://andrewtathamtraincheck.azurewebsites.net/api/traincheck/ismytreainontime"
url = prod


class TrainResult(object):
    def __init__(self, response):
        self._response = json.loads(response.text)
        self.TrainState = self._response["TrainStateDescription"]

    def __str__(self):
        return pprint.pformat(self._response)


def is_my_fucking_train_on_time():
    response = requests.get(url)
    result = TrainResult(response)
    print(result)
    return result


if __name__ == '__main__':
    is_my_fucking_train_on_time()
