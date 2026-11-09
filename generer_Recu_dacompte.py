from fpdf import FPDF
import os
from fpdf.enums import XPos, YPos

base_dir = os.path.dirname(os.path.abspath(__file__))
logo_path = os.path.join(base_dir, "assets", "Logo.jpeg")

VERT_FONCE = (6, 41, 22)
VERT = (14, 77, 46)
OR = (200, 160, 64)
GRIS = (45, 45, 45)
BLANC = (255, 255, 255)
FOND = (245, 247, 245)

class PDF(FPDF):
    def footer(self):
        self.set_y(-15)
        self.set_fill_color(*VERT_FONCE)
        self.rect(0, self.h - 15, self.w, 15, 'F')
        self.set_font("Helvetica", "B", 8)
        self.set_text_color(200, 200, 200)
        self.set_xy(10, self.h - 11)
        self.cell(0, 5, "ENAM DEV | Lome Togo | apgiv.net")
        self.set_xy(-60, self.h - 11)
        self.set_text_color(*OR)
        self.cell(50, 5, "Confidentiel APGIV", align='R')

pdf = PDF('P', 'mm', 'A4')
pdf.set_auto_page_break(auto=True, margin=22)
pdf.set_margins(14, 10, 14)
pdf.add_page()

# --- HEADER VERT 38mm + LOGO OFFICIEL APGIV OS GESTION DANS ASSETS ---
pdf.set_fill_color(*VERT_FONCE)
pdf.rect(0, 0, 210, 38, 'F')
pdf.set_fill_color(*BLANC)
pdf.rect(10, 5, 28, 28, 'F')
if os.path.exists(logo_path):
    pdf.image(logo_path, x=11, y=6, w=26, h=26)
pdf.set_xy(44, 10)
pdf.set_font("Helvetica", "B", 16)
pdf.set_text_color(*BLANC)
pdf.cell(0, 8, "RECU D'ACOMPTE - APGIV OS GESTION", new_x=XPos.LMARGIN, new_y=YPos.NEXT)
pdf.set_xy(44, 22)
pdf.set_font("Helvetica", "B", 11)
pdf.set_text_color(*OR)
pdf.cell(0, 6, "ENAM DEV - Lome Togo", new_x=XPos.LMARGIN, new_y=YPos.NEXT)

pdf.set_y(46)

def ligne(t, gras=False, taille=10.5):
    pdf.set_font("Helvetica", "B" if gras else "", taille)
    pdf.set_text_color(*GRIS)
    pdf.set_x(16)
    pdf.multi_cell(178, 6, t)
    pdf.ln(1)

def ligne_indent(t):
    pdf.set_font("Helvetica", "", 10.5)
    pdf.set_text_color(*GRIS)
    pdf.set_x(24)
    pdf.multi_cell(170, 6, t)
    pdf.ln(1)

pdf.ln(2)
ligne("Je soussigne ENAM DEV, developpeur du systeme APGIV OS Gestion pour le compte de apgiv.net, reconnais avoir recu de:")
pdf.ln(2)

ligne("Nom du client: APGIV SARL - ANGO POWER GROUP INTERNATIONAL VISION")
ligne("Represente par: ________________________ (Patron)")
pdf.ln(2)

ligne("La somme de: DEUX CENT MILLE (200.000) FRANCS CFA")
pdf.ln(2)

ligne("Au titre de: Acompte de 50% pour le developpement du logiciel APGIV OS - Gestion")
ligne_indent("(10 modules: Stock & Peremption, Reseau, Commissions, Caisse, Mobile Money...)")
pdf.ln(2)

ligne("Montant total du projet: 400.000 FCFA")
ligne("Reste a payer a la livraison: 200.000 FCFA")
ligne("Date de demarrage prevue:            ____/____/2026 (a reception des fichiers stock + distributeurs)")
ligne("Date de livraison prevue: 30 jours apres signature pour le demarrage")
pdf.ln(2)

ligne("Mode de paiement: [ ] Espece [ ] Flooz [ ] TMoney [ ] Virement")
pdf.ln(2)

ligne("Ce recu bloque le planning de developpement et garantit le prix de 400.000F.")
pdf.ln(2)

ligne("Fait a Lome, le            ____/____/2026")
pdf.ln(6)

# --- SIGNATURES 2 COLONNES ---
y_sig = pdf.get_y()
pdf.set_font("Helvetica", "", 10.5)
pdf.set_text_color(*GRIS)
pdf.set_xy(16, y_sig)
pdf.cell(85, 6, "Signature ENAM DEV")
pdf.set_xy(105, y_sig)
pdf.cell(85, 6, "Signature Client APGIV")
pdf.set_y(y_sig + 16)
pdf.set_xy(16, pdf.get_y())
pdf.cell(85, 6, "Tel:")
pdf.set_xy(105, pdf.get_y())
pdf.cell(85, 6, "Tel:")
pdf.ln(6)
pdf.set_x(16)
pdf.cell(85, 6, "Cachet:")
pdf.set_x(105)
pdf.cell(85, 6, "Cachet:")
pdf.ln(10)

ligne("Document valable comme preuve de paiement d'acompte. Merci pour votre confiance.")
ligne("L'Excellence au Naturel - APGIV OS Gestion.")

output = os.path.join(base_dir, "APGIV_OS_Gestion_RECU_ACOMPTE.pdf")
pdf.output(output)
print(f"PDF genere: {output} - {pdf.pages_count} page(s)")
