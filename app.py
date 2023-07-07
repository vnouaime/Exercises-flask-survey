from flask import Flask, render_template, request, redirect, flash, session
from flask_debugtoolbar import DebugToolbarExtension
from surveys import satisfaction_survey

all_responses = "all_responses"

app = Flask(__name__)
app.config['SECRET_KEY'] = "oh-so-secret"

debug = DebugToolbarExtension(app)

@app.route("/")
def home_page():
    """Home page of survey that instructs the user to click on start and then redirects the page to start route"""
    sat_survey = satisfaction_survey
    return render_template("start_survey.html", sat_survey=sat_survey)

@app.route("/start", methods=["POST"])

def survey_start():
    """Initializes empty list as a cookie to save responses of user and then redirects to first question of survey"""
    session[all_responses] = []
    return redirect("/questions/0")

@app.route("/questions/<int:qid>")
def get_questions(qid):
    """
    Displays one question at a time from the survey. Checks to see if cookies list, responses, has anything saved in it; This will redirect to home page. Checks to see if all questions have been answered. This will redirect user to complete route. Lastly checks to make sure that user is not going to a different question if the previous question has not been answered. This redirects user to the current question that user is on. 
    """
    responses = session.get(all_responses)

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
    """
    After user hits continue on the question page, server fires POST request to save user's reponses to responses list in session. Then checks to see if user has answered all questions in survey. Redirects user according to completion.
    """
    answer = request.form["answer"]
    
    responses = session[all_responses]
    responses.append(answer)
    session[all_responses] = responses
    
    if (len(responses) == len(satisfaction_survey.questions)):
    
        return redirect("/complete")

    else: 

        return redirect(f"/questions/{len(responses)}")


@app.route("/complete")
def completed_survey():  
    """Thanks user for completing survey and informs that responses have been recorded. """

    return render_template("complete.html")




