# -*- coding: utf-8 -*-
import json
import os, sys

from flask import Flask, render_template, redirect, url_for, request, send_from_directory, send_file, flash, jsonify
from werkzeug.utils import secure_filename

REPO_PATH = os.path.dirname(os.path.abspath(os.path.dirname((__file__))))
ML_PATH = os.path.join(REPO_PATH, "ml")
API_ROOT = os.path.abspath(os.path.dirname((__file__)))
UPLOAD_FOLDER = '/uploads'


sys.path.append(REPO_PATH)
sys.path.append(ML_PATH)

from ml.predict import predict_knn, predict_mlp

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

FULL_UPLOAD_PATH = os.path.abspath(os.path.dirname(__file__)) + app.config['UPLOAD_FOLDER']


pokemon_entries = {
    "Charmander": "The flame at the tip of its tail makes a sound as it burns. You can only hear it in quiet places.",
    "Pikachu": "It keeps its tail raised to monitor its surroundings. If you yank its tail, it will try to bite you.",
    "Squirtle": "Shoots water at prey while in the water. Withdraws into its shell when in danger.",
    "Blastoise": "Once it takes aim at its enemy, it blasts out water with even more force than a fire hose.",
    "Alakazam": "A Pokemon that can memorize anything. It never forgets what it learns - thats why this pokemon is smart.",
    "Charizard": "Charizard, the Flame Pokemon. Charizards powerful flame can melt absolutely anything.",
    "Bulbasaur": "It can go for days without eating a single morsel. In the bulb on its back, it stores energy.",
    "Articuno": "A legendary bird Pokemon. It freezes water that is contained in winter air and makes it snow.",
    "Arcanine": "A legendary Pokemon in China. Many people are charmed by its grace and beauty while running."

}

############## Helper functions ##############

def allowed_file(filename):
    allowed_extensions = set(['png', 'jpg', 'jpeg'])
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in allowed_extensions


############## Views ##############
@app.route('/', methods=['GET', 'POST'])
def index():
    return render_template('index.html')


@app.route('/predict', methods=['POST', 'GET'])
def predict():
    import ipdb; ipdb.set_trace(context=20)
    if 'file' not in request.files:
        flash('No file part')
        return redirect(request.url)
    file = request.files['file']
    
    if file.filename == '':
        flash('No selected file')
        return redirect(request.url)
    
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        try:
            pokemon_name = predict_mlp(file).capitalize()
            if pokemon_name == "Bulbassaur":
                pokemon_name = "Bulbasaur"
            pokemon_desc = pokemon_entries.get(pokemon_name)
            msg = ""
        except Exception as e:
            pokemon_name = None
            pokemon_desc = None
            msg = str(e)

    return jsonify({'name': pokemon_name, 'description': pokemon_desc, "msg": msg})


@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(FULL_UPLOAD_PATH, filename)

@app.route('/static/<path:path>')
def send_static(path):
    return send_from_directory('static', path)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000, debug=True)
