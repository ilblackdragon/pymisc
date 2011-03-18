from pymisc import abstract

import csvutils

class IReader(abstract.IBase):

    @classmethod
    def create(cls, conntection_dict):
        """
            Connection dictionary:
            Possible keys: path, login, password, type
        """
        pass

    @classmethod
    def support_formats(cls):
        return IReader.send_signal('support_formats')

    def read(self):
        pass

    def get_header(self):
        pass

    def set_header(self, header):
        pass

import csv
class CSVReader(IReader):

    @classmethod
    def create(cls, conntection_dict):
        return CSVReader(conntection_dict)

    @classmethod
    def support_formats(cls):
        return 'csv'

    def __init__(self, conntection_dict):
        self.reader = csv.reader(open(conntection_dict['path']))
        self.header = self.reader.next()
        self.custom_header = range(len(self.header))

    def read(self):
        try:
            line = self.reader.next()
        except StopIteration:
            return False
        res = []
        for i in self.custom_header:
            res.append(line[i])
        return res

    def get_header(self):
        return self.header

    def set_header(self, header):
        self.custom_header = []
        for h in header:
            if h in self.header:
                self.custom_header.append(self.header.index(h))

class XLSReader(IReader):

    @classmethod
    def support_formats(cls):
        return 'xls'

class IDataFilter(IReader):
    """
        Data Filter - can change or make some calculation on data in read process
    """
    pass

class NewFieldFilter(IDataFilter):

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

class IDataManager(abstract.IBase):

    @classmethod
    def connect(cls, connection_dict):
        pass

class DataManager(IDataManager):

    @classmethod
    def connect(cls, connection_dict):
        formats = IReader.support_formats()
        readers = dict([(x[1],x[0]) for x in formats])
        if 'type' not in connection_dict:
            return None # TODO: need to try find out type of connection
        if connection_dict['type'] in readers:
            return readers[connection_dict['type']].create(connection_dict)
        return None


