from flask import Blueprint, render_template, current_app
from webapp.models import models
from datetime import datetime

blueprint = Blueprint(
    'home_blueprint',
    __name__,
    url_prefix = '',
    template_folder = 'templates',
    static_folder = 'static'
    )

def get_cluster_health_color(health):

    if health == "green" :
        return "label-success"
    elif health == "yellow" :
        return "label-unknown"
    elif health == "red" :
        return "label-danger"
    else :
        return "label-primary"

def get_storage_usage_color(usage):

    if usage < 80 :
        return "green"
    elif usage < 90 :
        return "yellow"
    else :
        return "red"

@blueprint.route('/')
def index():

    count = 1

    elasticsearch_cluster_list = models.ElasticsearchCluster.query.all()
    for elasticsearch_cluster in elasticsearch_cluster_list:

        elasticsearch_cluster.count = count
        elasticsearch_cluster.health_color = get_cluster_health_color(elasticsearch_cluster.health)
        elasticsearch_cluster.storage_usage_color = get_storage_usage_color(elasticsearch_cluster.storage_usage)
        count += 1


    grafana_url = "http://%s/dashboard-solo/db/elasticsearch-disk-used-ratio-overall?orgId=1&panelId=1&theme=light" % ( current_app.config['GRAFANA_HOST'] )

    return render_template('index.html',
                            cluster_list=elasticsearch_cluster_list,
                            grafana_url=grafana_url)

@blueprint.route('/monitoring/<id>')
def monitoring(id):

    elasticsearch_cluster = models.ElasticsearchCluster.query.filter_by(id=id).first()
    grafana_url = "http://%s/dashboard/db/elasticsearch-monitoring?orgId=1&var-cluster_name=%s&theme=light" % (current_app.config['GRAFANA_HOST'], elasticsearch_cluster.url)

    return render_template('monitoring.html',
                            cluster_url = elasticsearch_cluster.url,
                            grafana_url=grafana_url)
