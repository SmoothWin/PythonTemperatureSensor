

class Status:

    def __init__(self, status, time):
        self.status = status
        self.time = time

    def to_dictionary(self):
        return {
            "onlinestatus": self.status,
            "time": self.time
        }
