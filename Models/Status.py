

class Status:

    def __init__(self, status, time):
        self.status = status
        self.time = time

    def to_dictionary(self):
        return {
            "online": self.status,
            "date_time": self.time
        }
