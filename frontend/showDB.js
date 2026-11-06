const API_URL = window.location.hostname === "localhost"
    ? "http://localhost:8000"
    : "https://acit-4420-exam-2.vercel.app";
async function showDB() {
    let urlPost = API_URL;
    urlPost += "/getDB/";

    const responsePost  = await fetch(urlPost);
        const db = await responsePost.json();

    const dbTable = document.getElementById("dbTable");
    dbTable.innerHTML = "";

    db.forEach((dbLine, index) => {
        const row = dbTable.insertRow();

        row.innerHTML = `
            <td>${dbLine[0]}</td>
            <td>${dbLine[1]}</td>
            <td>${dbLine[2]}</td>
            <td>${dbLine[3]}</td>
            <td>${dbLine[4]}</td>
            <td>${dbLine[5]}</td>
            <td>${dbLine[6]}</td>
            <td>${dbLine[7]}</td>
            <td>${dbLine[8]}</td>
            <td>${dbLine[9]}</td>
            <td>${dbLine[10]}</td>
            <td>${dbLine[11]}</td>
            <td>${dbLine[12]}</td>
            <td>${dbLine[13]}</td>
            <td>${dbLine[14]}</td>
        `;
    });
}
