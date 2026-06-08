const timerMinutes =
    parseInt(
        document
            .getElementById("timerData")
            .dataset
            .minutes
    );

const focusMinutes = timerMinutes;
const breakMinutes = 5;

let totalTime = focusMinutes * 60;
let timeLeft = totalTime;
let timerInterval = null;
let isBreak = false;

function playSound() {

    const audioContext =
        new (window.AudioContext ||
             window.webkitAudioContext)();

    const oscillator =
        audioContext.createOscillator();

    oscillator.type = "sine";

    oscillator.frequency.value = 880;

    oscillator.connect(
        audioContext.destination
    );

    oscillator.start();

    setTimeout(() => {

        oscillator.stop();

    }, 400);
}

function updateModeText() {

    document.getElementById("timerMode")
        .innerText =
            isBreak
                ? "☕ Break Session"
                : "🎯 Focus Session";
}

function updateCircleColor() {

    const circle =
        document.getElementById("progressCircle");

    if (isBreak) {

        circle.setAttribute(
            "stroke",
            "#4caf50"
        );

    } else {

        circle.setAttribute(
            "stroke",
            "#5c6bc0"
        );
    }
}

function updateTimerDisplay() {

    let min = Math.floor(timeLeft / 60);

    let sec = timeLeft % 60;

    document.getElementById("timerDisplay")
        .innerText =
            `${min}:${sec < 10 ? "0" : ""}${sec}`;

    let progress =
        597 - (597 * timeLeft / totalTime);

    document.getElementById("progressCircle")
        .style.strokeDashoffset =
            progress;
}

function startTimer() {

    if (timerInterval) {

        return;
    }

    timerInterval = setInterval(() => {

        if (timeLeft <= 0) {

            clearInterval(timerInterval);

            timerInterval = null;

            playSound();

            if (!isBreak) {

                alert("☕ Break Time! 5 Minutes");

                isBreak = true;

                totalTime =
                    breakMinutes * 60;

                timeLeft =
                    totalTime;

            } else {

                alert("🚀 Back To Work!");

                isBreak = false;

                totalTime =
                    focusMinutes * 60;

                timeLeft =
                    totalTime;
            }

            updateModeText();

            updateCircleColor();

            updateTimerDisplay();

            startTimer();

            return;
        }

        timeLeft--;

        updateTimerDisplay();

    }, 1000);
}

function pauseTimer() {

    clearInterval(timerInterval);

    timerInterval = null;
}

function resetTimer() {

    clearInterval(timerInterval);

    timerInterval = null;

    if (isBreak) {

        totalTime =
            breakMinutes * 60;

    } else {

        totalTime =
            focusMinutes * 60;
    }

    timeLeft = totalTime;

    updateTimerDisplay();
}

document.addEventListener(
    "DOMContentLoaded",
    () => {

        updateModeText();

        updateCircleColor();

        updateTimerDisplay();
    }
);