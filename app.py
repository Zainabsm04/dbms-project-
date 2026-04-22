from flask import Flask, render_template, request, redirect, url_for
from student_results import StudentResults

app = Flask(__name__)
sr = StudentResults()

@app.route('/')
def index():
    results = sr.calculate_all_sgpas()
    total = sr.total_students()
    return render_template('index.html', results=results, total=total)

@app.route('/add', methods=['GET', 'POST'])
def add_student():
    if request.method == 'POST':
        name = request.form['name']
        roll_no = request.form['roll_no']
        subjects = []

        subject_names = request.form.getlist('subject_name')
        grades = request.form.getlist('grade')
        credits = request.form.getlist('credits')

        for i in range(len(subject_names)):
            subjects.append({
                "name": subject_names[i],
                "grade": int(grades[i]),
                "credits": int(credits[i])
            })

        sr.add_student(name, roll_no, subjects)
        return redirect(url_for('index'))

    return render_template('add_student.html')

@app.route('/top')
def top_scorer():
    top = sr.top_scorer()
    return render_template('top_scorer.html', top=top)

if __name__ == '__main__':
    app.run(debug=True)
