from fpdf import FPDF
import os
from fpdf.enums import XPos, YPos

base_dir =os.path.dirname(os.path.abspath(__file__))
logo_path = os.path.join(base_dir, "assets", "Logo.jpeg")

VERT_FONCE = (6, 41, 22)
VERT = (14, 77, 46)
OR = (200, 160, 64)
FOND = (245, 247, 245)
FOND_OR = (255, 248, 225)
GRIS = (45, 45, 45)
GRIS_C = (110, 110, 110)
BLANC = (255, 255, 255)

class PDF(FPDF):
    def header(self):
        if self.page_no() == 1:
            # HEADER 38mm - Logo à gauche dans cadre blanc
            self.set_fill_color(*VERT_FONCE)
            self.rect(0, 0, 210, 38, 'F')
            self.set_fill_color(*BLANC)
            self.rect(10, 5, 52, 28, 'F')
            if os.path.exists(logo_path):
                self.image(logo_path, x=13, y=7, w=46)
            self.set_xy(68, 8)
            self.set_font("Helvetica", "B", 11.5)
            self.set_text_color(*BLANC)
            self.cell(0, 6, "APGIV OS - PLAN D'EXECUTION & OFFRE", new_x=XPos.LMARGIN, new_y=YPos.NEXT)
            self.set_xy(68, 15)
            self.set_font("Helvetica", "B", 11.5)
            self.set_text_color(*OR)
            self.cell(0, 6, "COMMERCIALE", new_x=XPos.LMARGIN, new_y=YPos.NEXT)
            self.set_xy(68, 24)
            self.set_font("Helvetica", "", 8.5)
            self.set_text_color(225, 225, 225)
            self.cell(0, 4, "Developpe par ENAM DEV - Systeme d'exploitation de APGIV ", new_x=XPos.LMARGIN, new_y=YPos.NEXT)
            self.set_y(44)
        else:
            self.set_fill_color(*VERT_FONCE)
            self.rect(0, 0, 210, 13, 'F')
            self.set_xy(12, 3.5)
            self.set_font("Helvetica", "B", 7.5)
            self.set_text_color(*BLANC)
            self.cell(0, 6, "APGIV OS - OFFRE COMMERCIALE")
            self.set_xy(-45, 3.5)
            self.set_text_color(*OR)
            self.cell(35, 6, "Confidentiel", align='R')
            self.set_y(19)

    def footer(self):
        # FIX BANDE VERTE : toujours à 13mm du bas, jamais sur le texte
        self.set_y(-13)
        self.set_fill_color(*VERT_FONCE)
        self.rect(0, self.h - 13, self.w, 13, 'F')
        self.set_font("Helvetica", "", 7.5)
        self.set_text_color(200, 200, 200)
        self.set_xy(12, self.h - 9)
        self.cell(0, 4, "ENAM DEV | Lome Togo | apgivosgestion.streamlit.app")
        self.set_xy(-48, self.h - 9)
        self.set_text_color(*OR)
        self.cell(38, 4, "Confidentiel - APGIV OS", align='R')

pdf = PDF('P', 'mm', 'A4')
pdf.set_auto_page_break(auto=True, margin=18) # 18mm de marge bas = footer ne touche jamais le texte
pdf.set_margins(14, 10, 14)
pdf.add_page()

def section(n, titre):
    pdf.ln(3)
    y = pdf.get_y()
    pdf.set_fill_color(*OR)
    pdf.rect(14, y, 1.2, 8, 'F')
    pdf.set_fill_color(*FOND)
    pdf.set_xy(16, y)
    pdf.set_font("Helvetica", "B", 11)
    pdf.set_text_color(*VERT_FONCE)
    pdf.cell(180, 8, f" {n}. {titre}", new_x=XPos.LMARGIN, new_y=YPos.NEXT, fill=True)
    pdf.ln(3)

def texte(t):
    pdf.set_font("Helvetica", "", 9.5)
    pdf.set_text_color(*GRIS)
    pdf.set_x(16)
    pdf.multi_cell(178, 5.2, t, align='J')
    pdf.ln(0.5)

def puce(t, gras=""):
    pdf.set_font("Helvetica", "", 9.5)
    pdf.set_text_color(*GRIS)
    pdf.set_x(18)
    if gras:
        pdf.set_font("Helvetica", "B", 9.5)
        pdf.cell(3, 5.2, "- ")
        pdf.cell(0, 5.2, gras, new_x=XPos.LMARGIN, new_y=YPos.NEXT)
        pdf.set_font("Helvetica", "", 8.8)
        pdf.set_text_color(*GRIS_C)
        pdf.set_x(22)
        pdf.multi_cell(172, 4.6, t)
    else:
        pdf.multi_cell(176, 5.2, f"- {t}")
    pdf.ln(0.5)

