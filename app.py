#!/usr/bin/env python
import os
import shutil
import csv
from flask import Flask, render_template, request, \
    Response, send_file, redirect, url_for
from camera import Camera
from flask import send_file, send_from_directory, safe_join, abort,session


app = Flask(__name__)
camera = None
app.secret_key = "abc"  
def get_camera():
    global camera
    if not camera:
        camera = Camera()

    return camera


"""
@app.route('/')
def root():
    return redirect(url_for('index'))
"""
@app.route('/', methods =["GET", "POST"])
def image():
   if request.method == "POST":
       first_name = request.form.get("fname")
    
       last_name = request.form["lname"]
       print(last_name)
       session["a"]=first_name
       session["c"]=last_name
       
       #os.mkdir(str(first_name)+"_"+str(last_name))
       #os.chdir(str(first_name)+"_"+str(last_name))
       #return "Your name is "+first_name + last_name
       """with open('nameList.csv','w') as inFile:
            
            writer = csv.DictWriter(inFile, fieldnames=fieldnames)

            
            writer.writerow({'name': name, 'comment': comment})"""

       return redirect(url_for('index'))
       
   
   return render_template('register.html')

@app.route('/index/', methods =["GET", "POST"])
def index():
    return render_template('index.html')

def gen(camera):
    while True:
        frame = camera.get_feed()
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

@app.route('/video_feed/')
def video_feed():
    camera = get_camera()
    return Response(gen(camera),
        mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/capture/')
def capture():
    name=session.get("a")
    last=session.get("c")
    #print(name)
    camera = get_camera()
    stamp,_ = camera.capture(name,last)
    #print(filename)
    #f = ('%s.jpeg' % time.strftime("%Y%m%d-%H%M%S"))
    #camera.save('%s/%s' % ('None_None', f))

    return redirect(url_for('show_capture', timestamp=stamp))
    

"""    
@app.route('/uploads/<path:filename>', methods=['GET', 'POST'])


def download(filename):
    filename=str(request.args.get('first_name'))
    uploads = os.path.join(current_app.root_path, app.config['UPLOAD_FOLDER'])
    return send_from_directory(directory=uploads, filename=filename)
"""    
def stamp_file(timestamp):
    name=session.get("a")
    last=session.get("c")
    return 'photos/'+str(name)+'_'+str(last)+'/'+ timestamp +'.jpg'
    
@app.route('/capture/image/<timestamp>', methods=['POST', 'GET'])
def show_capture(timestamp):
    
    path = stamp_file(timestamp)


    return render_template('capture.html',
        stamp=timestamp, path=path)
"""
@app.route('/capture/image/<timestamp>', methods=['POST', 'GET'])
def show_capture(timestamp):
    
    path = stamp_file(timestamp)


    #email_msg = None
    #if request.method == 'POST':
        

    return render_template('capture.html',
        stamp=timestamp, path=path)

</form>
 <form method="GET" action="{{url_for('index')}}">
<button type="submit" > Take photo </button>
</form>"""
if __name__ == '__main__':
    

    app.run(host='0.0.0.0', port=8080, debug=True)
