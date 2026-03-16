from flask import Flask
import subprocess

app = Flask(__name__)

@app.route("/")
def home():
    return "Naukri automation server running."

@app.route("/run-job")
def run_job():
    subprocess.run(["python", "update_naukri_ai.py"])
    return "Automation executed!"
