let score = 0;
let sec = 60;
let bestScore = 0;
const words = new Set();


async function wordFinder(word) {
	const response = await axios.get('/check-valid-word', { params: { word: word } });

	if (response.data.result === 'not-word') {
		$('#msg').text(`Sorry, but "${word}" is not a valid English word.`, 'err');
	}
	else if (response.data.result === 'not-on-board') {
		$('#msg').text(`Sorry, but "${word}" is not a valid word on this board`, 'err');
	}
	else {
		$('#msg').text(`Your word "${word}" is added`, 'ok');
		score += word.length;
		$('#score').text(score);
		addCheckedWord(word, response.data.result);
	}
	let addWords = document.querySelector('#forms');
	addWords.reset();
}

$('#submit_btn').click(async function(evt)  {
	evt.preventDefault();
	const $word = $('#inputs').val().toLowerCase();
	if (words.has($word)) {
		$('#msg').text(`Already found "${$word}"`, 'err');
	}
	else {
		words.add($word);
		wordFinder($word);
	}
});

function addCheckedWord(word, responseWord) {
    $("#player-words").append(
        `<h2 class="${responseWord} player-word">${word}</h2>`
    );
    return true;
}

let timer = setInterval(countdown, 1000);
function countdown(){
	sec -= 1;
	$('#timer').text(`0:${sec}`);
	if (sec === 0) {
		clearInterval(timer);
        $('#inputs, #submit_btn').attr('disabled', 'disabled');
		alert("Time is up!");
		newScore(score);
	}
}

async function newScore(yourScore) {
	const response = await axios.post('/score', { score: yourScore });
	$('#bestScore').text(response.data.score);
	$('#total_games').text(response.data.games);
}

