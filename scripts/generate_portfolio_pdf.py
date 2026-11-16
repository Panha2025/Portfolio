#!/usr/bin/env python3
"""Generate the public, text-selectable Portfolio PDF from current portfolio content.

Regenerate after updating portfolio copy or photos with:
    python3 -m pip install -r scripts/requirements-pdf.txt
    python3 scripts/generate_portfolio_pdf.py

Keep the DATA entries below aligned with index.html when editing portfolio content.
"""
from __future__ import annotations

from pathlib import Path
from tempfile import TemporaryDirectory
from xml.sax.saxutils import escape

from PIL import Image as PILImage, ImageOps
from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_RIGHT
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import mm
from reportlab.platypus import (
    Flowable,
    Image,
    KeepTogether,
    PageBreak,
    Paragraph,
    SimpleDocTemplate,
    Spacer,
    Table,
    TableStyle,
)

ROOT = Path(__file__).resolve().parents[1]
OUTPUT = ROOT / "files" / "Minh_Ouddom_Panha_Portfolio.pdf"

DATA = {
    "name": "Minh Ouddom Panha",
    "role": "Founder & Web Developer - Vendora",
    "tagline": "ICT Student | Aspiring Software Engineer",
    "intro": "I'm interested in technology, software development, and entrepreneurship, and I enjoy building practical solutions for everyday needs. I founded Vendora, a Cambodian marketplace connecting buyers and sellers of new and second-hand products.",
    "interests": "Technology, software development, entrepreneurship, and practical solutions for everyday needs.",
    "vendora": "As the founder and web developer of Vendora, I work on building and improving our Cambodian online marketplace while connecting with local businesses and promoting the platform through events and partnerships.",
    "contact": {
        "email": ("minh.ouddompanha@gmail.com", "mailto:minh.ouddompanha@gmail.com"),
        "phone": ("017 523 550", "tel:017523550"),
        "github": ("github.com/Panha2025", "https://github.com/Panha2025"),
        "linkedin": ("linkedin.com", "https://www.linkedin.com/"),
        "portfolio": ("panha2025.github.io/Portfolio", "https://panha2025.github.io/Portfolio/"),
        "vendora": ("vendorakh.com", "https://vendorakh.com"),
    },
    "skills": [
        ("Programming Languages", ["HTML", "CSS", "JavaScript", "Python", "Java", "C++", "PHP"]),
        ("Frameworks & Libraries", ["React", "Laravel", "Tailwind CSS", "Node.js", "Vite", "Streamlit"]),
        ("Databases", ["PostgreSQL", "MySQL", "SQLite", "Supabase", "IndexedDB"]),
        ("Tools & Platforms", ["Git", "GitHub", "VS Code", "Figma", "Vercel", "Render", "Cloudinary", "Cloudflare", "Google Colab", "Jupyter Notebook", "Teachable Machine"]),
    ],
    "projects": [
        ("Vendora - Cambodian Online Marketplace", "A marketplace for buying and selling new and second-hand products in Cambodia.", "https://vendorakh.com", "Visit website"),
        ("Student Management System", "A web application for managing student records and information.", "https://github.com/Panha2025/Student-Management-System", "GitHub repository"),
        ("MyPlanner - Smart Schedule & Task Manager", "A smart planner for managing tasks, schedules, and reminders.", "https://github.com/Panha2025/Schedule_Tracker", "GitHub repository"),
        ("Bank Management System", "A comprehensive solution for managing banking operations and customer data.", "https://github.com/Panha2025/Bank_Management", "GitHub repository"),
        ("AI-Sign Language Translator", "A machine learning-based application for translating sign language to text and vice versa.", "https://github.com/Panha2025/AI-SignLanguage-Detector", "GitHub repository"),
        ("Movie-ChatBOT", "A real-time chatbot application for movie recommendations.", "https://github.com/Panha2025/Movies-Chatbot", "GitHub repository"),
    ],
    "internship": (
        "Technical Support Intern - Digital Government Committee",
        "Worked as a Technical Support Intern at the Digital Government Committee, assisting with the DG Super App project and supporting technical operations to help improve digital government services.",
    ),
    "volunteering": [
        ("AIESEC Cambodia", "Responsible for the Out-Going-Exchange program."),
        ("CamTESOL", "Provided technical support and facilitation services."),
        ("Digital Government Forum", "Represented the AUPP booth to showcase new technologies."),
        ("Expert Education", "Provided translation and consultation services."),
        ("AMS BridgeBlue", "Provided translation and consultation services."),
        ("ACE Graduation", "Provided support for the graduation ceremony."),
    ],
    "achievement": (
        "AI in Education Hackathon",
        "Top 3 in Best Educational Technology Innovation",
        "This competition showcased my ability to apply AI techniques to solve real-world problems in education.",
    ),
}

