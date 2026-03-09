from fpdf import FPDF

class CV(FPDF):
    def footer(self):
        self.set_y(-15)
        self.set_font("Helvetica", "I", 8)
        self.set_text_color(150, 150, 150)
        self.cell(0, 10, f"Page {self.page_no()}", align="C")


def create_cv():
    pdf = CV(format="A4")
    pdf.add_page()
    pdf.set_auto_page_break(auto=True, margin=15)

    # === HEADER ===
    pdf.set_fill_color(30, 30, 55)
    pdf.rect(0, 0, 210, 44, "F")

    pdf.set_font("Helvetica", "B", 24)
    pdf.set_text_color(255, 255, 255)
    pdf.set_xy(0, 9)
    pdf.cell(0, 10, "NGUYEN VAN MINH", align="C", new_x="LMARGIN", new_y="NEXT")

    pdf.set_font("Helvetica", "", 11)
    pdf.set_text_color(180, 180, 220)
    pdf.cell(0, 7, "Software Engineer  |  Backend Developer", align="C", new_x="LMARGIN", new_y="NEXT")

    pdf.set_font("Helvetica", "", 9)
    pdf.set_text_color(160, 160, 200)
    pdf.cell(0, 6, "minh.nguyen@email.com  |  +84 912 345 678  |  Ho Chi Minh City, VN", align="C", new_x="LMARGIN", new_y="NEXT")

    pdf.ln(6)

    # === HELPERS ===
    def section(title):
        pdf.ln(3)
        pdf.set_fill_color(99, 102, 241)
        pdf.set_text_color(255, 255, 255)
        pdf.set_font("Helvetica", "B", 10)
        pdf.cell(0, 7, f"  {title}", fill=True, new_x="LMARGIN", new_y="NEXT")
        pdf.ln(2)

    def text(t, x=14):
        pdf.set_font("Helvetica", "", 10)
        pdf.set_text_color(40, 40, 40)
        pdf.set_x(x)
        pdf.multi_cell(190 - x, 5.5, t)
        pdf.ln(1)

    def bullet(t):
        pdf.set_x(12)
        pdf.set_font("Helvetica", "", 10)
        pdf.set_text_color(99, 102, 241)
        pdf.cell(5, 5.5, "-")
        pdf.set_text_color(40, 40, 40)
        pdf.multi_cell(175, 5.5, t)

    def job(title, company, period):
        pdf.ln(1)
        pdf.set_x(10)
        pdf.set_font("Helvetica", "B", 10)
        pdf.set_text_color(20, 20, 40)
        pdf.cell(130, 6, title)
        pdf.set_font("Helvetica", "I", 9)
        pdf.set_text_color(120, 120, 130)
        pdf.cell(0, 6, period, align="R", new_x="LMARGIN", new_y="NEXT")
        pdf.set_x(10)
        pdf.set_font("Helvetica", "I", 9)
        pdf.set_text_color(99, 102, 150)
        pdf.cell(0, 5, company, new_x="LMARGIN", new_y="NEXT")
        pdf.ln(1)

    # === SUMMARY ===
    section("PROFESSIONAL SUMMARY")
    text(
        "Experienced Software Engineer with 5+ years building scalable backend systems "
        "using Java, Spring Boot, Python, and REST APIs. Strong knowledge of microservices "
        "architecture, Docker, Kubernetes, AWS cloud deployment, and relational databases "
        "(MySQL, PostgreSQL). Passionate about clean code and agile development."
    )

    # === SKILLS ===
    section("TECHNICAL SKILLS")
    skills_data = [
        ("Languages",       "Java, Python, JavaScript, SQL"),
        ("Frameworks",      "Spring Boot, FastAPI, Django, Node.js"),
        ("Databases",       "MySQL, PostgreSQL, Redis, MongoDB"),
        ("DevOps / Cloud",  "Docker, Kubernetes, AWS (EC2, S3, RDS), CI/CD, Linux"),
        ("Tools",           "Git, Jira, IntelliJ IDEA, Postman, Maven, Gradle"),
    ]
    for label, value in skills_data:
        pdf.set_x(12)
        pdf.set_font("Helvetica", "B", 9)
        pdf.set_text_color(99, 102, 180)
        pdf.cell(42, 5.5, label + ":")
        pdf.set_font("Helvetica", "", 9)
        pdf.set_text_color(40, 40, 40)
        pdf.cell(0, 5.5, value, new_x="LMARGIN", new_y="NEXT")

    # === EXPERIENCE ===
    section("WORK EXPERIENCE")

    job("Senior Backend Developer", "FPT Software - Ho Chi Minh City", "Jan 2022 - Present")
    for b in [
        "Designed and maintained microservices for an e-commerce platform handling 500k+ daily users.",
        "Built REST APIs with Spring Boot and FastAPI; improved API response time by 35%.",
        "Containerized services using Docker, orchestrated with Kubernetes on AWS EKS.",
        "Participated in agile sprints, conducted code reviews, mentored junior developers.",
    ]:
        bullet(b)

    pdf.ln(1)
    job("Backend Developer", "Viettel Digital - Hanoi", "Jul 2019 - Dec 2021")
    for b in [
        "Developed internal management system using Java Spring Boot, MySQL, Redis cache.",
        "Integrated third-party payment gateways: VNPay, MoMo, and SMS notification services.",
        "Optimized slow database queries through indexing, reducing query time by 50%.",
        "Wrote unit/integration tests achieving 85% code coverage with JUnit and Mockito.",
    ]:
        bullet(b)

    # === EDUCATION ===
    section("EDUCATION")
    job("B.Eng. Computer Science", "Ho Chi Minh City University of Technology (HCMUT)", "2015 - 2019")
    text("GPA: 3.4/4.0  |  Graduated with Distinction")

    # === CERTIFICATIONS ===
    section("CERTIFICATIONS")
    for c in [
        "AWS Certified Developer - Associate (2023)",
        "Oracle Certified Professional: Java SE 11 Developer (2021)",
    ]:
        bullet(c)

    # === PROJECTS ===
    section("PROJECTS")
    pdf.ln(1)
    pdf.set_x(10)
    pdf.set_font("Helvetica", "B", 10)
    pdf.set_text_color(20, 20, 40)
    pdf.cell(0, 6, "CV AI Service (Personal Project, 2024)", new_x="LMARGIN", new_y="NEXT")
    text(
        "Built a machine learning REST API (FastAPI + SVM + TF-IDF) to classify CVs by industry. "
        "Frontend built in React with drag-and-drop PDF upload and real-time prediction results. "
        "Technologies: Python, scikit-learn, React, Docker."
    )

    out = "d:/DU_AN/cv-ai-service/sample_cv_nguyen_van_minh.pdf"
    pdf.output(out)
    print(f"[OK] CV PDF created: {out}")


if __name__ == "__main__":
    create_cv()
