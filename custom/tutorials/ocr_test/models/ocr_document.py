from odoo import models, fields
from odoo.exceptions import UserError
import pytesseract
from PIL import Image
import base64
import io
import PyPDF2  # Pour gérer les fichiers PDF


class OCRDocument(models.Model):
    _name = 'ocr.document'
    _description = 'Document with OCR'

    name = fields.Char(string="Document Name")
    document = fields.Binary(string="Document", attachment=True)
    ocr_text = fields.Text(string="Extracted Text")

    def extract_text(self):
        """Méthode pour extraire le texte du fichier binaire (PDF ou image)"""
        if not self.document:
            raise UserError("Veuillez télécharger un document avant d'extraire le texte.")

        # Convertir le fichier binaire en bytes
        file_data = base64.b64decode(self.document)
        try:
            # Tentative de traitement comme PDF
            pdf_reader = PyPDF2.PdfReader(io.BytesIO(file_data))
            text = ""
            for page_num in range(len(pdf_reader.pages)):
                page = pdf_reader.pages[page_num]
                text += page.extract_text()
            self.ocr_text = text
        except PyPDF2.errors.PdfReadError:
            # Si ce n'est pas un PDF, essayer avec une image
            image = Image.open(io.BytesIO(file_data))
            text = pytesseract.image_to_string(image)
            self.ocr_text = text
