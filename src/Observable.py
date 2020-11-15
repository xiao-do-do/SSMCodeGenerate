import abc
import os


class Observable(object):
    listObserve = []

    def add(self, obj):
        self.listObserve.append(obj)
        pass

    def delete(self, obj):
        self.listObserve.remove(obj)
        pass

    def go(self, data):
        for i in self.listObserve:
            i.update(data)


class Observer(metaclass=abc.ABCMeta):

    @abc.abstractmethod
    def update(self):
        print("write")
        pass

    def write(self, data, fileName, fileDirectory):
        print(fileDirectory)
        print(fileName)
        if not os.path.exists(fileDirectory):
            os.makedirs(fileDirectory)

        with open(fileDirectory + "\\" + fileName, 'w') as file_object:
            file_object.write(data)

    def appdendsGetterAndSetter(self):
        pass
