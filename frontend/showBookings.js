const API_URL = window.location.hostname === "localhost"
    ? "http://localhost:8000"
    : "https://acit-4420-exam-2.vercel.app";
async function showBooking() {
    let urlPost = API_URL;
    urlPost += "/getOffers/";

    const firstName = document.getElementById("firstName").value;
    const lastName = document.getElementById("lastName").value;

    const params = new URLSearchParams({
        firstName: firstName,
        lastName: lastName
    });
    
    if (firstName === "" || lastName === "") {
        alert("Please enter both first name and last name.");
        return;
    }
    const responsePost  = await fetch(`${urlPost}?${params}`);
    const db = await responsePost.json();

    const bookingsTable = document.getElementById("bookingsTable");
    bookingsTable.innerHTML = "";

    db.forEach((dbLine, index) => {
        const row = bookingsTable.insertRow();
        

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
            <td><button onclick="unBook(${dbLine[0]})">-</button></td>
        `;
    });
}

async function unBook(offerId) {
    let urlPost = API_URL;
    urlPost += "/unBook/";

    const firstName = document.getElementById("firstName").value;
    const lastName = document.getElementById("lastName").value;

    if (firstName === "" || lastName === "") {
        alert("Please enter both first name and last name.");
        return;
    }

    if (!confirm("Are you sure you want to cancle this offer?")) {
        return;
    }

    const responsePost = await fetch(urlPost, {
        method: "POST",
        headers: {
            "Content-Type": "application/json",
        },
            body: JSON.stringify({
                offerId: offerId,
                firstName: firstName,
                lastName: lastName,
            }),
    });

    console.log("Backend response:", responsePost.status);

    await showBooking();
    console.log("showBooking ferdig");
}
