import json
from flask import Blueprint, render_template, request
from webapp.models import models
from webapp import db

blueprint = Blueprint(
    'api_blueprint',
    __name__,
    url_prefix = '/api/v1'
    )

@blueprint.route('/elasticsearch/clusters', methods=['POST'])
def add_new_elasticsearch_cluster():

    data = request.get_json(force=True)
    db.session.add( models.ElasticsearchCluster(
                            url=data['es_cluster_url'],
                            version="0.0.0",
                            health="unknown",
                            storage_usage=0)
                    )
    db.session.commit()

    return "OK"

@blueprint.route('/elasticsearch/clusters/<id>', methods=['DELETE'])
def delete_elasticsearch_cluster(id):

    db.session.delete(models.ElasticsearchCluster.query.filter_by(id=id).first())
    db.session.commit()

    return "OK"
