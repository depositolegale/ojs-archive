from sqlalchemy import Column, Integer, String, Boolean, Enum, DateTime, Text, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from connection import engine
from datetime import datetime


Base = declarative_base()


class Item(Base):
	__tablename__ = 'items'
	__table_args__ = {
        'mysql_charset': 'utf8'
    }

	id = Column(Integer, primary_key=True)
	site = Column(String(25))
	oai_identifier = Column(String(150), index=True)
	raw_metadata = Column(Text)
	status = Column(Enum("new", "seeded", "indexed", "receipted", "validated"))
	created_on = Column(DateTime, default=datetime.now)
	updated_on = Column(DateTime, default=datetime.now, onupdate=datetime.now)

	site = Column(Integer, ForeignKey('sites.id'))

	components = relationship("Component", backref="items", cascade="all, delete-orphan", passive_deletes=True)

	def __repr__(self):
		return "<Item('%s')>" % (self.oai_identifier)

class Component(Base):
	__tablename__ = 'components'
	__table_args__ = {
        'mysql_charset': 'utf8'
    }


	id = Column(Integer, primary_key=True)
	url = Column(String(200), index=True)
	warcfile = Column(String(100), index=True)
	offset = Column(Integer)
	http_code = Column(Integer, index=True)
	sha1 = Column(String(50))
	mimetype = Column(String(50), index=True)
	crawl_date = Column(DateTime)

	item = Column(Integer, ForeignKey('items.id', ondelete='CASCADE'))

	def __repr__(self):
		return "<Component('%s')>" % (self.url)

class Site(Base):
	__tablename__ = 'sites'
	__table_args__ = {
        'mysql_charset': 'utf8'
    }


	id = Column(Integer, primary_key=True)
	name = Column(String(100), index=True)
	url = Column(String(100), index=True)
	contact = Column(String(50))
	format = Column(String(6))
	sets = Column(String(80))
	last = Column(DateTime)

	items = relationship("Item", backref="items")


	def __repr__(self):
		return "<Site('%s')>" % (self.name)



Base.metadata.create_all(engine)