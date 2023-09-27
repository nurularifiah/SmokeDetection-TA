from flask import Blueprint, render_template, session
from flask import current_app as app
from flask import request, flash, redirect, url_for
import json
import requests

# inisiasi blueprint
Auth = Blueprint (
    name='Auth', 
    import_name=__name__,
    url_prefix='/auth',
    template_folder='../../templates/pages/Auth'
)

"""
    👨‍🏫 Penjelasan : 
    Fungsi before_request
    akan dijalankan terlebih dahulu oleh flask sebelum memproses segala permintaan
    dalam kasus ini sebelum menjalankan fungsi yang diminta flask akan menjalankan fungsi cek_session terlebih dahulu
    karena fungsi cek_session merupakan fungsi yang didaftarkan pada fungsi before_request
"""
@Auth.before_request
def cek_session():
    if (session.get('user') != None):
        return redirect(url_for('Dashboard.index'))

def session_user(jwt, action):
    session['jwt'] = jwt

@Auth.route('/login')
def login():
    return render_template (
        title="NodeFlux",
        template_name_or_list='login.html',
    )

@Auth.route('/login', methods=['POST'])
def login_process():
    # mengambil data masukkan
    formData = request.form.to_dict()
    print(formData)
    payload = json.dumps(formData)
    header = {
        "Content-Type": "application/json"
    }
    # request permintaan register akun baru ke api
    response = requests.request(
        method="POST", 
        url=f"{app.config['BACKEND_URL']}/admin/login", 
        data=payload, 
        headers=header
    )

    # jika respon api tidak berhasil
    if(response.status_code == 499):
        flash (
            message='Username atau Password salah',
            category='danger'
        )
        return redirect(url_for('Auth.login'))

    if(response.status_code == 200):
        get = response.json().get('data')
        jwt = (get)["access_token"]
        session_user(jwt, "create")
        session['user'] = response.json().get('data')
        return redirect(url_for('Auth.login'))
    
    


@Auth.route('/register', methods=['POST'])
def register_process():
    # mengambil data masukkan
    dataInput = request.form.to_dict()
    
    # request permintaan register akun baru ke api
    payload = json.dumps(dataInput)
    headers = {'Content-Type' : 'application/json'}
    response = requests.request (
        method='POST', 
        url=app.config['BACKEND_URL'] + '/admin/',
        headers=headers,
        data=payload
    )
    
    # jika respon api tidak berhasil mendaftarkan akun baru, maka munculkan pesan error menggunakan flash
    if(response.status_code != 200):
        flash (
            message=response.json().get('description'),
            category='danger'
        )
        return redirect(url_for('Auth.register'))
    
    # jika berhasil, arahkan user ke halaman login
    else:
        flash (
            message=f'Pendaftaran akun berhasil silahkan verifikasi email {dataInput["email"]} untuk dapat login 😊',
            category='success'
        )
        return redirect(url_for('Auth.login'))

@Auth.route('/email/<token>')
def verifikasi_email(token):
    response = requests.request (
        method='GET',
        url=app.config['BACKEND_URL'] + f'/auth/email/{token}'
    )
    print(response.text, response.status_code)
    if response.status_code == 200:
        flash (
            message=response.json().get('message'),
            category='success'
        )
        return redirect(url_for('Auth.login'))
    
    else:
        flash (
            message='Gagal melakukan verifikasi email karena token tidak valid',
            category='danger'
        )
        return redirect(url_for('Auth.login'))