from flask import Flask, request, render_template, send_file, send_from_directory, redirect
import os
import random
from werkzeug.utils import secure_filename

ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg'])

app = Flask(__name__)
app.config["CLIENT_STYLE_IMG"] = "static/imgs/styled_imgs/"
app.config["CLIENT_IMG"] = "static/imgs/user_imgs/"
app.config["CHECKPOINT"]  ="checkpoints/"


def allowed_file(filename):
	return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/')
def index():
    return render_template("index.html")


@app.route('/about')
def about():
    return render_template("about.html")

@app.route('/result', methods=["POST"])
def result():
    
    if request.files:
        n = random.randint(0, 1000)
        img = request.files["image"]
        checkpoint = request.form["style-img"]  # option for checkpoint

        if img.filename == '' or not allowed_file(img.filename):
            return redirect(request.url)
        
        img_name = str(n) + checkpoint + img.filename 

        
        img_path = os.path.join(app.config["CLIENT_IMG"], img_name)
        checkpoint_path = os.path.join(app.config["CHECKPOINT"], checkpoint+'.ckpt')
    

        for file_name in os.listdir(app.config["CLIENT_IMG"]):
            os.remove(os.path.join(app.config["CLIENT_IMG"], file_name))

        for file_name in os.listdir(app.config["CLIENT_STYLE_IMG"]):
            os.remove(os.path.join(app.config["CLIENT_STYLE_IMG"], file_name))

        img.save(img_path)

        cmd = "python fast-style-transfer-master/evaluate.py --checkpoint "+checkpoint_path+" --in-path "+img_path+" --out-path ./static/imgs/styled_imgs/"

        os.system(cmd)
    return render_template("result.html", filename=img_name) 
if __name__ == "__main__":
    app.run(debug=True)