const API_URL = window.location.hostname === "localhost"
    ? "http://localhost:8000"
    : "https://acit-4420-exam-2.vercel.app";
async function showLogs() {
    let urlPost = API_URL;
    urlPost += "/getLog/";

    const responsePost  = await fetch(urlPost);
        const db = await responsePost.json();

    const logTable = document.getElementById("logTable");
    logTable.innerHTML = "";

    db.forEach((dbLine, index) => {
        const row = logTable.insertRow();

        row.innerHTML = `
            <td>${dbLine[0]}</td>
            <td>${dbLine[1]}</td>
        `;
    });
}
