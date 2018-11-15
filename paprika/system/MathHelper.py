class MathHelper:
    def __init__(self):
        pass

    @staticmethod
    def divide(x, y):
        try:
            return float(x) / float(y)
        except ZeroDivisionError:
            return 0
