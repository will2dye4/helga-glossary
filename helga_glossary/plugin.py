from __future__ import unicode_literals

import random

from helga import log
from helga.plugins import command, ACKS

from .data import TermRecord


ADD_COMMANDS = ['add', 'define']
DELETE_COMMANDS = ['delete', 'remove']
FIND_COMMANDS = ['find', 'lookup']
RANDOM_COMMANDS = ['random']
ALL_COMMANDS = ADD_COMMANDS + DELETE_COMMANDS + FIND_COMMANDS + RANDOM_COMMANDS
DATE_FORMAT = '%Y-%m-%d %I:%M%p'
TERM_DOES_NOT_EXIST_TEMPLATE = 'The term "{term}" is not in the glossary, {nick}'
TERM_FORMAT_TEMPLATE = '*{term}*. {definition} (added by {nick} {created})'


logger = log.getLogger(__name__)


def format_term(term_record):
    return TERM_FORMAT_TEMPLATE.format(
        term=term_record['term'],
        definition=term_record['definition'],
        nick=term_record['created_by'],
        created=term_record['created_datetime'].strftime(DATE_FORMAT)
    )


def add_term(cmd, subcmd, nick, args):
    if len(args) < 2:
        return 'Usage: helga {} {} "<term>" "<definition>"'.format(cmd, subcmd)
    if len(args) == 2:
        term, definition = args
    else:
        term = args[0]
        definition = ' '.join(args[1:])
    existing_term_record = TermRecord.get_term(term)
    if existing_term_record:
        return 'Sorry, {}, the term "{}" is already in the glossary'.format(nick, term)
    TermRecord.create_if_not_exists(term, definition, nick)
    return random.choice(ACKS)


def delete_term(cmd, subcmd, nick, args):
    if not args:
        return 'Usage: helga {} {} <term>'.format(cmd, subcmd)
    if len(args) == 1:
        term = args[0]
    else:
        term = ' '.join(args)
    term_record = TermRecord.get_term(term)
    if not term_record:
        return TERM_DOES_NOT_EXIST_TEMPLATE.format(term=term, nick=nick)
    term_record.delete()
    return random.choice(ACKS)


def find_term(cmd, subcmd, nick, args):
    if not args:
        return 'Usage: helga {} {} <term>'.format(cmd, subcmd)
    if len(args) == 1:
        term = args[0]
    else:
        term = ' '.join(args)
    term_record = TermRecord.get_term(term)
    if not term_record:
        return TERM_DOES_NOT_EXIST_TEMPLATE.format(term=term, nick=nick)
    return format_term(term_record)


def random_term(nick):
    random_term_record = TermRecord.get_random_term()
    if not random_term_record:
        return 'Sorry, {}, there are no terms in the glossary'.format(nick)
    return format_term(random_term_record)


@command('glossary', aliases=['g'], shlex=True,
         help='Define and look up terms. Usage: helga glossary [(add|define) <term> <definition>|'
              '(find|lookup) <term>|(delete|remove) <term>|random]')
def glossary(client, channel, nick, message, cmd, args):
    if args:
        if args[0].lower() in ALL_COMMANDS:
            subcmd = args[0].lower()
            args = args[1:]
        else:
            subcmd = 'find'
    else:
        subcmd = 'random'

    if subcmd in ADD_COMMANDS:
        return add_term(cmd, subcmd, nick, args)
    elif subcmd in DELETE_COMMANDS:
        return delete_term(cmd, subcmd, nick, args)
    elif subcmd in FIND_COMMANDS:
        return find_term(cmd, subcmd, nick, args)
    elif subcmd in RANDOM_COMMANDS:
        return random_term(nick)
    else:
        return "I don't know about that command, {}".format(nick)
