__author__ = 'ilblackdragon@gmail.com'

from pymisc import log, decorators

class RegisterSystem(object):

    interfaces = []
    classes = []

    @classmethod
    @decorators.logprint(log)
    def register(self, cls):
        if cls.__name__[0] == 'I':
            print("Regirstring interface `%s`" % cls.__name__)
            RegisterSystem.interfaces.append(cls)
        else:
            print("Regirstring class `%s`" % cls.__name__)
            RegisterSystem.classes.append(cls)

class InterfaceMeta(type):
    def __new__(cls, name, bases, dict):
        res = super(InterfaceMeta, cls).__new__(cls, name, bases, dict)
        RegisterSystem.register(res)
        if name[0] == 'I':
            res.children = []
        else:
            for b in bases:
                if b.children is not None:
                    b.children.append(res)
        return res

class IBase(object):
    __metaclass__ = InterfaceMeta

    @classmethod
    def send_signal(cls, method, *args, **kwargs):
        res = []
        for child in cls.children:
            res.append((child, child.__dict__[method].__get__('')(*args, **kwargs)))
        return res
