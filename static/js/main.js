'use strict';
document.addEventListener('DOMContentLoaded', () => {
  document.querySelectorAll('.alert-dismissible').forEach(el => {
    setTimeout(() => { try { bootstrap.Alert.getOrCreateInstance(el).close(); } catch(e){} }, 5000);
  });
  const form = document.getElementById('tripForm');
  if (form) {
    form.addEventListener('submit', e => {
      const src = form.querySelector('[name="source"]').value.trim().toLowerCase();
      const dst = form.querySelector('[name="destination"]').value.trim().toLowerCase();
      if (src && dst && src === dst) {
        e.preventDefault();
        alert('Source and destination cannot be the same city!');
        return;
      }
      const btn = document.getElementById('submitBtn');
      if (btn) {
        btn.disabled = true;
        btn.innerHTML = '<span class="spinner-border spinner-border-sm me-2"></span>Calculating your trip...';
      }
    });
  }
  document.querySelectorAll('[data-bs-toggle="tooltip"]').forEach(el => new bootstrap.Tooltip(el));
});