def carte_semaine(num, titre, sous, items):
    y = pdf.get_y()
    # Carte avec bordure gauche OR
    pdf.set_fill_color(*BLANC)
    pdf.set_draw_color(235, 235, 235)
    pdf.rect(14, y, 182, 24, 'F')
    pdf.set_fill_color(*VERT_FONCE)
    pdf.rect(14, y, 2, 24, 'F')
    pdf.set_xy(19, y+2)
    pdf.set_font("Helvetica", "B", 9.5)
    pdf.set_text_color(*VERT_FONCE)
    pdf.cell(0, 5, f"SEMAINE {num} ({titre}) : {sous}", new_x=XPos.LMARGIN, new_y=YPos.NEXT)
    pdf.set_font("Helvetica", "", 9)
    pdf.set_text_color(*GRIS)
    for it in items:
        pdf.set_x(19)
        pdf.cell(0, 4.8, f"- {it}", new_x=XPos.LMARGIN, new_y=YPos.NEXT)
    pdf.set_y(y + 27)


# ============ 6. OFFRE ============
section("6", "OFFRE COMMERCIALE APGIV - ROI EN 30 JOURS")

# Box OR recommandée
pdf.set_fill_color(*FOND_OR)
pdf.set_xy(14, pdf.get_y())
pdf.set_font("Helvetica", "B", 9.5)
pdf.set_text_color(*VERT_FONCE)
pdf.cell(182, 7, " PACK RECOMMANDE - RESEAU EXCELLENCE (10 modules)", new_x=XPos.LMARGIN, new_y=YPos.NEXT, fill=True)
pdf.ln(2)
puce("Developpement complet APGIV OS special sante / MLM avec votre logo vert")
puce("Installation, formation 2 sessions (bureau APGIV + video)")
puce("Connexion apgiv.net (publication auto produits & temoignages)")
puce("3 mois support inclus (WhatsApp prioritaire 7j/7)")
pdf.ln(1)

# Tableau Investissement - 2 colonnes pro
pdf.set_fill_color(*VERT_FONCE)
pdf.set_xy(14, pdf.get_y())
pdf.set_font("Helvetica", "B", 9)
pdf.set_text_color(*BLANC)
pdf.cell(91, 7, " INVESTISSEMENT", border=0, fill=True)
pdf.set_text_color(*OR)
pdf.cell(91, 7, "400.000 FCFA", align='C', fill=True)
pdf.ln(7)
pdf.set_font("Helvetica", "", 9)
pdf.set_text_color(*GRIS)
pdf.set_x(14)
pdf.cell(0, 5, "Paiement securise : 50% demarrage 200.000F | 50% livraison 200.000F apres formation", new_x=XPos.LMARGIN, new_y=YPos.NEXT)
pdf.set_font("Helvetica", "B", 9)
pdf.set_x(14)
pdf.cell(0, 5, "MAINTENANCE : 50.000F/mois (hebergement cloud, sauvegardes, MAJ peremptions, support, MAJ Flooz)", new_x=XPos.LMARGIN, new_y=YPos.NEXT)
pdf.ln(3)

# ROI Box verte
pdf.set_fill_color(*FOND)
pdf.set_xy(14, pdf.get_y())
pdf.set_font("Helvetica", "B", 9.5)
pdf.set_text_color(*VERT_FONCE)
pdf.cell(182, 7, " ROI CHIFFRE - Rentabilise en 30 jours", new_x=XPos.LMARGIN, new_y=YPos.NEXT, fill=True)
pdf.ln(1)
pdf.set_font("Helvetica", "", 9.5)
pdf.set_text_color(*GRIS)
pdf.set_x(18)
pdf.multi_cell(174, 5.2, "- 1 lot perime evite = 200.000F economise (1 seul)\n- 10 commandes Mobile Money recuperees / mois = 230.000F CA (Ramdan 23k x10)\n- 5 distributeurs mieux animes = +500.000F / mois ventes reseau")
pdf.ln(3)

# CTA Final
pdf.set_fill_color(*VERT_FONCE)
pdf.set_xy(14, pdf.get_y())
pdf.set_font("Helvetica", "B", 9.5)
pdf.set_text_color(*OR)
pdf.cell(182, 9, " PROCHAINE ETAPE : Demo 20 min a votre bureau avec vos produits Ramdan & Vidangeur", align='C', fill=True)
pdf.ln(11)
pdf.set_font("Helvetica", "", 9)
pdf.set_text_color(*GRIS)
pdf.set_x(16)
pdf.cell(0, 5, "+ Liste des infos necessaires pour demarrer Lundi (fichier stock, liste distributeurs).", new_x=XPos.LMARGIN, new_y=YPos.NEXT)

output = os.path.join(base_dir, "APGIV_OS_Gestion_OFFRE_PRO.pdf")
pdf.output(output)
print(f"PDF OFFRE PRO genere: {output}")