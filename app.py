from flask import Flask
import subprocess
import os

app = Flask(__name__)

@app.route("/")
def home():
    return "Naukri automation server running."

@app.route("/run-job")
def run_job():
    subprocess.run(["python", "update_naukri_ai.py"])
    return "Automation executed!"


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)
