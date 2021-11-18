

class Temperature:

    def __init__(self, temperature, time):
        self.temperature = temperature
        self.time = time

    def to_dictionary(self):
        return {
            "temperature": self.temperature,
            "time": self.time
        }
