from flask import Flask, render_template, request, redirect, flash, session
from flask_debugtoolbar import DebugToolbarExtension
from surveys import satisfaction_survey

app = Flask(__name__)
app.config['SECRET_KEY'] = "oh-so-secret"

debug = DebugToolbarExtension(app)

responses = []

@app.route("/")
def home_page():
    sat_survey = satisfaction_survey
    return render_template("start_survey.html", sat_survey=sat_survey)

@app.route("/start", methods=["POST"])
def survey_start():

    return redirect("/questions/0")

@app.route("/questions/<int:qid>")
def get_question(qid):
    if (responses is None):
        
        return redirect("/")

    if (len(responses) == len(satisfaction_survey.questions)):
    
        return redirect("/complete")

    if (len(responses) != qid):
        flash(f"Invalid question id: {qid}.")
        return redirect(f"/questions/{len(responses)}")

    question = satisfaction_survey.questions[qid]
    return render_template(
        "questions.html", question_id=qid, question=question)

@app.route("/answer", methods=["POST"])
def post_answer():
    answer = request.form["answer"]
    responses.append(answer)
    
    if (len(responses) == len(satisfaction_survey.questions)):
        print(responses)
        return redirect("/complete")

    else: 
        print(responses)
        return redirect(f"/questions/{len(responses)}")


@app.route("/complete")
def completed_survey(): 

    return render_template("complete.html")




