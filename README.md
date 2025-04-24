# Quiz Platform (Flask)

A simple quiz platform built with Flask where students can register, select a topic, take a quiz, and the results are stored in a database and exportable to Excel.

## Features
- User Registration
- Topic Selection
- MCQ-based Quiz
- Data stored in SQLite
- Export to Excel

## Run Locally
```bash
pip install -r requirements.txt
python app.py
```

## Deploy on Render
1. Push this project to GitHub.
2. Create a new Web Service on [Render](https://render.com).
3. Set the Start Command to:
```bash
gunicorn app:app
```
4. Done! Share your public URL with students.
