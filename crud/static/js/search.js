document.addEventListener("DOMContentLoaded", function () {
    const searchInput = document.getElementById("search-input");
    const tableBody = document.getElementById("users-table-body");

    searchInput.addEventListener("input", function () {
        const query = searchInput.value;

        fetch(`/user/list/?search=${query}`, {
            method: "GET",
            headers: {
                "X-Requested-With": "XMLHttpRequest"
            }
        })
        .then(response => {
            if (!response.ok) {
                throw new Error(`HTTP error! status: ${response.status}`);
            }
            return response.json();
        })
        .then(data => {
            // Clear the table body
            tableBody.innerHTML = "";

            // Populate the table with new data
            data.users.forEach(user => {
                const row = `
                    <tr class="hover:bg-gray-100 border-b border-gray-300">
                        <td class="px-4 py-3">${user.full_name}</td>
                        <td class="px-4 py-3">${user.gender}</td>
                        <td class="px-4 py-3">${user.birth_date}</td>
                        <td class="px-4 py-3">${user.address}</td>
                        <td class="px-4 py-3">${user.contact_number}</td>
                        <td class="px-4 py-3">${user.other_phone_number}</td>
                        <td class="px-4 py-3">${user.email}</td>
                        <td class="px-4 py-3">
                            <div class="inline-flex shadow-sm">
                                <a href="/user/edit/${user.user_id}" class="bg-green-600 px-3 py-2 font-medium text-sm text-white rounded-s-sm hover:bg-green-700 hover:outline-none">Edit</a>
                                <a href="/user/delete/${user.user_id}" class="bg-red-600 px-3 py-2.5 font-medium text-sm text-white rounded-e-sm hover:bg-red-700 hover:outline-none">Delete</a>
                            </div>
                        </td>
                    </tr>
                `;
                tableBody.insertAdjacentHTML("beforeend", row);
            });
        })
        .catch(error => {
            console.error("Error fetching data:", error);
        });
    });
});