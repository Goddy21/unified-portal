document.addEventListener('DOMContentLoaded', () => {
  const loginForm = document.getElementById('loginForm');
  const otpModal = document.getElementById('otpModal');
  const otpForm = document.getElementById('otpForm');
  const otpMessage = document.getElementById('otpMessage');

  loginForm.addEventListener('submit', async (e) => {
    e.preventDefault();
    const formData = new FormData(loginForm);

    const response = await fetch("{% url 'login' %}", {
      method: 'POST',
      headers: {
        'X-CSRFToken': formData.get('csrfmiddlewaretoken')
      },
      body: formData
    });

    const data = await response.json();

    if (data.status === 'otp_sent') {
      otpModal.style.display = 'block';
    } else {
      alert(data.message || 'Login failed');
    }
  });

  otpForm.addEventListener('submit', async (e) => {
    e.preventDefault();
    const otpData = new FormData(otpForm);

    const response = await fetch("{% url 'verify_otp' %}", {
      method: 'POST',
      headers: {
        'X-CSRFToken': otpData.get('csrfmiddlewaretoken')
      },
      body: otpData
    });

    const data = await response.json();

    if (data.status === 'verified') {
      window.location.href = data.redirect_url || '/';
    } else {
      otpMessage.textContent = data.message || 'Invalid OTP';
    }
  });
});