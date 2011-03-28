from pymisc import abstract

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

class IDataFilter(IReader):
    """
    Data Filter - can change or make some calculation on data in read process
    """
    pass

class IDataManager(abstract.IBase):

    @classmethod
    def connect(cls, connection_dict):
        pass


