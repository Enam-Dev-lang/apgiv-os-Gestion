from fpdf import FPDF
import os
from fpdf.enums import XPos, YPos

base_dir = os.path.dirname(os.path.abspath(__file__))
logo_path = os.path.join(base_dir, "assets", "Logo.jpeg")

VERT_FONCE = (6, 41, 22)
OR = (200, 160, 64)
GRIS = (45, 45, 45)

class PDF(FPDF):
    def footer(self):
        self.set_y(-15)
        self.set_fill_color(6, 41, 22)
        self.rect(0, self.h-15, self.w, 15, 'F')
        self.set_font("Helvetica", "B", 8)
        self.set_text_color(200, 200, 200)
        self.set_xy(10, self.h-11)
        self.cell(0, 5, "APGIV OS Gestion | L'Excellence au Naturel | apgiv.net")
        self.set_xy(-60, self.h-11)
        self.set_text_color(200, 160, 64)
        self.cell(50, 5, "Confidentiel - APGIV", align='R')

pdf = PDF('P', 'mm', 'A4')
pdf.set_auto_page_break(auto=True, margin=22)
pdf.add_page()

pdf.set_fill_color(*VERT_FONCE)
pdf.rect(0, 0, 210, 48, 'F')
pdf.set_xy(12, 10)
pdf.set_font("Helvetica", "B", 9)
pdf.set_text_color(255, 255, 255)
pdf.cell(0, 5, "APGIV - ANGO POWER GROUP INTERNATIONAL VISION", new_x=XPos.LMARGIN, new_y=YPos.NEXT)
pdf.set_xy(12, 18)
pdf.set_font("Helvetica", "B", 22)
pdf.set_text_color(*OR)
pdf.cell(0, 12, "APGIV OS - Gestion", new_x=XPos.LMARGIN, new_y=YPos.NEXT)
pdf.set_xy(12, 33)
pdf.set_font("Helvetica", "", 9.5)
pdf.set_text_color(230, 230, 230)
pdf.cell(0, 5, "Le Systeme d'Exploitation de L'Excellence au Naturel - Proposition Confidentielle", new_x=XPos.LMARGIN, new_y=YPos.NEXT)

pdf.set_y(55)
logo_w = 80
logo_x = (210 - logo_w) / 2
pdf.image(logo_path, x=logo_x, y=pdf.get_y(), w=logo_w)
pdf.set_y(pdf.get_y() + 38)
pdf.set_draw_color(*OR)
pdf.set_line_width(0.6)
pdf.line(85, pdf.get_y(), 125, pdf.get_y())
pdf.ln(10)

def st(n, t):
    pdf.ln(4)
    pdf.set_fill_color(240, 245, 240)
    pdf.set_draw_color(6, 41, 22)
    pdf.set_font("Helvetica", "B", 11.5)
    pdf.set_text_color(6, 41, 22)
    pdf.set_x(12)
    pdf.cell(186, 9, f" {n}. {t}", new_x=XPos.LMARGIN, new_y=YPos.NEXT, fill=True, border=0)
    pdf.ln(4)

def section(n, t):
    st(n, t)

def texte_fidele(t):
    pdf.set_font("Helvetica", "", 10)
    pdf.set_text_color(30, 30, 30)
    pdf.set_x(14)
    pdf.multi_cell(182, 6, t)
    pdf.ln(1)

def puce(t, label=""):
    pdf.set_font("Helvetica", "", 10)
    pdf.set_text_color(30, 30, 30)
    pdf.set_x(16)
    pdf.multi_cell(178, 6, f"- {label}{t}")
    pdf.ln(1)

def carte_semaine(n, periode, titre, items):
    pdf.set_font("Helvetica", "B", 10)
    pdf.set_text_color(6, 41, 22)
    pdf.set_x(16)
    pdf.cell(178, 6, f"Semaine {n} - {periode} : {titre}", new_x=XPos.LMARGIN, new_y=YPos.NEXT)
    pdf.ln(1)
    for it in items:
        pdf.set_font("Helvetica", "", 10)
        pdf.set_text_color(30, 30, 30)
        pdf.set_x(22)
        pdf.multi_cell(172, 6, f"- {it}")
        pdf.ln(0.5)
    pdf.ln(2)

