(function () {
  const form = document.getElementById("rental-form");
  const status = document.getElementById("form-status");
  if (!form || !status) return;

  const itemLabels = {
    "medical-grade-lift-chair": "Medical-grade lift chair",
    "electronic-medical-bed": "Electronic medical bed",
    both: "Both lift chair and bed",
    "not-sure": "Not sure — please call me",
  };

  const itemReadable = form.querySelector('input[name="rental_item"]');
  const submitBtn = form.querySelector('button[type="submit"]');

  form.setAttribute("method", "post");
  form.method = "post";

  if (/^https?:$/.test(window.location.protocol)) {
    let nextField = form.querySelector('input[name="_next"]');
    if (!nextField) {
      nextField = document.createElement("input");
      nextField.type = "hidden";
      nextField.name = "_next";
      form.appendChild(nextField);
    }
    nextField.value = window.location.href.split("#")[0].split("?")[0] + "?sent=1";
  }

  const params = new URLSearchParams(window.location.search);
  if (params.get("sent") === "1") {
    status.classList.remove("is-error");
    status.textContent =
      "Thank you. We received your request and will call you soon.";
    if (window.history && window.history.replaceState) {
      window.history.replaceState({}, "", window.location.pathname);
    }
  }

  form.addEventListener("submit", function (event) {
    event.preventDefault();
    status.classList.remove("is-error");

    const name = form.name.value.trim();
    const phone = form.phone.value.trim();
    const zip = form.zip.value.trim();
    const item = form.item.value;

    if (!name || !phone || !zip || !item) {
      status.classList.add("is-error");
      status.textContent = "Please fill in every required field so we can reach you.";
      return;
    }

    if (itemReadable) {
      itemReadable.value = itemLabels[item] || item;
    }

    if (submitBtn) {
      submitBtn.textContent = "Sending...";
    }
    status.textContent = "Sending your request...";

    HTMLFormElement.prototype.submit.call(form);
  });
})();
