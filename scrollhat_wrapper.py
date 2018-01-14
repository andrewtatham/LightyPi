import datetime
import scrollphathd
import time
from scrollphathd.fonts import font5x7smoothed

scrollphathd.rotate(degrees=180)
scrollphathd.clear()
scrollphathd.show()


class ScrollHatWrapper(object):
    def __init__(self):
        self.scroll_until_x = 0
        self.q = [
            datetime.datetime.now().strftime("%x"),  # Date
            datetime.datetime.now().strftime("%X"),  # Time
            "Hello World"
        ]

        self.status_length = 0

    def enqueue(self, text):
        print("_enqueue text = {}".format(text))
        self.q.insert(0, text)

    def _dequeue(self):
        scrollphathd.clear()
        print("len(q) = {}".format(len(self.q)))
        status = self.q.pop()
        self.status_length = scrollphathd.write_string(status, x=18, y=0, font=font5x7smoothed, brightness=1.0) + 17
        scrollphathd.show()
        time.sleep(0.01)

    def _scroll(self):
        scrollphathd.scroll(1)
        self.status_length -= 1
        scrollphathd.show()
        time.sleep(0.01)

    def _scroll_finished(self):
        return self.status_length <= self.scroll_until_x

    def scroll(self):
        while True:
            if not self._scroll_finished():
                self._scroll()
            elif self._scroll_finished() and any(self.q):
                self._dequeue()
            else:
                scrollphathd.clear()
                self.enqueue(datetime.datetime.now().strftime("%X"))  # Time
                scrollphathd.show()
                time.sleep(0.25)

    def show(self, text):
        self.enqueue(text)

    def close(self):
        scrollphathd.clear()
        scrollphathd.show()
