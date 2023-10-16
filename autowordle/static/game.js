let simKeyPressDuration = 200; // Milliseconds between simulated keypresses

let inputLength = 0;

let addEnabled = true;
let backspaceEnabled = false;

let manualInputEnabled = true;

let numberOfAttempts = (gameType === "wordle") ? 6 : -1; // -1 means infinite attempts
let numberOfCells = (numberOfAttempts === -1) ? 5 : numberOfAttempts * 5;

// Array of arrays (one per move) of dictionaries (one per position) with info on color and letter in each position
let gameState = [];

// Event that gets called whenever a new line of colors is received from the server
let stateChangeEvent = new Event("game-state-change");

// Add the specified amount of single-letter cells to the attempts view
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
addAttemptBoxes(numberOfCells);

// Get the DOM elements for the keyboard buttons
let keyboardButtons = document.querySelectorAll(".keyboard .letter-box");

// Receive keyboard input

function enableManualInput() {
    manualInputEnabled = true;
}
function disableManualInput() {
    manualInputEnabled = false;
}

const alphabet = "ABCDEFGHIJKLMNOPQRSTUVWXYZ".split("");
document.addEventListener("keydown", function(event) {
    if (!manualInputEnabled) return;
    let key = event.key.toUpperCase();
    if (alphabet.includes(key) || key === "BACKSPACE") {
        highlightKey(key);
        handleKeyPress(key);
    }
});
document.addEventListener("keyup", function(event) {
    if (!manualInputEnabled) return;
    let key = event.key.toUpperCase();
    if (alphabet.includes(key) || key === "BACKSPACE") {
        dehighlightKey(key);
    }
});

// Receive input on the keyboard buttons on screen
keyboardButtons.forEach(function(b) {
    b.addEventListener("click", function() {
        if (!manualInputEnabled) return;
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

function dehighlightAllKeys() {
    keyboardButtons.forEach((b) => b.classList.remove("active"));
}

// Add a letter to the attempts view
function addLetter(letter) {
    if (!addEnabled)
        return;

    hideError();

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

// Remove a letter from the attempts view
function backspace() {
    if (!backspaceEnabled)
        return;

    hideError();

    inputLength--;
    attemptBoxes[inputLength].innerHTML = "";

    if (inputLength % 5 == 0)
        backspaceEnabled = false;
    addEnabled = true;
}

let autoTyper = {
    ids: [],

    // Clear the current word by simulating backspaces as if they came from the user
    clearWord: function(callback) {
        if (!backspaceEnabled) {
            callback();
            return;
        }

        highlightKey("BACKSPACE");

        let id = setInterval(() => {
            if (!backspaceEnabled) {
                clearInterval(id);
                this.ids = this.ids.filter((thatID) => thatID != id);
                dehighlightKey("BACKSPACE");
                callback();
            }
            backspace();
        }, simKeyPressDuration);

        this.ids.push(id);
    },

    // Simulate key presses as if they came from the user
    type: function(str) {
        if (!addEnabled)
            return;

        let next = 0; // 0: press, 1: release
        let i = 0;

        let id = setInterval(() => {
            if (next === 0) {
                addLetter(str.charAt(i));
                highlightKey(str.charAt(i));
                next = 1;
            } else {
                dehighlightKey(str.charAt(i));
                i++;
                next = 0;

                if (i === str.length) {
                    clearInterval(id);
                    this.ids = this.ids.filter((thatID) => thatID != id);
                }
            }
        }, simKeyPressDuration / 2);

        this.ids.push(id);
    },

    // Stop anything the autotyper is doing
    stop: function() {
        this.ids.forEach(function(id) {
            clearInterval(id);
        });
        dehighlightAllKeys();
        this.ids = [];
    }
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
                showError("No such word");
                return;
            }

            let result = resp.result;

            gameState.push([]);
            let gameStateIndex = gameState.length - 1;

            let countGreen = 0;
            for (let i = 0; i < result.length; i++) {
                let letter = word.charAt(i);
                let outcome = result[i];

                // Update the game state with this cell
                gameState[gameStateIndex].push({
                    letter: letter,
                    color: outcome
                });

                // Display the new cell color and update the keyboard

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

            // Handle victory/defeat
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

            document.dispatchEvent(stateChangeEvent);
        });
    });
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
    elem.classList.remove("error");
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
