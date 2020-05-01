from abc import ABC

import homework.recorder as recorder
import pandas
"""Каждому полю объекта, переданному в качестве аргумента,
 выделяем колонку с записываемым значением, где и храним данные"""


class CsvRecorder(recorder.Recorder, ABC):
    def __init__(self, classname, filename):
        super().__init__(classname, filename)
        d = [p for p in dir(classname) if isinstance(getattr(classname, p), property)]
        self.df = pandas.DataFrame(columns=d)
        self.filename = filename
        self.empty = True

    def record(self, obj):
        # Добавим столбцы таблицы с именами свойств (property) объекта
        # Значениями таблицы будут значения свойств объекта
        insertion = [getattr(obj, column) for column in self.df.columns]
        df = pandas.DataFrame([insertion], columns=self.df.columns)
        if self.empty:
            self.df = df
            self.empty = False
        else:
            self.df = self.df.append(df, ignore_index=True)
        self.df.to_csv(self.filename, sep='|')
