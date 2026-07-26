const API_URL = "http://127.0.0.1:8000";

async function callAPI(endpoint) {

    const message = document.getElementById("message").value.trim();
    const output = document.getElementById("output");

    if (message === "") {
        output.innerHTML = "⚠️ Please enter a message.";
        return;
    }

    output.innerHTML = "⏳ Processing...";

    try {

        const response = await fetch(`${API_URL}/${endpoint}`, {

            method: "POST",

            headers: {
                "Content-Type": "application/json"
            },

            body: JSON.stringify({
                text: message
            })

        });

        if (!response.ok) {

            const errorText = await response.text();

            output.innerHTML =
                "❌ Backend Error\n\n" + errorText;

            return;
        }

        const data = await response.json();

        output.innerHTML = data.result;

    }

    catch (error) {

        output.innerHTML =
            "❌ Cannot connect to backend.\n\n" +
            "Make sure FastAPI is running.";

    }

}

function analyze() {
    callAPI("analyze");
}

function improve() {
    callAPI("improve");
}

function reply() {
    callAPI("reply");
}

function sentiment() {
    callAPI("sentiment");
}