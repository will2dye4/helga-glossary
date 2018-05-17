from __future__ import unicode_literals

import datetime
import random
import sys

import six

from helga import log
from helga.db import db


logger = log.getLogger(__name__)


class TermRecord(object):

    def __init__(self, record):
        self.record = record

    @classmethod
    def get_new_record(cls, term, definition, created_by):
        return cls({
            'term': term,
            'definition': definition,
            'created_by': created_by,
            'created_datetime': datetime.datetime.utcnow(),
        })

    @classmethod
    def get_random_term(cls):
        terms = db.glossary_term.find()
        count = terms.count()
        if count == 0:
            return None
        skip = random.randint(0, count - 1)
        return terms.limit(-1).skip(skip).next()    # Bleh, this is how we randomly grab one

    @classmethod
    def get_term(cls, term):
        record = db.glossary_term.find_one({'term': term})
        if record:
            return cls(record)
        return None

    @classmethod
    def create_if_not_exists(cls, term, definition, created_by):
        record = cls.get_term(term)
        if not record:
            record = cls.get_new_record(term, definition, created_by)
            record.save()

    def save(self):
        db.glossary_term.update(
            {'term': self['term']},
            self.record,
            upsert=True
        )

    def delete(self):
        db.glossary_term.remove({'term': self['term']})

    def get(self, key, default=None):
        try:
            return self[key]
        except KeyError:
            return default

    def __getitem__(self, key):
        return self.record[key]

    def __setitem__(self, key, value):
        self.record[key] = value

    def __iter__(self):
        return six.iteritems(self.record)

    def __str__(self):
        if sys.version_info > (3, 0):
            return self.__unicode__()
        return self.__unicode__().encode(sys.getdefaultencoding())

    def __unicode__(self):
        return six.text_type(self.record)

    def __repr__(self):
        return "<Term Record '{record}'>".format(
            record=six.text_type(self)
        )
