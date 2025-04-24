
from flask import Flask, render_template, request, redirect, url_for, session, send_file
from flask_sqlalchemy import SQLAlchemy
import pandas as pd
import io

app = Flask(__name__)
app.secret_key = 'supersecretkey'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///quiz.db'
db = SQLAlchemy(app)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    email = db.Column(db.String(100), unique=True)
    password = db.Column(db.String(100))

class Answer(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer)
    topic = db.Column(db.String(50))
    question = db.Column(db.String(200))
    answer = db.Column(db.String(100))

questions = {
    "Math": [
        ("What is 2+2?", ["3", "4", "5"]),
        ("What is 5*3?", ["15", "20", "10"])
    ],
    "Science": [
        ("What planet do we live on?", ["Mars", "Earth", "Jupiter"]),
        ("Water freezes at?", ["0C", "100C", "50C"])
    ]
}

@app.route('/')
def index():
    return render_template('register.html')

@app.route('/register', methods=['POST'])
def register():
    name = request.form['name']
    email = request.form['email']
    password = request.form['password']
    user = User(name=name, email=email, password=password)
    db.session.add(user)
    db.session.commit()
    session['user_id'] = user.id
    return redirect(url_for('select_topic'))

@app.route('/select')
def select_topic():
    return render_template('select_topic.html', topics=questions.keys())

@app.route('/quiz', methods=['POST'])
def quiz():
    session['topic'] = request.form['topic']
    return render_template('quiz.html', topic=session['topic'], questions=questions[session['topic']])

@app.route('/submit', methods=['POST'])
def submit():
    topic = session['topic']
    user_id = session['user_id']
    for q in questions[topic]:
        answer = request.form.get(q[0], '')
        db.session.add(Answer(user_id=user_id, topic=topic, question=q[0], answer=answer))
    db.session.commit()
    return 'Quiz submitted! <a href="/export">Download Results</a>'

@app.route('/export')
def export():
    data = Answer.query.all()
    export_data = [{
        "User ID": d.user_id,
        "Topic": d.topic,
        "Question": d.question,
        "Answer": d.answer
    } for d in data]
    df = pd.DataFrame(export_data)
    output = io.BytesIO()
    with pd.ExcelWriter(output, engine='openpyxl') as writer:
        df.to_excel(writer, index=False, sheet_name='Results')
    output.seek(0)
    return send_file(output, download_name="quiz_results.xlsx", as_attachment=True)

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run()
