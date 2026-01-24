const API_BASE = "http://127.0.0.1:8000";

const promptInput = document.getElementById("prompt");
const generateBtn = document.getElementById("generateBtn");
const outputDiv = document.getElementById("output");

generateBtn.addEventListener("click", async () => {
  const promptText = promptInput.value.trim();

  if (!promptText) {
    outputDiv.innerText = "Please enter a prompt.";
    return;
  }

  outputDiv.innerText = "Generating…";

  try {
    // 1️⃣ Send prompt to backend
    const res = await fetch(`${API_BASE}/api/generate`, {
      method: "POST",
      headers: {
        "Content-Type": "application/json"
      },
      body: JSON.stringify({
        prompt: promptText,
        template: "insta_square"
      })
    });

    const data = await res.json();
    const jobId = data.job_id;

    outputDiv.innerText = `Job queued (ID: ${jobId}). Processing…`;

    // 2️⃣ Poll status once after 2 seconds (simple + safe)
    setTimeout(async () => {
      const statusRes = await fetch(`${API_BASE}/api/status/${jobId}`);
      const job = await statusRes.json();

      if (job.status === "done") {
        outputDiv.innerText =
          "✅ Done!\nPreview generated at:\n" +
          job.result.preview;
      } else {
        outputDiv.innerText = `Status: ${job.status}`;
      }
    }, 2000);

  } catch (err) {
    console.error(err);
    outputDiv.innerText = "❌ Error connecting to backend.";
  }
});
