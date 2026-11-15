const API_URL = window.location.hostname === "localhost"
    ? "http://localhost:8000"
    : "https://acit-4420-exam-2.vercel.app";
async function showErrors() {
    let urlPost = API_URL;
    urlPost += "/getAllErrors/";

    const responsePost  = await fetch(urlPost);
        const db = await responsePost.json();

    const dbTable = document.getElementById("errorTable");
    dbTable.innerHTML = "";

    db.forEach((dbLine, index) => {
        const row = dbTable.insertRow();

        row.innerHTML = `
            <td>${dbLine[0]}</td>
            <td>${dbLine[1]}</td>
            <td>${dbLine[2]}</td>
        `;
    });
}
