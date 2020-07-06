from flask import Flask, render_template

app = Flask(__name__)
app.config['TEMPLATES_AUTO_RELOAD'] = True

@app.route('/')
def homepage():
  return render_template('index.html')

@app.route('/add.html/')
def add():
  return render_template('add.html')

@app.route('/edit.html/')
def delete():
  return render_template('edit.html')

if __name__ == "__main__":
  app.run(debug=True)