import logging
from pkg_resources import iter_entry_points

log = logging.getLogger(__name__)
EXTENSIONS = {}


def get_extensions(section):
    if section not in EXTENSIONS:
        EXTENSIONS[section] = {}
    if not EXTENSIONS[section]:
        for ep in iter_entry_points(section):
            EXTENSIONS[section][ep.name] = ep.load()
    return EXTENSIONS[section]


def get_init():
    return get_extensions('aleph.init')


def get_crawlers():
    crawlers = get_extensions('aleph.crawlers')
    for name, clazz in crawlers.items():
        clazz.CRAWLER_NAME = name
    return crawlers


def get_ingestors():
    return get_extensions('aleph.ingestors')


def get_analyzers():
    return get_extensions('aleph.analyzers').values()
