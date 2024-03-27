from pathlib import Path

from flask import Flask, Response, render_template, request
from flask_cors import CORS
from werkzeug.datastructures.file_storage import FileStorage

app = Flask(__name__)
CORS(app)

CWD: Path = Path(__file__).parent


@app.route("/")
def index() -> str:
    return render_template("index.html")


@app.route("/upload", methods=["POST"])
def upload_file() -> Response | None:
    uploaded_file: FileStorage = request.files["uploaded"]

    if uploaded_file.filename != "":
        content: str = uploaded_file.stream.read().decode("utf-8")
        content += "\nhello world"
        return content


if __name__ == "__main__":
    app.run(debug=True, host="localhost", port=5000)
