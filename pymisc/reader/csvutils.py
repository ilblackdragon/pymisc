#!/usr/bin/python
"""
    Module with CSVFile class, that helps to work with csv files as dictionary of columns
"""

import csv

class CSVFile(object):
    
    def __init__(self, filename=None, *args, **kwargs):
        self.data = {}
        self.header = []
        self.length = 0
        if filename:
            self.load(filename, *args, **kwargs)

    def load(self, filename, *args, **kwargs):
        self.data = {}
        self.length = 0
        try:
            f = open(filename)
            reader = csv.reader(f, delimiter=kwargs.get('delimiter', ','))
            self.header = reader.next()
            self.header = [name.upper() for name in self.header]
        except Exception as e:
            print(e)
            return
        for name in self.header:
            self.data[name] = []
        for line in reader:
            for i, name in enumerate(self.header):
                if i < len(line):
                    self.data[name].append(line[i])
                else:
                    self.data[name].append('')
            self.length += 1

    def get_line(self, line_number):
        return [self.data[name][line_number] for name in self.header]

    def get_line_by_id(self, id_column, value):
        try:
            idx = self.data[id_column].index(value)
            return self.get_line(idx)
        except ValueError:
            print("Index %s not found" % value)
            return []
        
    def get_dict_line(self, line_number):
        return dict([(name, self.data[name][line_number]) for name in self.header])
        
    def save(self, filename):
        f = open(filename, 'wb')
        writer = csv.writer(f)
        if self.header:
            writer.writerow(self.header)
            for i in range(self.length):
                writer.writerow(self.get_line(i))
        f.close()
    
    def add_column(self, column, val=None):
        column = column.upper()
        if column in self.header:
            return
        self.header.append(column)
        self.data[column] = []
        for i in range(self.length):
            if callable(val):
                self.data[column].append('')
                self.data[column][-1] = val(self.get_dict_line(i))
            else:
                self.data[column].append(val or '')

    def remove_column(self, column):
        column = column.upper()
        if column in self.header:
            self.header.remove(column)
            self.data.pop(column)
                
    def add_row(self, row, default=None):
        if isinstance(row, dict):
            for key in self.header:
                if key in row:
                    self.data[key].append(row[key])
                else:
                    self.data[key].append(default or '')
        else:
            if len(row) != len(self.header):
                return
            for i, key in enumerate(self.header):
                self.data[key].append(row[i])
        self.length +=1

    def __str__(self):
        res =  reduce(lambda x,y: x + str(y) + '\t', self.header, '') + '\n'
        for i in range(self.length):
            res += reduce(lambda x,y: x + str(y) + '\t', self.get_line(i), '') + '\n'
        return res
        
    def __repr__(self):
        return str(self)
        
if __name__ == "__main__":
    from random import random
    f = CSVFile()
    f.add_column('test0', lambda line: random())
    f.add_row(['tttt'])
    f.add_column('test1', lambda line: random())
    f.add_column('test2', lambda line: line['TEST1'] + 2)
    f.save('test.csv')
    f2 = CSVFile('test.csv')
    f2.add_row(['1', '2', '3'])
    f2.remove_column('test0')
    f2.save('test.csv')
