let autopilotEnabled = false;
let solverID = null;
let nextGameStateToSend = 0;

let currentInterval = null;

// Listen for status changes
document.addEventListener("game-state-change", autopilotIteration);
document.addEventListener("win", handleEnd);
document.addEventListener("lose", handleEnd);

// When the button is clicked, toggle autopilot mode
let toggleAutopilotButton = document.getElementById("toggle-autopilot");
toggleAutopilotButton.addEventListener("click", function(e) {
    if (autopilotEnabled) {
        autopilotEnabled = false;
        toggleAutopilotButton.innerHTML = "Start autopilot";
        stopAutopilot();
    } else {
        autopilotEnabled = true;
        toggleAutopilotButton.innerHTML = "Stop autopilot";
        startAutopilot();
    }
});

function handleEnd() {
    toggleAutopilotButton.innerHTML = "Start autopilot";
    toggleAutopilotButton.disabled = true;
}

function startAutopilot() {
    autopilotEnabled = true;
    disableManualInput();
    autoTyper.clearWord(autopilotIteration);
}

function stopAutopilot() {
    autopilotEnabled = false;
    enableManualInput();
    autoTyper.stop();
    hideLoading();
}

async function autopilotIteration() {
    if (!autopilotEnabled)
        return;

    let newGameState = gameState.slice(nextGameStateToSend);
    nextGameStateToSend = gameState.length;

    let payload = {
        newGameState: newGameState
    };
    if (solverID) {
        payload = {
            ...payload,
            solverID: solverID
        };
    } else {
        payload = {
            ...payload,
            gameTypeID: gameType
        }
    }

    let loaded = false;
    setTimeout(() => {
        if (!loaded) {
            showLoading();
        }
    }, 500);
    try {
        const response = await fetch(solverURL, {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
            },
            body: JSON.stringify(payload),
        });

        loaded = true;

        if (!response.ok) {
            showError(response.status + ": " + response.statusText);
            return;
        }

        const result = await response.json();

        if (!autopilotEnabled)
            return;

        if (result.solverID)
            solverID = result.solverID;

        if (!result.word) {
            console.error("No valid word found by solver");
            return;
        }

        autoTyper.type(result.word);
    } catch (error) {
        console.error("Error:", error);
    } finally {
        hideLoading();
    }
}

function showLoading() {
    document.getElementById("loading-overlay").style.display = "";
}

function hideLoading() {
    document.getElementById("loading-overlay").style.display = "none";
}
