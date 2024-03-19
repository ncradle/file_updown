from pathlib import Path

from flask import Flask, request, send_file
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

CWD = Path(__file__).parent
RETUEN_FILE = "modified_file.txt"
RETUEN_FILE = CWD / RETUEN_FILE


@app.route("/upload", methods=["POST"])
def upload_file():
    uploaded_file = request.files["uploaded"]
    if uploaded_file.filename != "":
        content = uploaded_file.read().decode("utf-8")
        content += "\nhello world"
        with open(RETUEN_FILE, "w") as f:
            f.write(content)
        return send_file(RETUEN_FILE, as_attachment=True)


if __name__ == "__main__":
    app.run(debug=True, host="localhost", port=5000)
