async function booking(id) {
    let urlPost = API_URL;
    urlPost += "/booking/";

    const firstName = document.getElementById("firstName").value;
    const lastName = document.getElementById("lastName").value;

    if (firstName === "" || lastName === "") {
        alert("Please enter both first name and last name.");
        return;
    }

    if (!confirm("Are you sure you want to book this offer?")) {
        return;
    }

    const responsePost = await fetch(urlPost, {
        method: "POST",
        headers: {
            "Content-Type": "application/json",
        },
            body: JSON.stringify({
                firstName: firstName,
                lastName: lastName,
                id: id,
            }),
    });
}
