from flask import current_app as app
from flask import Blueprint, render_template, flash,request, make_response, session, redirect, url_for, Response
import json
import requests
from models import Detection
from datetime import datetime
from flask import render_template
from collections import defaultdict

cctv = Blueprint(
    name='cctv',
    import_name=__name__,
    url_prefix='/cctv',
    template_folder='../../../templates/pages/Dashboard/cctv'
)
from object_detection import *
from camera_settings import *

@cctv.route('/daftarcctv')
def daftarCCTV():
    return render_template(
        title="Dashboard - Daftar CCTV",
        template_name_or_list='daftarCCTV.html',
        active='Dashboard.cctv.daftarCCTV',
        navigation=app.config['NAVIGATION'],
        # data=data,
    )

@cctv.route('/datamaster', methods=['GET', 'POST'])
def dataMaster():
    # Mengambil data deteksi dari database
    detections = Detection.query.all()

    # Filter data deteksi per hari
    if request.method == 'POST' and 'filter_date' in request.form:
        date = request.form['filter_date']
        try:
            
            filter_date = datetime.datetime.strptime(date, "%Y-%m-%d").date()
            detections = Detection.query.filter(Detection.timestamp >= filter_date).all()
        except ValueError:
            # Tangkap kesalahan jika format tanggal tidak valid
            flash('Format tanggal tidak valid!', 'error')

    # Mengubah objek Detection menjadi representasi dictionary
    detections_json = [{'id': detection.id, 'timestamp': detection.timestamp, 'result': detection.result} for detection in detections]
    detection_counts = defaultdict(int)
    for detection in detections:
        date = detection.timestamp.date()
        detection_counts[date] += 1
    return render_template(
        title="Dashboard - Data Master CCTV",
        template_name_or_list='dataMasterCCTV.html',
        active='Dashboard.cctv.dataMasterCCTV',
        navigation=app.config['NAVIGATION'],
        detections=detections_json, # Menyertakan data detections dalam representasi JSON
        detection_counts=detection_counts 
    )


@cctv.route('/api/datamaster')
def datamasterapi():
    header = {'Authorization': f"Bearer {session['jwt']}"}
    response = requests.request(
        method='GET',
        url=app.config['BACKEND_URL'] + "/cctv/",
        params=request.args.to_dict(),
        headers=header
    )
    return make_response(response.text,response.status_code)

