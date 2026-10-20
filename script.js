(function () {
  const form = document.getElementById("rental-form");
  const status = document.getElementById("form-status");
  if (!form || !status) return;

  const STORAGE_KEY = "dmr-rental-requests";

  function saveRequest(data) {
    let existing = [];
    try {
      existing = JSON.parse(localStorage.getItem(STORAGE_KEY) || "[]");
      if (!Array.isArray(existing)) existing = [];
    } catch (err) {
      existing = [];
    }
    existing.push(data);
    localStorage.setItem(STORAGE_KEY, JSON.stringify(existing));
  }

  form.addEventListener("submit", function (event) {
    event.preventDefault();
    status.classList.remove("is-error");
    status.textContent = "";

    const name = form.name.value.trim();
    const phone = form.phone.value.trim();
    const zip = form.zip.value.trim();
    const item = form.item.value;

    if (!name || !phone || !zip || !item) {
      status.classList.add("is-error");
      status.textContent = "Please fill in every field so we can reach you.";
      return;
    }

    const request = {
      name: name,
      phone: phone,
      zip: zip,
      item: item,
      submittedAt: new Date().toISOString(),
    };

    saveRequest(request);

    status.textContent =
      "Thank you, " +
      name +
      ". We received your request and will call you soon at " +
      phone +
      ".";
    form.reset();
  });
})();
