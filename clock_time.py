class CurrentTime:
    def __init__(self):
        self.hour = -1
        self.minute = -1

    def get_time(self):
        return self.hour, self.minute

    def increment(self):
        if self.minute < 59:
            self.minute += 1
        else:
            self.minute = 0
            self.hour = (self.hour+1)%12

    def set_time(self, hour: int, minute: int):
        if hour < 0 or hour >= 24 or minute < 0 or minute >= 60:
            self.hour = hour%12
            self.minute = minute



