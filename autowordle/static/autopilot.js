let autopilotEnabled = false;
let solverID = null;
let nextGameStateToSend = 0;

let currentInterval = null;

// Listen for status changes
document.addEventListener("game-state-change", autopilotIteration);

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

function startAutopilot() {
    autopilotEnabled = true;
    disableManualInput();
    autoTyper.clearWord(() => autopilotIteration());
}

function stopAutopilot() {
    autopilotEnabled = false;
    enableManualInput();
    autoTyper.stop();
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
            gameID: solverID
        }
    };

    try {
        const response = await fetch(solverURL, {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
            },
            body: JSON.stringify(payload),
        });

        if (!response.ok) {
            showError(response.status + ": " + response.statusText);
            return;
        }

        const result = await response.json();

        if (!autopilotEnabled)
            return;

        autoTyper.type(result.word);
    } catch (error) {
        console.error("Error:", error);
    }
}