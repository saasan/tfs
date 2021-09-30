function formatDate(date) {
    let YYYY = date.getFullYear();
    let MM = (date.getMonth() + 1).toString().padStart(2, '0');
    let DD = date.getDate().toString().padStart(2, '0');
    let hh = date.getHours().toString().padStart(2, '0');
    let mm = date.getMinutes().toString().padStart(2, '0');

    return `${YYYY}-${MM}-${DD} ${hh}:${mm}`;
}

function generateToastHTML(message) {
    return `
        <div class="toast d-flex align-items-center mx-auto" role="alert" aria-live="assertive" aria-atomic="true">
            <div class="toast-body">
            ${message}
            </div>
            <button type="button" class="btn-close ms-auto me-2" data-bs-dismiss="toast" aria-label="閉じる"></button>
        </div>
    `;
}

function showToast(message) {
    const html = generateToastHTML(message);
    const toastContainer = document.getElementById('toast-container');

    toastContainer.insertAdjacentHTML('beforeend', html);

    const toast = toastContainer.lastElementChild;
    toast.addEventListener('hidden.bs.toast', () => toast.remove());
    (new bootstrap.Toast(toast)).show();
}

function copyLink(file_id) {
    const host = location.protocol + '//' + location.host;
    navigator.clipboard.writeText(`${host}/files/${file_id}`);
    showToast('コピーしました。');
}

function removeFile(file_id, file_name) {
    fetch('/api/files/' + file_id, {
        method: 'DELETE',
        cache: 'no-cache'
    })
    .then(response => {
        if (!response.ok) {
            throw new Error(`${response.status} ${response.statusText}`);
        }

        document.getElementById(file_id)?.remove();
        showToast(`${file_name} を削除しました。`);
    })
    .catch(error => {
        showToast('エラーが発生しました。\n' + error.toString());
    });
}

function confirmRemoveFile(file_id, file_name) {
    const filenameElement = document.getElementById('remove-modal-filename');
    filenameElement.textContent = file_name;

    const yesElement = document.getElementById('remove-modal-yes');
    yesElement.onclick = () => removeFile(file_id, file_name);

    const modalElement = document.getElementById('remove-modal');
    let modal = bootstrap.Modal.getInstance(modalElement);
    if (modal === null) {
        modal = new bootstrap.Modal(document.getElementById('remove-modal'));
    }
    modal.show();
}
