from flask import Flask, request, render_template, redirect, flash
from flask_debugtoolbar import DebugToolbarExtension
from surveys import Survey, satisfaction_survey

app = Flask(__name__)
app.config['SECRET_KEY'] = "secret"
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False

debug = DebugToolbarExtension(app)

responses = []


@app.route('/')
def home_page():
    TITLE = satisfaction_survey.title
    INSTRUCTIONS = satisfaction_survey.instructions
    return render_template("base.html", title=TITLE, instructions=INSTRUCTIONS)


@app.route('/questions/<num>')
def survey_questions(num):
    num = int(float(num))
    QUESTIONS = satisfaction_survey.questions[num].question
    CHOICES = satisfaction_survey.questions[num].choices

    if (responses is None):
        return redirect("/")

    if (len(responses) == len(satisfaction_survey.questions)):
        return redirect("/end")

    if (len(responses) != num):
        flash("Invalid question.")
        return redirect(f"/questions/{len(responses)}")

    return render_template("form.html", num=num, questions=QUESTIONS, choices=CHOICES)


@ app.route('/answer', methods=['POST'])
def survey_answers():
    answers = request.form['answers']

    responses.append(answers)
    if (len(responses) == len(satisfaction_survey.questions)):
        return redirect("/end")
    else:
        return redirect(f"/questions/{len(responses)}")


@ app.route('/end')
def end_survey():
    return render_template('end.html')
