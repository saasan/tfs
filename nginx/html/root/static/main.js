function generateTr(file) {
    return `
        <tr id="${file.id}">
            <td><a href="/files/${file.id}" class="text-decoration-none">${file.name}</a></td>
            <td>${file.human_readable_size}</td>
            <td>${formatDate(new Date(file.upload_epoch_ms))}</td>
            <td class="text-center">
                <a href="/api/files/${file.id}" target="_blank" class="btn btn-light btn-sm" title="ダウンロード" role="button">
                    <i class="bi bi-download"></i> ダウンロード
                </a>
            </td>
            <td class="text-center">
                <button type="button" class="btn btn-light btn-sm" title="リンクをコピー" onclick="copyLink('${file.id}');">
                    <i class="bi bi-clipboard"></i>
                </button>
            </td>
            <td class="text-center">
                <button type="button" class="btn-close" title="削除" aria-label="削除" onclick="confirmRemoveFile('${file.id}', '${file.name}');"></button>
            </td>
        </tr>
    `;
}

function showFileList(files) {
    const tableBody = document.getElementById('file-list-table-body');
    let tr = [];
    files.forEach(file => tr.unshift(generateTr(file)));
    tableBody.innerHTML = tr.join('');
}

function getFileList() {
    fetch('/api/files/')
        .then(response => {
            if (!response.ok) {
                throw new Error(`${response.status} ${response.statusText}`);
            }
            return response.json();
        })
        .then(data => showFileList(data))
        .catch(error => {
            showToast('エラーが発生しました。\n' + error.toString());
        });
}

function onUploadComplete(result) {
    const tableBody = document.getElementById('file-list-table-body');
    let tr = [];
    result.successful.forEach(successful => tr.unshift(generateTr(successful.response.body)));
    tableBody.insertAdjacentHTML('afterbegin', tr.join(''));
}

function onDragOver(event) {
    event.preventDefault();

    const modalElement = document.getElementById('upload-modal');
    let modal = bootstrap.Modal.getInstance(modalElement);

    if (modal === null) {
        modal = new bootstrap.Modal(document.getElementById('upload-modal'));
    }
    modal.show();
}

function onDOMContentLoaded() {
    const uppy = new Uppy.Core({
        locale: Uppy.locales.ja_JP,
        autoProceed: true
    });
    uppy.use(Uppy.Dashboard, {
        inline: true,
        target: '#drag-drop-area',
        width: '100%'
    });
    uppy.use(Uppy.XHRUpload, {
        endpoint: '/api/files/',
        formData: true,
        fieldName: 'upload_file'
    });

    uppy.on('complete', result => onUploadComplete(result));

    document.addEventListener('dragover', onDragOver);

    getFileList();
}

if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', onDOMContentLoaded);
}
else {
    onDOMContentLoaded();
}
