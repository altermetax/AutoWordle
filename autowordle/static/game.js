let simKeyPressDuration = 200; // Milliseconds between simulated keypresses

let inputLength = 0;

let addEnabled = true;
let backspaceEnabled = false;

let numberOfAttempts = (gameType === "wordle") ? 6 : -1; // -1 means infinite attempts
let numberOfCells = (numberOfAttempts === -1) ? 5 : numberOfAttempts * 5;

// Adds the specified amount of single-letter cells to the attempts view
let attemptBoxes = [];
function addAttemptBoxes(amount) {
    let container = document.getElementById("attempts-view");
    for (let i = 0; i < amount; i++) {
        let elem = document.createElement("div");
        elem.classList.add("letter-box");
        container.appendChild(elem);
        attemptBoxes.push(elem);
        elem.scrollIntoView();
    }
}

// Generate grid
addAttemptBoxes(numberOfCells)

let keyboardButtons = document.querySelectorAll(".keyboard .letter-box");

// Receive keyboard input
const alphabet = "ABCDEFGHIJKLMNOPQRSTUVWXYZ".split("");
document.addEventListener("keydown", function(event) {
    let key = event.key.toUpperCase();
    if (alphabet.includes(key) || key === "BACKSPACE") {
        highlightKey(key);
        handleKeyPress(key);
    }
});
document.addEventListener("keyup", function(event) {
    let key = event.key.toUpperCase();
    if (alphabet.includes(key) || key === "BACKSPACE") {
        dehighlightKey(key);
    }
});

// Receive input on the keyboard buttons on screen
keyboardButtons.forEach(function(b) {
    b.addEventListener("click", function() {
        handleKeyPress(b.innerHTML === "⌫" ? "BACKSPACE" : b.innerHTML);
    });
});

function handleKeyPress(key) {
    if (key === "BACKSPACE") {
        backspace();
    } else {
        addLetter(key);
    }
}

function highlightKey(key) {
    document.getElementById("key-" + key).classList.add("active");
}

function dehighlightKey(key) {
    document.getElementById("key-" + key).classList.remove("active");
}

function addLetter(letter) {
    if (!addEnabled)
        return;

    attemptBoxes[inputLength++].innerHTML = letter;

    if (inputLength % 5 == 0) {
        let word = "";
        for (let i = inputLength - 5; i < inputLength; i++) {
            word += attemptBoxes[i].innerHTML.trim();
        }
        guessWord(word);
        return;
    }
    backspaceEnabled = true;
}

function backspace() {
    if (!backspaceEnabled)
        return;

    inputLength--;
    attemptBoxes[inputLength].innerHTML = "";

    if (inputLength % 5 == 0)
        backspaceEnabled = false;
    addEnabled = true;
}

function simClearCurrentWord() {
    let length = inputLength % 5;
    if (length === 0) length = 5;
    let count = 0;

    highlightKey("BACKSPACE");

    let id = setInterval(function() {
        backspace();
        count++;
        if (count === length) {
            clearInterval(id);
            dehighlightKey("BACKSPACE");
        }
    }, simKeyPressDuration);
}

function simKeyPresses(str) {
    let next = 0; // 0: press, 1: release
    let i = 0;

    let id = setInterval(function() {
        if (next === 0) {
            addLetter(str.charAt(i));
            highlightKey(str.charAt(i));
            next = 1;
        } else {
            dehighlightKey(str.charAt(i));
            i++;
            next = 0;

            if (i === str.length)
                clearInterval(id);
        }
    }, simKeyPressDuration / 2)
}

function showError(error) {
    let elem = document.getElementById("message");
    elem.innerHTML = error;
    elem.classList.add("error");
    elem.classList.remove("win");
    elem.classList.remove("lose");
    elem.style.display = "";
}

function hideError(error) {
    let elem = document.getElementById("message");
    elem.style.display = "none";
}

function win() {
    addEnabled = false;
    backspaceEnabled = false;
    let elem = document.getElementById("message");
    elem.innerHTML = "You win!";
    elem.style.display = "";
    elem.classList.add("win");
}

function lose(correctWord = null) {
    addEnabled = false;
    backspaceEnabled = false;
    let elem = document.getElementById("message");
    elem.innerHTML = "You lose!";
    if (gameType === "wordle")
        elem.innerHTML += " The correct word was " + correctWord + ".";
    elem.style.display = "";
    elem.classList.add("lose");
}

function guessWord(word) {
    hideError();
    addEnabled = false;
    backspaceEnabled = false;

    let url = guessURL + "?word=" + word;

    fetch(url).then((response) => {
        if (!response.ok) {
            showError(response.status + ": " + response.statusText);
            return;
        }
        response.text().then((text) => {
            let resp = JSON.parse(text);

            if (!resp.valid) {
                backspaceEnabled = true;
                return;
            }

            let result = resp.result;

            let countGreen = 0;
            for (let i = 0; i < result.length; i++) {
                let letter = word.charAt(i);
                let outcome = result[i];

                let key = document.getElementById("key-" + letter);

                if (outcome === "green") {
                    attemptBoxes[inputLength - 5 + i].classList.add("green");
                    key.classList.add("green");
                    key.classList.remove("yellow", "gray");
                    countGreen++;
                } else if (outcome === "yellow") {
                    attemptBoxes[inputLength - 5 + i].classList.add("yellow");
                    if (!key.classList.contains("green")) {
                        key.classList.add("yellow");
                        key.classList.remove("gray");
                    }
                } else if (outcome === "gray") {
                    attemptBoxes[inputLength - 5 + i].classList.add("gray");
                    if (!key.classList.contains("green") && !key.classList.contains("yellow")) {
                        key.classList.add("gray");
                    }
                }
            }

            if (countGreen === 5) {
                win();
                return;
            } else if (numberOfAttempts !== -1 && inputLength === numberOfCells) {
                if (resp.correct)
                    lose(resp.correct);
                else
                    lose();
                return;
            } else {
                if (numberOfAttempts === -1)
                    addAttemptBoxes(5);
                addEnabled = true;
            }
        });
    });
}