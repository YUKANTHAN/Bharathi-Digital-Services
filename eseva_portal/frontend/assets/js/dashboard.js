const API_BASE = "http://127.0.0.1:5000/api";
const userPhone = localStorage.getItem('userPhone');

if (!userPhone) {
    window.location.href = 'index.html';
}

// DOM Elements
const vaultGrid = document.getElementById('vault-grid');
const uploadModal = document.getElementById('upload-modal');
const openUploadBtn = document.getElementById('open-upload-btn');
const closeUploadBtn = document.getElementById('close-modal-btn');
const uploadForm = document.getElementById('upload-form');
const logoutBtn = document.getElementById('logout-btn');
const stats = {
    total: document.getElementById('total-docs'),
    pending: document.getElementById('pending-docs'),
    approved: document.getElementById('approved-docs')
};

// Initial Load
fetchDocs();

// Fetch Documents
async function fetchDocs() {
     try {
        const res = await fetch(`${API_BASE}/upload/vault?phone=${userPhone}`);
        const data = await res.json();
        
        if (data.status === 'success') {
            renderDocs(data.vault);
            updateStats(data.vault);
        }
    } catch (err) {
        console.error(err);
        vaultGrid.innerHTML = `<p class="error">Failed to load vault. Server might be down.</p>`;
    }
}

// Render Docs to UI
function renderDocs(vault) {
    if (vault.length === 0) {
        vaultGrid.innerHTML = `<div class="empty-state text-center mt-2">
            <i class="fa-solid fa-folder-open fa-3x mb-1 text-secondary opacity-20"></i>
            <p>No documents found in your vault.</p>
        </div>`;
        return;
    }

    vaultGrid.innerHTML = vault.map(doc => `
        <div class="doc-card glass">
            <div class="doc-card-header">
                <span class="status-badge ${doc.status}">${doc.status.replace('_', ' ')}</span>
                <i class="fa-solid fa-file-image blue"></i>
            </div>
            <div class="doc-main">
                <span class="doc-type">${doc.doc_type}</span>
                <span class="doc-date">${new Date(doc.submitted_at).toLocaleDateString()}</span>
            </div>
            <div class="doc-footer">
                <button class="btn-sm-secondary" onclick="viewDoc('${doc.doc_id}')">View</button>
                ${doc.status === 'approved' ? `<button class="btn-sm-primary" style="flex:1" onclick="downloadCert('${doc.doc_id}')"><i class="fa-solid fa-download"></i> Cert</button>` : ''}
                ${doc.status === 'rejected' ? `<div class="small mt-1 text-danger">Reason: ${doc.feedback || "Blurry photo"}</div>` : ''}
            </div>
        </div>
    `).join('');
}

function updateStats(vault) {
    stats.total.innerText = vault.length;
    stats.pending.innerText = vault.filter(d => d.status === 'pending_review').length;
    stats.approved.innerText = vault.filter(d => d.status === 'approved').length;
}

// Modal Handlers
openUploadBtn.addEventListener('click', () => uploadModal.classList.remove('hidden'));
closeUploadBtn.addEventListener('click', () => uploadModal.classList.add('hidden'));

// File Input Preview
const dropZone = document.getElementById('drop-zone');
const fileInput = document.getElementById('file-input');
const previewImg = document.getElementById('file-preview-img');
const placeholder = document.getElementById('upload-placeholder');

dropZone.addEventListener('click', () => fileInput.click());

fileInput.addEventListener('change', (e) => {
    const file = e.target.files[0];
    if (file) {
        const reader = new FileReader();
        reader.onload = (e) => {
            previewImg.src = e.target.result;
            previewImg.classList.remove('hidden');
            placeholder.classList.add('hidden');
        }
        reader.readAsDataURL(file);
    }
});

// Form Submission
uploadForm.addEventListener('submit', async (e) => {
    e.preventDefault();
    const docType = document.getElementById('doc-type').value;
    const file = fileInput.files[0];
    
    if (!file) return alert("Please select a document image");

    const formData = new FormData();
    formData.append('phone', userPhone);
    formData.append('doc_type', docType);
    formData.append('file', file);

    const btn = document.getElementById('submit-upload-btn');
    btn.innerHTML = "Processing...";
    btn.disabled = true;

    try {
        const res = await fetch(`${API_BASE}/upload/file`, {
            method: 'POST',
            body: formData
        });
        const data = await res.json();
        
        if (data.status === 'success') {
            alert("Upload Success! Your document is being reviewed.");
            uploadModal.classList.add('hidden');
            uploadForm.reset();
            previewImg.classList.add('hidden');
            placeholder.classList.remove('hidden');
            fetchDocs();
        } else {
            alert(`Upload Failed: ${data.message} ${data.blur_score ? `(Blur Score: ${data.blur_score.toFixed(2)})` : ''}`);
        }
    } catch (err) {
        alert("Upload Error. Please try again.");
    } finally {
        btn.innerHTML = "Upload & Review";
        btn.disabled = false;
    }
});

// Download Certificate
window.downloadCert = (docId) => {
    // In a real app, this would be a signed PDF from the server.
    // For this MVP, we generate a secure digital confirmation text.
    const certContent = `
    eSEVA PORTAL - DIGITAL VERIFICATION CERTIFICATE
    ------------------------------------------------
    Certificate ID: CERT-${docId.toUpperCase()}
    Verified For: Citizen ${userPhone}
    Document Type: ${document.querySelector('.doc-type').innerText}
    Status: VERIFIED & AUTHENTICATED
    Date of Issue: ${new Date().toLocaleString()}
    
    This is a digitally generated document. No physical signature required.
    ------------------------------------------------
    Verified by: eSeva Franchise Hub
    `;

    const blob = new Blob([certContent], { type: 'text/plain' });
    const url = window.URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = `eSeva_Certificate_${docId}.txt`;
    a.click();
};

logoutBtn.addEventListener('click', () => {
    localStorage.clear();
    window.location.href = 'index.html';
});
