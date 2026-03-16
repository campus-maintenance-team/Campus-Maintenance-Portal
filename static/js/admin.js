// ---------- ADMIN AUTH ----------

async function checkAdminAccess() {

    const password = prompt("Enter admin password:");

    if (!password) {
        window.location.href = "/";
        return false;
    }

    try {
        const response = await fetch("/admin-auth", {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({ password })
        });

        if (!response.ok) {
            alert("Wrong password");
            window.location.href = "/";
            return false;
        }

        return true;

    } catch (err) {
        alert("Authentication error");
        window.location.href = "/";
        return false;
    }
}


// ---------- FETCH REPORTS ----------

async function fetchReports() {
    try {
        const response = await fetch('/api/reports');
        const data = await response.json();

        if (data.status !== 'success') {
            console.error('failed to fetch reports', data.message);
            return;
        }

        populateTable(data.reports);

    } catch (err) {
        console.error('error fetching reports', err);
    }
}


// ---------- POPULATE TABLE ----------

function populateTable(reports) {

    const tbody = document.querySelector('#reportsTable tbody');
    tbody.innerHTML = '';

    reports.forEach(r => {

        const tr = document.createElement('tr');

        tr.innerHTML = `
            <td>${r.ticket_id}</td>
            <td>${r.name}</td>
            <td>${r.block}</td>
            <td>${r.floor}</td>
            <td>${r.room_no}</td>
            <td>${r.category}</td>
            <td>${r.priority}</td>
            <td>
                <select class="status-select status-${r.status.replace(/\s/g,'').toLowerCase()}" data-ticket="${r.ticket_id}">
                    <option${r.status==='Pending'?' selected':''}>Pending</option>
                    <option${r.status==='In Progress'?' selected':''}>In Progress</option>
                    <option${r.status==='Completed'?' selected':''}>Completed</option>
                    <option${r.status==='Cancelled'?' selected':''}>Cancelled</option>
                </select>
            </td>
            <td>
                <button class="update-btn" data-ticket="${r.ticket_id}">Update</button>
                <button class="view-btn" data-ticket="${r.ticket_id}">View</button>
            </td>
        `;

        tbody.appendChild(tr);
    });

    // update buttons

    document.querySelectorAll('.update-btn').forEach(btn => {

        btn.addEventListener('click', async e => {

            const ticket = e.target.dataset.ticket;

            const select = document.querySelector(
                `.status-select[data-ticket="${ticket}"]`
            );

            const newStatus = select.value;

            await updateStatus(ticket, newStatus);

        });
    });

    // view buttons

    document.querySelectorAll('.view-btn').forEach(btn => {

        btn.addEventListener('click', async e => {

            const ticket = e.target.dataset.ticket;

            await showDetails(ticket);

        });
    });
}


// ---------- UPDATE STATUS ----------

async function updateStatus(ticketId, status) {

    try {

        const response = await fetch(`/api/reports/${ticketId}`, {

            method: 'PUT',

            headers: {
                'Content-Type': 'application/json'
            },

            body: JSON.stringify({ status })

        });

        const data = await response.json();

        if (data.status === 'success') {
            alert('Status updated');
            fetchReports();
        } 
        else {
            alert('Failed: ' + data.message);
        }

    } 
    catch (err) {

        console.error(err);
        alert('Error updating status');

    }
}


// ---------- SHOW REPORT DETAILS ----------

async function showDetails(ticketId) {

    try {

        const response = await fetch(`/api/reports/${ticketId}`);

        const data = await response.json();

        if (data.status === 'success') {

            const r = data.report;

            const detailArea = document.getElementById('detailContent');

            detailArea.innerHTML = `
            <table class="details-table">
                <tr>
                    <td class="label">Ticket ID</td>
                    <td>${r.ticket_id}</td>
                </tr>
                <tr>
                    <td class="label">Name</td>
                    <td>${r.name}</td>
                </tr>
                <tr>
                    <td class="label">Email</td>
                    <td>${r.email}</td>
                </tr>
                <tr>
                    <td class="label">Phone</td>
                    <td>${r.phone}</td>
                </tr>
                <tr>
                    <td class="label">Block</td>
                    <td>${r.block}</td>
                </tr>
                <tr>
                    <td class="label">Floor</td>
                    <td>${r.floor}</td>
                </tr>
                <tr>
                    <td class="label">Room Number</td>
                    <td>${r.room_no}</td>
                </tr>
                <tr>
                    <td class="label">Category</td>
                    <td>${r.category}</td>
                </tr>
                <tr>
                    <td class="label">Other Detail</td>
                    <td>${r.other_detail || "None"}</td>
                </tr>
                <tr>
                    <td class="label">Priority</td>
                    <td>${r.priority}</td>
                </tr>
                <tr>
                    <td class="label">Status</td>
                    <td>${r.status}</td>
                </tr>
                <tr>
                    <td class="label">Description</td>
                    <td>${r.description}</td>
                </tr>
                <tr>
                    <td class="label">Submitted At</td>
                    <td>${r.timestamp}</td>
                </tr>
                <tr>
                    <td class="label">QR Code</td>
                    <td>
                        <img src="data:image/png;base64,${r.qr_code}" class="qr-image">
                    </td>
                </tr>
            </table>
            `;

            document.getElementById('details').classList.remove('hidden');

        } 
        else {

            alert('Report not found');

        }

    } 
    catch (err) {

        console.error(err);

    }

}


// ---------- INITIAL LOAD ----------

async function initAdmin() {

    const allowed = await checkAdminAccess();

    if (allowed) {
        fetchReports();
    }

}

initAdmin();