import os
from flask import Flask, render_template_string, make_response

app = Flask(__name__)

@app.route("/", methods=["GET", "HEAD"])
def home():
    if os.path.exists("index.html"):
        with open("index.html", "r") as f:
            html_content = f.read()
    else:
        html_content = "<h1>My Corner</h1><p>index.html was not found.</p>"
        
    return render_template_string(html_content)

@app.route("/style.css", methods=["GET"])
def css():
    if os.path.exists("style.css"):
        with open("style.css", "r") as f:
            css_content = f.read()
        
        response = make_response(css_content)
        response.headers["Content-Type"] = "text/css"
        return response
    return make_response("", 404)

if __name__ == "__main__":
    app.run(port=8000)
