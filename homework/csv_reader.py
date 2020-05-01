from abc import ABC

import homework.reader as reader
import pandas
import pathlib


class CsvReader(reader.Reader, ABC):
    def __init__(self, classname, source):
        super().__init__(classname, source)
        self.classname = classname
        self.source = source
        self.path = pathlib.Path(source)
        self._parse_file()
        self.last_modified = self._last_modification_time()

    def _parse_file(self):
        self.last_modified = self._last_modification_time()
        if self.path.read_bytes() == 0:
            self._patients = list()
            return
        try:
            self.df = pandas.read_csv(self.source, sep='|', dtype=str)
        except pandas.errors.EmptyDataError:
            self._patients = list()
            return

        columns = self.df.columns
        axes = [self.df[i].values.tolist() for i in columns]
        values = dict(zip(columns, axes))
        self._patients = list()
        for i in self.df.index:
            first_name = str(values['first_name'][i])
            last_name = str(values['last_name'][i])
            birth_date = str(values['birth_date'][i])
            phone = str(values['phone'][i])
            document_id = str(values['document_id'][i])
            document_type = str(values['document_type'][i])
            new_patient = self.classname(first_name, last_name, birth_date,
                                         phone, document_type, document_id)
            self._patients.append(new_patient)

    def _last_modification_time(self):
        return self.path.stat().st_mtime
