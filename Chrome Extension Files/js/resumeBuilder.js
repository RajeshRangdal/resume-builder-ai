function initializeResumeForm() {
  const form = document.getElementById("resumeForm");

  // Handle education section
  let educationCount = 1;
  document.getElementById("addEducation").addEventListener("click", () => {
    const container = document.getElementById("educationContainer");
    const newEntry = createEducationEntry(++educationCount);
    container.appendChild(newEntry);
  });

  // Handle work experience section
  let experienceCount = 1;
  document.getElementById("addExperience").addEventListener("click", () => {
    const container = document.getElementById("workExperienceContainer");
    const newEntry = createExperienceEntry(++experienceCount);
    container.appendChild(newEntry);
  });

  // Handle projects section
  let projectCount = 1;
  document.getElementById("addProject").addEventListener("click", () => {
    const container = document.getElementById("projectContainer");
    const newEntry = createProjectEntry(++projectCount);
    container.appendChild(newEntry);
  });

  // Handle form submission
  form.addEventListener("submit", handleResumeSubmission);
}

function createEducationEntry(id) {
  const div = utils.createElementWithClasses("div", "education-entry mb-4");
  div.innerHTML = `
        <div class="row">
            <div class="col-md-6 mb-3">
                <input type="text" class="form-control" name="course${id}" placeholder="Course Name" required>
            </div>
            <div class="col-md-6 mb-3">
                <input type="text" class="form-control" name="institution${id}" placeholder="Institution/University" required>
            </div>
            <div class="col-md-6 mb-3">
                <input type="number" class="form-control" name="marks${id}" placeholder="Marks (%)" required>
            </div>
            <div class="col-md-6 mb-3">
                <input type="text" class="form-control" name="duration${id}" placeholder="Duration" required>
            </div>
            <div class="col-12">
                <button type="button" class="btn btn-danger remove-entry">Remove</button>
            </div>
        </div>
    `;

  div
    .querySelector(".remove-entry")
    .addEventListener("click", () => div.remove());
  return div;
}

function createExperienceEntry(id) {
  const div = utils.createElementWithClasses(
    "div",
    "work-experience-entry mb-4"
  );
  div.innerHTML = `
        <div class="row">
            <div class="col-md-6 mb-3">
                <input type="text" class="form-control" name="title${id}" placeholder="Job Title" required>
            </div>
            <div class="col-md-6 mb-3">
                <input type="text" class="form-control" name="duration${id}" placeholder="Duration" required>
            </div>
            <div class="col-12 mb-3">
                <textarea class="form-control" name="description${id}" placeholder="Job Description" rows="3" required></textarea>
            </div>
            <div class="col-12">
                <button type="button" class="btn btn-danger remove-entry">Remove</button>
            </div>
        </div>
    `;

  div
    .querySelector(".remove-entry")
    .addEventListener("click", () => div.remove());
  return div;
}

function createProjectEntry(id) {
  const div = utils.createElementWithClasses("div", "project-entry mb-4");
  div.innerHTML = `
        <div class="row">
            <div class="col-12 mb-3">
                <input type="text" class="form-control" name="projectTitle${id}" placeholder="Project Title" required>
            </div>
            <div class="col-12 mb-3">
                <textarea class="form-control" name="projectDescription${id}" placeholder="Project Description" rows="3" required></textarea>
            </div>
            <div class="col-12">
                <button type="button" class="btn btn-danger remove-entry">Remove</button>
            </div>
        </div>
    `;

  div
    .querySelector(".remove-entry")
    .addEventListener("click", () => div.remove());
  return div;
}

function handleResumeSubmission(event) {
  event.preventDefault();

  // Collect form data
  const formData = {
    personalInfo: getPersonalInfo(),
    education: getEducationEntries(),
    experience: getExperienceEntries(),
    projects: getProjectEntries(),
    skills: getSkillsInfo(),
  };

  // Generate LaTeX resume using the template
  const latex = generateLatexResume(formData);

  // Download the LaTeX file
  downloadLatex(latex);
}

// Helper functions to collect form data
function getPersonalInfo() {
  return {
    fullName: document.getElementById("fullName").value,
    phone: document.getElementById("phone").value,
    email: document.getElementById("email").value,
    linkedin: document.getElementById("linkedin").value,
    github: document.getElementById("github").value,
    summary: document.getElementById("summary").value,
  };
}

function getEducationEntries() {
  const entries = [];
  document.querySelectorAll(".education-entry").forEach((entry, index) => {
    entries.push({
      course: entry.querySelector(`[name="course${index + 1}"]`).value,
      institution: entry.querySelector(`[name="institution${index + 1}"]`)
        .value,
      marks: entry.querySelector(`[name="marks${index + 1}"]`).value,
      duration: entry.querySelector(`[name="duration${index + 1}"]`).value,
    });
  });
  return entries;
}

function getExperienceEntries() {
  const entries = [];
  document
    .querySelectorAll(".work-experience-entry")
    .forEach((entry, index) => {
      entries.push({
        title: entry.querySelector(`[name="title${index + 1}"]`).value,
        duration: entry.querySelector(`[name="duration${index + 1}"]`).value,
        description: entry.querySelector(`[name="description${index + 1}"]`)
          .value,
      });
    });
  return entries;
}

function getProjectEntries() {
  const entries = [];
  document.querySelectorAll(".project-entry").forEach((entry, index) => {
    entries.push({
      title: entry.querySelector(`[name="projectTitle${index + 1}"]`).value,
      description: entry.querySelector(
        `[name="projectDescription${index + 1}"]`
      ).value,
    });
  });
  return entries;
}

function getSkillsInfo() {
  return {
    technical: document
      .getElementById("technicalSkills")
      .value.split(",")
      .map((s) => s.trim()),
    soft: document
      .getElementById("softSkills")
      .value.split(",")
      .map((s) => s.trim()),
    certifications: document
      .getElementById("certifications")
      .value.split(",")
      .map((s) => s.trim()),
    activities: document
      .getElementById("activities")
      .value.split(",")
      .map((s) => s.trim()),
    languages: document
      .getElementById("languages")
      .value.split(",")
      .map((s) => s.trim()),
  };
}

function downloadLatex(latex) {
  const blob = new Blob([latex], { type: "text/plain" });
  const url = URL.createObjectURL(blob);
  const a = document.createElement("a");
  a.href = url;
  a.download = "resume.tex";
  document.body.appendChild(a);
  a.click();
  document.body.removeChild(a);
  URL.revokeObjectURL(url);
}
