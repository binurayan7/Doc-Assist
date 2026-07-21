from xhtml2pdf import pisa


class PDFGenerator:
    """
    Generates a PDF from HTML.
    """

    def generate(self, html: str, output_path: str):

        with open(output_path, "wb") as pdf_file:
            result = pisa.CreatePDF(
                src=html,
                dest=pdf_file,
            )

        if result.err:
            raise Exception("Failed to generate PDF.")
