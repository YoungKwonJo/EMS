from flask import Blueprint, render_template, redirect, request, url_for

blueprint = Blueprint(
    'base_blueprint',
    __name__,
    url_prefix = '',
    template_folder = 'templates',
    static_folder = 'static'
    )
