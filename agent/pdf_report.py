from reportlab.platypus import SimpleDocTemplate, Paragraph
from reportlab.lib.styles import getSampleStyleSheet


class PDFReport:

    def generate(self, text):

        pdf = SimpleDocTemplate("CloudWarden_Report.pdf")

        styles = getSampleStyleSheet()

        story = []

        story.append(
            Paragraph(
                "<b>CloudWarden AI Report</b>",
                styles["Heading1"]
            )
        )

        story.append(
            Paragraph(text.replace("\n", "<br/>"),
            styles["BodyText"])
        )

        pdf.build(story)

        return "CloudWarden_Report.pdf"