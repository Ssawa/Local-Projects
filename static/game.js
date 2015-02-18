var Game = {

	gameData : null,

	score : null,

	answered : null,

	questionsPerGame : null,

	processing : null,

	currentQuestion : null,

	// The Game entry point
	startGame : function (data) {
		this.gameData = data;
		// Get reference to processing sketch
		if (this.processing == null) {
			this.processing = Processing.getInstanceById("gameCanvas");
			bindJavascript(this.processing);
		}
		this.processing.setLoading(false);

		// If we have less questions than the specified questionsPerGame we just use how many questions we have
		this.questionsPerGame = this.gameData.questionsPerGame > this.gameData.questions.length ? this.gameData.questions.length : this.gameData.questionsPerGame;
		this.answered = 0;
		this.score = {};
		for (i in this.gameData.tokens) {
			this.score[this.gameData.tokens[i][0]] = 0;
		}
		renderScores();
		nextQuestion();
	}
}

function nextQuestion() {
	if(Game.answered < Game.questionsPerGame) {
		var index = Math.floor(Math.random() * Game.gameData.questions.length);

		// Pop out the question from the array
		Game.currentQuestion = Game.gameData.questions[index];
		Game.gameData.questions.splice(index, 1);
		Game.processing.setQuestion(Game.currentQuestion.questionName);
		Game.processing.showPaper();
		Game.answered++;
	} else {
		Game.processing.setGameOver(true);
		$('#restart').append("<button id='restartButton'>Restart Game</button>");

		$('#restartButton').click(function() {
			Game.processing.setGameOver(false);
			Game.processing.setLoading(true);

			$('#restartButton').remove()

			for (i in Game.gameData.tokens) {
				$("#" + Game.gameData.tokens[i][0]).remove();
			}

			$.getJSON( "api/gameinfo.json", function(data) {
				Game.startGame(data);
			});
		});
	}
}



// true for yes, false for no
function updateScores(yesOrNo) {
	$('#questionsAnswered').text(Game.answered + "/" + Game.questionsPerGame);
	
	for (i in Game.currentQuestion.tokens) {
		var currentToken = Game.currentQuestion.tokens[i]
		if (yesOrNo) {
			//Answered Yes
			Game.score[currentToken.tokenId] += currentToken.Yes;
		} else {
			// Answered No
			Game.score[currentToken.tokenId] += currentToken.No;
		}
		$('#' + currentToken.tokenId + ' span').text(Game.score[currentToken.tokenId]);
	}
}

function yesCalled() {
	console.log("Yes Called");
	updateScores(true);
	setTimeout(nextQuestion, 400);
}

function noCalled() {
	console.log("No Called");
	updateScores(false);
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

function renderScores() {
	$('#questionsAnswered').text(Game.answered + "/" + Game.questionsPerGame);

	for (i in Game.gameData.tokens) {
		$('#scores').append("<div id='" + Game.gameData.tokens[i][0] + "'><b>" + Game.gameData.tokens[i][1] + ": </b><span>0</span></div>");
	}
}

$( document ).ready(function() {
	// Wait for the DOM to load and then wait to retrieve game data before starting the game.
	$.getJSON( "api/gameinfo.json", function(data) {
		Game.startGame(data);
	});
});