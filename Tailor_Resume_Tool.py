import gradio as gr
from mistralai import Mistral
import os
import re

def generate_summary_and_skills(job_description):
    api_key = os.environ["MISTRAL_API_KEY"]
    model = "mistral-large-latest"
    client = Mistral(api_key=api_key)
    chat_response = client.chat.complete(
        model=model,
        messages=[
            {
                "role": "user",
                "content": f"Based on this job description: {job_description}, provide a short and professional summary (1-2 sentences) and a list of key skills for a resume. Format your response as follows:\nSummary: [Your summary here]\nKey Skills: [Your comma-separated list of skills here]"
            },
        ]
    )
    summary_and_skills = chat_response.choices[0].message.content
    print("Raw output from Mistral:", summary_and_skills)

    # Use regex to extract summary and skills
    summary_match = re.search(r'Summary:\s*(.*?)(?:\n|$)', summary_and_skills, re.DOTALL)
    skills_match = re.search(r'Key Skills:\s*(.*?)(?:\n|$)', summary_and_skills, re.DOTALL)

    summary = summary_match.group(1).strip() if summary_match else "Summary not found."
    skills = skills_match.group(1).strip() if skills_match else "Skills not found."

    # Format the skills as a bullet point list
    skills_list = [skill.strip() for skill in skills.split(',') if skill.strip()]
    formatted_skills = "\n".join([f"- {skill}" for skill in skills_list])

    output = f"**Summary:**\n{summary}\n\n**Key Skills:**\n{formatted_skills}"
    return output

iface = gr.Interface(
    fn=generate_summary_and_skills,
    inputs=gr.components.Textbox(label="Enter Job Description"),
    outputs=gr.components.Markdown(label="Output"),
    title="Mistral AI Resume Builder",
    description="Enter a job description and get a short and professional summary and list of key skills for your resume.",
    examples=[["Give me only skills"]],
    allow_flagging="never"
)

iface.launch()
