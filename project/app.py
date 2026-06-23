from flask import Flask, render_template, request
from rembg import remove
from PIL import Image
import os

app = Flask(__name__)

UPLOAD_FOLDER = "static/uploads"
OUTPUT_FOLDER = "static/output"

os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(OUTPUT_FOLDER, exist_ok=True)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/remove", methods=["POST"])
def remove_bg():

    file = request.files["image"]
    bg_color = request.form["bgcolor"]

    input_path = os.path.join(UPLOAD_FOLDER, file.filename)

    file.save(input_path)

    img = Image.open(input_path).convert("RGBA")

    removed = remove(img)

    hex_color = bg_color.lstrip('#')
    rgb = tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))

    background = Image.new(
        "RGBA",
        removed.size,
        rgb + (255,)
    )

    final_image = Image.alpha_composite(
        background,
        removed
    )

    output_path = os.path.join(
        OUTPUT_FOLDER,
        "final_image.png"
    )

    final_image.save(output_path)

    return render_template(
        "index.html",
        result="output/final_image.png"
    )

if __name__ == "__main__":
    app.run(debug=False)