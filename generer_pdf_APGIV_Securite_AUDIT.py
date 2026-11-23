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
pdf.cell(0, 12, "APGIV SECURITE - apgiv.net", new_x=XPos.LMARGIN, new_y=YPos.NEXT)
pdf.set_xy(12, 33)
pdf.set_font("Helvetica", "", 9.5)
pdf.set_text_color(230, 230, 230)
pdf.cell(0, 5, "Audit Securite WordPress + Offre Protection - Proposition Confidentielle", new_x=XPos.LMARGIN, new_y=YPos.NEXT)

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

def puce(t):
    pdf.set_font("Helvetica", "", 10)
    pdf.set_text_color(30, 30, 30)
    pdf.set_x(16)
    pdf.multi_cell(178, 6, f"- {t}")
    pdf.ln(1)

def carte_semaine(n, periode, titre, items):
    pdf.set_font("Helvetica", "B", 10)
    pdf.set_text_color(6, 41, 22)
    pdf.set_x(16)
    pdf.cell(178, 6, f"Jour {n} - {periode} : {titre}", new_x=XPos.LMARGIN, new_y=YPos.NEXT)
    pdf.ln(1)
    for it in items:
        pdf.set_font("Helvetica", "", 10)
        pdf.set_text_color(30, 30, 30)
        pdf.set_x(22)
        pdf.multi_cell(172, 6, f"- {it}")
        pdf.ln(0.5)
    pdf.ln(2)

# 1. AUDIT
section("1", "AUDIT SECURITE : APGIV.NET - WORDPRESS - ANALYSE REELLE")
texte_fidele("Votre site apgiv.net est votre boutique ouverte 24h/7j. Aujourd'hui elle est ouverte sans alarme, sans coffre, sans serrure renforcee.")
texte_fidele("Si demain le site tombe, vous perdez : vos produits (Ramdan 23k, Vidangeur 8k, Ango Power 14k, Soyayya 16k, Slim Tea 16k, Lait Ango 11k), vos temoignages, vos commandes, votre image.")
pdf.set_font("Helvetica", "B", 10)
pdf.set_x(14)
pdf.cell(0, 6, "FAILLES CRITIQUES IDENTIFIEES:", new_x=XPos.LMARGIN, new_y=YPos.NEXT)
pdf.ln(2)
for f in [
    "Pas de sauvegarde automatique quotidienne externe -> 1 bug = tout perdu",
    "Pas de firewall / anti-brute-force -> wp-login.php attaque en continu",
    "Pas de 2FA sur compte admin -> 1 mot de passe vole = site vole",
    "Pas de scan malware / alerte intrusion -> piratage decouvert trop tard",
    "Certificat SSL non securise a 100% / HTTPS non force partout -> perte de confiance + SEO",
    "Pas de cache / images lourdes -> site lent sur mobile a Lome, Kpalime = clients qui partent",
    "Plugins / theme / WordPress non mis a jour avec test -> mise a jour = site casse",
    "Pas de restauration en 1 clic -> 3 a 7 jours de boutique fermee en cas de probleme",
]:
    puce(f)

# 2. SAUVEGARDE
section("2", "SAUVEGARDE AUTOMATIQUE - LE COFFRE APGIV")
texte_fidele("Objectif : meme si le site est detruit, on le remet en ligne en moins de 1 heure.")
for x in [
    "Sauvegarde automatique quotidienne : fichiers + base de donnees + commandes + images",
    "Copie externe : Cloud + copie locale chez ENAM DEV (2 copies, jamais 1 seule)",
    "Retention 30 jours : on peut revenir a hier, avant-hier, il y a 7 jours",
    "Test de restauration mensuel : on verifie que la sauvegarde marche VRAIMENT",
    "Restauration en 1 clic en cas d'urgence, sans attendre l'hebergeur",
    "Rapport sauvegarde envoye au Patron : 'Sauvegarde du 06/11 OK - 100%'",
]:
    puce(x)

