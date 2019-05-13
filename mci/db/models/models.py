"""Database Models.

This module contains all MCI database models.

"""

from mci.id_factory import MasterClientIDFactory
from mci.app.app import db


class Address(db.Model):
    """The individuals's address.

    Args:
        address (str): The physical address of the individual.

        city (str): The city where the address is located.

        state (str): The state where the address is located.

        postal_code (str): The postal code of the location.

        country (str): The two digit country code where the location exists.

    """
    id = db.Column(db.Integer, primary_key=True)
    address = db.Column(db.String(100), nullable=False)
    city = db.Column(db.String(100), nullable=False)
    state = db.Column(db.String(20), nullable=False)
    postal_code = db.Column(db.String(20), nullable=False)
    country = db.Column(db.String(2), nullable=False)

    def __init__(self, address=None, city=None, state=None, postal_code=None, country=None):
        self.address = address
        self.city = city
        self.state = state
        self.postal_code = postal_code
        self.country = country


class Source(db.Model):
    """Source by which the individual got registered with the MCI.

    Args:
        source (str): Name of the source by which the individual entered the MCI (e.g PAIRIN)

    """
    id = db.Column(db.Integer, primary_key=True)
    source = db.Column(db.String(100), nullable=False)

    def __init__(self, source=None):
        self.source = source


class Gender(db.Model):
    """The individual's gender.

    Args:
        gender (str): The individual's gender.

    """
    id = db.Column(db.Integer, primary_key=True)
    gender = db.Column(db.String(50), nullable=False)

    def __init__(self, gender=None):
        self.gender = gender


class Disposition(db.Model):
    """The individual's disposition types.

    Args:
        disposition (str): The individual's disposition

    """

    id = db.Column(db.Integer, primary_key=True)
    disposition = db.Column(db.String(100), nullable=False)

    def __init__(self, disposition=None):
        self.disposition = disposition


class EthnicityRace(db.Model):
    """The individual's ethnicity/race.

    Args:
        ethnicity_race (str): The individual's ethnicity/race.

    """
    id = db.Column(db.Integer, primary_key=True)
    ethnicity_race = db.Column(db.String(50), nullable=False)

    def __init__(self, ethnicity_race=None):
        self.ethnicity_race = ethnicity_race


class EducationLevel(db.Model):
    """The individual's education level.

    Args:
        education_level (str): The individual's education level.

    """
    id = db.Column(db.Integer, primary_key=True)
    education_level = db.Column(db.String(50), nullable=False)

    def __init__(self, education_level=None):
        self.education_level = education_level


class EmploymentStatus(db.Model):
    """The individual's employment status.

    Args:
        employment_status (str): The individual's employment status.

    """
    id = db.Column(db.Integer, primary_key=True)
    employment_status = db.Column(db.String(50), nullable=False)

    def __init__(self, employment_status=None):
        self.employment_status = employment_status


class Individual(db.Model):
    """The individual being managed by the MCI.

    Note:
        "Individual" is a generic term that could be used to refer anything from
        user, client, patient, and so on.

    Args:
        vendor_id (str): Internal identifier provided by consumer of API.

        ssn (int): Individual's Social Security Number.

        registration_date (date): Date individual was registered with the MCI.

        first_name (str): Individual's first name.

        middle_name (str): Individual's middle name.

        last_name (str): Individual's last name.

        date_of_birth (date): Individual's date of birth.

        email_address (str): Individual's email address.

        telephone (str): Individual's telephone number.

    """
    mci_id = db.Column(db.String(40), primary_key=True)
    vendor_id = db.Column(db.String(40))
    ssn = db.Column(db.String(20))
    registration_date = db.Column(
        db.DateTime, server_default=db.func.now(), nullable=False)
    first_name = db.Column(db.String(100), nullable=False)
    suffix = db.Column(db.String(10))
    middle_name = db.Column(db.String(100))
    last_name = db.Column(db.String(100))
    date_of_birth = db.Column(db.Date, nullable=False)
    email_address = db.Column(db.String(100))
    telephone = db.Column(db.String(20))
    mailing_address_id = db.Column(
        db.Integer, db.ForeignKey(Address.id, ondelete='CASCADE'))
    gender_id = db.Column(db.Integer, db.ForeignKey(
        Gender.id, ondelete='CASCADE'))
    ethnicity_races = db.relationship(
        'EthnicityRace', secondary='individual_ethnicity_race')
    education_level_id = db.Column(db.Integer, db.ForeignKey(
        EducationLevel.id, ondelete='CASCADE'))
    employment_status_id = db.Column(db.Integer, db.ForeignKey(
        EmploymentStatus.id, ondelete='CASCADE'))
    source_id = db.Column(db.Integer, db.ForeignKey(
        Source.id, ondelete='CASCADE'))
    dispositions = db.relationship(
        'Disposition', secondary='individual_disposition')

    def __init__(self,
                 vendor_id=None,
                 ssn=None,
                 registration_date=None,
                 first_name=None,
                 suffix=None,
                 middle_name=None,
                 last_name=None,
                 date_of_birth=None,
                 email_address=None,
                 telephone=None,
                 dispositions=None):
        self.mci_id = MasterClientIDFactory.get_id()
        self.vendor_id = vendor_id
        self.ssn = ssn
        self.registration_date = registration_date
        self.first_name = first_name
        self.suffix = suffix
        self.middle_name = middle_name
        self.last_name = last_name
        self.date_of_birth = date_of_birth
        self.email_address = email_address
        self.telephone = telephone


class IndividualDisposition(db.Model):
    individual_id = db.Column(db.String(40), db.ForeignKey(
        Individual.mci_id, ondelete='CASCADE'), nullable=False, primary_key=True)
    disposition_id = db.Column(db.Integer, db.ForeignKey(
        Disposition.id, ondelete='CASCADE'), nullable=False, primary_key=True)


class IndividualEthnicityRace(db.Model):
    individual_id = db.Column(db.String(40), db.ForeignKey(
        Individual.mci_id, ondelete='CASCADE'), nullable=False, primary_key=True)
    ethnicity_race_id = db.Column(db.Integer, db.ForeignKey(
        EthnicityRace.id, ondelete='CASCADE'), nullable=False, primary_key=True)


class Referral(db.Model):
    """An individual's referral.

    This table is used to capture when an individual receives a referral to a program by some referring agency.

    Args:
        program_id (int): Identifier of the program the individual is referred to.

        mci_id (str): The individual's MCI ID.

        referring_id (int): Identifier of the individual or organization that refers the individual.

        date_referred (date): Date the individual was referred.

    """
    program_id = db.Column(db.Integer, nullable=False, primary_key=True)
    mci_id = db.Column(db.String(40), db.ForeignKey(
        Individual.mci_id, ondelete='CASCADE'), nullable=False, primary_key=True)
    referring_id = db.Column(db.Integer, nullable=False, primary_key=True)
    date_referred = db.Column(db.Date, nullable=False, primary_key=True)

    def __init__(self,
                 program_id=None,
                 mci_id=None,
                 referring_id=None,
                 date_referred=None):
        self.program_id = program_id
        self.mci_id = mci_id
        self.referring_id = referring_id
        self.date_referred = date_referred
