const socket = io()

function runCode() {
  const code = document.getElementById("code input").value;
  socket.emit("run code", code)
};

socket.on('code result', (result) => {
  document.getElementById('output').textContent = result.output;
});
