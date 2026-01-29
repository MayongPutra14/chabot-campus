const chatBody = document.getElementById("chatBody");
const userInput = document.getElementById("userInput");
const sendBtn = document.getElementById("sendBtn");

// HELPER: ADD MESSAGE BUBBLE
function addMessage(text, sender) {
  const messageDiv = document.createElement("div");
  messageDiv.classList.add("message", sender);

  const bubbleDiv = document.createElement("div");
  bubbleDiv.classList.add("bubble");
  bubbleDiv.textContent = text;

  messageDiv.appendChild(bubbleDiv);
  chatBody.appendChild(messageDiv);

  // AUTO SCROLL
  chatBody.scrollTop = chatBody.scrollHeight;
}

async function sendMessage() {
  const message = userInput.value.trim();
  if (!message) return;

  // SHOW USER MESSAGE ON THE SCREEN
  addMessage(message, "user");
  userInput.value = "";

  try {
    const response = await fetch("api/chat", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({
        message: message,
      }),
    });

    // GET RESPONSE FROM BOT
    const dataResponse = await response.json();

    // SHOW BOT MESSAGE ON THE SCREEN
    addMessage(dataResponse.reply, "bot");
  } catch (error) {
    addMessage("Terjadi kesalaha. Silahkan coba lagi.", "bot");
    console.error(error);
  }
}

// EVENT: CLICK BUTTON
sendBtn.addEventListener("click", sendMessage); 
// EVENT: PRESS ENTER
userInput.addEventListener("keydown", function (element) {
  console.log(element.key);
  if(element.key.toLowerCase() === "enter"){
    sendMessage()
  }
})