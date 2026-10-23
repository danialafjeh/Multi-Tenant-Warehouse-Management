/* Stockroom - small UI helpers (no framework). Backend logic lives in Django. */
document.addEventListener('DOMContentLoaded', function () {
  // Stock movement modal: show the warehouse fields that match the chosen type.
  var typeInputs = document.querySelectorAll('input[name="movement_type"]');
  var fromBox = document.getElementById('fromBox');
  var toBox = document.getElementById('toBox');
  var title = document.getElementById('movementTitle');
  var submit = document.getElementById('movementSubmit');
  var labels = {
    in:  ['Record stock in',  'Save stock in',  'btn btn-success'],
    out: ['Record stock out', 'Save stock out', 'btn btn-out'],
    transfer: ['Transfer stock', 'Save transfer', 'btn btn-move']
  };
  function apply(type) {
    if (!fromBox) return;
    fromBox.classList.toggle('d-none', type === 'in');
    toBox.classList.toggle('d-none', type === 'out');
    title.textContent = labels[type][0];
    submit.textContent = labels[type][1];
    submit.className = labels[type][2];
  }
  typeInputs.forEach(function (el) {
    el.addEventListener('change', function () { apply(el.value); });
  });
  // Buttons that open the modal with a preset type.
  document.querySelectorAll('[data-movement]').forEach(function (btn) {
    btn.addEventListener('click', function () {
      var el = document.querySelector('input[name="movement_type"][value="' + btn.dataset.movement + '"]');
      if (el) { el.checked = true; apply(btn.dataset.movement); }
    });
  });
  // Show/hide password.
  document.querySelectorAll('[data-toggle-password]').forEach(function (btn) {
    btn.addEventListener('click', function () {
      var input = document.getElementById(btn.dataset.togglePassword);
      input.type = input.type === 'password' ? 'text' : 'password';
      btn.querySelector('i').className = input.type === 'password' ? 'bi bi-eye' : 'bi bi-eye-slash';
    });
  });
});
