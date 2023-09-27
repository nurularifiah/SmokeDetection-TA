from flask import current_app as app
from flask import Blueprint, render_template, request, make_response, session, redirect, url_for
import json
import requests

report = Blueprint(
    name='report',
    import_name=__name__,
    url_prefix='/report',
    template_folder='../../../templates/pages/Dashboard/report'
)

@report.route('/')
def Datareport():
    return render_template (
        title="Dashboard - Keterangan",
        template_name_or_list='keterangan.html',
        active='Dashboard.report.Datareport',
        navigation=app.config['NAVIGATION'],
    )