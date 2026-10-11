
const inspectButton = document.getElementById("inspectButton");
const repoName = document.getElementById("repoName");
const repoLink = document.getElementById("repoLink");
const status = document.getElementById("status");

inspectButton.addEventListener("click", async () => {
  inspectButton.disabled = true;
  status.textContent = "Inspecting repository...";

  try {
    const [tab] = await chrome.tabs.query({
      active: true,
      currentWindow: true
    });

    if (!tab?.url) {
      throw new Error("Could not read the current tab.");
    }

    const response = await fetch(
      "http://127.0.0.1:8000/inspect-repo",
      {
        method: "POST",
        headers: {
          "Content-Type": "application/json"
        },
        body: JSON.stringify({ url: tab.url })
      }
    );

    const result = await response.json();

    if (!response.ok) {
      throw new Error(
        result.detail || "Could not inspect this repository."
      );
    }

    repoName.textContent = `${result.owner}/${result.repo}`;
    repoLink.href = result.repository_url;
    repoLink.hidden = false;
    status.textContent = result.message;
  } catch (error) {
    status.textContent =
      error.message === "Failed to fetch"
        ? "Backend is unavailable. Start the Python server first."
        : error.message;
  } finally {
    inspectButton.disabled = false;
  }
});
