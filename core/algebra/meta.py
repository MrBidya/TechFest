class AlgebraMeta(type):
    def __new__(cls, name, bases, clsdict):
        clsobj = super().__new__(cls, name, bases, clsdict)

        methods = []
        for attr, value in clsdict.items():
            if callable(value) and not attr.startswith('_'):
                methods.append(attr)
        clsobj.methods = methods
        return clsobj
