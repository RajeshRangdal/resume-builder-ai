function generateLatexResume(data) {
  return `\\documentclass[11pt,a4paper]{article}

\\usepackage[empty]{fullpage}
\\usepackage{titlesec}
\\usepackage{hyperref}
\\usepackage[usenames,dvipsnames]{color}
\\usepackage{enumitem}
\\usepackage[english]{babel}
\\usepackage{tabularx}

% Adjust margins
\\addtolength{\\oddsidemargin}{-0.5in}
\\addtolength{\\evensidemargin}{-0.5in}
\\addtolength{\\textwidth}{1in}
\\addtolength{\\topmargin}{-.5in}
\\addtolength{\\textheight}{1.0in}

\\begin{document}

% Name and Contact Information
\\begin{center}
    {\\huge \\textbf{${data.personalInfo.fullName}}}\\\\[5pt]
    \\href{mailto:${data.personalInfo.email}}{${data.personalInfo.email}} $|$
    ${data.personalInfo.phone} $|$
    \\href{${data.personalInfo.linkedin}}{LinkedIn} $|$
    \\href{${data.personalInfo.github}}{GitHub}
\\end{center}

% Professional Summary
\\section*{Professional Summary}
${data.personalInfo.summary}

% Education Section
\\section*{Education}
\\begin{itemize}[leftmargin=*]
${data.education
  .map(
    (edu) => `
    \\item \\textbf{${edu.course}} \\hfill ${edu.duration}\\\\
    ${edu.institution} \\hfill ${edu.marks}\\%
`
  )
  .join("\n")}
\\end{itemize}

% Experience Section
\\section*{Work Experience}
\\begin{itemize}[leftmargin=*]
${data.experience
  .map(
    (exp) => `
    \\item \\textbf{${exp.title}} \\hfill ${exp.duration}\\\\
    ${exp.description
      .split("\n")
      .map((line) => `    ${line.trim()}`)
      .join("\\\\\n")}
`
  )
  .join("\n")}
\\end{itemize}

% Projects Section
\\section*{Projects}
\\begin{itemize}[leftmargin=*]
${data.projects
  .map(
    (proj) => `
    \\item \\textbf{${proj.title}}\\\\
    ${proj.description
      .split("\n")
      .map((line) => `    ${line.trim()}`)
      .join("\\\\\n")}
`
  )
  .join("\n")}
\\end{itemize}

% Skills Section
\\section*{Skills}
\\begin{itemize}[leftmargin=*]
    \\item \\textbf{Technical Skills:} ${data.skills.technical.join(", ")}
    \\item \\textbf{Soft Skills:} ${data.skills.soft.join(", ")}
${
  data.skills.certifications.length
    ? `    \\item \\textbf{Certifications:} ${data.skills.certifications.join(
        ", "
      )}`
    : ""
}
${
  data.skills.activities.length
    ? `    \\item \\textbf{Activities:} ${data.skills.activities.join(", ")}`
    : ""
}
${
  data.skills.languages.length
    ? `    \\item \\textbf{Languages:} ${data.skills.languages.join(", ")}`
    : ""
}
\\end{itemize}

\\end{document}`;
}

function escapeLaTeX(text) {
  return text
    .replace(/\\/g, "\\textbackslash{}")
    .replace(/[&%$#_{}]/g, "\\$&")
    .replace(/\^/g, "\\textasciicircum{}")
    .replace(/~/g, "\\textasciitilde{}");
}

// Export the function
window.generateLatexResume = generateLatexResume;
