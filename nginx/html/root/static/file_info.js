function generateTableBody(file) {
    return `
        <tr>
            <td>ファイル名</td>
            <td>${file.name}</td>
        </tr>
        <tr>
            <td>サイズ</td>
            <td>${file.human_readable_size}</td>
        </tr>
        <tr>
            <td>アップロード日時</td>
            <td>${formatDate(new Date(file.upload_epoch_ms))}</td>
        </tr>
    `;
}

function generateButtons(file) {
    return `
        <a href="/api/files/${file.id}" target="_blank" class="btn btn-light" role="button">
            <i class="bi bi-download"></i> ダウンロード
        </a>

        <button type="button" class="btn btn-light" onclick="copyLink('${file.id}');">
            <i class="bi bi-clipboard"></i> リンクをコピー
        </button>

        <button type="button" class="btn btn-light" onclick="confirmRemoveFile('${file.id}', '${file.name}');">
            <i class="bi bi-x"></i> 削除
        </button>
    `;
}

function showFileInfo(file) {
    document.title = `${document.title} - ${file.name} (${file.human_readable_size})`;

    const tableBody = document.getElementById('file-info-table-body');
    tableBody.innerHTML = generateTableBody(file);

    const buttons = document.getElementById('file-info-buttons');
    buttons.innerHTML = generateButtons(file);
}

function getFileInfo() {
    if (!/^\/files\/([A-Z0-9]{26})$/.test(location.pathname)) {
        showToast('file_id がありません。');
        return;
    }

    const file_id = location.pathname.substring(location.pathname.length - 26);

    fetch(`/api/files/${file_id}/info`)
        .then(response => {
            if (!response.ok) {
                throw new Error(`${response.status} ${response.statusText}`);
            }
            return response.json();
        })
        .then(data => showFileInfo(data))
        .catch(error => {
            showToast('エラーが発生しました。\n' + error.toString());
        });
}

function onDOMContentLoaded() {
    getFileInfo();
}

if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', onDOMContentLoaded);
}
else {
    onDOMContentLoaded();
}
