function searchProduct() {
  const query = document.getElementById('searchInput').value;
  if (query.trim() !== "") {
    // yaha direct search.html page open hoga
    window.location.href = "search.html?q=" + encodeURIComponent(query);
  } else {
    alert("⚠️ Please enter a product to search.");
  }
}



console.log("JavaScript connected successfully!");

document.addEventListener("DOMContentLoaded", function () {
    alert("JS working on ElectroHub homepage");
});
