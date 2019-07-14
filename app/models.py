
"""

"""
import os
import sys
import datetime

from flask_appbuilder import Model
from flask import Markup
from flask_appbuilder.models.mixins import FileColumn
from flask_appbuilder.upload import FileUploadField

from sqlalchemy import (Column, Integer, String, Enum, ForeignKey, 
                        DateTime)
from sqlalchemy.orm import relationship
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from flask import g

from . import appbuilder


basedir = os.path.abspath(os.path.dirname(__file__))
parentdir = os.path.split(basedir)[0]
sys.path.append(parentdir)


def currentdate():
    return datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
def get_currentuser():
    #user = g.user("username")
    #if not user:
    #    username = "Guest"
    #else:
    #    username = user()
    return g.user.username


class UploadRegistry(Model):


    def autoincrement():
        session = appbuilder.get_session()
        query = 'select MAX(%s) AS "max" from %s' % ('FAB_ID', 'UPLOAD_REGISTRY')
        results = session.execute(query)
        max = results.first()[0]
        if max is None:
            max = 0
        return max + 1
    
    fab_id = Column(Integer, primary_key=True, nullable=False)
    car_brand = Column(Enum(*['Toyota', 'Peugot']))
    car_model = Column(Enum(*['Toyota Corola', 'Toyota Pickup', 'Peugot Solaris', 'Peugot Cresida', "Other"]))
    car_other = Column(String(60))
    created = Column(DateTime, default=currentdate, onupdate=currentdate, nullable=False)    
    uploaded_file_name = Column(FileColumn)
        
    @property
    def true_filename(self):
        return str(self.uploaded_file_name).split("_sep_")[1]
        
    def __repr__(self):
        return self.fab_id
        
# create the table the first time

        
session = appbuilder.get_session()
query = """
SELECT 
    count(*)
FROM 
    sqlite_master 
WHERE 
    type ='table' AND 
    name = 'upload_registry';
"""
results = session.execute(query)
max = results.first()[0]
query2 = """
CREATE TABLE "upload_registry" (
    fab_id             INTEGER  NOT NULL PRIMARY KEY AUTOINCREMENT,
    car_brand          STRING,
    car_model           STRING,
    car_other           STRING,
    created            DATETIME NOT NULL,
    uploaded_file_name TEXT
    
);
"""
if not max:
    session.execute(query2)