from pymisc.reader import IReader, CSVReader, DataManager, NewFieldFilter

def test_csv():
    test = CSVReader.create({'path': 'data/iris.csv'})
    print(test.get_header())
    test.set_header(['SPECIES','SEPALWID'])
    while 1:
        res = test.read()
        if not res:
            break
        print(res)

def test_datamanager():
    print(IReader.support_formats())
    obj = DataManager.connect({'path': 'data/iris.csv', 'type': 'csv'})
    obj = NewFieldFilter(obj, 'test', lambda line: float(line[0]) + float(line[1]))
    print(obj.get_header())
    print(obj.read())

if __name__ == "__main__":
    test_csv()
    test_datamanager()

