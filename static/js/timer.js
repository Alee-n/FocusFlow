let totalTime = 20 * 60;
let timeLeft = totalTime;
let timerInterval = null;

function updateTimerDisplay() {

    let min = Math.floor(timeLeft / 60);
    let sec = timeLeft % 60;

    document.getElementById("timerDisplay").innerText =
        `${min}:${sec < 10 ? "0" : ""}${sec}`;

    let progress =
        597 - (597 * timeLeft / totalTime);

    document.getElementById("progressCircle")
        .style.strokeDashoffset = progress;
}

function startTimer() {

    if (timerInterval) {
        return;
    }

    timerInterval = setInterval(() => {

        if (timeLeft <= 0) {

            clearInterval(timerInterval);

            timerInterval = null;

            alert("🎉 Focus Session Complete!");

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

    timeLeft = totalTime;

    updateTimerDisplay();
}

document.addEventListener("DOMContentLoaded", () => {

    updateTimerDisplay();
});