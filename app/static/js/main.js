let btn = document.querySelector("#btn");
let sidebar = document.querySelector(".sidebar");
let projectReqBtn = document.querySelector("#projectReqBtn");
let loginBtn = document.querySelector("#loginBtn");
let logoutBtn = document.querySelector("#logoutBtn");
let onUsers = document.getElementById("#result");

let homeBtn = document.getElementById("#homeBtn");

btn.onclick = function () {
  sidebar.classList.toggle("active");
};

// projectReqBtn.onclick = "location.href='/request'";
// loginBtn.onclick = "location.href='/login'";


// const onlineCount = document.getElementById("online-count");

// const socket = new WebSocket("ws://127.0.0.1:8000/ws/online");

//   socket.onmessage = function (event) {
//     const data = JSON.parse(event.data);
//     onlineCount.textContent = data.online;
//   };
//     socket.onclose = function () {
//     console.log("WebSocket closed");
//   };


const ws = new WebSocket("ws://127.0.0.1:8000/ws");

ws.onmessage = function(event){
    const data = JSON.parse(event.data);
    document.getElementById("onlineCount").innerText = data.online;
};

//   // WebSocket Connection
// const socket = new WebSocket(`wss://127.0.0.1:8000//ws/online`);

// socket.onopen = function(e) {
//     console.log("WebSocket connected");
// };

// socket.onmessage = function(event) {
//     const data = JSON.parse(event.data);
//     document.getElementById('#online-count').textContent = data.online_count;
// };

// socket.onclose = function(event) {
//     console.log("WebSocket disconnected");
// };

// socket.onerror = function(error) {
//     console.error("WebSocket error:", error);
// };

// // برای تست می‌توانید هر 30 ثانیه پیام ping بفرستید
// setInterval(() => {
//     if (socket.readyState === WebSocket.OPEN) {
//         socket.send('ping');
//     }
// }, 30000);

  //  // WebSocket Connection
  //   let ws;
  //   let reconnectAttempts = 0;
  //   const maxReconnectAttempts = 5;
    
  //   function connectWebSocket() {
  //       const protocol = window.location.protocol === 'https:' ? 'wss:' : 'ws:';
  //       const wsUrl = `${protocol}//${window.location.host}/ws/online`;
        
  //       ws = new WebSocket(wsUrl);
        
  //       ws.onopen = function() {
  //           console.log('WebSocket connected');
  //           reconnectAttempts = 0;
  //       };
  //     }



// const form = document.getElementById("projectForm");

// form.addEventListener("submit", function (e) {
//   e.preventDefault();

//   const data = {
//     name: document.getElementById("name").value,
//     email: document.getElementById("email").value,
//     description: document.getElementById("description").value,
//     budget: document.getElementById("budget").value,
//     deadline: document.getElementById("deadline").value
//   };

//   fetch("/api/projects", {
//     method: "POST",
//     headers: {
//       "Content-Type": "application/json"
//     },
//     body: JSON.stringify(data)
//   })
//   .then(res => res.json())
//   .then(result => {
//     console.log("Saved:", result);
//     alert("Project saved!");
//     form.reset();
//   })
//   .catch(err => {
//     console.error(err);
//   });
// });

// const sidebar = document.getElementById("sidebar");
// const openBtn = document.getElementById("openSidebar");
// const closeBtn = document.getElementById("closeSidebar");

// openBtn.addEventListener("click", () => {
//   sidebar.classList.add("active");
// });

// closeBtn.addEventListener("click", () => {
//   sidebar.classList.remove("active");
// });

// console.log(document.getElementById("openSidebar"));
// console.log(document.getElementById("sidebar"));
