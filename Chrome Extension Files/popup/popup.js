// Wait for DOM to be fully loaded before executing
document.addEventListener("DOMContentLoaded", function () {
  const mainMenu = document.getElementById("mainMenu");
  const resumeForm = document.getElementById("resumeForm");
  const tailorForm = document.getElementById("tailorForm");

  if (mainMenu) {
    const resumeBuilderButton = mainMenu.querySelector("#resumeBuilderButton");
    const tailorResumeButton = mainMenu.querySelector("#tailorResumeButton");

    if (resumeBuilderButton) {
      resumeBuilderButton.addEventListener("click", () => {
        mainMenu.style.display = "none";
        if (resumeForm) resumeForm.style.display = "block";
      });
    }

    if (tailorResumeButton) {
      tailorResumeButton.addEventListener("click", () => {
        mainMenu.style.display = "none";
        if (tailorForm) tailorForm.style.display = "block";
      });
    }
  } else {
    console.error("Main menu not found!");
  }

  if (resumeForm) {
    console.log("Resume form is ready for interaction.");
  } else {
    console.error("Resume form not found!");
  }

  if (tailorForm) {
    console.log("Tailor form is ready for interaction.");
  } else {
    console.error("Tailor form not found!");
  }
});
