#!/usr/bin/env python

import re
import datetime
import logging
import sys
from db.connection import engine
from db.model import Site, Item, Component
from db.session import session
from sickle import Sickle

logging.basicConfig(filename='logs/harvest.log', level=logging.DEBUG)

if len(sys.argv) < 2:
    sys.exit('Usage: %s repository-name' % sys.argv[0])

repository = sys.argv[1]
site = session.query(Site).filter_by(name=repository).first()

if site is None:
    sys.exit('repository not exists.')


print "{} - {}".format(site.id, site.url)
sickle = Sickle(site.url)

if site.last:
    last = site.last.strftime("%Y-%m-%d")
    records = sickle.ListRecords(
        **{'metadataPrefix': 'oai_dc', 'ignore_deleted': True, 'from': last})
else:
    records = sickle.ListRecords(
        **{'metadataPrefix': 'oai_dc', 'ignore_deleted': True})


for record in records:
    id = record.header.identifier
    item = Item(oai_identifier=id, raw_metadata=record.raw,
                site=site.id, status="new")

    components = []
    for url in record.metadata['identifier']:
        if re.match("^(https?)://.+$", url):
            components.append(Component(url=url))

    item.components = components
    session.add(item)

now = datetime.datetime.now()
site.last = now
session.commit()
