import streamlit as st
import requests
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer, PageBreak
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.lib import colors
from io import BytesIO
from datetime import datetime

API_URL = "http://127.0.0.1:9000/predict"

# Updated user database with stored info
VALID_USERS = {
    "raj": {"password": "163", "name": "raj Kumar", "rollno": "101", "section": "A"},
    "kiran": {"password": "159", "name": "kiran Singh", "rollno": "102", "section": "B"},
    "mohan": {"password": "146", "name": "mohan Rao", "rollno": "103", "section": "C"},
}

DOMAINS = ["English", "Biology", "Physics", "Chemistry", "Social"]

def login_page():
    st.title("Essay Assessment System - Login")
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")
    if st.button("Login"):
        if username in VALID_USERS and VALID_USERS[username]["password"] == password:
            st.session_state["logged_in"] = True
            st.session_state["username"] = username
            # Store user info in session
            st.session_state["name"] = VALID_USERS[username]["name"]
            st.session_state["rollno"] = VALID_USERS[username]["rollno"]
            st.session_state["section"] = VALID_USERS[username]["section"]
            st.success(f"Welcome {st.session_state['name']}! Please select your domain on the next page.")
        else:
            st.error("Invalid username or password")

def domain_page():
    st.title("Select Domain")
    st.write(f"Welcome, **{st.session_state.get('name', '')}**!")
    domain = st.selectbox("Choose the domain of your essay:", DOMAINS)
    if st.button("Continue"):
        st.session_state["selected_domain"] = domain
        st.success(f"Domain selected: {domain}. Go to the next section to assess your essay.")

def generate_misconception_reason(bio_tags, tokens):
    reasons = []
    selected_domain = st.session_state.get('selected_domain', '')
    length = min(len(bio_tags), len(tokens))
    for i in range(length):
        if bio_tags[i] == 1:
            token = tokens[i].lower()
            if token in {"is", "are", "was", "were", "has", "have"}:
                reasons.append(f"Possible subject-verb agreement issue near '{tokens[i]}'.")
            elif token in {"in", "on", "at", "by", "to"}:
                reasons.append(f"Possible preposition error near '{tokens[i]}'.")
            elif token in {"a", "an", "the"}:
                reasons.append(f"Possible article usage error near '{tokens[i]}'.")
            else:
                reasons.append(f"Error related to '{tokens[i]}'.")
    if reasons:
        return "; ".join(sorted(set(reasons)))
    else:
        return "No major misconceptions detected."

def generate_pdf_report(name, roll_no, section, domain, essay, coherence_score, vocabulary_score, grammar_score, overall, corrected_essay, explanation, cognitive_load):
    buffer = BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=letter)
    elements = []
    styles = getSampleStyleSheet()

    title_style = ParagraphStyle(
        'Title',
        parent=styles['Heading1'],
        fontSize=16,
        alignment=1,
        spaceAfter=12
    )
    heading_style = ParagraphStyle('Heading', parent=styles['Heading2'], fontSize=12, spaceAfter=6)

    elements.append(Paragraph("Essay Assessment Report", title_style))
    elements.append(Spacer(1, 0.2*inch))

    # Student info table
    student_data = [
        ['Student Name:', name],
        ['Roll Number:', roll_no],
        ['Section:', section],
        ['Domain:', domain],
        ['Date:', datetime.now().strftime("%Y-%m-%d %H:%M:%S")],
    ]
    table = Table(student_data, colWidths=[2*inch, 4*inch])
    table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (0, -1), colors.grey),
        ('TEXTCOLOR', (0, 0), (-1, -1), colors.black),
        ('FONTNAME', (0, 0), (0, -1), 'Helvetica-Bold'),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.black),
        ('BOTTOMPADDING', (0,0), (-1,-1), 6),
    ]))
    elements.append(table)
    elements.append(Spacer(1, 0.4*inch))

    # Scores
    elements.append(Paragraph("Scores", heading_style))
    scores_data = [
        ["Score Type", "Value", "Max"],
        ["Overall Score", f"{overall:.2f}", "10"],
        ["Coherence", f"{coherence_score:.2f}", "10"],
        ["Vocabulary", f"{vocabulary_score:.2f}", "10"],
        ["Grammar", f"{grammar_score:.2f}", "10"],
    ]
    scores_table = Table(scores_data, colWidths=[3*inch, 1.5*inch, 1.5*inch])
    scores_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.darkblue),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
        ('ALIGN', (1, 1), (-1, -1), 'CENTER'),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.black),
    ]))
    elements.append(scores_table)
    elements.append(Spacer(1, 0.4*inch))

    # Cognitive Load
    elements.append(Paragraph("Cognitive Load", heading_style))
    elements.append(Paragraph(f"This essay is classified as: <b>{cognitive_load.upper()}</b> to understand.", styles['Normal']))
    elements.append(Spacer(1, 0.4*inch))

    # Essays
    elements.append(Paragraph("Original Essay", heading_style))
    elements.append(Paragraph(essay.replace('\n', '<br />'), styles['Normal']))
    elements.append(Spacer(1, 0.4*inch))

    elements.append(PageBreak())

    elements.append(Paragraph("Corrected Essay", heading_style))
    elements.append(Paragraph(corrected_essay.replace('\n', '<br />'), styles['Normal']))
    elements.append(Spacer(1, 0.4*inch))

    elements.append(Paragraph("Explanation of Mistakes", heading_style))
    elements.append(Paragraph(explanation.replace('\n', '<br />'), styles['Normal']))

    doc.build(elements)
    buffer.seek(0)
    return buffer

