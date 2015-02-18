var Game = {

	gameData : null,

	score : null,

	answered : null,

	questionsPerGame : null,

	processing : null,

	// The Game entry point
	startGame : function (data) {
		this.gameData = data;
		// Get reference to processing sketch
		this.processing = Processing.getInstanceById("gameCanvas");
		bindJavascript(this.processing);

		this.processing.setLoading(false);

		// If we have less questions than the specified questionsPerGame we just use how many questions we have
		this.questionsPerGame = this.gameData.questionsPerGame > this.gameData.questions.length ? this.gameData.questions.length : this.gameData.questionsPerGame;
		this.answered = 0;
		this.score = {};
		for (i in this.gameData.tokens) {
			this.score[this.gameData.tokens[i][0]] = 0;
		}
		nextQuestion();
	}
}

function nextQuestion() {
	if(Game.answered < Game.questionsPerGame) {
		var index = Math.floor(Math.random() * Game.gameData.questions.length);

		// Pop out the question from the array
		var question = Game.gameData.questions[index];
		Game.gameData.questions.splice(index, 1);
		Game.processing.setQuestion(question.questionName);
		Game.processing.showPaper();
		Game.answered++;
	} else {
		Game.processing.setGameOver(true);
	}
}

function yesCalled() {
	console.log("Yes Called");
	setTimeout(nextQuestion, 400);
}

function noCalled() {
	console.log("No Called");
	setTimeout(nextQuestion, 400);
}

function bindJavascript(processing) {
	var bound = false;
	if (processing != null) {
		processing.bindJavascript(this);
		bound = true;
	}
	if(!bound) {setTimeout(bindJavascript, 250);}
}

$( document ).ready(function() {
	// Wait for the DOM to load and then wait to retrieve game data before starting the game.
	$.getJSON( "api/gameinfo.json", function(data) {
		Game.startGame(data);
	});
});