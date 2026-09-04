import os
from flask import Flask, render_template_string

app = Flask(__name__)

@app.route("/", methods=["GET", "HEAD"])
def home():
    # This simply reads your index.html and displays it on the screen
    if os.path.exists("index.html"):
        with open("index.html", "r") as f:
            html_content = f.read()
    else:
        html_content = "<h1>My Corner</h1><p>index.html was not found.</p>"
        
    return render_template_string(html_content)

if __name__ == "__main__":
    # Runs the local development server if you ever test it on your laptop
    app.run(port=8000)
