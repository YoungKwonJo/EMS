import threading
import urlparse
import time
import json

from base import Session, engine, Base
from base import ElasticSearchClusterHealthHelper, ElasticSearchStatsHelper, ElasticSearchNodesStatsHelper
from base import logger
from datetime import datetime
from urllib3 import connection_from_url
from models import ElasticsearchCluster

def get_cluster_health(session):

    response = session.request('GET',"/_cat/health?format=json")
    return json.loads(response.data)[0]

def get_stats(session):

    response = session.request('GET',"/_stats")
    return json.loads(response.data)

def get_nodes_stats(session):

    response = session.request('GET',"/_nodes/stats")
    return json.loads(response.data)['nodes']

def get_cluster_stats(session):

    response = session.request('GET',"/_cluster/stats")
    return json.loads(response.data)

def monitoring_cluster(id, url):

    elasticsearch_cluster_session = connection_from_url(url, maxsize=1, timeout=10)

    influxdb_timestamp = datetime.utcnow().strftime('%Y-%m-%dT%H:%M:%S')
    mysql_timestamp = datetime.now().strftime('%Y-%m-%dT%H:%M:%S')

    cluster_health_data = get_cluster_health(elasticsearch_cluster_session)
    ElasticSearchClusterHealthHelper(cluster_name = url,
                            time = influxdb_timestamp,
                            status = cluster_health_data['status'],
                            node_total = int(cluster_health_data['node.total']),
                            node_data = int(cluster_health_data['node.data']),
                            shards = int(cluster_health_data['shards']),
                            pri = int(cluster_health_data['pri']),
                            relo = int(cluster_health_data['relo']),
                            init = int(cluster_health_data['init']),
                            unassign = int(cluster_health_data['unassign']),
                            active_shards_percent = cluster_health_data['active_shards_percent']
                            )
    ElasticSearchClusterHealthHelper.commit()

    cluster_stat_data = get_stats(elasticsearch_cluster_session)
    ElasticSearchStatsHelper(cluster_name = url,
                            time = influxdb_timestamp,
                            primaries_docs_count = int(cluster_stat_data['_all']['primaries']['docs']['count']),
                            primaries_docs_deleted = int(cluster_stat_data['_all']['primaries']['docs']['deleted']),
                            primaries_store_size_in_bytes = int(cluster_stat_data['_all']['primaries']['store']['size_in_bytes']),
                            primaries_indexing_index_total = int(cluster_stat_data['_all']['primaries']['indexing']['index_total']),
                            primaries_indexing_index_time_in_millis = int(cluster_stat_data['_all']['primaries']['indexing']['index_time_in_millis']),
                            primaries_indexing_delete_total = int(cluster_stat_data['_all']['primaries']['indexing']['delete_total']),
                            primaries_indexing_delete_time_in_millis = int(cluster_stat_data['_all']['primaries']['indexing']['delete_time_in_millis']),
                            primaries_get_total = int(cluster_stat_data['_all']['primaries']['get']['total']),
                            total_docs_count = int(cluster_stat_data['_all']['total']['docs']['count']),
                            total_docs_deleted = int(cluster_stat_data['_all']['total']['docs']['deleted']),
                            total_store_size_in_bytes = int(cluster_stat_data['_all']['total']['store']['size_in_bytes']),
                            total_indexing_index_total = int(cluster_stat_data['_all']['total']['indexing']['index_total']),
                            total_indexing_index_time_in_millis = int(cluster_stat_data['_all']['total']['indexing']['index_time_in_millis']),
                            total_indexing_delete_total = int(cluster_stat_data['_all']['total']['indexing']['delete_total']),
                            total_indexing_delete_time_in_millis = int(cluster_stat_data['_all']['total']['indexing']['delete_time_in_millis']),
                            total_get_total = int(cluster_stat_data['_all']['total']['get']['total'])
                            )
    ElasticSearchStatsHelper.commit()

    nodes_stats_data = get_nodes_stats(elasticsearch_cluster_session)
    fs_total_used_ratio_list = []
    for node_stat in nodes_stats_data:
        node_stat_data = nodes_stats_data[node_stat]
        fs_total_used_ratio = (1.0 - (float(node_stat_data['fs']['total']['available_in_bytes']) / float(node_stat_data['fs']['total']['total_in_bytes'])))*100
        ElasticSearchNodesStatsHelper(cluster_name = url,
                                    node_name = node_stat_data['name'],
                                    time = influxdb_timestamp,
                                    jvm_mem_heap_used_percent = int(node_stat_data['jvm']['mem']['heap_used_percent']),
                                    jvm_gc_collectors_young_collection_count = int(node_stat_data['jvm']['gc']['collectors']['young']['collection_count']),
                                    jvm_gc_collectors_young_collection_time_in_millis = int(node_stat_data['jvm']['gc']['collectors']['young']['collection_time_in_millis']),
                                    jvm_gc_collectors_old_collection_count = int(node_stat_data['jvm']['gc']['collectors']['old']['collection_count']),
                                    jvm_gc_collectors_old_collection_time_in_millis = int(node_stat_data['jvm']['gc']['collectors']['old']['collection_time_in_millis']),
                                    fs_total_used_ratio = fs_total_used_ratio,
                                    thread_pool_bulk_queue = int(node_stat_data['thread_pool']['bulk']['queue']),
                                    thread_pool_bulk_rejected = int(node_stat_data['thread_pool']['bulk']['rejected']),
                                    thread_pool_index_queue = int(node_stat_data['thread_pool']['index']['queue']),
                                    thread_pool_index_rejected = int(node_stat_data['thread_pool']['index']['rejected']),
                                    thread_pool_search_queue = int(node_stat_data['thread_pool']['search']['queue']),
                                    thread_pool_search_rejected = int(node_stat_data['thread_pool']['search']['rejected']),
                                    )
        ElasticSearchNodesStatsHelper.commit()
        fs_total_used_ratio_list.append(fs_total_used_ratio)

    cluster_stats_data = get_cluster_stats(elasticsearch_cluster_session)

    db_session = Session()

    elasticsearch_cluster = db_session.query(ElasticsearchCluster).filter_by(id=id).first()
    elasticsearch_cluster.health = cluster_health_data['status']
    elasticsearch_cluster.version = cluster_stats_data['nodes']['versions']
    elasticsearch_cluster.storage_usage = max(fs_total_used_ratio_list)
    elasticsearch_cluster.updated_time = mysql_timestamp

    db_session.commit()
    db_session.close()

def main():

    Base.metadata.create_all(engine)
    db_session = Session()

    while True:

        elasticsearch_cluster_list = db_session.query(ElasticsearchCluster).all()
        threads = []

        for cluster in elasticsearch_cluster_list:

            thread = threading.Thread(target=monitoring_cluster, args=[cluster.id, cluster.url])
            thread.start()

            threads.append(thread)

    	for thread in threads:
    		thread.join()

        time.sleep(60)

if __name__ == "__main__":
    main()
