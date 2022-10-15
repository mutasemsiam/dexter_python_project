
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
    fetch("/search-patients", {
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
            data.forEach((patient) => {
            tbody.innerHTML += `
            <tr>
            <td><a href="/patient/${patient.id}">${patient.first_name} ${patient.last_name}</a></td>
            <td>${patient.phone}</td>
            <td>${patient.national_id}</td>
            <td>${patient.date_of_birth}</td>
            <td>${patient.updated_at}</td>
            <td><a href="/patient/${patient.id}">Edit<a href="#"></a> <a href="/patients/delete/${patient.id}">Delete</a></td>
        
            </tr>`;
        });
    }
  });
} else {
tableOutput.style.display = "none";
appTable.style.display = "block";
}
});