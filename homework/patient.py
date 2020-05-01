from homework.logger import error_logger, info_logger
import homework.csv_recorder as csv_recorder
from homework.csv_reader import CsvReader


class Patient(object):
    def __init__(self, first_name, last_name, birth_date,
                 phone, document_type, document_id):
        for string in (first_name, last_name, birth_date, phone, document_id, document_type):
            if not isinstance(string, str):
                error_logger.error(f'{string} must be string')
                raise TypeError
        for word in (first_name, last_name):
            if not word.isalpha():
                error_logger.error(f'{word} must be an alpha')
                raise ValueError

        if not self.__check_birth_date(str(birth_date)):
            error_logger.error('Bad parameter named "birth_date" for Patient')
            raise ValueError
        if not self.__check_phone(str(phone)):
            error_logger.error('Bad parameter named "phone" for Patient')
            raise ValueError
        if not self.__check_doc_type(str(document_type)):
            error_logger.error('Bad parameter named "document_type" for Patient')
            raise ValueError
        if not self.__check_doc_id(str(document_id)):
            error_logger.error('Bad parameter named "document_id" for Patient')
            raise ValueError

        self._first_name = str(first_name)
        self._last_name = str(last_name)
        self._birth_date = str(birth_date)
        self._phone = Patient.parse_phone(phone)
        self._doc_type = str(document_type)
        self._doc_id = Patient.parse_document_id(document_id)
        info_logger.info("Created new Patient {} {}".format(str(first_name), str(last_name)))

    def __str__(self):
        return ' '.join((self._first_name, self._last_name, self._birth_date,
                         self._phone, self._doc_type, self._doc_id))

    @staticmethod
    def create(fname, lname, birth_date, phone, document_type, document_id):
        return Patient(fname, lname, birth_date, phone, document_type, document_id)

    @staticmethod
    def __check_birth_date(date):
        import time
        try:
            time.strptime(date, '%Y-%m-%d')
            res = True
        except ValueError:
            try:
                time.strptime(date, '%Y.%m.%d')
                res = True
            except ValueError:
                res = False
        return res

    @staticmethod
    def parse_phone(phone):
        return phone.replace('+', '').replace('-', '').replace('(', '').replace(')', '').replace(' ', '')

    @staticmethod
    def __check_phone(phone):
        res = Patient.parse_phone(phone)
        if len(res) == 11 and res[0] in {'7', '8'}:
            return True
        if len(res) == 10:
            return True
        return False

    @staticmethod
    def __check_doc_type(doc_type):
        if doc_type in {'водительское удостоверение', 'паспорт', 'заграничный паспорт'}:
            return True
        return False

    @staticmethod
    def parse_document_id(doc_id):
        return doc_id.replace(' ', '').replace('-', '').replace('/', '')

    @staticmethod
    def __check_doc_id(doc_id):
        res = Patient.parse_document_id(doc_id)
        if not res.isdigit():
            return False
        return True

    def save(self):
        info_logger.info("Patient {} {} has been successfully saved".format(self._first_name, self._last_name))
        Patient_recorder.record(self)

    @property
    def first_name(self):
        return self._first_name

    @first_name.setter
    def first_name(self, val):
        error_logger.error('First name assignment forbidden')
        raise AttributeError('First name assignment forbidden')

    @property
    def last_name(self):
        return self._last_name

    @last_name.setter
    def last_name(self, val):
        error_logger.error('Last name assignment forbidden')
        raise AttributeError('Last name assignment forbidden')

    @property
    def birth_date(self):
        return self._birth_date

    @birth_date.setter
    def birth_date(self, value):
        if not isinstance(value, str):
            error_logger.error(f'{value} must be string')
            raise TypeError

        if not self.__check_birth_date(str(value)):
            error_msg = 'Cannot set new value for field "birth_date": bad value {}'.format(str(value))
            error_logger.error(error_msg)
            raise ValueError('Bad parameter {}'.format(str(value)))

        success_msg = "Patient {} field named 'birth_date' changed from {} to {} ".format(
                             self._first_name + ' ' + self._last_name, self._birth_date, str(value))
        info_logger.info(success_msg)
        self._birth_date = str(str(value))

    @property
    def phone(self):
        return self._phone

    @phone.setter
    def phone(self, value):
        if not isinstance(value, str):
            error_logger.error(f'{value} must be string')
            raise TypeError

        if not self.__check_phone(str(value)):
            error_msg = 'Cannot set new value for field "phone": bad value {}'.format(str(value))
            error_logger.error(error_msg)
            raise ValueError('Bad parameter {}'.format(str(value)))

        success_msg = "Patient {} field named 'birth_date' changed from {} to {} ".format(
            self._first_name + ' ' + self._last_name, self._birth_date, str(value))
        info_logger.info(success_msg)
        self._phone = str(value)

    @property
    def document_type(self):
        return self._doc_type

    @document_type.setter
    def document_type(self, value):
        if not isinstance(value, str):
            error_logger.error(f'{value} must be string')
            raise TypeError
        if not self.__check_doc_type(str(value)):
            error_msg = 'Cannot set new value for field "doc_type": bad value {}'.format(str(value))
            error_logger.error(error_msg)
            raise ValueError('Bad parameter {}'.format(str(value)))
        success_msg = "Patient {} field named 'birth_date' changed from {} to {} ".format(
            self._first_name + ' ' + self._last_name, self._birth_date, str(value))
        info_logger.info(success_msg)
        self._doc_type = str(value)

    @property
    def document_id(self):
        return self._doc_id

    @document_id.setter
    def document_id(self, value):
        if not isinstance(value, str):
            error_logger.error(f'{value} must be string')
            raise TypeError
        if not self.__check_doc_id(str(value)):
            error_msg = 'Cannot set new value for field "doc_id": bad value {}'.format(str(value))
            error_logger.error(error_msg)
            raise ValueError('Bad parameter {}'.format(str(value)))
        success_msg = "Patient {} field named 'birth_date' changed from {} to {} ".format(
            self._first_name + ' ' + self._last_name, self._birth_date, str(value))
        info_logger.info(success_msg)
        self._doc_id = str(value)


Patient_recorder = csv_recorder.CsvRecorder(Patient, "output.csv")


class PatientCollection(object):
    def __init__(self, path_to_file):
        self.reader = CsvReader(Patient, path_to_file)

    def limit(self, n):
        counter = 0
        while counter < n:
            if self.reader._last_modification_time() > self.reader.last_modified:
                self.reader._parse_file()
            if counter < len(self.reader._patients):
                yield self.reader._patients[counter]
            else:
                break
            counter += 1

    def __iter__(self):
        counter = 0
        while True:
            if counter >= len(self.reader._patients):
                raise StopIteration
            if self.reader._last_modification_time() > self.reader.last_modified:
                self.reader._parse_file()
            if counter < len(self.reader._patients):
                yield self.reader._patients[counter]
            else:
                yield
            counter += 1

#
# p = Patient('Oleg', 'Ivanov', '2000-10-10', '79160000000', 'паспорт', '1111111111')
# p.save()
# p = Patient('Oleg1', 'Ivanov1', '2000-10-10', '79160000001', 'паспорт', '2222222222')
# p.save()
