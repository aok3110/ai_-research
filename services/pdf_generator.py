from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.pagesizes import A4
import os


def generate_pdf(company, website, analysis, competitors):

    # Create reports folder if it doesn't exist
    os.makedirs("reports", exist_ok=True)

    file_path = f"reports/{company}_report.pdf"

    doc = SimpleDocTemplate(file_path, pagesize=A4)
    styles = getSampleStyleSheet()

    content = []

    # ==========================
    # Title
    # ==========================
    content.append(
        Paragraph(f"<b>AI Company Research Report</b>", styles["Title"])
    )
    content.append(Spacer(1, 15))

    # ==========================
    # Company Information
    # ==========================
    content.append(
        Paragraph(f"<b>Company:</b> {company}", styles["Heading2"])
    )

    content.append(
        Paragraph(
            f"<b>Website:</b> {website if website else 'Not Found'}",
            styles["Normal"]
        )
    )

    content.append(Spacer(1, 12))

    # ==========================
    # Summary
    # ==========================
    content.append(
        Paragraph("<b>Company Summary</b>", styles["Heading2"])
    )

    content.append(
        Paragraph(analysis.get("summary", "N/A"), styles["Normal"])
    )

    content.append(Spacer(1, 12))

    # ==========================
    # Industry
    # ==========================
    content.append(
        Paragraph("<b>Industry</b>", styles["Heading2"])
    )

    content.append(
        Paragraph(analysis.get("industry", "Unknown"), styles["Normal"])
    )

    content.append(Spacer(1, 12))

    # ==========================
    # Keywords
    # ==========================
    content.append(
        Paragraph("<b>Keywords</b>", styles["Heading2"])
    )

    keywords = analysis.get("keywords", [])

    if keywords:
        for k in keywords:
            content.append(
                Paragraph(f"• {k}", styles["Normal"])
            )
    else:
        content.append(
            Paragraph("No keywords found.", styles["Normal"])
        )

    content.append(Spacer(1, 12))

    # ==========================
    # Products
    # ==========================
    content.append(
        Paragraph("<b>Products / Services</b>", styles["Heading2"])
    )

    products = analysis.get("products", [])

    if products:
        for p in products:
            content.append(
                Paragraph(f"• {p}", styles["Normal"])
            )
    else:
        content.append(
            Paragraph("No products found.", styles["Normal"])
        )

    content.append(Spacer(1, 12))

    # ==========================
    # Pain Points
    # ==========================
    content.append(
        Paragraph("<b>AI Generated Pain Points</b>", styles["Heading2"])
    )

    pains = analysis.get("pain_points", [])

    if pains:
        for p in pains:
            content.append(
                Paragraph(f"• {p}", styles["Normal"])
            )
    else:
        content.append(
            Paragraph("No pain points found.", styles["Normal"])
        )

    content.append(Spacer(1, 12))

    # ==========================
    # Competitors
    # ==========================
    content.append(
        Paragraph("<b>Competitors</b>", styles["Heading2"])
    )

    if competitors:
        for c in competitors:
            name = c.get("name", "Unknown")
            website = c.get("website", "")

            content.append(
                Paragraph(
                    f"• <b>{name}</b><br/>{website}",
                    styles["Normal"]
                )
            )
    else:
        content.append(
            Paragraph("No competitors found.", styles["Normal"])
        )

    content.append(Spacer(1, 20))

    # ==========================
    # Footer
    # ==========================
    content.append(
        Paragraph(
            "Generated automatically by AI Company Research Assistant",
            styles["Italic"]
        )
    )

    # Build PDF
    doc.build(content)

    return file_path