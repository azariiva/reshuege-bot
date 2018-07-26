class BasicUser:
    def __init__(self):
        self.__step__ = 0
        self.__subject__ = None

    def set_step(self, step):
        self.__step__ = step

    def get_step(self):
        return self.__step__

    def set_subject(self, subject):
        self.__subject__ = subject

    def get_subject(self):
        return self.__subject__
