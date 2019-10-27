from flask import Flask, request
import json

app = Flask(__name__)

def main():
    app.run(host="0.0.0.0", port=3000, debug=True)


@app.route("/", methods=["GET"])
def index():
    return "Hello, Podcast!"

@app.route("/create", methods=["POST"])
def create_container():
    if request.method == "POST":
        print(json.loads(request.data))
        return "Create, World!"

if __name__ == "__main__":
    main()