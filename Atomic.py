import threading
import json
class AtomicNumber(object):
    """An atomic, thread-safe number"""
    def __init__(self, initial=0):
        """Initialize a new atomic counter to given initial value"""
        self._value = initial
        self._lock = threading.Lock()

    def set(self, num):
        """Atomically sets the counter by num and return the new value"""
        with self._lock:
            self._value = num
            return self._value

    def get(self):
        """Atomically gets the counter by num and return the new value"""
        with self._lock:
            return self._value
        
class AtomicDictionary(object):
    def __init__(self, d = {}):
        self._value = d
        self._lock = threading.Lock()
    
    def set(self, key, value):
        #Lock befor doing this
        self._value[key] = value
    
    def get(self, key):
        #Lock befor doing this
        return self._value[key]
    

    

class AtomicPrinter(object):
    """An atomic, thread-safe printer"""
    def __init__(self):
        """Initialize a new atomic printer"""
        self._lock = threading.Lock()

    def printit(self, contents):
        """Atomically prints content"""
        with self._lock:
            print(contents)


