// async function loadProjects() {
//   const res = await fetch("/api/projects");
//   const projects = await res.json();

//   const tbody = document.getElementById("projectsTable");
//   tbody.innerHTML = "";

//   projects.forEach(p => {
//     const tr = document.createElement("tr");
//     tr.innerHTML = `
//       <td>${p.name}</td>
//       <td>${p.email}</td>
//       <td>${p.description}</td>
//       <td>${p.budget}</td>
//       <td>${p.deadline}</td>
//       <td>${p.status || "pending"}</td>
//       <td>
//         <button onclick="deleteProject(${p.id})">Delete</button>
//       </td>
//     `;
//     tbody.appendChild(tr);
//   });
// }

// loadProjects();
// async function deleteProject(id) {
//   const res = await fetch(`/api/projects/${id}`, { method: "DELETE" });
//   if (res.ok) {
//     alert("Deleted!");
//     loadProjects(); 
//   }
// }
