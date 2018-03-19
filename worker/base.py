# coding=utf-8

import ConfigParser

# parsing config file
CONFIGPATH = 'worker.conf'

config = ConfigParser.ConfigParser()
config.read(CONFIGPATH)

database_uri = config.get('DEFAULT', 'SQLALCHEMY_DATABASE_URI')

influxdb_host = config.get('DEFAULT', 'INFLUXDB_HOST')
influxdb_port = config.get('DEFAULT', 'INFLUXDB_PORT')
influxdb_username = config.get('DEFAULT', 'INFLUXDB_USERNAME')
influxdb_password = config.get('DEFAULT', 'INFLUXDB_PASSWORD')
influxdb_database = config.get('DEFAULT', 'INFLUXDB_DATABASE')

interval = config.getint('DEFAULT', 'INTERVAL')
logfile = config.get('DEFAULT', 'LOGFILE')

# set log handler

import logging

logger = logging.getLogger("ems_logger")
logger.setLevel(logging.DEBUG)

formatter = logging.Formatter('[ems][%(filename)s:%(lineno)s] %(asctime)s > %(message)s')

file_handler = logging.FileHandler(logfile)
file_handler.setFormatter(formatter)

logger.addHandler(file_handler)

# base code about database connection

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

engine = create_engine(database_uri)
Session = sessionmaker(bind=engine)

Base = declarative_base()

# base code about influxdb connection and series helpers

from influxdb import SeriesHelper
from influxdb import InfluxDBClient

print influxdb_database

influxdb_client = InfluxDBClient(influxdb_host,
                                influxdb_port,
                                influxdb_username,
                                influxdb_password,
                                influxdb_database)

influxdb_client.create_database(influxdb_database)
influxdb_client.create_retention_policy("ems_retention_policy", "1d", 3, default=True)

class ElasticSearchClusterHealthHelper(SeriesHelper):
    class Meta:
        client = influxdb_client

        series_name = 'cluster_health'
        fields = [
            'status',
            'node_total',
            'node_data',
            'shards',
            'pri',
            'relo',
            'init',
            'unassign',
            'active_shards_percent'
        ]
        tags = [ 'cluster_name' ]
        bulk_size = 10
        autocommit = True

class ElasticSearchStatsHelper(SeriesHelper):
    class Meta:
        client = influxdb_client

        series_name = 'cluster_stats'
        fields = [
            'primaries_docs_count',
            'primaries_docs_deleted',
            'primaries_store_size_in_bytes',
            'primaries_indexing_index_total',
            'primaries_indexing_index_time_in_millis',
            'primaries_indexing_delete_total',
            'primaries_indexing_delete_time_in_millis',
            'primaries_get_total',
            'total_docs_count',
            'total_docs_deleted',
            'total_store_size_in_bytes',
            'total_indexing_index_total',
            'total_indexing_index_time_in_millis',
            'total_indexing_delete_total',
            'total_indexing_delete_time_in_millis',
            'total_get_total'

        ]
        tags = [ 'cluster_name' ]
        bulk_size = 10
        autocommit = True

class ElasticSearchNodesStatsHelper(SeriesHelper):
    class Meta:
        client = influxdb_client

        series_name = 'nodes_stats'
        fields = [
            'jvm_mem_heap_used_percent',
            'jvm_gc_collectors_young_collection_count',
            'jvm_gc_collectors_young_collection_time_in_millis',
            'jvm_gc_collectors_old_collection_count',
            'jvm_gc_collectors_old_collection_time_in_millis',
            'fs_total_used_ratio',
            'thread_pool_bulk_queue',
            'thread_pool_bulk_rejected',
            'thread_pool_index_queue',
            'thread_pool_index_rejected',
            'thread_pool_search_queue',
            'thread_pool_search_rejected'

        ]
        tags = [ 'cluster_name', 'node_name' ]
        bulk_size = 10
        autocommit = True
