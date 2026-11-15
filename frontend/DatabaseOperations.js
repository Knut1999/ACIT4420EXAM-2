const API_URL = window.location.hostname === "localhost"
    ? "http://localhost:8000"
    : "https://acit-4420-exam-2.vercel.app";
async function newDatabase() {
    let urlPost = API_URL;
    urlPost += "/newDatabase/";

    const responsePost  = await fetch(urlPost, {
        method: "POST",
    });


    const data = await responsePost.json();
    alert(data.message);
}

async function emptyErrors() {
    await fetch(API_URL + "/deleteErrors", { method: "DELETE" });
    alert("Errors emptied");
}

async function emptyLogs() {
    await fetch(API_URL + "/deleteLog", { method: "DELETE" });
    alert("Logs emptied");
}

async function emptyBookings() {
    await fetch(API_URL + "/deleteBookings", { method: "DELETE" });
    alert("Bookings emptied");
}