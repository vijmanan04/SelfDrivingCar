from flask import Flask, render_template

app = Flask(__name__) #create instance of append

@app.route("/") #send to home page

def home():
    return render_template("index.html")


if __name__ == "__main__":
    app.run()
