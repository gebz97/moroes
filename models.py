from sqlalchemy import (
  Column, Integer, String, ForeignKey
)
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

Base = declarative_base()

class System(Base):
  __tablename__ = 'systems'
  id   = Column(Integer, primary_key=True)
  name = Column(String, unique=True, nullable=False)
  services = relationship('Service', back_populates='system', cascade='all, delete')

class Service(Base):
  __tablename__ = 'services'
  id        = Column(Integer, primary_key=True)
  name      = Column(String, nullable=False)
  system_id = Column(Integer, ForeignKey('systems.id'), nullable=False)
  system    = relationship('System', back_populates='services')
  servers   = relationship('Server', back_populates='service', cascade='all, delete')

class Server(Base):
  __tablename__ = 'servers'
  id          = Column(Integer, primary_key=True)
  hostname    = Column(String, unique=True, nullable=False)
  ip_address  = Column(String, nullable=False)
  service_id  = Column(Integer, ForeignKey('services.id'), nullable=False)
  service     = relationship('Service', back_populates='servers')
  databases   = relationship('Database', back_populates='server', cascade='all, delete')

class Database(Base):
  __tablename__ = 'databases'
  id         = Column(Integer, primary_key=True)
  name       = Column(String, nullable=False)
  version    = Column(String)
  server_id  = Column(Integer, ForeignKey('servers.id'), nullable=False)
  server     = relationship('Server', back_populates='databases')

class Credential(Base):
  __tablename__ = 'credentials'
  id            = Column(Integer, primary_key=True)
  vault_path    = Column(String, nullable=False)
  resource_type = Column(String, nullable=False)
  resource_id   = Column(Integer, nullable=False)
