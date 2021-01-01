from flask import Flask, request, render_template, redirect, flash, session
from flask_debugtoolbar import DebugToolbarExtension
from surveys import satisfaction_survey as survey

response = "responses"

app = Flask(__name__)
app.config['SECRET_KEY'] = "secret"
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False

debug = DebugToolbarExtension(app)


@app.route('/')
def home_page():
    # TITLE = satisfaction_survey.title
    # INSTRUCTIONS = satisfaction_survey.instructions
    return render_template("base.html", survey=survey)
# title=TITLE, instructions=INSTRUCTIONS



@app.route("/start", methods=["POST"])
def start_survey():
    session[response] = []
    return redirect("questions/0")



@app.route('/answer', methods=['POST'])
def survey_answers():
    answers = request.form['answers']

    responses = session[response]
    responses.append(answers)
    session[response] = responses
    
    if (len(responses) == len(survey.questions)):
        return redirect("/end")
    else:
        return redirect(f"/questions/{len(responses)}")



@app.route('/questions/<num>')
def survey_questions(num):
    num = int(float(num))
    # QUESTIONS = satisfaction_survey.questions[num].question
    # CHOICES = satisfaction_survey.questions[num].choices
    responses = session.get(response)

    if (responses is None):
        return redirect("/")

    if (len(responses) == len(survey.questions)):
        return redirect("/end")

    if (len(responses) != num):
        flash("Invalid question.")
        return redirect(f"/questions/{len(responses)}")

    question = survey.questions[num]
    return render_template("form.html", num=num, question=question)


@ app.route('/end')
def end_survey():
    return render_template('end.html')