# 3. ANTI-PIRATAGE + CERTIFICAT
section("3", "PROTECTION ANTI-PIRATAGE + CERTIFICAT SSL")
texte_fidele("Objectif : apgiv.net devient une forteresse, mais reste simple pour les clients.")
for x in [
    "Firewall WordPress + blocage IP suspectes + anti-brute-force sur wp-login.php",
    "2FA obligatoire sur tous les comptes admin + mots de passe forts",
    "Changement URL admin / masquage wp-admin + limitation tentatives : 5 essais = blocage",
    "Scan malware quotidien + alerte WhatsApp immediate en cas d'intrusion",
    "Certificat SSL installe / renouvele + HTTPS force sur toutes les pages + cadenas vert",
    "Mises a jour securisees : test sur copie avant mise en ligne, jamais sur le site live",
    "Suppression comptes / utilisateurs inutiles + logs de connexion anti-vol",
]:
    puce(x)

# 4. VITESSE
section("4", "OPTIMISATION VITESSE - VENDRE PLUS VITE")
texte_fidele("Au Togo, 90% des clients sont sur mobile. 1 seconde de lenteur = 1 client perdu.")
for x in [
    "Compression images produits sans perte de qualite (Ramdan, Soyayya, Lait Ango...)",
    "Cache WordPress + optimisation base de donnees + nettoyage plugins lourds",
    "Chargement rapide mobile : objectif < 3 secondes sur 4G a Lome",
    "Optimisation PageSpeed / Core Web Vitals -> meilleur classement Google",
    "CDN + minification CSS / JS sans casser le design Vert APGIV + Or",
    "Test avant / apres : capture vitesse fournie au Patron",
]:
    puce(x)

# 5. OFFRE
section("5", "OFFRE SECURITE APGIV - 3 NIVEAUX")
texte_fidele("Pack ESSENTIEL : Sauvegarde auto + SSL + mises a jour securisees. Pour ne plus jamais perdre le site.")
texte_fidele("Pack PROTECTION [RECOMMANDE] : Essentiel + Firewall + 2FA + Scan malware + Alertes WhatsApp + Optimisation vitesse. Le site protege et rapide.")
texte_fidele("Pack PATRON 360 : Protection + Maintenance mensuelle + Support prioritaire 7j/7 + Rapport mensuel Patron + Restauration prioritaire < 1h.")
texte_fidele("Montant total du projet : a definir avec le Patron selon le Pack choisi.")
texte_fidele("Acompte : 50% pour demarrer, 50% a la livraison + test de restauration reussi devant le Patron.")
texte_fidele("Garantie : Si restauration echoue au test, remboursement acompte.")

# 6. ROADMAP
section("6", "ROADMAP 7 JOURS - MISE EN SECURITE")
carte_semaine("1", "J1-J2", "SAUVEGARDE + DIAGNOSTIC COMPLET", [
    "Sauvegarde complete immediate avant tout changement",
    "Diagnostic complet : plugins, theme, SSL, vitesse, utilisateurs",
    "Rapport failles remis au Patron"
])
carte_semaine("2", "J3-J5", "BLINDAGE + CERTIFICAT", [
    "Installation Firewall + 2FA + anti-brute-force + scan malware",
    "Installation / renouvellement SSL + HTTPS force partout",
    "Mises a jour securisees sur copie test, puis mise en ligne"
])
carte_semaine("3", "J6-J7", "VITESSE + LIVRAISON", [
    "Optimisation vitesse : cache + images + base de donnees",
    "Test de restauration devant le Patron + test vitesse avant / apres",
    "Remise acces + guide simple : 'Que faire si alerte ?' + formation 30 min"
])

output = os.path.join(base_dir, "APGIV_Securite_AUDIT.pdf")
pdf.output(output)
print(f"PDF genere: {output} - {pdf.pages_count} page(s)")