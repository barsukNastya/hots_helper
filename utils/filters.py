import random
import re
from itertools import dropwhile

from data.structures import BlizzHero


def take_talent_by_name(talents_form_api, name):
    talent_search = dropwhile(lambda talent: talent['name'] != name,
                              talents_form_api)
    try:
        talent = next(talent_search)
    except StopIteration:
        talent = None

    return talent


def take_by_name(bheroes, name):

    assert all([type(bhero) == BlizzHero
                for bhero in bheroes]), f'Not the all of heroes is BlizzHero.'

    matching = [bhero for bhero in bheroes
                if name.lower() in bhero.hero.name.lower()]

    def match_score(hero):
        ru_pos = hero.ru_name.lower().find(name.lower())
        en_pos = hero.en_name.lower().find(name.lower())

        return ru_pos if ru_pos > en_pos else en_pos

    matching.sort(key=lambda x: match_score(x.hero))

    if matching \
       and (matching[0].hero.en_name == name
            or matching[0].hero.ru_name == name
            or len(matching) == 1):

        certain_match = matching[0]

    else:
        certain_match = None

    return matching, certain_match


def by_role(blizzard_heroes, role):
    return [bhero for bhero in blizzard_heroes
            if bhero.hero.role.lower() == role]


# TODO: hardcode range
def is_cyrillic(text):
    return bool(re.search('[\u0400-\u04FF]', text))


def get_cyrillic(from_list):
    ru_name_search = dropwhile(lambda name: not is_cyrillic(name),
                               from_list)
    try:
        ru_name = next(ru_name_search)
    except StopIteration:
        ru_name = ''

    return ru_name


def get_cyrillic_str(from_str):
    ru_str_list = list(dropwhile(lambda c: not is_cyrillic(c),
                                 from_str))
    return ''.join(ru_str_list) if ru_str_list else from_str
