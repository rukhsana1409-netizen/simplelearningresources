document.addEventListener("DOMContentLoaded", () => {
  const container=document.querySelector(".resources .card-container");
  if(!container)return;
  const subjects=[["Math","Counting, numbers, addition, subtraction, and early math skills.","math.html"],["Reading & Language","Activities supporting letters, sounds, early reading, and language.","reading.html"],["Communication & Life Skills","Resources for communication, social understanding, routines, and independence.","communication.html"],["Science & Discovery","Explore nature, weather, living things, and scientific thinking.","science.html"],["Social Studies","Explore communities, civics, geography, and economics.","social-studies.html"],["Seasonal & Holidays","Browse timely learning activities by season and holiday.","seasonal.html"]];
  container.innerHTML=subjects.map(([title,description,href])=>`<div class="card"><h3>${title}</h3><p>${description}</p><a href="${href}">Explore &rarr;</a></div>`).join("");
});
