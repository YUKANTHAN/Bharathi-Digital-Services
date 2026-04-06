const API_BASE = "http://127.0.0.1:5000/api";

// DOM Elements
const loginStep1 = document.getElementById('login-step-1');
const loginStep2 = document.getElementById('login-step-2');
const sendOtpBtn = document.getElementById('send-otp-btn');
const verifyOtpBtn = document.getElementById('verify-otp-btn');
const backToPhoneBtn = document.getElementById('back-to-phone');
const phoneInput = document.getElementById('login-phone');
const otpInput = document.getElementById('login-otp');
const displayPhone = document.getElementById('display-phone');
const roleBtns = document.querySelectorAll('.role-btn');

let currentRole = 'citizen';

// Toggle Role Selectors
roleBtns.forEach(btn => {
    btn.addEventListener('click', () => {
        roleBtns.forEach(b => b.classList.remove('active'));
        btn.classList.add('active');
        currentRole = btn.getAttribute('data-role');
    });
});

// Step 1: Send OTP
sendOtpBtn.addEventListener('click', async () => {
    const phone = phoneInput.value.trim();
    if (!phone) return alert("Please enter your phone number");

    try {
        const res = await fetch(`${API_BASE}/auth/request-otp`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ phone })
        });

        const data = await res.json();
        if (data.status === 'success') {
            displayPhone.innerText = phone;
            loginStep1.classList.add('hidden');
            loginStep2.classList.remove('hidden');
        } else {
            alert(data.message);
        }
    } catch (err) {
        console.error(err);
        alert("Server error. Make sure Python app is running!");
    }
});

// Step 2: Verify OTP
verifyOtpBtn.addEventListener('click', async () => {
    const phone = phoneInput.value.trim();
    const otp = otpInput.value.trim();

    if (!otp) return alert("Please enter the OTP");

    try {
        const res = await fetch(`${API_BASE}/auth/verify-otp`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ phone, otp, role: currentRole })
        });

        const data = await res.json();
        if (data.status === 'success') {
            // Save to LocalStorage
            localStorage.setItem('userPhone', phone);
            localStorage.setItem('userRole', currentRole);
            
            // Redirect based on role
            if (currentRole === 'franchise') {
                window.location.href = 'operator.html';
            } else {
                window.location.href = 'dashboard.html';
            }
        } else {
            alert(data.message);
        }
    } catch (err) {
        console.error(err);
        alert("Server error. Check console.");
    }
});

// Navigation
backToPhoneBtn.addEventListener('click', () => {
    loginStep2.classList.add('hidden');
    loginStep1.classList.remove('hidden');
});
