$( document ).ready(function() {
	// Wait for the DOM to load and then wait to retrieve game data before starting the game.
	$.getJSON( "api/gameinfo.json", function(data) {
		startGame(data);
	});
});
var gameData;
var score;

// The game entry point
function startGame(data) {
	gameData = data;
	console.log(gameData);

	// Get reference to processing sketch
	var processing = Processing.getInstanceById("gameCanvas");
	bindJavascript();

	// If we have less questions than the specified questionsPerGame we just use how many questions we have
	var questionsPerGame = gameData.questionsPerGame > gameData.questions.length ? gameData.questions.length : gameData.questionsPerGame;
	var answered = 0;
	score = {};
	for (i in gameData.tokens) {
		score[gameData.tokens[i][0]] = 0;
	}

	if(answered < questionsPerGame) {
		var index = Math.floor(Math.random() * gameData.questions.length);

		// Pop out the question from the array
		var question = gameData.questions[index];
		gameData.questions.splice(index, 1);
		processing.setQuestion(question.questionName);
		processing.showPaper();
	}

	function bindJavascript() {
		var bound = false;
		if (processing != null) {
			processing.bindJavascript(this);
			bound = true;
		}
		if(!bound) {setTimeout(bindJavascript, 250);}
	}
}

function yesCalled() {
	console.log("Yes Called");
}

function noCalled() {
	console.log("No Called");
}