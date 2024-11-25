import tkinter as tk
from tkinter import scrolledtext
import re
import subprocess
import requests
import os

# You'll need to replace this with your actual Mistral AI API key
MISTRAL_API_KEY = "RUFhkrSLwMn37TXnO5TbYNG3MABH3nxn"

def tailor_resume():
    # Get the job description from the text area
    job_description = text_area.get("1.0", tk.END).strip()

    # Read the LaTeX resume file
    try:
        with open(r"C:\Users\rajes\Resume_Builder\resume.tex", "r", encoding="utf-8") as file:
            resume_content = file.read()
        print("Resume file read successfully.")
    except Exception as e:
        print(f"Error reading resume file: {e}")
        result_label.config(text="Error reading resume file. Check the file path and permissions.")
        return

    print("Full resume content:")
    print(resume_content)

    # Extract current summary and skills
    summary_match = re.search(r'\\section\*{Summary}(.*?)\\section', resume_content, re.DOTALL)
    skills_match = re.search(r'\\section\*{Skills}(.*?)\\section', resume_content, re.DOTALL)

    print("Summary match:", summary_match)
    print("Skills match:", skills_match)

    if summary_match and skills_match:
        current_summary = summary_match.group(1).strip()
        current_skills = skills_match.group(1).strip()

        print("Current Summary:", current_summary)
        print("Current Skills:", current_skills)

        # Use Mistral AI to tailor the summary and skills
        prompt = f"""
        Job Description: {job_description}

        Current Resume Summary: {current_summary}

        Current Resume Skills: {current_skills}

        Please provide a short and professional tailored summary (1-2 Sentences) and skills section for this resume based on the job description. Format your response as follows:

        Tailored Summary:
        [Your tailored summary here]

        Tailored Skills:
        [Your tailored skills here]
        """

        try:
            response = requests.post(
                "https://api.mistral.ai/v1/chat/completions",
                headers={"Authorization": f"Bearer {MISTRAL_API_KEY}"},
                json={
                    "model": "mistral-tiny",
                    "messages": [{"role": "user", "content": prompt}]
                }
            )

            if response.status_code == 200:
                ai_response = response.json()['choices'][0]['message']['content']
                print("AI Response:", ai_response)

                # Extract tailored summary and skills
                tailored_summary = re.search(r'Tailored Summary:(.*?)Tailored Skills:', ai_response, re.DOTALL)
                tailored_skills = re.search(r'Tailored Skills:(.*)', ai_response, re.DOTALL)

                if tailored_summary and tailored_skills:
                    tailored_summary = tailored_summary.group(1).strip()
                    tailored_skills = tailored_skills.group(1).strip()

                    # Split the tailored skills by '-' and create formatted bullet points in LaTeX
                    skills_list = tailored_skills.split('-')
                    formatted_skills = '\\begin{itemize}\n' + '\n'.join([f'\\item {skill.strip()}' for skill in skills_list if skill.strip()]) + '\n\\end{itemize}'

                    print("Tailored Summary:", tailored_summary)
                    print("Tailored Skills:", formatted_skills)

                    # Replace the summary and skills in the resume content
                    resume_content = resume_content.replace(current_summary, tailored_summary)
                    resume_content = resume_content.replace(current_skills, formatted_skills)

                    # Write the updated content back to the file
                    with open(r"C:\Users\rajes\Resume_Builder\resume.tex", "w", encoding="utf-8") as file:
                        file.write(resume_content)

                    # Compile the LaTeX file to PDF
                    output_dir = r"C:\Users\rajes\Resume_Builder"
                    input_file = r"C:\Users\rajes\Resume_Builder\resume.tex"
                    try:
                        subprocess.check_output(["pdflatex", f"-output-directory={output_dir}", input_file])
                        result_label.config(text="Resume tailored and saved successfully!")
                    except subprocess.CalledProcessError as e:
                        print(f"Error compiling LaTeX file: {e}")
                        result_label.config(text="Error compiling LaTeX file. Please check the file for errors.")
                else:
                    result_label.config(text="Error in parsing AI response. Please try again.")
            else:
                result_label.config(text=f"Error in AI processing. Status code: {response.status_code}")
        except Exception as e:
            print(f"Error in API request: {e}")
            result_label.config(text="Error in API request. Please check your internet connection and API key.")
    else:
        result_label.config(text="Couldn't find Summary or Skills section in the resume.")

# Create the main window
window = tk.Tk()
window.title("Resume Tailor")

# Create and pack the text area for job description
text_area = scrolledtext.ScrolledText(window, width=60, height=10)
text_area.pack(pady=10)

# Create and pack the button
tailor_button = tk.Button(window, text="Tailor Resume", command=tailor_resume)
tailor_button.pack(pady=5)

# Create and pack the result label
result_label = tk.Label(window, text="")
result_label.pack(pady=5)

# Start the GUI event loop
window.mainloop()
