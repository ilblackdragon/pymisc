from pymisc import abstract

import interfaces
import csvutils

class CSVReader(intefaces.IReader):

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


