function initializeTailorForm() {
  const form = document.getElementById("tailorForm");

  form.addEventListener("submit", handleTailorSubmission);
}

function handleTailorSubmission(event) {
  event.preventDefault();

  const jobDescription = document.getElementById("jobDescription").value;

  // Get the stored resume data
  chrome.storage.local.get(["resumeData"], function (result) {
    if (result.resumeData) {
      const tailoredResume = tailorResumeToJob(
        result.resumeData,
        jobDescription
      );
      const latex = generateLatexResume(tailoredResume);
      downloadLatex(latex);
    } else {
      utils.showError(form, "Please create a resume first!");
    }
  });
}

function tailorResumeToJob(resumeData, jobDescription) {
  // Convert job description to lowercase for easier matching
  const jobDesc = jobDescription.toLowerCase();

  // Create a copy of the resume data to modify
  const tailored = JSON.parse(JSON.stringify(resumeData));

  // Reorder skills based on job description mentions
  tailored.skills.technical.sort((a, b) => {
    const aCount = (jobDesc.match(new RegExp(a.toLowerCase(), "g")) || [])
      .length;
    const bCount = (jobDesc.match(new RegExp(b.toLowerCase(), "g")) || [])
      .length;
    return bCount - aCount;
  });

  // Reorder experiences based on relevance
  tailored.experience.sort((a, b) => {
    const aRelevance = calculateRelevance(a, jobDesc);
    const bRelevance = calculateRelevance(b, jobDesc);
    return bRelevance - aRelevance;
  });

  // Reorder projects based on relevance
  tailored.projects.sort((a, b) => {
    const aRelevance = calculateRelevance(a, jobDesc);
    const bRelevance = calculateRelevance(b, jobDesc);
    return bRelevance - aRelevance;
  });

  return tailored;
}

function calculateRelevance(item, jobDescription) {
  let relevance = 0;
  const text = (item.description + " " + item.title).toLowerCase();

  // Split job description into keywords
  const keywords = jobDescription.split(/\W+/);

  // Count matching keywords
  keywords.forEach((keyword) => {
    if (text.includes(keyword.toLowerCase())) {
      relevance++;
    }
  });

  return relevance;
}
