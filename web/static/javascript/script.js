const chabotButton = document.getElementById("chatbot-button");
const chatbotBox = document.getElementById("chatbot-box");
const sendButton = document.getElementById("send-btn");
const userInput = document.getElementById("user-input");
const messages = document.getElementById("chatbot-messages");

// TOGGLE CHATBOT
chabotButton.onclick = () => {
  chatbotBox.classList.toggle("hidden");
};

// SEND MESSAGE  EVENT LISTENER
sendButton.onclick = sendMessage;
userInput.addEventListener("keypress", function (event) {
  if (event.key === "enter") sendMessage();
});

// FUNCTION SEND MESSAGE TO CHATBOT
function sendMessage() {
  const text = userInput.value.trim();
  if (!text) return;

  addMessage(text, "user-message");
  userInput.value = "";

  fetch("/chat", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ message: text }),
  })
    .then((response) => response.json())
    .then((data) => {
      addMessage(data.reply, "bot-message");
    })
    .catch(() => {
      addMessage("Terjadi kesalahan, coba lagi", "bot-message");
    });
}

// FUNCTION ADD MESSAGE || GIVE ANSWER
function addMessage(text, className) {
  if (!messages) {
    console.error("Elemen container pesan tidak ditemukan di HTML!");
    return;
  }

  const msg = document.createElement("div");
  msg.className = className;
  msg.innerText = text;
  messages.appendChild(msg);
  messages.scrollTop = messages.scrollHeight;
}
