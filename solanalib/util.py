class SafeDict(dict):
    def __getitem__(self, key):
        try:
            value = dict.__getitem__(self, key)
            if isinstance(value, dict):
                value = type(self)(value)
        except:
            value = type(self)()
        return value
