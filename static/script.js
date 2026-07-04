const researchBtn = document.getElementById("researchBtn");
const companyInput = document.getElementById("companyInput");
const chatBox = document.getElementById("chatBox");
const pdfBtn = document.getElementById("pdfBtn");

// ----------------------
// Press Enter to Search
// ----------------------
companyInput.addEventListener("keypress", function (e) {
    if (e.key === "Enter") {
        researchBtn.click();
    }
});

// ----------------------
// Clean Website URL
// ----------------------
function cleanWebsite(url) {

    if (!url) return "Not found";

    try {

        // DuckDuckGo redirect
        if (url.includes("uddg=")) {

            const params = new URL(url).searchParams;

            url = decodeURIComponent(params.get("uddg"));

        }

        return new URL(url).hostname.replace("www.", "");

    } catch {

        return url;

    }

}

// ----------------------
// Time
// ----------------------
function getTime() {

    return new Date().toLocaleTimeString([], {
        hour: "2-digit",
        minute: "2-digit"
    });

}

// ----------------------
// Search Button
// ----------------------
researchBtn.addEventListener("click", async () => {

    const input = companyInput.value.trim();

    if (!input) return;

    // clear textbox
    companyInput.value = "";

    // disable button
    researchBtn.disabled = true;

    researchBtn.innerHTML = `
        <span class="spinner-border spinner-border-sm"></span>
        Researching...
    `;

    // user message
    chatBox.innerHTML += `

        <div class="message user shadow-sm">

            ${input}

            <div class="text-end small mt-2">
                ${getTime()}
            </div>

        </div>

    `;

    chatBox.scrollTop = chatBox.scrollHeight;

    // typing animation

    chatBox.innerHTML += `

        <div class="message ai shadow-sm" id="loadingMessage">

            <span class="spinner-border spinner-border-sm"></span>

            AI is researching the company...

        </div>

    `;

    chatBox.scrollTop = chatBox.scrollHeight;

    try {

        const response = await fetch("/research", {

            method: "POST",

            headers: {
                "Content-Type": "application/json"
            },

            body: JSON.stringify({
                company: input
            })

        });

        const data = await response.json();

        document.getElementById("loadingMessage").remove();

        const ai = data.analysis || {};

        const summary = ai.summary || "No summary available.";

        const industry = ai.industry || "Unknown";

        const keywords = ai.keywords || [];

        const products = ai.products || [];

        const pains = ai.pain_points || [];

        const competitors = data.competitors || [];

        let competitorHTML = "None";

        if (competitors.length) {

            competitorHTML = competitors.map(c =>

                `• <a href="${c.website}" target="_blank">${c.name}</a>`

            ).join("<br>");

        }

        chatBox.innerHTML += `

        <div class="message ai shadow-sm">

            <h4 class="mb-3">
                📌 ${data.company}
            </h4>

            <p>

                <b>🌐 Website</b><br>

                ${data.website ?

                `<a href="${data.website}" target="_blank">${cleanWebsite(data.website)}</a>`

                :

                "Not Found"}

            </p>

            <p>

                <b>🧠 Company Summary</b><br>

                ${summary}

            </p>

            <p>

                <b>🏭 Industry</b><br>

                ${industry}

            </p>

            <p>

                <b>🔑 Keywords</b><br>

                ${keywords.length ? keywords.join(", ") : "None"}

            </p>

            <p>

                <b>📦 Products / Services</b><br>

                ${products.length ?

                products.map(x => "• " + x).join("<br>")

                :

                "None"}

            </p>

            <p>

                <b>⚠️ AI Generated Pain Points</b><br>

                ${pains.length ?

                pains.map(x => "• " + x).join("<br>")

                :

                "None"}

            </p>

            <p>

                <b>🏢 Competitors</b><br>

                ${competitorHTML}

            </p>

            <div class="text-end text-muted small">

                ${getTime()}

            </div>

        </div>

        `;

        // show download button

        pdfBtn.classList.remove("d-none");

        pdfBtn.href = `/download-pdf/${data.company}_report.pdf`;

        // scroll

        chatBox.lastElementChild.scrollIntoView({

            behavior: "smooth"

        });

    }

    catch (err) {

        console.log(err);

        document.getElementById("loadingMessage").remove();

        chatBox.innerHTML += `

            <div class="message ai shadow-sm">

                ❌ Unable to generate report.<br><br>

                Please check your API keys or internet connection.

            </div>

        `;

    }

    finally {

        researchBtn.disabled = false;

        researchBtn.innerHTML = "🔎 Research";

    }

});