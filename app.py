import os
import subprocess
import re
import tkinter as tk
from tkinter import messagebox, simpledialog, filedialog, scrolledtext
from docx import Document
from docx.enum.text import WD_PARAGRAPH_ALIGNMENT
from mistralai import Mistral

class ResumeBuilderApp:
    def __init__(self, master):
        self.master = master
        master.title("Resume Builder")
        master.geometry("600x700")

        # Resume Details Inputs
        self.create_input_fields()

        # Buttons
        self.create_buttons()

        # Global variables to store resume details
        self.resume_details = {}

    def create_input_fields(self):
        # Create scrollable frame for inputs
        self.canvas = tk.Canvas(self.master)
        self.scrollbar = tk.Scrollbar(self.master, orient="vertical", command=self.canvas.yview)
        self.scrollable_frame = tk.Frame(self.canvas)

        self.scrollable_frame.bind(
            "<Configure>",
            lambda e: self.canvas.configure(
                scrollregion=self.canvas.bbox("all")
            )
        )

        self.canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")
        self.canvas.configure(yscrollcommand=self.scrollbar.set)

        # Place canvas and scrollbar
        self.canvas.pack(side="left", fill="both", expand=True)
        self.scrollbar.pack(side="right", fill="y")

        # Input fields
        fields = [
            ("Name", "name"),
            ("Contact Number", "contact_number"),
            ("Email", "email"),
            ("LinkedIn URL", "linkedin"),
            ("GitHub URL", "github"),
            ("Summary", "summary"),
            ("Technical Skills (comma-separated)", "technical_skills"),
            ("Soft Skills (comma-separated)", "soft_skills"),
            ("Certifications (comma-separated)", "certifications"),
            ("Activities (comma-separated)", "activities"),
            ("Languages (comma-separated)", "languages")
        ]

        self.entry_vars = {}
        for i, (label_text, key) in enumerate(fields):
            if key in ["summary"]:
                # Multiline text for summary
                label = tk.Label(self.scrollable_frame, text=label_text)
                label.grid(row=i, column=0, sticky="w", padx=10, pady=5)
                entry = tk.Text(self.scrollable_frame, height=4, width=50)
                entry.grid(row=i, column=1, padx=10, pady=5)
                self.entry_vars[key] = entry
            else:
                label = tk.Label(self.scrollable_frame, text=label_text)
                label.grid(row=i, column=0, sticky="w", padx=10, pady=5)
                entry = tk.Entry(self.scrollable_frame, width=50)
                entry.grid(row=i, column=1, padx=10, pady=5)
                self.entry_vars[key] = entry

        # Education Section
        tk.Label(self.scrollable_frame, text="Education Details", font=('Helvetica', 12, 'bold')).grid(row=len(fields), column=0, columnspan=2, pady=10)
        
        self.education_frames = []
        self.add_education_frame()

        # Add Education Button
        add_edu_btn = tk.Button(self.scrollable_frame, text="Add Another Education", command=self.add_education_frame)
        add_edu_btn.grid(row=len(fields)+2, column=0, columnspan=2, pady=10)

        # Work Experience Section
        tk.Label(self.scrollable_frame, text="Work Experience", font=('Helvetica', 12, 'bold')).grid(row=len(fields)+3, column=0, columnspan=2, pady=10)
        
        self.work_exp_frames = []
        self.add_work_experience_frame()

        # Add Work Experience Button
        add_work_btn = tk.Button(self.scrollable_frame, text="Add Another Work Experience", command=self.add_work_experience_frame)
        add_work_btn.grid(row=len(fields)+5, column=0, columnspan=2, pady=10)

        # Projects Section
        tk.Label(self.scrollable_frame, text="Projects", font=('Helvetica', 12, 'bold')).grid(row=len(fields)+6, column=0, columnspan=2, pady=10)
        
        self.project_frames = []
        self.add_project_frame()

        # Add Project Button
        add_project_btn = tk.Button(self.scrollable_frame, text="Add Another Project", command=self.add_project_frame)
        add_project_btn.grid(row=len(fields)+8, column=0, columnspan=2, pady=10)

    def add_education_frame(self):
        frame = tk.Frame(self.scrollable_frame)
        row = len(self.education_frames) + len(self.entry_vars) + 2
        frame.grid(row=row, column=0, columnspan=2, pady=5)

        tk.Label(frame, text="Course:").grid(row=0, column=0)
        course_entry = tk.Entry(frame, width=30)
        course_entry.grid(row=0, column=1)

        tk.Label(frame, text="Institution:").grid(row=1, column=0)
        institution_entry = tk.Entry(frame, width=30)
        institution_entry.grid(row=1, column=1)

        tk.Label(frame, text="Marks (%):").grid(row=2, column=0)
        marks_entry = tk.Entry(frame, width=30)
        marks_entry.grid(row=2, column=1)

        tk.Label(frame, text="Duration:").grid(row=3, column=0)
        duration_entry = tk.Entry(frame, width=30)
        duration_entry.grid(row=3, column=1)

        self.education_frames.append({
            'course': course_entry,
            'institution': institution_entry,
            'marks': marks_entry,
            'duration': duration_entry
        })

    def add_work_experience_frame(self):
        frame = tk.Frame(self.scrollable_frame)
        row = len(self.work_exp_frames) + len(self.entry_vars) + len(self.education_frames) + 5
        frame.grid(row=row, column=0, columnspan=2, pady=5)

        tk.Label(frame, text="Title:").grid(row=0, column=0)
        title_entry = tk.Entry(frame, width=30)
        title_entry.grid(row=0, column=1)

        tk.Label(frame, text="Duration:").grid(row=1, column=0)
        duration_entry = tk.Entry(frame, width=30)
        duration_entry.grid(row=1, column=1)

        tk.Label(frame, text="Descriptions (one per line):").grid(row=2, column=0)
        desc_text = tk.Text(frame, height=3, width=30)
        desc_text.grid(row=2, column=1)

        self.work_exp_frames.append({
            'title': title_entry,
            'duration': duration_entry,
            'descriptions': desc_text
        })

    def add_project_frame(self):
        frame = tk.Frame(self.scrollable_frame)
        row = len(self.project_frames) + len(self.entry_vars) + len(self.education_frames) + len(self.work_exp_frames) + 8
        frame.grid(row=row, column=0, columnspan=2, pady=5)

        tk.Label(frame, text="Project Title:").grid(row=0, column=0)
        title_entry = tk.Entry(frame, width =30)
        title_entry.grid(row=0, column=1)

        tk.Label(frame, text="Descriptions (one per line):").grid(row=1, column=0)
        desc_text = tk.Text(frame, height=3, width=30)
        desc_text.grid(row=1, column=1)

        self.project_frames.append({
            'title': title_entry,
            'descriptions': desc_text
        })

    def create_buttons(self):
        generate_resume_btn = tk.Button(self.master, text="Generate Resume", command=self.generate_resume)
        generate_resume_btn.pack(pady=10)

        tailor_resume_btn = tk.Button(self.master, text="Tailor Resume", command=self.tailor_resume)
        tailor_resume_btn.pack(pady=10)

    def generate_resume(self):
        # Collecting data from input fields
        name = self.entry_vars['name'].get()
        contact_number = self.entry_vars['contact_number'].get()
        email = self.entry_vars['email'].get()
        linkedin = self.entry_vars['linkedin'].get()
        github = self.entry_vars['github'].get()
        summary = self.entry_vars['summary'].get("1.0", tk.END).strip()
        
        education = [
            {
                'course': edu['course'].get(),
                'institution': edu['institution'].get(),
                'marks': edu['marks'].get(),
                'duration': edu['duration'].get()
            }
            for edu in self.education_frames
        ]

        work_experiences = [
            {
                'title': work['title'].get(),
                'duration': work['duration'].get(),
                'descriptions': work['descriptions'].get("1.0", tk.END).strip().splitlines()
            }
            for work in self.work_exp_frames
        ]

        projects = [
            {
                'title': proj['title'].get(),
                'descriptions': proj['descriptions'].get("1.0", tk.END).strip().splitlines()
            }
            for proj in self.project_frames
        ]

        technical_skills = self.entry_vars['technical_skills'].get()
        soft_skills = self.entry_vars['soft_skills'].get()
        certifications = self.entry_vars['certifications'].get()
        activities = self.entry_vars['activities'].get()
        languages = self.entry_vars['languages'].get()

        # Create LaTeX resume
        latex_content = self.create_latex_resume(name, contact_number, email, linkedin, github, summary,
                                                  education, work_experiences, projects, technical_skills,
                                                  soft_skills, certifications, activities, languages)

        # Compile to PDF
        self.compile_latex_to_pdf(latex_content)

    def create_latex_resume(self, name, contact_number, email, linkedin, github, summary, education, work_experiences, projects, technical_skills, soft_skills, certifications, activities, languages):
        # LaTeX preamble with UTF-8 support
        latex_preamble = r"""
\usepackage[utf8]{inputenc}
\usepackage[T1]{fontenc}
"""

        # Format work experiences and projects for LaTeX
        work_exp_latex = self.format_work_experience_latex(work_experiences)
        projects_latex = self.format_projects_latex(projects)

        # Format education as LaTeX code
        education_latex = ""
        for edu in education:
            education_latex += f"""\\item \\textbf{{{edu['course']}}}\\\\
{edu['institution']} \\hfill {edu['marks']}\\% \\\\
\\hfill {edu['duration']}
"""

        # Format skills
        technical_skills_latex = r"\begin{itemize}" + "\n" + '\n'.join([f"  \\item {skill.strip()}" for skill in technical_skills.split(",") if skill.strip()]) + "\n\\end{itemize}"
        soft_skills_latex = r"\begin{itemize}" + "\n" + '\n'.join([f"  \\item {skill.strip()}" for skill in soft_skills.split(",") if skill.strip()]) + "\n\\end{itemize}"

        # Format other sections
        certifications_latex = r"\item " + r"\item ".join(certifications.split(","))
        activities_latex = r"\item " + r"\item ".join(activities.split(","))
        languages_latex = r"\item " + r"\item ".join(languages.split(","))

        # Rest of the LaTeX template
        latex_content = r"""\documentclass[a4paper,10pt]{article}
\usepackage[left=0.6in,right=0.6in,top=0.5in,bottom=1 in]{geometry}
\usepackage{xcolor}
\usepackage{enumitem}
\usepackage[hidelinks]{hyperref}
\usepackage{titlesec}
""" + latex_preamble + r"""
% Define custom colors
\definecolor{darkblue}{RGB}{26,13,171}
\setlength{\parindent}{0pt}

% Set section formatting
\titleformat{\section}{\large\bfseries\color{darkblue}}{}{0em}{}[\titlerule]

% Set hyperlink color
\hypersetup{colorlinks=true, linkcolor=darkblue, urlcolor=darkblue}

\newenvironment{myitemize}{\begin{itemize}[leftmargin=*,labelsep=0.5em,itemsep=0.5em]}{\end{itemize}}

\begin{document}

\pagestyle{empty}

\begin{center}
  \textbf{\LARGE """ + name + r"""}
\end{center}

\begin{center}
  \textbf{Mobile:} """ + contact_number + r""" \quad
  \textbf{Email:} \href{mailto:""" + email + r"""}{""" + email + r"""} \quad
  \href{""" + linkedin + r"""}{LinkedIn} \quad
  \href{""" + github + r"""}{GitHub}
\end{center}

\section*{Summary}
""" + summary + r"""

\section*{Education}
\begin{myitemize}
  """ + education_latex + r"""
\end{myitemize}

\section*{Work Experience}
\begin{itemize}
  """ + work_exp_latex + r"""
\end{itemize}

\section*{Projects}
\begin{itemize}
  """ + projects_latex + r"""
\end{itemize}

\section*{Skills}
\subsection*{Technical Skills}
""" + technical_skills_latex + r"""

\subsection*{Soft Skills}
""" + soft_skills_latex + r"""

\section*{Courses \& Certifications}
\begin{itemize}
  """ + certifications_latex + r"""
\end{itemize}

\section*{Co-curricular and Extracurricular Activities}
\begin{itemize}
  """ + activities_latex + r"""
\end{itemize}

\section*{Languages}
\begin{itemize}
  """ + languages_latex + r"""
\end{itemize}

\end{document}
"""

        return latex_content

    def compile_latex_to_pdf(self, latex_content):
        try:
            output_filename = filedialog.asksaveasfilename(defaultextension=".pdf", filetypes=[("PDF files", "*.pdf")])
            if not output_filename:
                return

            with open('resume.tex', 'w', encoding='utf-8') as f:
                f.write(latex_content)

            subprocess.run(['pdflatex', '-interaction=nonstopmode', 'resume.tex'], check=True)
            os.rename('resume.pdf', output_filename)
            messagebox.showinfo("Success", f'PDF created successfully: {output_filename}')
        except subprocess.CalledProcessError as e:
            messagebox.showerror("Error", f'Error in compiling LaTeX to PDF: {e}')
            print('Please ensure you have LaTeX and pdflatex installed on your system.')

    def tailor_resume(self):
        job_description = simpledialog.askstring("Job Description", "Enter the job description:")
        if not job_description:
            return

        try:
            with open('resume.tex', 'r', encoding='utf-8') as file:
                resume_content = file.read()

            summary_match = re.search(r'\\section\*{Summary}(.*?)\\section', resume_content, re.DOTALL)
            technical_skills_match = re.search(r'\\subsection\*{Technical Skills}(.*?)\\subsection', resume_content, re.DOTALL)
            soft_skills_match = re.search(r'\\subsection\*{Soft Skills}(.*?)\\section', resume_content, re.DOTALL)

            if summary_match and technical_skills_match and soft_skills_match:
                current_summary = summary_match.group(1).strip()
                current_technical_skills = technical_skills_match.group(1).strip()
                current_soft_skills = soft_skills_match.group(1).strip()

                api_key = os.environ.get("MISTRAL_API_KEY")
                if not api_key:
                    messagebox.showerror("Error", "MISTRAL_API_KEY not found in environment variables.")
                    return

                model = "mistral-tiny"
                client = Mistral(api_key=api_key)

                prompt = f"""
Job Description: {job_description[:3000]}

Current Resume Summary: {current_summary[:500]}

Current Resume Technical Skills: {current_technical_skills[:1000]}

Current Resume Soft Skills: {current_soft_skills[:1000]}

Please provide a short and professional tailored summary (2-3 sentences), a tailored technical skills list, and a tailored soft skills list for this resume based on the job description. Format your response as follows:

Tailored Summary:
[Your tailored summary here]

Tailored Technical Skills:
- Skill 1
- Skill 2
- Skill 3
...

Tailored Soft Skills:
- Skill 1
- Skill 2
- Skill 3
...
"""

                chat_response = client.chat.complete(
                    model=model,
                    messages=[{"role": "user", "content": prompt}]
                )

                ai_response = chat_response.choices[0].message.content
                tailored_summary = re.search(r'Tailored Summary:(.*?)Tailored Technical Skills:', ai_response, re.DOTALL)
                tailored_technical_skills = re.search(r'Tailored Technical Skills:(.*?)Tailored Soft Skills:', ai_response, re.DOTALL)
                tailored_soft_skills = re.search(r'Tailored Soft Skills:(.*)', ai_response, re.DOTALL)

                if tailored_summary and tailored_technical_skills and tailored_soft_skills:
                    tailored_summary = tailored_summary.group(1).strip()
                    tailored_technical_skills = tailored_technical_skills.group(1).strip()
                    tailored_soft_skills = tailored_soft_skills.group(1).strip()

                    # Format Technical Skills
                    tech_skills_list = re.findall(r'-\s*(.*)', tailored_technical_skills)
                    formatted_technical_skills = '\\begin{itemize}\n' + '\n'.join([f'  \\item {skill.strip()}' for skill in tech_skills_list if skill.strip()]) + '\n\\end{itemize}'

                    # Format Soft Skills
                    soft_skills_list = re.findall(r'-\s*(.*)', tailored_soft_skills)
                    formatted_soft_skills = '\\begin{itemize}\n' + '\n'.join([f'  \\item {skill.strip()}' for skill in soft_skills_list if skill.strip()]) + '\n\\end{itemize}'

                    # Replace Summary
                    resume_content = resume_content.replace(current_summary, tailored_summary)

                    # Replace Technical Skills
                    resume_content = resume_content.replace(current_technical_skills, formatted_technical_skills)

                    # Replace Soft Skills
                    resume_content = resume_content.replace(current_soft_skills, formatted_soft_skills)

                    with open('resume.tex', 'w', encoding='utf-8') as file:
                        file.write(resume_content)

                    # Compile PDF
                    self.compile_latex_to_pdf(resume_content)
                else:
                    messagebox.showerror("Error", "Error in parsing AI response. Please try again.")
            else:
                messagebox.showerror("Error", "Couldn't find Summary or Skills sections in the resume.")
        except Exception as e:
            messagebox.showerror("Error", f"Error in processing resume: {e}")

if __name__ == "__main__":
    root = tk.Tk()
    app = ResumeBuilderApp(root)
    root.mainloop()