

class Humidity:

    def __init__(self, humidity, time):
        self.humidity = humidity
        self.time = time

    def to_dictionary(self):
        return {
            "humidity": self.humidity,
            "time": self.time
        }
