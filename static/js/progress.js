document.addEventListener("DOMContentLoaded", () => {

    const sessions =
        document.querySelectorAll(".session");

    const progressBar =
        document.getElementById("progressBar");

    const progressText =
        document.getElementById("progressText");

    function updateProgress() {

        const checked =
            document.querySelectorAll(".session:checked").length;

        const total = sessions.length;

        const percent =
            total === 0 ? 0 : Math.round((checked / total) * 100);

        progressBar.style.width = percent + "%";

        progressText.innerText =
            percent + "% completed";
    }

    sessions.forEach(session => {

        session.addEventListener(
            "change",
            updateProgress
        );

    });

});