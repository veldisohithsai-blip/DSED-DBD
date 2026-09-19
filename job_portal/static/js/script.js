// SkillBridge — small progressive-enhancement script.
// Handles: filling mini match-score rings, resume dropzone feedback,
// and auto-dismissing flash messages.

document.addEventListener("DOMContentLoaded", function () {
  // ---- Fill any mini/large match rings based on their data-score attr ----
  document.querySelectorAll("[data-ring-score]").forEach(function (svg) {
    const score = parseFloat(svg.getAttribute("data-ring-score")) || 0;
    const fg = svg.querySelector(".mini-ring-fg, .ring-fg");
    if (!fg) return;
    const radius = fg.r ? fg.r.baseVal.value : 0;
    const circumference = 2 * Math.PI * radius;
    fg.style.strokeDasharray = circumference;
    fg.style.strokeDashoffset = circumference; // start empty
    // animate fill after a short delay so it's visible
    requestAnimationFrame(function () {
      setTimeout(function () {
        const offset = circumference - (score / 100) * circumference;
        fg.style.transition = "stroke-dashoffset 1s cubic-bezier(.22,.9,.35,1)";
        fg.style.strokeDashoffset = offset;
      }, 150);
    });
  });

  // ---- Resume upload dropzone ----
  const dropzone = document.getElementById("dropzone");
  const fileInput = document.getElementById("resume-file-input");
  const filenameLabel = document.getElementById("dropzone-filename");

  if (dropzone && fileInput) {
    dropzone.addEventListener("click", () => fileInput.click());

    fileInput.addEventListener("change", () => {
      if (fileInput.files.length > 0) {
        filenameLabel.textContent = "Selected: " + fileInput.files[0].name;
      }
    });

    ["dragenter", "dragover"].forEach((evt) => {
      dropzone.addEventListener(evt, (e) => {
        e.preventDefault();
        dropzone.classList.add("dragover");
      });
    });
    ["dragleave", "drop"].forEach((evt) => {
      dropzone.addEventListener(evt, (e) => {
        e.preventDefault();
        dropzone.classList.remove("dragover");
      });
    });
    dropzone.addEventListener("drop", (e) => {
      if (e.dataTransfer.files.length > 0) {
        fileInput.files = e.dataTransfer.files;
        filenameLabel.textContent = "Selected: " + e.dataTransfer.files[0].name;
      }
    });
  }

  // ---- Auto-dismiss flash messages after a few seconds ----
  document.querySelectorAll(".flash").forEach(function (el) {
    setTimeout(function () {
      el.style.transition = "opacity 0.4s ease";
      el.style.opacity = "0";
      setTimeout(() => el.remove(), 400);
    }, 5000);
  });
});
