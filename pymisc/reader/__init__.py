from pymisc import abstract

import csvutils
import interfaces
import csv

class XLSReader(interfaces.IReader):

    @classmethod
    def support_formats(cls):
        return 'xls'

class NewFieldFilter(interfaces.IDataFilter):

    def __init__(self, base, name, func):
        self.base = base
        self.name = name
        self.func = func
        self.header = self.base.get_header() + [self.name]
        self.custom_header = []

    def read(self):
        res = self.base.read()
        res.append(self.func(res))
        return res

    def get_header(self):
        return self.header

    def set_header(self, header):
        self.base.set_header(header)

class DataManager(interfaces.IDataManager):

    @classmethod
    def connect(cls, connection_dict):
        formats = IReader.support_formats()
        readers = dict([(x[1],x[0]) for x in formats])
        if 'type' not in connection_dict:
            return None # TODO: need to try find out type of connection
        if connection_dict['type'] in readers:
            return readers[connection_dict['type']].create(connection_dict)
        return None


