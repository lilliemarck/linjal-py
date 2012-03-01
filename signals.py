from weakref import WeakValueDictionary

class Signal:
    """A signal and slots implementation.
    
    Only methods may be used as slots. Two equivalent methods with the same
    function and object can't be added at the same time. The order in which the
    methods will be called is undefined.
    
    """

    def __init__(self):
        self._dict = WeakValueDictionary()

    def __call__(self, *args, **kwargs):
        """Call all connected methods with the given arguments."""
        for key, obj in self._dict.items():
            key[0](obj, *args, **kwargs)

    def __len__(self):
        """Return the number of connected methods."""
        return len(self._dict)

    def connect(self, method):
        """Connect a method to this slot."""
        key = (method.__func__, id(method.__self__))
        self._dict[key] = method.__self__

    def disconnect(self, method):
        """Disconnect a method from this slot."""
        key = (method.__func__, id(method.__self__))
        if key in self._dict:
            del self._dict[key]
