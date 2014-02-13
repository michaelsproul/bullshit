from bullshit import horoscope
from flask import Flask, render_template

app = Flask(__name__)

@app.route("/")
def get_horoscope():
	return render_template("horoscope.html", horoscope=horoscope.generate())

@app.route("/dirty/")
def get_dirty_horoscope():
	return render_template("horoscope.html", horoscope=horoscope.generate(dirty=True))


if __name__ == "__main__":
	app.run(debug=True)

