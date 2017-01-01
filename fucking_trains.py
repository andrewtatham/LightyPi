import json
import pprint
import requests

prod = "http://fuckingtrains.azurewebsites.net/api/FuckingTrains/IsMyFuckingTrainOnTime"
local = "http://localhost:53322/api/FuckingTrains/IsMyFuckingTrainOnTime"

url = prod
# url = local


class TrainResult(object):
    def __init__(self, response):
        self._response = json.loads(response.text)
        self.FuckingTrainStateDescription = self._response["FuckingTrainStateDescription"]

    def __str__(self):
        return pprint.pformat(self._response)


def is_my_fucking_train_on_time():
    response = requests.get(url)
    print(TrainResult(response))
    return response


if __name__ == '__main__':
    is_my_fucking_train_on_time()
