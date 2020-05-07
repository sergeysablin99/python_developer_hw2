from homework.logger import error_logger, info_logger

from sqlalchemy import Column, Integer, String, create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

import click

engine = create_engine('sqlite:///:memory:', echo=False)
Session = sessionmaker(bind=engine)

session = Session()

Base = declarative_base()


def logging_decorator(func):
    def wrapper(self, *args):
        if func.__name__ == '__init__':
            first_name, last_name, birth_date, \
            phone, document_type, document_id = args
            try:
                result = func(self, first_name, last_name, birth_date,
                              phone, document_type, document_id)
                info_logger.info("Created new Patient {} {}".format(str(first_name), str(last_name)))
            except ValueError:
                error_logger.error('Bad value for Patient')
                raise ValueError
            except TypeError:
                error_logger.error('Bad type for Patient')
                raise TypeError
            return result
        elif func.__name__ == 'save':
            func(self)
            info_logger.info(
                "Patient {} {} has been successfully saved".format(self._first_name, self._last_name))

    return wrapper


class Patient(Base):
    __tablename__ = 'patients'
    id = Column(Integer, primary_key=True)
    first_name = Column(String)
    last_name = Column(String)
    birth_date = Column(String)
    phone = Column(String)
    document_type = Column(String)
    document_id = Column(String)

    @logging_decorator
    def __init__(self, first_name, last_name, birth_date,
                 phone, document_type, document_id):
        for string in (first_name, last_name, birth_date, phone, document_id, document_type):
            if not isinstance(string, str):
                raise TypeError
        for word in (first_name, last_name):
            if not word.isalpha():
                raise ValueError

        if not self.__check_birth_date(str(birth_date)) or \
                not self.__check_phone(str(phone)) or \
                not self.__check_doc_type(str(document_type)) or \
                not self.__check_doc_id(str(document_id)):
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

    @logging_decorator
    def save(self):
        info_logger.info("Patient {} {} has been successfully saved".format(self._first_name, self._last_name))
        session.add(self)

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

    def __repr__(self):
        return "<Patient('%s','%s', '%s', '%s','%s', '%s')>" \
               % (self.first_name, self.last_name, self.birth_date,
                  self.phone, self.document_type, self.document_id)


Base.metadata.create_all(engine)


class PatientCollection(object):
    def limit(self, n):
        for patient in session.query(Patient)[:n]:
            yield patient

    def __iter__(self):
        for patient in session.query(Patient).all():
            yield patient
        raise StopIteration

    @staticmethod
    def size():
        return session.query(Patient).count()


@click.group()
def cli():
    pass


@click.command()
@click.argument('first_name')
@click.argument('last_name')
@click.option('--birth_date', default='1900-1-1')
@click.option('--phone', default='9161111111')
@click.option('--document_type', default='паспорт')
@click.option('--document_number', default='1111 111111')
def create(first_name, last_name, birth_date,
           phone, document_type, document_number):
    p = Patient(first_name, last_name, birth_date,
                phone, document_type, document_number)
    p.save()


@click.command()
@click.argument('COUNT', default='10')
def show(c):
    p = PatientCollection()
    for i in p.limit(c):
        click.echo(i)


@click.command()
def count():
    click.echo(PatientCollection.size())


cli.add_command(show)
cli.add_command(count)
cli.add_command(create)
if __name__ == '__main__':
    p = Patient('o', 'l', '2000-11-11', '9160000000', 'паспорт', '1111111111')
    p.save()
    s = Patient('oo', 'll', '2000-12-11', '9120000000', 'паспорт', '1211111111')
    s.save()
    cli()
