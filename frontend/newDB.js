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
