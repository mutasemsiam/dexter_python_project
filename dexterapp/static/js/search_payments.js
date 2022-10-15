
const searchField = document.querySelector("#searchField");

const tableOutput = document.querySelector(".table-output");
const appTable = document.querySelector(".app-table");
tableOutput.style.display = "none";
const noResults = document.querySelector(".no-results");
const tbody = document.querySelector(".table-body");
searchField.addEventListener("keyup", (e) => {
    const searchValue = e.target.value;

    if (searchValue.trim().length > 0) {
    tbody.innerHTML = "";
    fetch("/search-payments", {
        body: JSON.stringify({ searchText: searchValue }),
        method: "POST",
    })
    .then((res) => res.json())
    .then((data) => {
        console.log("data", data);
        appTable.style.display = "none";
        tableOutput.style.display = "block";

        console.log("data.length", data.length);
        if (data.length === 0) {
            noResults.style.display = "block";
            tableOutput.style.display = "none";
        } else {
            noResults.style.display = "none";
            data.forEach((payment) => {
            tbody.innerHTML += `
            <tr>
            <td>${payment.date}</td>
            <td>${payment.amount}</td>
            <td>${payment.method}</td>
            <td>${payment.updated_at}</td>
            <td><a href="/payments/delete/${payment.id}">Delete</a> | <a href="/payments/details/${payment.id}">Details</a></td>

        
            </tr>`;
        });
    }
  });
} else {
tableOutput.style.display = "none";
appTable.style.display = "block";
}
});