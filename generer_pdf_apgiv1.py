from fpdf import FPDF
import os

base_dir = os.path.dirname(os.path.abspath(__file__))
logo_path = os.path.join(base_dir, "assets", "Logo.jpeg")

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
VERT_APGIV=(14,77,46)
OR=(200,160,64)

# HEADER
pdf.set_fill_color(*VERT_FONCE)
pdf.rect(0,0,210,48,'F')
pdf.set_xy(12,8)
pdf.set_font("Helvetica","B",9)
pdf.set_text_color(255,255,255)
pdf.cell(0,5,"APGIV - ANGO POWER GROUP INTERNATIONAL VISION",ln=True)
pdf.set_xy(12,16)
pdf.set_font("Helvetica","B",20)
pdf.set_text_color(*OR)
pdf.cell(0,12,"APGIV OS - Gestion",ln=True)
pdf.set_xy(12,32)
pdf.set_font("Helvetica","",9)
pdf.set_text_color(230,230,230)
pdf.cell(0,5,"Le Systeme d'Exploitation de L'Excellence au Naturel - Proposition Confidentielle",ln=True)

pdf.image(logo_path,x=40,y=52,w=130)
pdf.set_y(82)

def st(n,t):
    pdf.ln(4)
    pdf.set_fill_color(240,245,240)
    pdf.set_font("Helvetica","B",11.5)
    pdf.set_text_color(*VERT_FONCE)
    pdf.cell(0,8,f" {n}. {t}",ln=True,fill=True)
    pdf.ln(3)

def txt(s):
    pdf.set_font("Helvetica","",10)
    pdf.set_text_color(30,30,30)
    pdf.set_x(12)
    pdf.multi_cell(186,5.5,s)
    pdf.ln(2)

st("1","AUDIT STRATEGIQUE : APGIV.NET - ANALYSE REELLE")

txt("D'apres vos captures apgiv.net, votre business n'est pas de la telephonie. C'est de la SANTE NATURELLE & MLM.\nProduits identifies: Ramdan Gourmet 23.000F, Vidangeur Anti-Cancer 8.000F, Ango Power 8 sachets 14.000F, Soyayya L 16.000F, Ramdan Slim Tea 16.000F, Lait Ango Goat Milk 11.000F.")

pdf.set_font("Helvetica","B",10)
pdf.set_text_color(0,0,0)
pdf.set_x(12)
pdf.cell(0,6,"FAILLES CRITIQUES IDENTIFIEES:",ln=True)
pdf.ln(1)

pdf.set_font("Helvetica","",10)
pdf.set_text_color(40,40,40)
failles = [
    "Stock sans gestion de lot & date de peremption -> Risque majeur pour produits bio",
    "Aucune gestion du reseau distributeur (votre banner 'Chacun de dever... Partager la reussi...')",
    "Pas de calcul de commission reseau automatique",
    "Section Temoignages vide sur le site alors que c'est votre meilleure arme de vente",
    "Panier a 0 sans paiement Mobile Money Flooz / TMoney integre -> 90% de perte de vente au Togo",
    "Aucun dashboard pour voir quel produit se vend (Ramdan vs Soyayya vs Vidangeur)"
]
for f in failles:
    pdf.set_x(12)
    pdf.multi_cell(186,5.5,f"- {f}")
    pdf.ln(1)

pdf.output(os.path.join(base_dir,"APGIV_OS_Gestion_AUDIT_SEUL.pdf"))
print("PDF AUDIT seul genere: APGIV_OS_Gestion_AUDIT_SEUL.pdf")