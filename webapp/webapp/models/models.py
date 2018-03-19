from sqlalchemy import Column, Integer, String, DateTime
from webapp import db

class ElasticsearchCluster(db.Model):

    __tablename__ = 'ems_elasticsearch_cluster'

    id = Column(Integer, primary_key=True)
    url = Column(String(255))
    version = Column(String(100))
    health = Column(String(100))
    storage_usage = Column(Integer)
    updated_time = Column(DateTime)

    def __repr__(self):
        return str(self.id)
