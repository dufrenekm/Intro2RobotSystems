from readerwriterlock import rwlock

class Bus():
    """ Bus class for week 4"""
    def __init__(self):
        self.lock = rwlock.RWLockWriteD()
        self.msg = None

    def write(self, message):
        with self.lock.gen_wlock():
            self.msg = message

    def read(self):
        with self.lock.gen_rlock():
            return self.msg