def assessment_page():
    st.title("Essay Assessment System")

    current_domain = st.selectbox(
        "Select Domain",
        DOMAINS,
        index=DOMAINS.index(st.session_state.get('selected_domain', DOMAINS[0]))
    )
    st.session_state["selected_domain"] = current_domain

    st.write(f"**Current domain:** {current_domain}")

    essay_text = st.text_area("Paste or type your essay here:", height=200, value=st.session_state.get("essay_text", ""))
    st.session_state["essay_text"] = essay_text

    if st.button("Assess Essay"):
        if not essay_text.strip():
            st.warning("Please enter some essay text to assess.")
        else:
            with st.spinner("Assessing essay..."):
                response = requests.post(API_URL, json={"essay": essay_text, "domain": current_domain})
                if response.status_code == 200:
                    res = response.json()

                    coherence_score = res.get("coherence_score", 0.0)
                    vocabulary_score = res.get("vocabulary_score", 0.0)
                    grammar_score = res.get("grammar_score", 0.0)
                    overall = 0.3 * coherence_score + 0.3 * vocabulary_score + 0.4 * grammar_score

                    st.subheader("Scores")
                    st.write(f"Overall Score: {overall:.2f} / 10")
                    st.write(f"Coherence: {coherence_score:.2f} / 10")
                    st.write(f"Vocabulary: {vocabulary_score:.2f} / 10")
                    st.write(f"Grammar: {grammar_score:.2f} / 10")

                    st.subheader("Feedback")
                    st.success(res.get("feedback", "No feedback available."))

                    st.subheader("Corrected Essay")
                    corrected_essay = res.get("corrected_essay", "No corrected essay provided.")
                    st.markdown(corrected_essay, unsafe_allow_html=True)

                    st.subheader("Explanation of Mistakes")
                    tokens = essay_text.split()
                    bio_tags = res.get("bio_tags", [])
                    reason = generate_misconception_reason(bio_tags, tokens)
                    st.error(reason)

                    st.subheader("Error Highlights")
                    highlighted_text = ""
                    for i, token in enumerate(tokens):
                        tag = bio_tags[i] if i < len(bio_tags) else 0
                        if tag == 1:
                            highlighted_text += f"<span style='background-color: #ffd700'>{token} </span>"
                        else:
                            highlighted_text += f"{token} "
                    st.markdown(highlighted_text, unsafe_allow_html=True)

                    # Cognitive Load
                    cognitive_load = res.get("cognitive_load", "unknown")
                    st.subheader("Cognitive Load")
                    if cognitive_load == "easy":
                        st.info("This essay is easy to understand.")
                    elif cognitive_load == "medium":
                        st.warning("This essay is moderately difficult to understand.")
                    else:
                        st.error("This essay is difficult to understand.")

                    # Generate PDF Report
                    pdf_buffer = generate_pdf_report(
                        name=st.session_state.get("name", "Unknown"),
                        roll_no=st.session_state.get("rollno", "Unknown"),
                        section=st.session_state.get("section", "Unknown"),
                        domain=current_domain,
                        essay=essay_text,
                        coherence_score=coherence_score,
                        vocabulary_score=vocabulary_score,
                        grammar_score=grammar_score,
                        overall=overall,
                        corrected_essay=corrected_essay,
                        explanation=reason,
                        cognitive_load=cognitive_load
                    )

                    # Provide Download button
                    st.download_button(
                        label="📥 Download PDF Report",
                        data=pdf_buffer,
                        file_name=f"Essay_Assessment_{st.session_state.get('rollno', 'unknown')}.pdf",
                        mime="application/pdf"
                    )

                else:
                    st.error(f"Server error: {response.status_code}")

    st.markdown("---")
    if st.button("Logout"):
        st.session_state.clear()
        st.experimental_rerun()

def main():
    if "logged_in" not in st.session_state:
        st.session_state["logged_in"] = False
    if "selected_domain" not in st.session_state:
        st.session_state["selected_domain"] = None

    if not st.session_state["logged_in"]:
        login_page()
    elif st.session_state["selected_domain"] is None:
        domain_page()
    else:
        assessment_page()

if __name__ == "__main__":
    main()
