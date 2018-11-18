class MuScore(object):
    def __init__(self, nmutants, covering, tdetected, rnot_detected=0, skipped=0, eqv=[], timedout=[]):
        self.__dict__.update(i for i in locals().items() if i[0] != 'self')
        self.rtimedout = len(timedout)
        num = self.nmutants - self.rtimedout
        self.score = -1 if num == 0 else tdetected * 100.0 / num

    def __str__(self):
        return "Mutants: %d, Covering %d, Detected: %d, Timedout: %d, Score: %f%%" % \
               (self.nmutants, self.covering, self.tdetected, self.rtimedout, \
                self.tdetected * 100.0 / self.nmutants)

    def failed(self):
        return self.nmutants == 0


def summarize(muarr):
    nmutants = sum([i.nmutants for i in muarr])
    covering = sum([i.covering for i in muarr])
    tdetected = sum([i.tdetected for i in muarr])
    rnot_detected = sum([i.rnot_detected for i in muarr])
    skipped = sum([i.skipped for i in muarr])
    eqv = sum([i.eqv for i in muarr], [])
    timedout = sum([i.timedout for i in muarr], [])
    return MuScore(nmutants, covering, tdetected, rnot_detected, skipped, eqv, timedout)
