// UTCの日時文字列をJSTに変換して表示
function toJST(utcStr) {
    if (!utcStr) return "";
    const dt = new Date(utcStr + "Z");
    return dt.toLocaleString("ja-JP", { timeZone: "Asia/Tokyo" });
}

// ページ読み込み時に一覧を取得
window.onload = () => {
    fetchRecords();
};

// 台帳一覧を取得して表示
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
            <td>${toJST(record.remind_at)}</td>
            <td>${record.paid ? "完済" : "未払い"}</td>
            <td>
                <button onclick="markPaid(${record.id})">完済</button>
                <button onclick="deleteRecord(${record.id})">削除</button>
            </td>
        `;
        tbody.appendChild(tr);
    });
}

// 台帳に追加
async function addRecord() {
    const data = {
        lender:    document.getElementById("lender").value,
        borrower:  document.getElementById("borrower").value,
        amount:    Number(document.getElementById("amount").value),
        memo:      document.getElementById("memo").value,
        remind_at: document.getElementById("remind_at").value || null,
    };

    await fetch("/records", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(data),
    });

    fetchRecords();
}

// 完済マーク
async function markPaid(id) {
    await fetch(`/records/${id}/paid`, { method: "PATCH" });
    fetchRecords();
}

// 削除
async function deleteRecord(id) {
    await fetch(`/records/${id}`, { method: "DELETE" });
    fetchRecords();
}