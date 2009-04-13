from threading import Thread

class Builder(Thread):
    def run(self,Command,Arguments):
        Attr = getattr(self,Command)
        Attr()
    def make(self):
        pass