NAVY = colors.HexColor("#17324D")
TEAL = colors.HexColor("#1F9AA5")
CHARCOAL = colors.HexColor("#293642")
MUTED = colors.HexColor("#657482")
PALE = colors.HexColor("#E7F1F4")
RULE = colors.HexColor("#D8E1E8")
WHITE = colors.white
PAGE_W, PAGE_H = A4
LEFT = RIGHT = 17 * mm
TOP = 21 * mm
BOTTOM = 17 * mm
CONTENT_W = PAGE_W - LEFT - RIGHT

styles = getSampleStyleSheet()
styles.add(ParagraphStyle(name="Kicker", parent=styles["Normal"], fontName="Helvetica-Bold", fontSize=8, leading=10, textColor=TEAL, spaceAfter=5, tracking=1.0))
styles.add(ParagraphStyle(name="TitlePremium", parent=styles["Title"], fontName="Helvetica-Bold", fontSize=25, leading=29, textColor=NAVY, alignment=TA_LEFT, spaceAfter=5))
styles.add(ParagraphStyle(name="Role", parent=styles["Normal"], fontName="Helvetica-Bold", fontSize=11.4, leading=15, textColor=CHARCOAL, spaceAfter=2))
styles.add(ParagraphStyle(name="Tagline", parent=styles["Normal"], fontName="Helvetica", fontSize=9.4, leading=13, textColor=MUTED, spaceAfter=9))
styles.add(ParagraphStyle(name="BodyPremium", parent=styles["BodyText"], fontName="Helvetica", fontSize=9.4, leading=14, textColor=CHARCOAL, spaceAfter=6))
styles.add(ParagraphStyle(name="BodyCompact", parent=styles["BodyText"], fontName="Helvetica", fontSize=8.5, leading=11.5, textColor=CHARCOAL, spaceAfter=3))
styles.add(ParagraphStyle(name="SmallMuted", parent=styles["Normal"], fontName="Helvetica", fontSize=7.8, leading=10.4, textColor=MUTED))
styles.add(ParagraphStyle(name="SectionTitle", parent=styles["Heading2"], fontName="Helvetica-Bold", fontSize=17, leading=21, textColor=NAVY, spaceBefore=1, spaceAfter=4))
styles.add(ParagraphStyle(name="SectionSub", parent=styles["Heading3"], fontName="Helvetica-Bold", fontSize=12.2, leading=15, textColor=NAVY, spaceBefore=5, spaceAfter=5))
styles.add(ParagraphStyle(name="CardTitle", parent=styles["Normal"], fontName="Helvetica-Bold", fontSize=9.1, leading=11.5, textColor=NAVY, spaceAfter=3))
styles.add(ParagraphStyle(name="Link", parent=styles["Normal"], fontName="Helvetica-Bold", fontSize=7.8, leading=10, textColor=TEAL, spaceBefore=2))
styles.add(ParagraphStyle(name="Contact", parent=styles["Normal"], fontName="Helvetica", fontSize=8.4, leading=12, textColor=CHARCOAL))
styles.add(ParagraphStyle(name="SkillHeading", parent=styles["Normal"], fontName="Helvetica-Bold", fontSize=9.2, leading=12, textColor=NAVY, spaceAfter=4))
styles.add(ParagraphStyle(name="Caption", parent=styles["Normal"], fontName="Helvetica", fontSize=7.4, leading=9, textColor=MUTED, alignment=TA_CENTER))
styles.add(ParagraphStyle(name="Achievement", parent=styles["Normal"], fontName="Helvetica-Bold", fontSize=10.1, leading=13, textColor=NAVY, spaceAfter=4))


