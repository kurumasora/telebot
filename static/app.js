window.onload = () => {
    fetchRecords();
};

async function fetchRecords() {
    const res = await fetch("/records");
    const records = await res.json();

    const tbody = document.getElementById("ledger-body");
    tbody.innerHTML = "";

    records.forEach(record => {
        const tr = document.createElement("tr");
        tr.innerHTML = `
            <td>${record.lender}</td>
            <td>${record.borrower}</td>
            <td>${record.amount}円</td>
            <td>${record.memo ?? ""}</td>
            <td>${record.paid ? "完済" : "未払い"}</td>
            <td>
                <button onclick="markPaid(${record.id})">完済</button>
                <button onclick="deleteRecord(${record.id})">削除</button>
            </td>
        `;
        tbody.appendChild(tr);
    });
}

async function addRecord() {
    const data = {
        lender:   document.getElementById("lender").value,
        borrower: document.getElementById("borrower").value,
        amount:   Number(document.getElementById("amount").value),
        memo:     document.getElementById("memo").value,
    };

    await fetch("/records", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(data),
    });

    fetchRecords();
}

async function markPaid(id) {
    await fetch(`/records/${id}/paid`, { method: "PATCH" });
    fetchRecords();
}

async function deleteRecord(id) {
    await fetch(`/records/${id}`, { method: "DELETE" });
    fetchRecords();
}
