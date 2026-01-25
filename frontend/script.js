// frontend/script.js
// Fully expanded, production-safe frontend logic
// Works with FastAPI backend at http://localhost:8000/generate

const API_URL = "http://localhost:8000/generate";

// DOM references
const promptInput = document.getElementById("prompt");
const generateBtn = document.getElementById("generate-btn");
const tagsContainer = document.getElementById("tags");
const imageEl = document.getElementById("image");
const statusEl = document.getElementById("status");

// Utility: update status text
function setStatus(message, isError = false) {
  statusEl.innerText = message;
  statusEl.style.color = isError ? "red" : "black";
}

// Utility: clear previous results
function clearOutput() {
  tagsContainer.innerText = "";
  imageEl.src = "";
}

// Validate prompt before sending
function isValidPrompt(text) {
  return text && text.trim().length >= 3;
}

// Main action
async function generate() {
  const prompt = promptInput.value;

  // Validation
  if (!isValidPrompt(prompt)) {
    setStatus("Please enter a meaningful prompt (at least 3 characters).", true);
    return;
  }

  clearOutput();
  setStatus("Generating… please wait");
  generateBtn.disabled = true;

  try {
    const response = await fetch(API_URL, {
      method: "POST",
      headers: {
        "Content-Type": "application/json"
      },
      body: JSON.stringify({ prompt })
    });

    if (!response.ok) {
      throw new Error(`Server error: ${response.status}`);
    }

    const data = await response.json();

    // Render tags
    if (Array.isArray(data.tags)) {
      tagsContainer.innerText = data.tags.join(", ");
    } else {
      tagsContainer.innerText = "No tags returned";
    }

    // Render image (if provided)
    if (data.image) {
      imageEl.src = data.image;
      imageEl.alt = "Generated design";
    }

    setStatus("Done");

  } catch (error) {
    console.error(error);
    setStatus("Failed to generate. Check backend or network.", true);

  } finally {
    generateBtn.disabled = false;
  }
}

// Event binding (safe after DOM load)
if (generateBtn) {
  generateBtn.addEventListener("click", generate);
}
