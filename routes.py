from flask import Blueprint, render_template, request, redirect, url_for, jsonify
import db

routes = Blueprint('routes', __name__)

questionsPerGame = 10

@routes.route('/')
def home():
    return render_template('home.html')

@routes.route('/game')
def game():
    return render_template('game.html')

# Very simple api call that will be accessed via ajax (Or should it just be passed in
# as part of the template?) to initilize the game with all the information it needs,
# in JSON format
@routes.route('/api/gameinfo')
def getGameInfo():
    # Obviously, doing two different database hits for one api call is sloppy but for
    # prototyping purposes it makes sense just to reuse the functions we already wrote
    return jsonify(questionsPerGame=questionsPerGame,
                    tokens=db.readTokens(),
                    questions=db.getAllQuestions())

@routes.route('/admin/tokens', methods=['POST', 'GET'])
def tokens():
    if request.method == 'POST':
        token = request.form['token']
        db.createToken(token)
    return render_template('tokens.html', tokens=db.readTokens())

# I would have much rathered keep this RESTful and just add a DELETE method check
# within /tokens route but currently most browsers only support forms submitting POST
# and GET. We could have theoretically used ajax to send the DELETE request but this
# just simplifies things for prototyping purposes
@routes.route('/admin/tokens/delete', methods=['POST'])
def deleteTokesn():
    tokenIds = request.form.getlist('tokenId')
    db.deleteTokens(tokenIds)
    return redirect(url_for('.tokens'))

@routes.route('/admin/questions', methods=['POST', 'GET'])
def questions():
    global questionsPerGame
    if request.method == 'POST':
        question = request.form['question']
        yesList = request.form.getlist('yes')
        noList = request.form.getlist('no')
        tokenIds = request.form.getlist('id')
        db.createQuestion(question, yesList, noList, tokenIds)
    return render_template('questions.html', questions=db.readQuestions(), tokens=db.readTokens(), questionsPerGame=questionsPerGame)

@routes.route('/admin/questions/pergame', methods=['POST'])
def updateQuestionsPerGame():
    global questionsPerGame
    questionsPerGame = int(request.form.get('questionsPerGame'))
    return redirect(url_for('.questions'))

@routes.route('/admin/questions/<questionId>', methods=['POST', 'GET'])
def question(questionId):
    if request.method == 'POST':
        yesList = request.form.getlist('yes')
        noList = request.form.getlist('no')
        tokenIds = request.form.getlist('id')
        db.updateQuestion(questionId, yesList, noList, tokenIds)
    return render_template('question-single.html', question=db.getQuestion(questionId), questionId=questionId)

@routes.route('/admin/questions/<questionId>/delete', methods=['POST'])
def deleteQuestion(questionId):
    db.deleteQuestion(questionId)
    return redirect(url_for('.questions'))

