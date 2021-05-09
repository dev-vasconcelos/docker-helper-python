import flask
import os
from flask import request, flash, Flask, redirect, url_for, send_from_directory
from werkzeug.utils import secure_filename

UPLOAD_FOLDER = './pastaArquivos'
ALLOWED_EXTENSIONS = {'txt', 'pdf', 'dockerfile', ''}

app = flask.Flask(__name__)

app.config["DEBUG"]
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.secret_key = 'super secret key'
app.config['SESSION_TYPE'] = 'filesystem'


@app.route('/hellothere', methods=["GET"])
def helloThere():
    return "General Kennoby"

@app.route('/', methods=["GET"])
def list():
    some = "somequeijo"
    return os.popen('docker ps').read()

@app.route('/listall', methods=["GET"])
def listall():
    return os.popen('docker ps -a').read()

@app.route('/check', methods=["GET"])
def checkContainer():
    checkName = request.args.get('name', default = "000", type = str)
    
    returnStr = os.popen('docker ps -a').read()
    if ( checkName in returnStr ):
        return "True"
    else:
        return "False"

@app.route('/create', methods=["GET"])
def createContainer():
    
    containerName = request.args.get('name', default = "defaultName", type = str)
    osName = request.args.get('os', default = "ubuntu", type = str)

    command = "docker run -td "

    if str(containerName) != "defaultName":
        command += " --name " + str(containerName)
    
    command += " " + str(osName)
    
    # os.system(command)
    return os.popen(command).read()

@app.route('/removeContainer', methods=["GET"])
def removeContainer():
    containerName = request.args.get('name', default = "000", type = str)
    
    if str(containerName) != "000":
        command = "docker rm -f " + containerName
    else:
        return "no container name sent, wish to delete all? go to /deleteAllContainers"
    
    return os.popen(command).read()

@app.route('/removeAllContainers', methods=["GET"])
def removeAllContainers():
    command = "docker rm -f $(docker ps -q)"

    return os.popen(command).read()

@app.route('/getImage')
def getImage():
    imageName = request.args.get('name', default = " ", type = str)

    if(imageName):
        command = "docker pull " + imageName
    else:
        return "Imagem veio nula"

    return os.popen(command).read()

@app.route('/execContainer')
def exeContainer():
    commandContainer = request.args.get('command', default = "ls", type = str)
    name = request.args.get('name', default = "000", type = str)
    
    if ( str(name) != "000"):
        command = 'docker exec ' + str(name)

    command += ' "' + str(commandContainer) + '"'
    print(command)
    return os.popen(command).read()

def allowed_file(filename):
    return '.' in filename and \
        filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/dockerfile', methods=["GET", "POST"])
def uploadDockerfile():
    imageName = request.form["imageName"]
    path = app.config['UPLOAD_FOLDER'] + "/" + imageName

    if 'file' not in request.files:
        flash('No file sent')
        return 'No file'

    file = request.files['file']

    if file.filename == '':
        flash('No file')
        return 'No file'

    filename = secure_filename(file.filename)
    os.system("mkdir -p " + path)
    file.save(os.path.join(path, filename))
    #return redirect(url_for('uploaded_file', filename=filename))

    os.system("docker build -t " + str(imageName).lower()  + " " + path)

    return os.popen('docker images | grep ' + str(imageName).lower()).read()

@app.route('/deleteEverything', methods=["DELETE"])
def deleteEverything():
    return os.popen('docker system prune --force').read()

@app.route('/unused/<option>', methods=["DELETE"])
def pruneUnused(option):
    if("image" in option):
        return os.popen('docker image prune --force').read()
    elif("container" in option):
        return os.popen('docker container prune --force').read()

@app.route('/size', methods=["GET"])
def getSize():
    return os.popen('docker system df').read()

app.run(debug=True)
