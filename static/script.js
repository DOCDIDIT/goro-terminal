document.addEventListener("DOMContentLoaded", function () {
  const sendBtn = document.getElementById("send-button");
  const inputBox = document.getElementById("user-input");
  const chatBox = document.getElementById("chatbox");

  function appendMessage(role, text) {
    const msg = document.createElement("div");
    msg.className = "message " + role;
    msg.innerText = (role === "user" ? "💬 " : "🔥 ") + text;
    chatBox.appendChild(msg);
    chatBox.scrollTop = chatBox.scrollHeight;
  }

  function sendPrompt() {
    const prompt = inputBox.value.trim();
    if (!prompt) return;
    appendMessage("user", prompt);
    fetch("/command", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ user_input: prompt })
    })
    .then(res => res.json())
    .then(data => {
      console.log("🧠 Response from backend:", data);
      appendMessage("bot", data.response);
    })
    .catch(err => appendMessage("bot", "Internal Error: " + err.message));
    inputBox.value = "";
  }

  sendBtn.addEventListener("click", sendPrompt);
  inputBox.addEventListener("keypress", function (e) {
    if (e.key === "Enter") {
      e.preventDefault();
      sendPrompt();
    }
  });
});