from flask import Flask, url_for, render_template, request, redirect, session, Response
from flask_sqlalchemy import SQLAlchemy

from object_detection import *
from camera_settings import *
from models import User, Detection

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
db = SQLAlchemy(app)

# import navigasi
from routes.Dashboard import Navigation
# dashboard sidebar navigation
app.config['NAVIGATION'] = Navigation
# import blueprint
from routes.Dashboard import Dashboard
from routes.Auth import Auth
# register blueprint
app.register_blueprint(Dashboard)
app.register_blueprint(Auth)

@app.route('/', methods=['GET'])
def index():
    return render_template('pages/Auth/login.html')

@app.route('/dash', methods=['GET'])
def dash():
    return render_template(
        title="Dashboard",
        template_name_or_list='index.html',
        active='Dashboard.index',
        navigation=app.config['NAVIGATION']
    )
    
@app.route('/login/', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        return render_template('pages/Auth/login.html')
    else:
        u = request.form['username']
        p = request.form['password']
        data = User.query.filter_by(username=u, password=p).first()
        if data is not None:
            return redirect(url_for('dash'))
        return render_template('pages/Auth/index.html', message="Incorrect Details")

@app.route('/register/', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        try:
            db.session.add(User(username=request.form['username'], password=request.form['password']))
            db.session.commit()
            return redirect(url_for('login'))
        except:
            return render_template('pages/Auth/index.html', message="User Already Exists")
    else:
        return render_template('pages/Auth/register.html')

    
@app.route('/logout', methods=['GET', 'POST'])
def logout():
    return redirect(url_for('login'))

@app.route("/comingsoon")
def comingsoon():
    return render_template("components/coming-soon.html")

check_settings()
VIDEO = VideoStreaming()

@app.route('/video_feed')
def video_feed():
    '''
    Video streaming route.
    '''
    return Response(
        VIDEO.show(),
        mimetype='multipart/x-mixed-replace; boundary=frame'
    )

# Button requests called from ajax
@app.route('/request_preview_switch')
def request_preview_switch():
    VIDEO.preview = not VIDEO.preview
    print('*'*10, VIDEO.preview)
    return "nothing"

@app.route('/request_flipH_switch')
def request_flipH_switch():
    VIDEO.flipH = not VIDEO.flipH
    print('*'*10, VIDEO.flipH)
    return "nothing"

@app.route('/request_model_switch')
def request_model_switch():
    VIDEO.detect = not VIDEO.detect
    print('*'*10, VIDEO.detect)
    return "nothing"

@app.route('/request_exposure_down')
def request_exposure_down():
    VIDEO.exposure -= 1
    print('*'*10, VIDEO.exposure)
    return "nothing"

@app.route('/request_exposure_up')
def request_exposure_up():
    VIDEO.exposure += 1
    print('*'*10, VIDEO.exposure)
    return "nothing"

@app.route('/request_contrast_down')
def request_contrast_down():
    VIDEO.contrast -= 4
    print('*'*10, VIDEO.contrast)
    return "nothing"

@app.route('/request_contrast_up')
def request_contrast_up():
    VIDEO.contrast += 4
    print('*'*10, VIDEO.contrast)
    return "nothing"

@app.route('/reset_camera')
def reset_camera():
    STATUS = reset_settings()
    print('*'*10, STATUS)
    return "nothing"

if(__name__ == '__main__'):
    app.secret_key = "ThisIsNotASecret:p"
    db.create_all()
    app.run()
    