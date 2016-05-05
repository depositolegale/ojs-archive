#!/usr/bin/env python

import datetime
import os
import sys
from db.connection import engine
from db.model import Site, Item, Component
from db.session import session

if len(sys.argv) < 2:
    sys.exit('Usage: %s repository-name' % sys.argv[0])

repository = sys.argv[1]
site = session.query(Site).filter_by(name=repository).first()

if site is None:
    sys.exit('repository not exists.')

now = datetime.datetime.now().strftime("%Y%m%d")
output = os.path.join(os.getcwd(), "data", "seeds",
                      "{}-{}.seeds").format(now, repository)

if len(site.items) != 0:
    print output

    out_file = open(output, "wb")

    for item in site.items:
        for component in item.components:
            out_file.write(component.url + "\n")
        item.status = "seeded"
        session.commit()

    out_file.close()