def P(text: str, style: str = "BodyPremium") -> Paragraph:
    return Paragraph(text, styles[style])


def plain(text: str) -> str:
    return escape(text)


def link(label: str, url: str) -> str:
    return f'<link href="{escape(url, {chr(34): "&quot;"})}" color="#{TEAL.hexval()[2:]}">{escape(label)}</link>'


def rule(space_before=1, space_after=10):
    from reportlab.platypus import HRFlowable
    return HRFlowable(width="100%", thickness=1, color=RULE, spaceBefore=space_before, spaceAfter=space_after)


def heading(kicker: str, title: str):
    return [P(plain(kicker.upper()), "Kicker"), P(plain(title), "SectionTitle"), rule()]


def cropped_image(path: str, width: float, height: float, tempdir: Path, center=(0.5, 0.5)) -> Image:
    source = ROOT / path
    with PILImage.open(source) as source_image:
        image = ImageOps.fit(source_image.convert("RGB"), (round(width * 3), round(height * 3)), method=PILImage.Resampling.LANCZOS, centering=center)
        output = tempdir / (source.stem.replace(" ", "_") + f"_{round(width)}x{round(height)}.jpg")
        image.save(output, format="JPEG", quality=94, optimize=True)
    return Image(str(output), width=width, height=height)


def contained_image(path: str, max_width: float, max_height: float) -> Image:
    image = Image(str(ROOT / path), width=max_width, height=max_height)
    image._restrictSize(max_width, max_height)
    return image


def project_cell(project):
    title, description, url, link_label = project
    return [P(plain(title), "CardTitle"), P(plain(description), "BodyCompact"), P(link(plain(link_label), url), "Link")]


def volunteer_cell(item):
    title, description = item
    return [P(plain(title), "CardTitle"), P(plain(description), "BodyCompact")]


def header_footer(canvas, doc):
    canvas.saveState()
    page = canvas.getPageNumber()
    labels = {
        1: "PROFILE",
        2: "FOUNDER EXPERIENCE & PROJECTS",
        3: "SKILLS, EXPERIENCE & COMMUNITY",
    }
    canvas.setFillColor(NAVY)
    canvas.setFont("Helvetica-Bold", 8)
    canvas.drawString(LEFT, PAGE_H - 11 * mm, "MINH OUDDOM PANHA")
    canvas.setFillColor(MUTED)
    canvas.setFont("Helvetica", 7.6)
    canvas.drawRightString(PAGE_W - RIGHT, PAGE_H - 11 * mm, labels.get(page, "PORTFOLIO"))
    canvas.setStrokeColor(TEAL)
    canvas.setLineWidth(1.2)
    canvas.line(LEFT, PAGE_H - 14 * mm, PAGE_W - RIGHT, PAGE_H - 14 * mm)
    canvas.setStrokeColor(RULE)
    canvas.setLineWidth(0.65)
    canvas.line(LEFT, 12 * mm, PAGE_W - RIGHT, 12 * mm)
    canvas.setFillColor(MUTED)
    canvas.setFont("Helvetica", 7.5)
    canvas.drawString(LEFT, 7.4 * mm, "PORTFOLIO | SOFTWARE & ENTREPRENEURSHIP")
    canvas.drawRightString(PAGE_W - RIGHT, 7.4 * mm, f"{page:02d} / 03")
    canvas.restoreState()


