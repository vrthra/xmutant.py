class Cov():
    def __init__(self, cov):
        self.cov = cov

    def __enter__(self):
        self.cov.start()
        return self.cov

    def __exit__(self, type, value, traceback):
        self.cov.stop()
