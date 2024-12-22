#write web server
#using flask library 

from dotenv import load_dotenv
from flask import Flask, render_template, request, jsonify
from icebreaker import ice_break_with

load_dotenv()

app = Flask(__name__)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/process", methods=["POST"])
def process():
    name = request.form.get("name")
    summary, profile_pic_url = ice_break_with(name)
    return jsonify(
        {
            "summary": summary.to_dict(), #turn summary object into dictionary
            "picture_url": profile_pic_url
        }
    )

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080, debug=True)