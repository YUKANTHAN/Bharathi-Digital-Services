const API_BASE = "http://127.0.0.1:5000/api";
const userPhone = localStorage.getItem('userPhone');
const userRole = localStorage.getItem('userRole');

if (!userPhone || userRole !== 'franchise') {
    window.location.href = 'index.html';
}

// DOM Elements
const reviewList = document.getElementById('review-list');
const reviewModal = document.getElementById('review-modal');
const closeReviewBtn = document.getElementById('close-modal-btn');
const logoutBtn = document.getElementById('logout-btn');
const pendingCount = document.getElementById('pending-count');

let pendingDocs = [];
let currentDocId = null;

// Initial Load
fetchReviews();

// Fetch Reviews
async function fetchReviews() {
     try {
        const res = await fetch(`${API_BASE}/franchise/dashboard?franchise_id=franchise_001`);
        const data = await res.json();
        
        if (data.status === 'success') {
            pendingDocs = data.pending_docs;
            renderReviews(data.pending_docs);
            pendingCount.innerText = data.pending_docs.length;
        }
    } catch (err) {
        console.error(err);
        reviewList.innerHTML = `<p class="error">Failed to load verification queue.</p>`;
    }
}

// Render Reviews to UI
function renderReviews(docs) {
    if (docs.length === 0) {
        reviewList.innerHTML = `<div class="empty-state text-center mt-2">
            <i class="fa-solid fa-square-check fa-3x mb-1 text-secondary opacity-20"></i>
            <p>Queue Clear! No pending reviews found.</p>
        </div>`;
        return;
    }

    reviewList.innerHTML = docs.map(doc => `
        <div class="doc-card glass">
            <div class="doc-card-header">
                <span class="status-badge pending_review">Review Required</span>
            </div>
            <div class="doc-main">
                <span class="doc-type">${doc.doc_type}</span>
                <span class="doc-date">Submitted by ${doc.user_name || doc.user_phone}</span>
            </div>
            <div class="doc-footer">
                <button class="main-btn btn-sm-primary" onclick="openReview('${doc.doc_id}')">Review Doc</button>
            </div>
        </div>
    `).join('');
}

// Review Modal Handlers
window.openReview = (docId) => {
    const doc = pendingDocs.find(d => d.doc_id === docId);
    if (!doc) return;

    currentDocId = docId;
    document.getElementById('review-doc-img').src = `file://${doc.file_url}`; // For local preview during development
    document.getElementById('review-user').innerText = doc.user_name || doc.user_phone;
    document.getElementById('review-type').innerText = doc.doc_type;
    document.getElementById('review-date').innerText = new Date(doc.submitted_at).toLocaleString();
    document.getElementById('review-feedback').value = "";
    
    reviewModal.classList.remove('hidden');
}

closeReviewBtn.addEventListener('click', () => reviewModal.classList.add('hidden'));

// Action Handlers
const submitAction = async (action) => {
    const feedback = document.getElementById('review-feedback').value;

    const btn = action === 'approved' ? document.getElementById('approve-btn') : document.getElementById('reject-btn');
    btn.innerHTML = "Processing...";
    btn.disabled = true;

    try {
        const res = await fetch(`${API_BASE}/franchise/action`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ 
                doc_id: currentDocId, 
                action, 
                feedback: feedback || `Document ${action}` 
            })
        });

        const data = await res.json();
        if (data.status === 'success') {
            alert(`Document ${action} successfully!`);
            reviewModal.classList.add('hidden');
            fetchReviews();
        } else {
            alert("Action Failed: " + data.message);
        }
    } catch (err) {
        alert("Server Error. Please try again.");
    } finally {
        btn.innerHTML = action === 'approved' ? "Approve & Verify" : "Reject Document";
        btn.disabled = false;
    }
};

document.getElementById('approve-btn').addEventListener('click', () => submitAction('approved'));
document.getElementById('reject-btn').addEventListener('click', () => submitAction('rejected'));

logoutBtn.addEventListener('click', () => {
    localStorage.clear();
    window.location.href = 'index.html';
});
