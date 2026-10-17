// Progressive enhancement only; all validation remains on the server.
document.addEventListener("DOMContentLoaded", () => {
  document.querySelectorAll("[aria-describedby]").forEach(control => {
    const ids = control.getAttribute("aria-describedby").split(/\s+/).filter(id => document.getElementById(id));
    if (ids.length) control.setAttribute("aria-describedby", ids.join(" "));
    else control.removeAttribute("aria-describedby");
  });
});
// Run after fragment restoration (for example after using the skip link).
window.addEventListener("load", () => {
  const error = document.querySelector("[data-error-summary]");
  if (error) requestAnimationFrame(() => error.focus());
});