def build_story(tempdir: Path):
    story = []

    # PAGE 1 - Profile
    story += heading("Personal profile", "Minh Ouddom Panha")
    profile_text = [
        P(plain(DATA["role"]), "Role"),
        P(plain(DATA["tagline"]), "Tagline"),
        P(plain(DATA["intro"]), "BodyPremium"),
    ]
    portrait = cropped_image("Professional Pic.jpg", 32 * mm, 43 * mm, tempdir, center=(0.5, 0.33))
    profile = Table([[profile_text, portrait]], colWidths=[CONTENT_W - 39 * mm, 35 * mm], hAlign="LEFT")
    profile.setStyle(TableStyle([
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ("ALIGN", (1, 0), (1, 0), "RIGHT"),
        ("LEFTPADDING", (0, 0), (-1, -1), 0),
        ("RIGHTPADDING", (0, 0), (-1, -1), 0),
        ("TOPPADDING", (0, 0), (-1, -1), 0),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 0),
    ]))
    story += [profile, Spacer(1, 6 * mm)]
    story += [P("TECHNICAL INTERESTS", "Kicker"), P(plain(DATA["interests"]), "BodyPremium"), rule(2, 7)]
    story += [P("CONTACT", "Kicker")]
    contact_rows = []
    for label, key in [("EMAIL", "email"), ("PHONE", "phone"), ("GITHUB", "github"), ("LINKEDIN", "linkedin"), ("PORTFOLIO", "portfolio"), ("VENDORA", "vendora")]:
        value, url = DATA["contact"][key]
        contact_rows.append([P(plain(label), "SmallMuted"), P(link(plain(value), url), "Contact")])
    contact = Table(contact_rows, colWidths=[26 * mm, CONTENT_W - 26 * mm], hAlign="LEFT")
    contact.setStyle(TableStyle([
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ("LEFTPADDING", (0, 0), (-1, -1), 0), ("RIGHTPADDING", (0, 0), (-1, -1), 0),
        ("TOPPADDING", (0, 0), (-1, -1), 2), ("BOTTOMPADDING", (0, 0), (-1, -1), 2),
        ("LINEBELOW", (0, 0), (-1, -2), 0.35, RULE),
    ]))
    story += [contact, Spacer(1, 5 * mm), rule(2, 7), P("PROFILE AT A GLANCE", "Kicker")]
    story += [P("Founder and web developer building a Cambodian online marketplace, with interests across software development, product building, and entrepreneurship.", "BodyPremium")]

    # PAGE 2 - Founder and all six projects
    story.append(PageBreak())
    story += heading("Founder experience & featured projects", "Building Vendora")
    story += [P(plain(DATA["role"]), "Role"), P(plain(DATA["vendora"]), "BodyPremium")]
    photo_a = cropped_image("1 Vendora Booth.jpg", 36 * mm, 48 * mm, tempdir, center=(0.5, 0.48))
    photo_b = cropped_image("2 Vendora Booth.jpg", 36 * mm, 48 * mm, tempdir, center=(0.5, 0.47))
    booth = Table([
        [[photo_a, Spacer(1, 1.5 * mm), P("Vendora at a university event", "Caption")],
         [photo_b, Spacer(1, 1.5 * mm), P("Visitors exploring the booth", "Caption")]],
    ], colWidths=[CONTENT_W / 2, CONTENT_W / 2], hAlign="LEFT")
    booth.setStyle(TableStyle([
        ("ALIGN", (0, 0), (-1, -1), "CENTER"), ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ("LEFTPADDING", (0, 0), (-1, -1), 4), ("RIGHTPADDING", (0, 0), (-1, -1), 4),
        ("TOPPADDING", (0, 0), (-1, -1), 2), ("BOTTOMPADDING", (0, 0), (-1, -1), 2),
    ]))
    story += [booth, Spacer(1, 4 * mm), P("SELECTED PROJECTS", "Kicker")]
    projects = [[project_cell(DATA["projects"][i]), project_cell(DATA["projects"][i + 1])] for i in range(0, 6, 2)]
    project_table = Table(projects, colWidths=[CONTENT_W / 2, CONTENT_W / 2], hAlign="LEFT")
    project_table.setStyle(TableStyle([
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ("LEFTPADDING", (0, 0), (-1, -1), 5), ("RIGHTPADDING", (0, 0), (-1, -1), 7),
        ("TOPPADDING", (0, 0), (-1, -1), 5), ("BOTTOMPADDING", (0, 0), (-1, -1), 7),
        ("LINEBELOW", (0, 0), (-1, -2), 0.45, RULE),
        ("LINEAFTER", (0, 0), (0, -1), 0.45, RULE),
    ]))
    story.append(project_table)

    # PAGE 3 - Skills, professional experience, volunteering and award
    story.append(PageBreak())
    story += heading("Skills, experience & community", "Technical toolkit")
    skill_data = []
    for title, items in DATA["skills"]:
        skill_data.append([P(plain(title), "SkillHeading"), P(plain(", ".join(items)), "BodyCompact")])
    skills_table = Table([[skill_data[0], skill_data[1]], [skill_data[2], skill_data[3]]], colWidths=[CONTENT_W / 2, CONTENT_W / 2], hAlign="LEFT")
    skills_table.setStyle(TableStyle([
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ("LEFTPADDING", (0, 0), (-1, -1), 8), ("RIGHTPADDING", (0, 0), (-1, -1), 8),
        ("TOPPADDING", (0, 0), (-1, -1), 8), ("BOTTOMPADDING", (0, 0), (-1, -1), 9),
        ("BACKGROUND", (0, 0), (-1, -1), colors.HexColor("#F6F9FB")),
        ("LINEBEFORE", (1, 0), (1, -1), 0.55, RULE),
        ("LINEBELOW", (0, 0), (-1, 0), 0.55, RULE),
    ]))
    story += [skills_table, Spacer(1, 8 * mm), P("PROFESSIONAL EXPERIENCE", "Kicker"), P(plain(DATA["internship"][0]), "SectionSub")]
    internship_text = [P("DIGITAL GOVERNMENT COMMITTEE", "Kicker"), P(plain(DATA["internship"][1]), "BodyPremium")]
    internship_photo = cropped_image("Internship at DGC.jpg", 46 * mm, 34 * mm, tempdir, center=(0.5, 0.43))
    internship = Table([[internship_text, internship_photo]], colWidths=[CONTENT_W - 50 * mm, 46 * mm], hAlign="LEFT")
    internship.setStyle(TableStyle([
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ("LEFTPADDING", (0, 0), (-1, -1), 0), ("RIGHTPADDING", (0, 0), (-1, -1), 5),
        ("TOPPADDING", (0, 0), (-1, -1), 0), ("BOTTOMPADDING", (0, 0), (-1, -1), 0),
    ]))
    story.append(internship)

    story += [Spacer(1, 6 * mm), P("VOLUNTEERING", "Kicker")]
    volunteers = [[volunteer_cell(DATA["volunteering"][i]), volunteer_cell(DATA["volunteering"][i + 1])] for i in range(0, 6, 2)]
    volunteer_table = Table(volunteers, colWidths=[CONTENT_W / 2, CONTENT_W / 2], hAlign="LEFT")
    volunteer_table.setStyle(TableStyle([
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ("LEFTPADDING", (0, 0), (-1, -1), 8), ("RIGHTPADDING", (0, 0), (-1, -1), 8),
        ("TOPPADDING", (0, 0), (-1, -1), 8), ("BOTTOMPADDING", (0, 0), (-1, -1), 9),
        ("LINEBELOW", (0, 0), (-1, -2), 0.45, RULE),
        ("LINEAFTER", (0, 0), (0, -1), 0.45, RULE),
    ]))
    story += [volunteer_table, Spacer(1, 5 * mm), P("COMPETITION & ACHIEVEMENT", "Kicker")]
    ach_title, award, ach_desc = DATA["achievement"]
    achievement_text = [
        P(plain(ach_title), "Achievement"),
        P(plain(award), "Role"),
        P(plain(ach_desc), "BodyCompact"),
    ]
    competition_photo = cropped_image("competition.JPG", 46 * mm, 30 * mm, tempdir, center=(0.5, 0.42))
    achievement = Table([[achievement_text, competition_photo]], colWidths=[CONTENT_W - 51 * mm, 46 * mm], hAlign="LEFT")
    achievement.setStyle(TableStyle([
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ("LEFTPADDING", (0, 0), (-1, -1), 0), ("RIGHTPADDING", (0, 0), (-1, -1), 5),
        ("TOPPADDING", (0, 0), (-1, -1), 0), ("BOTTOMPADDING", (0, 0), (-1, -1), 0),
    ]))
    story.append(achievement)
    return story


def main():
    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    with TemporaryDirectory(prefix="portfolio-pdf-") as work:
        doc = SimpleDocTemplate(
            str(OUTPUT), pagesize=A4, rightMargin=RIGHT, leftMargin=LEFT,
            topMargin=TOP, bottomMargin=BOTTOM, title="Minh Ouddom Panha | Portfolio",
            author=DATA["name"], subject="Software development, Vendora, projects, skills and experience",
        )
        doc.build(build_story(Path(work)), onFirstPage=header_footer, onLaterPages=header_footer)
    print(f"Generated {OUTPUT}")


if __name__ == "__main__":
    main()