st("1", "AUDIT STRATEGIQUE : APGIV.NET - ANALYSE REELLE")
pdf.set_font("Helvetica", "", 10)
pdf.set_text_color(30, 30, 30)
pdf.set_x(14)
pdf.multi_cell(182, 6, "D'apres l'étude de votre site apgiv.net, votre business c'est de la SANTE NATURELLE & MLM. dont j'ai pris les produits: Ramdan 23k, Vidangeur 8k, Ango Power 14k, Soyayya 16k, Slim Tea 16k, Lait Ango 11k.", align='J')
pdf.ln(4)
pdf.set_font("Helvetica", "B", 10)
pdf.set_x(14)
pdf.cell(0, 6, "FAILLES CRITIQUES IDENTIFIEES:", new_x=XPos.LMARGIN, new_y=YPos.NEXT)
pdf.ln(2)
pdf.set_font("Helvetica", "", 10)
failles = [
    "Stock sans gestion de lot & peremption -> Risque majeur pour produits bio",
    "Aucune gestion reseau distributeur (votre banner 'Chacun de dever... Partager la reussi...')",
    "Pas de calcul de commission reseau automatique",
    "Section Temoignages vide sur le site alors que c'est votre meilleure arme de vente",
    "Panier a 0 sans paiement Mobile Money Flooz / TMoney integre -> 90% de perte de vente au Togo",
    "Pas de dashboard CA temps reel"
]
for f in failles:
    pdf.set_x(16)
    pdf.multi_cell(180, 6, f"- {f}")
    pdf.ln(1)

section("2", "VISION : GERER UN RESEAU DE SANTE, PAS UN SITE WORDPRESS")
texte_fidele("WordPress affiche des produits. APGIV OS fait tourner votre reseau.")
texte_fidele("Objectif: Un logiciel unique qui controle apgiv.net + distributeurs + lots + peremptions + commissions + temoignages + paiements Flooz/TMoney.")
texte_fidele("Resultat: Vous voyez votre benefice reel par produit, par distributeur, depuis votre tel.")

section("3", "ARCHITECTURE APGIV OS - 10 MODULES POINTE SANTE")
modules_fideles = [
    "[1] STOCK & PEREMPTION: Lot, alerte 'Lot VD-24-11 expire 30j', methode FIFO obligatoire bio",
    "[2] RESEAU DISTRIBUTEUR: Code parrain unique, arbre, niveaux Starter/Pro/Leader",
    "[3] COMMISSIONS AUTO: % par niveau, solde, historique, export Mobile Money",
    "[4] CAISSE INTELLIGENTE: Vente avec marge, ticket avec posologie/conseils utilisation",
    "[5] MOBILE MONEY CONNECT: API TMoney/Flooz, validation auto commande apgiv.net",
    "[6] TEMOIGNAGES MANAGER: Collecte WhatsApp, validation, push auto sur apgiv.net",
    "[7] PRODUITS PHARES BOOSTER: Depuis OS, mettre Ramdan 23k en avant en 1 clic sur site",
    "[8] COMPTA PATRON Privee: CA par produit, par distributeur, marge reelle, benefice net",
    "[9] ALERTES RUPTURE: 'Stock Soyayya Ladies <20' -> Notif WhatsApp auto",
    "[10] SECURITE: Logs anti-vol, sauvegarde cloud quotidienne, acces Patron unique",
]
for ligne in modules_fideles:
    pdf.set_font("Helvetica", "", 9.5)
    pdf.set_text_color(*GRIS)
    pdf.set_x(16)
    pdf.multi_cell(178, 5.2, ligne)
    pdf.ln(0.8)

section("4", "STACK TECHNIQUE")
puce("Python / Streamlit Pro securise (un système uniquement pensé pour APGIV OS Gestion)", "Backend : ")
puce("Chiffree, sauvegarde auto quotidienne, conforme gestion produits sante", "DB : Cloud ")
puce("PWA installable pour distributeurs sur le terrain", "Frontend : Responsive Mobile & PC, ")
puce("API apgiv.net + API TMoney/Flooz -> connexion sans casser votre site", "API : WooCommerce ")
puce("Acces 24h/7jrs depuis Lome, Kpalime, partout", "Hebergement : Streamlit Cloud Securise - ")
puce("Fidele à 'L'Excellence au Naturel'", "Design : 100% Vert APGIV #0E4D2E + Or #C8A040 - ")

section("5", "ROADMAP 21 JOURS - SPECIAL APGIV")
carte_semaine("1", "J1-J7", "COEUR SANTE - Livrable operationnel", [
    "Deploiement Stock & Peremption + Caisse + Compta Patron",
    "Import de vos produits reels: Ramdan 23k, Vidangeur 8k, Soyayya 16k, Lait 11k",
    "Formation: Comment saisir un lot avec date peremption"
])
carte_semaine("2", "J8-J14", "RESEAU & VENTES - Votre reseau devient automatique", [
    "Reseau Distributeur + Commissions Auto + Mobile Money Flooz / TMoney",
    "Import de vos distributeurs actuels, generation codes parrains",
    "Formation equipe sur calcul commissions"
])
carte_semaine("3", "J15-J21", "SCALE & SITE - apgiv.net devient intelligent", [
    "Temoignages Manager + Produits Phares Booster connecte a apgiv.net",
    "Mise en prod + Formation finale Patron: Comment lire votre dashboard reseau",
    "Remise acces Patron + codes distributeurs"
])

output = os.path.join(base_dir, "APGIV_OS_Gestion_AUDIT.pdf")
pdf.output(output)
print(f"PDF genere: {output} - {pdf.pages_count} page(s)")