from flask import Flask, request, render_template, redirect, flash, session
from flask_debugtoolbar import DebugToolbarExtension
import surveys

app = Flask(__name__)
app.config['SECRET_KEY'] = "12345"
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False
toolbar = DebugToolbarExtension(app)

RESPONSE = 'response'

@app.route('/')
def home():
    return render_template('homepage.html')

@app.route("/begin", methods=["POST"])
def start_survey():
    """Clear the session of responses."""
    session[RESPONSE] = []
    return redirect("/survey/0")

@app.route('/completed')
def completed():
    '''lets user know they completed the survey'''
    return render_template('completed.html')

@app.route('/next_page')
def next_page():
    '''logic to know which page to render'''
    if len(session[RESPONSE]) == len(surveys.satisfaction_survey.questions):
        return redirect("/completed")
    else:
        return redirect(f"/survey/{len(session[RESPONSE])}")

@app.route('/add_answers', methods=["POST"])
def add_answer():
    '''adds response to session'''
    answer = request.form['answer']
    
    responses = session[RESPONSE]
    responses.append(answer)
    session[RESPONSE] = responses
    return redirect('/next_page')

    if len(session[RESPONSE]) == len(surveys.satisfaction_survey.questions):
        return redirect("/completed")

@app.route("/survey/<int:index>")
def survey(index):
    """ survey page"""
    responses = session.get(RESPONSE)

    if responses is None:
        return redirect("/")

    if len(responses) != index:
        flash(f"Invalid question id: {index}.")
        return redirect(f"/survey/{len(responses)}")

    question = surveys.satisfaction_survey.questions[index]
    return render_template("questions.html", question=question, index=index)

if __name__ == '__main__':
    app.run(debug=True)
