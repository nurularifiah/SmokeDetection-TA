
from flask import current_app as app
from flask import Blueprint, render_template, session, redirect, url_for, request, jsonify, make_response
from flask import current_app as app
from flask import Blueprint, render_template, flash,request, make_response, session, redirect, url_for, Response
import json
import requests
from models import Detection
from datetime import datetime
from flask import render_template
from collections import defaultdict
from datetime import datetime, date


# inisiasi blueprint
Dashboard = Blueprint (
    name='Dashboard', 
    import_name=__name__,
    url_prefix='/dashboard',
    template_folder='../../templates/pages/Dashboard'
)

# @Dashboard.before_request
# def cek_session():
#     if (session.get('user') == None):
#         return redirect(url_for('Auth.login'))

@Dashboard.route('/')
def index():
    # Mengambil data deteksi dari database
    detections = Detection.query.all()

    # Filter data deteksi hanya untuk hari ini
    today = date.today()
    today_detections = [detection for detection in detections if detection.timestamp.date() == today]

    # Mengubah objek Detection menjadi representasi dictionary
    detections_json = [{'id': detection.id, 'timestamp': detection.timestamp, 'result': detection.result} for detection in today_detections]
    detection_counts = defaultdict(int)
    for detection in today_detections:
        detection_date = detection.timestamp.date()
        detection_counts[detection_date] += 1

    return render_template(
        title="Dashboard",
        template_name_or_list='index.html',
        active='Dashboard.index',
        navigation=app.config['NAVIGATION'],
        detections=detections_json,  # Menyertakan data detections dalam representasi JSON
        detection_counts=detection_counts
    )

# import navigation
from .__navigation__ import Navigation
# import child blueprint
from .cctv import cctv
from .report import report


# register child blueprint
Dashboard.register_blueprint(cctv)
Dashboard.register_blueprint(report)
