from fpdf import FPDF
import os
from fpdf.enums import XPos, YPos

base_dir = os.path.dirname(os.path.abspath(__file__))
logo_path = os.path.join(base_dir, "assets", "Logo.jpeg")

print(f"Logo: {logo_path}")

class PDF(FPDF):
    def footer(self):
        self.set_y(-15)
        self.set_fill_color(6,41,22)
        self.rect(0,self.h-15,self.w,15,'F')
        self.set_font("Helvetica","B",8)
        self.set_text_color(200,200,200)
        self.set_xy(10,self.h-11)
        self.cell(0,5,"APGIV OS Gestion | L'Excellence au Naturel | apgiv.net")
        self.set_xy(-60,self.h-11)
        self.set_text_color(200,160,64)
        self.cell(50,5,"Confidentiel - APGIV",align='R')

pdf = PDF('P','mm','A4')
pdf.set_auto_page_break(auto=True, margin=20)
pdf.add_page()

VERT_FONCE=(6,41,22)
VERT=(14,77,46)
OR=(200,160,64)

pdf.set_fill_color(*VERT_FONCE)
pdf.rect(0,0,210,35,'F')
pdf.set_xy(10,8)
pdf.set_font("Helvetica","B",14)
pdf.set_text_color(255,255,255)
pdf.cell(0,8,"APGIV OS - PLAN D'EXECUTION & OFFRE COMMERCIALE", new_x=XPos.LMARGIN, new_y=YPos.NEXT)
pdf.set_xy(10,18)
pdf.set_font("Helvetica","",9)
pdf.set_text_color(*OR)
pdf.cell(0,5,"Developpe par APGIV OS Gestion - Systeme L'Excellence au Naturel", new_x=XPos.LMARGIN, new_y=YPos.NEXT)

pdf.image(logo_path,x=40,y=40,w=130)
pdf.set_y(72)

def st(n,t):
    pdf.ln(4)
    pdf.set_fill_color(240,245,240)
    pdf.set_font("Helvetica","B",12)
    pdf.set_text_color(*VERT)
    pdf.cell(0,9,f" {n}. {t}", new_x=XPos.LMARGIN, new_y=YPos.NEXT, fill=True)
    pdf.ln(3)

def bullet(t):
    pdf.set_font("Helvetica","",10.5)
    pdf.set_text_color(40,40,40)
    pdf.set_x(15)
    pdf.multi_cell(180,6,f"- {t}")
    pdf.ln(1)

st("4","STACK TECHNIQUE INTERNATIONALE SANTE")
for t in ["Backend Python / Streamlit Pro - Systeme APGIV OS Gestion","Base de donnees Cloud chiffree sauvegardee quotidienne","Frontend Responsive Mobile & PC, PWA installable","API WooCommerce + TMoney/Flooz pour apgiv.net","Hebergement Cloud Securise Acces 24/7","Design Vert APGIV #0E4D2E + Or #C8A040 - Charte L'Excellence au Naturel"]:
    bullet(t)

st("5","ROADMAP 30 JOURS - SPECIAL APGIV")
pdf.set_font("Helvetica","B",11); pdf.set_text_color(*VERT_FONCE); pdf.set_x(12)
pdf.cell(0,7," SEMAINE 1 (J1-J14): Coeur Sante", new_x=XPos.LMARGIN, new_y=YPos.NEXT)
pdf.set_font("Helvetica","",10.5); pdf.set_x(15)
pdf.multi_cell(180,6,"- Stock & Peremption + Caisse Intelligente + Import Ramdan 23k, Vidangeur 8k, Soyayya 16k"); pdf.ln(2)

pdf.set_font("Helvetica","B",11); pdf.set_text_color(*VERT_FONCE); pdf.set_x(12)
pdf.cell(0,7," SEMAINE 2 (J14-J24): Reseau & Ventes", new_x=XPos.LMARGIN, new_y=YPos.NEXT)
pdf.set_font("Helvetica","",10.5); pdf.set_x(15)
pdf.multi_cell(180,6,"- Reseau Distributeur + Commissions Auto + Mobile Money Flooz/TMoney"); pdf.ln(2)

pdf.set_font("Helvetica","B",11); pdf.set_text_color(*VERT_FONCE); pdf.set_x(12)
pdf.cell(0,7," SEMAINE 3 (J24-J30): Scale & Site", new_x=XPos.LMARGIN, new_y=YPos.NEXT)
pdf.set_font("Helvetica","",10.5); pdf.set_x(15)
pdf.multi_cell(180,6,"- Temoignages Manager + Produits Phares Booster -> connecte a apgiv.net")

st("6","OFFRE COMMERCIALE APGIV OS GESTION")
pdf.set_fill_color(255,243,205)
pdf.set_font("Helvetica","B",11); pdf.set_text_color(*VERT_FONCE)
pdf.cell(0,8," OPTION RECOMMANDEE - PACK RESEAU EXCELLENCE", new_x=XPos.LMARGIN, new_y=YPos.NEXT, fill=True)
pdf.ln(2)

pdf.set_font("Helvetica","",10.5); pdf.set_text_color(40,40,40); pdf.set_x(12)
pdf.multi_cell(186,6,"- Developpement APGIV OS Gestion complet (10 modules sante/MLM)\n- Installation, formation equipe APGIV (2 sessions)\n- Connexion a apgiv.net (produits & temoignages auto)\n- 3 mois de support & mises a jour inclus")
pdf.ln(3)

pdf.set_font("Helvetica","B",11); pdf.set_text_color(0,0,0); pdf.set_x(12)
pdf.cell(0,7," INVESTISSEMENT: 600.000 FCFA (50% demarrage 300k, 50% livraison 300k)", new_x=XPos.LMARGIN, new_y=YPos.NEXT)
pdf.set_font("Helvetica","",10.5); pdf.set_x(12)
pdf.multi_cell(186,6," MAINTENANCE: 50.000 FCFA / mois (hebergement, sauvegardes, support prioritaire)")
pdf.ln(3)

pdf.set_font("Helvetica","B",11); pdf.set_text_color(*VERT); pdf.set_x(12)
pdf.cell(0,7," ROI IMMEDIAT:", new_x=XPos.LMARGIN, new_y=YPos.NEXT)
pdf.set_font("Helvetica","",10.5); pdf.set_text_color(40,40,40); pdf.set_x(12)
pdf.multi_cell(186,6,"- 1 lot perime evite = 200.000F economises\n- 10 commandes Mobile Money/mois = 230.000F CA\n- 5 distributeurs mieux suivis = +500.000F/mois")
pdf.ln(4)

pdf.set_fill_color(240,245,240)
pdf.set_font("Helvetica","B",11); pdf.set_text_color(*VERT_FONCE)
pdf.cell(0,8," OPTION DEMARRAGE RAPIDE: 350.000 FCFA + 30.000F/mois", new_x=XPos.LMARGIN, new_y=YPos.NEXT, fill=True)

output = os.path.join(base_dir,"APGIV_OS_Gestion_Partie2_Offre.pdf")
pdf.output(output)
print(f"PDF Partie 2 OFFRE genere SANS warning: {output}")