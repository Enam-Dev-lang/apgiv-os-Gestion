# ============================================================
# APGIV OS GESTION - V3 FINALE - CLIENTS + LIVRAISON + SUPABASE
# UN SEUL FICHIER - A COLLER EN ENTIER DANS app.py
# CORRIGE : panier + menu == + confirmer unique + Comptabilite Centrale + Rapports PDF Boss + Inventaire + Inventaire Auto
# ============================================================
import streamlit as st
import pandas as pd
import hashlib
import os
import json
import urllib.parse
import base64
import tempfile
import requests
from datetime import datetime, date

try:
    import gspread
    from google.oauth2.service_account import Credentials
    HAS_GSPREAD = True
except ImportError:
    gspread = None
    Credentials = None
    HAS_GSPREAD = False

try:
    from fpdf import FPDF
    HAS_FPDF = True
except ImportError:
    FPDF = None
    HAS_FPDF = False

LOGO_PATH = "assets/Logo.png"
VERT_FONCE = "#062914"
VERT = "#0E4D2E"
OR = "#C8A040"
FOND = "#F7F8F5"

SUPABASE_URL = "https://qamnmvaxnfyelvmyfugq.supabase.co/rest/v1"
SUPABASE_KEY = "sb_publishable_PHzlpQTbOA-KCUsj8kaV5A_pe1XgGG_"

def supa_get(table):
    r = requests.get(f"{SUPABASE_URL}/{table}?select=*&apikey={SUPABASE_KEY}", timeout=15)
    r.raise_for_status()
    return r.json()

def supa_insert(table, data):
    r = requests.post(f"{SUPABASE_URL}/{table}?apikey={SUPABASE_KEY}", json=data, headers={"Content-Type": "application/json", "Prefer": "return=representation"}, timeout=15)
    r.raise_for_status()
    return r.json()[0]

def supa_update(table, id_col, id_val, data):
    r = requests.patch(f"{SUPABASE_URL}/{table}?{id_col}=eq.{id_val}&apikey={SUPABASE_KEY}", json=data, headers={"Content-Type": "application/json", "Prefer": "return=representation"}, timeout=15)
    r.raise_for_status()
    return r.json()

def supa_update_stock(pid, stock):
    return supa_update("produits", "id", pid, {"stock_actuel": stock})

def charger_produits_supabase():
    try:
        rows = supa_get("produits")
        out = []
        for p in rows:
            out.append({"id": p.get("id"), "Produit": p.get("nom",""), "Prix": p.get("prix_fcfa",0), "Stock": p.get("stock_actuel") or 0, "Lot": p.get("lot") or "-", "Peremption": p.get("peremption") or "-", "Famille": p.get("famille") or ""})
        if out:
            return out
    except Exception as e:
        st.warning(f"Supabase injoignable : {e}")
    return [{"Produit": "Ango Power", "Prix": 14000, "Stock": 65, "Lot": "AP-25-01", "Peremption": "01/2027"}]

def charger_agents_supabase():
    try:
        rows = supa_get("agents")
        out = []
        for a in rows:
            out.append({"id": a.get("id"), "Nom": a.get("nom",""), "Code": a.get("code",""), "Type": a.get("type_agent") or "MLM", "Niveau": a.get("niveau","Starter"), "Parrain": a.get("parrain","Boss"), "Telephone": a.get("telephone",""), "Boutique": a.get("boutique","—"), "Commission": a.get("commission_fcfa") or 0})
        return out
    except Exception:
        return []

def supa_delete(table, id_col, id_val):
    r = requests.delete(f"{SUPABASE_URL}/{table}?{id_col}=eq.{id_val}&apikey={SUPABASE_KEY}", timeout=15)
    r.raise_for_status()
    return True

def charger_temoignages_supabase():
    try:
        rows = supa_get("temoignages")
        return [{"id": t.get("id"), "Client": t.get("client",""), "Produit": t.get("produit",""), "Note": t.get("note",5), "Message": t.get("message",""), "Date": t.get("date","")} for t in rows]
    except Exception:
        return [{"id": None, "Client": "Maman Chantal", "Produit": "Ango Power", "Note": 5, "Message": "Mon mari est redevenu jeune, merci APGIV!", "Date": "01/11/2026"}]

def charger_clients_supabase():
    try:
        rows = supa_get("clients")
        out = []
        for c in rows:
            out.append({"id": c.get("id"), "Nom": c.get("nom",""), "Telephone": c.get("telephone",""), "Quartier": c.get("quartier",""), "Ville": c.get("ville","Lome"), "Type": c.get("type_client","Particulier")})
        return out
    except Exception:
        return [{"Nom": "M. Kodjo", "Telephone": "90 12 34 56", "Quartier": "Agoe", "Ville": "Lome", "Type": "Particulier"}]

def charger_zones_supabase():
    try:
        rows = supa_get("zones_livraison")
        out = []
        for z in rows:
            out.append({"id": z.get("id"), "Nom": z.get("nom",""), "Frais": z.get("frais_fcfa",0), "Delai": z.get("delai_texte",""), "Seuil": z.get("gratuite_des_fcfa",0)})
        if out:
            return out
    except Exception:
        pass
    return [
        {"Nom": "Retrait Siege - Gratuit", "Frais": 0, "Delai": "Immediat", "Seuil": 0},
        {"Nom": "Grand Lome", "Frais": 1000, "Delai": "24h", "Seuil": 50000},
        {"Nom": "Peripherie Lome", "Frais": 1500, "Delai": "24-48h", "Seuil": 0},
        {"Nom": "Autres villes Togo", "Frais": 2500, "Delai": "48-72h", "Seuil": 0},
        {"Nom": "Sous-region - Sur devis", "Frais": 0, "Delai": "3-7 jours", "Seuil": 0},
    ]

def calculer_livraison(zone_nom, sous_total, zones):
    z = next((x for x in zones if x["Nom"]==zone_nom), None)
    if not z:
        return 0, ""
    frais = int(z["Frais"])
    if z["Seuil"] and sous_total >= int(z["Seuil"]):
        return 0, f"Livraison OFFERTE - {zone_nom} (seuil {z['Seuil']} atteint)"
    if frais == 0:
        return 0, f"Zone : {zone_nom} - {z['Delai']}"
    return frais, f"Zone : {zone_nom} - {z['Delai']} - Frais {frais} F"

st.set_page_config(page_title="APGIV OS Gestion", page_icon="Logo(1).png", layout="wide")

def get_logo_b64():
    if os.path.exists(LOGO_PATH):
        with open(LOGO_PATH, "rb") as f:
            return base64.b64encode(f.read()).decode()
    return ""
logo_b64 = get_logo_b64()

if "entrer" not in st.session_state:
    st.session_state.entrer = False
if not st.session_state.entrer:
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        if os.path.exists(LOGO_PATH):
            st.image(LOGO_PATH, use_container_width=True)
        st.markdown("<h2 style='text-align: center;'>APGIV OS GESTION</h2>", unsafe_allow_html=True)
        st.markdown("<p style='text-align: center;'>Gestion & Controle - Acces 100% Securise</p>", unsafe_allow_html=True)
        st.write("")
        if st.button("ENTRER ➡", use_container_width=True):
            st.session_state.entrer = True
            st.rerun()
    st.stop()

def get_client():
    if not HAS_GSPREAD:
        raise Exception("gspread non installe")
    creds = Credentials.from_service_account_info(dict(st.secrets["gcp_service_account"]), scopes=["https://www.googleapis.com/auth/spreadsheets","https://www.googleapis.com/auth/drive"])
    return gspread.authorize(creds)

def get_users():
    try:
        sh = get_client().open("APGIV-Config")
        ws = sh.sheet1
        users = {}
        for row in ws.get_all_values()[1:]:
            if len(row) >= 3 and row[0]:
                users[row[0].strip().lower()] = {"pwd_hash": row[1].strip(), "role": row[2].strip()}
        if users:
            return users
    except Exception:
        pass
    try:
        return dict(st.secrets["users"])
    except Exception:
        return {}

def check_password():
    if "auth" not in st.session_state:
        st.session_state["auth"] = False
        st.session_state["role"] = None
    if st.session_state["auth"]:
        return True
    st.title("🔒 APGIV OS Gestion - Accès Securisé")
    st.warning("Acces reservé au personnel APGIV. Veuillez vous connecter.")
    user = st.text_input("Utilisateur").strip().lower()
    pwd = st.text_input("Mot de passe", type="password")
    if st.button("Se connecter"):
        users = get_users()
        h = hashlib.sha256(pwd.encode()).hexdigest()
        if user in users and h == users[user]["pwd_hash"]:
            st.session_state["auth"] = True
            st.session_state["role"] = users[user]["role"]
            st.session_state["user"] = user
            st.rerun()
        else:
            st.error("Identifiants incorrects.")
    return False

if not check_password():
    st.stop()

st.markdown(f"""
<style>
    .stApp {{ background:{FOND}; }}
    .block-container {{ padding-top: 0.5rem !important; }}
    header[data-testid="stHeader"] {{ background: transparent !important; height: 0px !important; }}
    [data-testid="collapsedControl"] {{ display: block !important; visibility: visible !important; color: {VERT_FONCE} !important; z-index: 99999 !important; }}
    [data-testid="stSidebar"] {{ background: linear-gradient(180deg, {VERT_FONCE} 0%, #0A3D1F 100%) !important; border-right: 3px solid {OR} !important; }}
    div[data-testid="stRadio"] {{ gap:12px; }}
    div[data-testid="stRadio"] > div {{ gap:12px; }}
    div[data-testid="stRadio"] label {{ background: transparent !important; border: 1.5px solid rgba(255,255,255,0.7) !important; border-radius: 22px !important; padding: 12px 18px !important; color: white !important; font-weight: 600 !important; }}
    div[data-testid="stRadio"] label[data-checked="true"] {{ background: linear-gradient(90deg, #1DB954, #0E8A3E) !important; border-left: 5px solid {OR} !important; font-weight: 800 !important; }}
    .apgiv-header-final {{ width: 100vw; margin-left: -5rem; margin-right: -5rem; height: 92px; background: #FFFFFF; display: flex; position: relative; overflow: hidden; box-shadow: 0 4px 24px rgba(0,0,0,0.07); border-bottom: 1px solid #E8EAEF; margin-bottom: 24px; }}
    .apgiv-logo-box {{ width: 88px; background: #FFFFFF; display: flex; align-items: center; justify-content: center; flex-shrink: 0; z-index: 5; }}
    .apgiv-logo-box img {{ width: 72px; height: auto; border-radius: 0; object-fit: contain; background: white; padding: 4px; }}
    .apgiv-header-content {{ flex: 1; background: white; display: flex; flex-direction: column; justify-content: center; padding-left: 22px; z-index: 3; }}
    .apgiv-title-line {{ display: flex; align-items: baseline; gap: 8px; line-height: 1; }}
    .apgiv-title-os {{ font-weight: 900; font-size: 26px; color: #0E4D2E; }}
    .apgiv-title-gestion {{ font-weight: 800; font-size: 26px; color: #C8A040; }}
    .apgiv-slogan {{ font-size: 12.5px; color: #000000; font-style: italic; font-weight: 500; margin-top: 6px; border-top: 1px solid #EDEEF2; padding-top: 5px; display: inline-block; width: fit-content; padding-right: 20px; }}
    .apgiv-waves {{ position: absolute; right: 0; top: 0; width: 58%; height: 100%; z-index: 2; pointer-events: none; }}
    .wave {{ position: absolute; right: -10%; width: 110%; height: 55px; border-radius: 100% 0 0 0; }}
    .wave-1 {{ bottom: -18px; background: #0E4D2E; transform: rotate(-6deg) skewX(-12deg); opacity: 0.95; }}
    .wave-2 {{ bottom: -2px; background: linear-gradient(90deg, #C8A040 0%, #E8C86A 50%, #C8A040 100%); height: 22px; transform: rotate(-7deg) skewX(-12deg); box-shadow: 0 2px 10px rgba(200,160,64,0.4); z-index: 3; }}
    .wave-3 {{ top: -8px; right: -15%; width: 115%; height: 68px; background: linear-gradient(105deg, #062914 0%, #0E4D2E 40%, #1A6B3C 65%, #C8A040 90%, #E8C86A 100%); transform: rotate(-8deg) skewX(-10deg); opacity: 0.98; clip-path: ellipse(90% 80% at 80% 20%); }}
    .kpi-card {{ background:white; border-radius:18px; padding:18px 20px; box-shadow: 0 8px 24px rgba(0,0,0,0.08); display:flex; align-items:flex-start; gap:16px; position:relative; overflow:hidden; height:115px; border:1px solid #EAECF0; }}
    .kpi-card::before {{ content:''; position:absolute; top:0; left:0; width:6px; height:100%; }}
    .kpi-ventes::before {{ background: #0E4D2E; }}
    .kpi-alerte::before {{ background: linear-gradient(180deg, #F97316, #EF4444); }}
    .kpi-top::before {{ background: #0E4D2E; }}
    .kpi-icon {{ width:48px; height:48px; border-radius:50%; display:flex; align-items:center; justify-content:center; font-size:22px; flex-shrink:0; color:white; }}
    .kpi-icon-ventes {{ background: #0E4D2E; }}
    .kpi-icon-alerte {{ background: #F97316; }}
    .kpi-icon-top {{ background: #0E4D2E; }}
    .section-header {{ background: linear-gradient(90deg, #062914 0%, #0E4D2E 55%, #C8A040 100%); border-radius:14px; padding:14px 20px; display:flex; align-items:center; gap:14px; box-shadow: 0 6px 18px rgba(10,46,28,0.25); border:1.5px solid #C8A040; margin:18px 0 14px 0; }}
    .section-header-gold-bar {{ width:5px; height:22px; background:#C8A040; border-radius:10px; }}
</style>
""", unsafe_allow_html=True)

if 'stock' not in st.session_state:
    st.session_state.stock = charger_produits_supabase()
if 'agents' not in st.session_state:
    st.session_state.agents = charger_agents_supabase()
if 'temoignages' not in st.session_state:
    st.session_state.temoignages = charger_temoignages_supabase()
if 'clients' not in st.session_state:
    st.session_state.clients = charger_clients_supabase()
if 'zones' not in st.session_state:
    st.session_state.zones = charger_zones_supabase()
if 'ventes' not in st.session_state:
    st.session_state.ventes = []
if 'panier' not in st.session_state:
    st.session_state.panier = []
if 'pin' not in st.session_state:
    st.session_state.pin = "1234"
if 'auth_compta' not in st.session_state:
    st.session_state.auth_compta = False
if 'derniere_vente' not in st.session_state:
    st.session_state.derniere_vente = None
if 'tel_patron' not in st.session_state:
    st.session_state.tel_patron = ""

def generer_facture_pdf(vente):
    if not HAS_FPDF:
        st.error("Installe fpdf2 : pip install fpdf2")
        return None
    pdf = FPDF()
    pdf.add_page()
    if os.path.exists(LOGO_PATH):
        pdf.image(LOGO_PATH, x=10, y=8, w=40)
    pdf.set_font("Arial", 'B', 16)
    pdf.set_text_color(6,41,20)
    pdf.cell(0,12,'APGIV OS Gestion', new_x="LMARGIN", new_y="NEXT", align='C')
    pdf.set_font("Arial", 'B', 11)
    pdf.set_text_color(200,160,64)
    pdf.cell(0,7,"L'Excellence au Naturel", new_x="LMARGIN", new_y="NEXT", align='C')
    pdf.ln(10)
    pdf.set_font("Arial", 'B', 11)
    pdf.set_text_color(0,0,0)
    pdf.cell(0,7,f"Client: {vente['Client']} - Tel: {vente.get('Telephone','')}", new_x="LMARGIN", new_y="NEXT")
    pdf.cell(0,7,f"Date: {vente['Date']} | Vendeur: {vente['Agent']} ({vente['Code']}) | Zone: {vente.get('Zone','-')}", new_x="LMARGIN", new_y="NEXT")
    pdf.ln(4)
    pdf.set_fill_color(6,41,20)
    pdf.set_text_color(255,255,255)
    pdf.set_font("Arial", 'B', 11)
    pdf.cell(55,11,'Produit',1,0,'C',True)
    pdf.cell(25,11,'Lot',1,0,'C',True)
    pdf.cell(15,11,'Qte',1,0,'C',True)
    pdf.cell(35,11,'Prix U.',1,0,'C',True)
    pdf.cell(50,11,'Total',1,1,'C',True)
    pdf.set_text_color(0,0,0)
    pdf.set_font("Arial", '', 11)
    lignes = vente.get("Lignes", [{"Produit": vente['Produit'], "Qte": vente['Qte'], "Prix": vente['SousTotal']//vente['Qte'], "Lot": vente['Lot']}])
    for li in lignes:
        pdf.cell(55,11,li["Produit"][:28],1)
        pdf.cell(25,11,li.get("Lot","-"),1)
        pdf.cell(15,11,str(li["Qte"]),1)
        pdf.cell(35,11,f"{li['Prix']} F",1)
        pdf.cell(50,11,f"{li['Prix']*li['Qte']} F CFA",1,1)
    pdf.ln(4)
    pdf.set_font("Arial", '', 11)
    pdf.cell(0,7,f"Livraison ({vente.get('Zone','-')}): {vente.get('Livraison',0)} F CFA", new_x="LMARGIN", new_y="NEXT", align='R')
    pdf.set_font("Arial", 'B', 14)
    pdf.set_text_color(6,41,20)
    pdf.cell(0,12,f"TOTAL: {vente['Total']} F CFA - {vente['Paiement']}", new_x="LMARGIN", new_y="NEXT", align='R')
    pdf.ln(10)
    pdf.set_font("Arial", 'I', 8)
    pdf.set_text_color(100,100,100)
    pdf.cell(0,6,"Merci pour votre confiance - APGIV - Produits 100% Naturels", align='C')
    tmp = tempfile.NamedTemporaryFile(delete=False, suffix=".pdf")
    tmp.close()
    pdf.output(tmp.name)
    return tmp.name

def nettoyer_numero_tel(tel):
    tel = ''.join(filter(str.isdigit, str(tel)))
    if tel.startswith('0'):
        tel = '228' + tel[1:]
    if not tel.startswith('228') and len(tel)==8:
        tel = '228' + tel
    return tel

CAISSE_FILE = "caisse_journal.json"
LOG_FILE = "caisse_audit.log"
METHODS_CAISSE = ["Espèces", "Flooz", "TMoney", "Mixx"]
SEUIL_ALERTE_CAISSE = 50000

def _map_methode_caisse(methode_dashboard):
    if "Mixx" in str(methode_dashboard):
        return "Mixx"
    if methode_dashboard in METHODS_CAISSE:
        return methode_dashboard
    return "Espèces"

def load_caisse():
    if not os.path.exists(CAISSE_FILE):
        return {}
    try:
        with open(CAISSE_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception:
        return {}

def save_caisse(data):
    with open(CAISSE_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)

def log_action_caisse(action_type, details, user="Système"):
    try:
        line = f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S')} | {user} | {action_type} | {details}\n"
        with open(LOG_FILE, "a", encoding="utf-8") as f:
            f.write(line)
    except Exception:
        pass

def get_today_data_caisse(all_data, today_str):
    return all_data.get(today_str, {"ouverture": {m: 0 for m in METHODS_CAISSE}, "ventes_auto": {m: 0 for m in METHODS_CAISSE}, "ventes_manuelles": [], "depenses": [], "transferts": [], "ouverture_par": "", "heure_ouverture": "", "cloture": False, "heure_cloture": "", "cloture_par": "", "comptage_reel": {}, "ecarts": {}, "logs": []})

def add_log_caisse(today_data, action, user, montant=0, methode="", note=""):
    today_data["logs"].append({"heure": datetime.now().strftime("%H:%M:%S"), "user": user, "action": action, "montant": montant, "methode": methode, "note": note})
    log_action_caisse(action, f"{montant}F {methode} - {note}", user)

def sync_ventes_auto_caisse():
    today_str = str(date.today())
    all_data = load_caisse()
    today_data = get_today_data_caisse(all_data, today_str)
    ventes_auto = {m: 0 for m in METHODS_CAISSE}
    jour = datetime.now().strftime("%d/%m/%Y")
    for v in st.session_state.get("ventes", []):
        if jour in v.get("Date", ""):
            m = _map_methode_caisse(v.get("Paiement", "Espèces"))
            ventes_auto[m] += int(v.get("Total", 0))
    today_data["ventes_auto"] = ventes_auto
    all_data[today_str] = today_data
    save_caisse(all_data)
    return today_data

def _dates_de_periode(type_periode, ref_date):
    out = []
    if type_periode == "Journalier":
        out = [ref_date.isoformat()]
        lib = ref_date.strftime("%d/%m/%Y")
    elif type_periode == "Mensuel":
        y, m = ref_date.year, ref_date.month
        d = date(y, m, 1)
        while d.month == m:
            out.append(d.isoformat())
            d = date.fromordinal(d.toordinal() + 1)
        lib = ref_date.strftime("%m/%Y")
    else:
        for m in range(1, 13):
            d = date(ref_date.year, m, 1)
            while d.month == m:
                out.append(d.isoformat())
                d = date.fromordinal(d.toordinal() + 1)
        lib = str(ref_date.year)
    return out, lib

def calculer_stats_periode(all_data, type_periode, ref_date):
    dates_list, libelle = _dates_de_periode(type_periode, ref_date)
    total_ouverture = {m: 0 for m in METHODS_CAISSE}
    total_ventes_auto = {m: 0 for m in METHODS_CAISSE}
    total_ventes_man = {m: 0 for m in METHODS_CAISSE}
    total_depenses = {m: 0 for m in METHODS_CAISSE}
    nb_depenses = 0
    total_transferts = 0
    nb_jours = 0
    nb_clotures = 0
    total_ecarts = {m: 0 for m in METHODS_CAISSE}
    lignes_jours = []
    toutes_ops = []
    for ds in dates_list:
        d = all_data.get(ds)
        if not d:
            continue
        nb_jours += 1
        if d.get("cloture"):
            nb_clotures += 1
        for m in METHODS_CAISSE:
            total_ouverture[m] += int(d.get("ouverture", {}).get(m, 0))
            total_ventes_auto[m] += int(d.get("ventes_auto", {}).get(m, 0))
            total_ventes_man[m] += sum([v["montant"] for v in d.get("ventes_manuelles", []) if v["methode"] == m])
            total_depenses[m] += sum([x["montant"] for x in d.get("depenses", []) if x["methode"] == m])
            total_ecarts[m] += int(d.get("ecarts", {}).get(m, 0))
        nb_depenses += len(d.get("depenses", []))
        total_transferts += len(d.get("transferts", []))
        ventes_j = sum(d.get("ventes_auto", {}).values()) + sum([v["montant"] for v in d.get("ventes_manuelles", [])])
        dep_j = sum([x["montant"] for x in d.get("depenses", [])])
        ouv_j = sum(d.get("ouverture", {}).values())
        solde_j = ouv_j + ventes_j - dep_j
        lignes_jours.append({"Date": ds, "Ouverture": ouv_j, "Ventes": ventes_j, "Depenses": dep_j, "Solde jour": solde_j, "Cloture": "Oui" if d.get("cloture") else "Non"})
        for lg in d.get("logs", []):
            toutes_ops.append({"Date": ds, "Heure": lg.get("heure",""), "User": lg.get("user",""), "Action": lg.get("action",""), "Montant": lg.get("montant",0), "Methode": lg.get("methode",""), "Note": lg.get("note","")})
    total_ventes = sum(total_ventes_auto.values()) + sum(total_ventes_man.values())
    total_dep = sum(total_depenses.values())
    total_ouv = sum(total_ouverture.values())
    solde_theorique = total_ouv + total_ventes - total_dep
    benefice_estime = int(total_ventes * 0.42)
    return {"libelle": libelle, "dates": dates_list, "nb_jours": nb_jours, "nb_clotures": nb_clotures, "ouverture": total_ouverture, "total_ouverture": total_ouv, "ventes_auto": total_ventes_auto, "ventes_man": total_ventes_man, "total_ventes": total_ventes, "depenses": total_depenses, "total_depenses": total_dep, "nb_depenses": nb_depenses, "transferts_nb": total_transferts, "solde_theorique": solde_theorique, "ecarts": total_ecarts, "benefice_estime": benefice_estime, "lignes_jours": lignes_jours, "ops": toutes_ops}

def generer_rapport_pdf_caisse(type_periode, ref_date, stats, auteur=""):
    if not HAS_FPDF:
        return None
    pdf = FPDF()
    pdf.set_auto_page_break(auto=True, margin=15)
    pdf.add_page()
    if os.path.exists(LOGO_PATH):
        pdf.image(LOGO_PATH, x=10, y=8, w=38)
    pdf.set_font("Arial", 'B', 16)
    pdf.set_text_color(6,41,20)
    pdf.cell(0,12,'APGIV OS Gestion', new_x="LMARGIN", new_y="NEXT", align='C')
    pdf.set_font("Arial", 'B', 11)
    pdf.set_text_color(200,160,64)
    pdf.cell(0,7,"L'Excellence au Naturel", new_x="LMARGIN", new_y="NEXT", align='C')
    pdf.ln(4)
    pdf.set_font("Arial", 'B', 14)
    pdf.set_text_color(6,41,20)
    titre = {"Journalier": "RAPPORT JOURNALIER", "Mensuel": "RAPPORT MENSUEL", "Annuel": "RAPPORT ANNUEL"}[type_periode]
    pdf.cell(0,10, f"{titre} - COMPTABILITE CENTRALE", new_x="LMARGIN", new_y="NEXT", align='C')
    pdf.set_font("Arial", '', 11)
    pdf.set_text_color(0,0,0)
    pdf.cell(0,7, f"Periode : {stats['libelle']}  |  Edite le : {datetime.now().strftime('%d/%m/%Y %H:%M')}  |  Par : {auteur or 'APGIV'}", new_x="LMARGIN", new_y="NEXT", align='C')
    pdf.cell(0,7, f"Jours avec activite : {stats['nb_jours']}  |  Jours clotures : {stats['nb_clotures']}  |  Depenses : {stats['nb_depenses']}  |  Transferts : {stats['transferts_nb']}", new_x="LMARGIN", new_y="NEXT", align='C')
    pdf.ln(4)
    pdf.set_fill_color(6,41,20)
    pdf.set_text_color(255,255,255)
    pdf.set_font("Arial", 'B', 11)
    pdf.cell(0,10, "  CHIFFRES CLES", new_x="LMARGIN", new_y="NEXT", fill=True)
    pdf.set_text_color(0,0,0)
    pdf.set_font("Arial", '', 11)
    lignes_cles = [("Ouverture totale", stats['total_ouverture']), ("Ventes totales (Auto Dashboard + Manuelles)", stats['total_ventes']), ("  - Ventes Auto Dashboard", sum(stats['ventes_auto'].values())), ("  - Ventes Manuelles Caisse", sum(stats['ventes_man'].values())), ("Depenses totales", stats['total_depenses']), ("Solde theorique (Ouverture + Ventes - Depenses)", stats['solde_theorique']), ("Benefice estime 42% sur ventes", stats['benefice_estime'])]
    for lib, val in lignes_cles:
        pdf.cell(130,8, f"  {lib}", 1)
        pdf.cell(60,8, f"{val:,} F CFA", 1, 1, 'R')
    pdf.ln(4)
    pdf.set_fill_color(6,41,20)
    pdf.set_text_color(255,255,255)
    pdf.set_font("Arial", 'B', 11)
    pdf.cell(0,10, "  DETAIL PAR METHODE DE PAIEMENT", new_x="LMARGIN", new_y="NEXT", fill=True)
    pdf.set_text_color(255,255,255)
    pdf.cell(38,9, "Methode", 1, 0, 'C', True)
    pdf.cell(38,9, "Ouverture", 1, 0, 'C', True)
    pdf.cell(38,9, "Ventes", 1, 0, 'C', True)
    pdf.cell(38,9, "Depenses", 1, 0, 'C', True)
    pdf.cell(38,9, "Solde", 1, 1, 'C', True)
    pdf.set_text_color(0,0,0)
    pdf.set_font("Arial", '', 10)
    for m in METHODS_CAISSE:
        v = stats['ventes_auto'][m] + stats['ventes_man'][m]
        s = stats['ouverture'][m] + v - stats['depenses'][m]
        pdf.cell(38,8, m, 1)
        pdf.cell(38,8, f"{stats['ouverture'][m]:,} F", 1)
        pdf.cell(38,8, f"{v:,} F", 1)
        pdf.cell(38,8, f"{stats['depenses'][m]:,} F", 1)
        pdf.cell(38,8, f"{s:,} F", 1, 1)
    pdf.ln(4)
    if stats['lignes_jours']:
        pdf.set_fill_color(6,41,20)
        pdf.set_text_color(255,255,255)
        pdf.set_font("Arial", 'B', 11)
        pdf.cell(0,10, "  DETAIL PAR JOUR", new_x="LMARGIN", new_y="NEXT", fill=True)
        pdf.set_text_color(255,255,255)
        pdf.cell(32,9, "Date", 1, 0, 'C', True)
        pdf.cell(32,9, "Ouverture", 1, 0, 'C', True)
        pdf.cell(32,9, "Ventes", 1, 0, 'C', True)
        pdf.cell(32,9, "Depenses", 1, 0, 'C', True)
        pdf.cell(32,9, "Solde", 1, 0, 'C', True)
        pdf.cell(30,9, "Cloture", 1, 1, 'C', True)
        pdf.set_text_color(0,0,0)
        pdf.set_font("Arial", '', 10)
        for lj in stats['lignes_jours'][:40]:
            pdf.cell(32,8, lj["Date"], 1)
            pdf.cell(32,8, f"{lj['Ouverture']:,} F", 1)
            pdf.cell(32,8, f"{lj['Ventes']:,} F", 1)
            pdf.cell(32,8, f"{lj['Depenses']:,} F", 1)
            pdf.cell(32,8, f"{lj['Solde jour']:,} F", 1)
            pdf.cell(30,8, lj["Cloture"], 1, 1)
    pdf.ln(4)
    pdf.set_fill_color(6,41,20)
    pdf.set_text_color(255,255,255)
    pdf.set_font("Arial", 'B', 11)
    pdf.cell(0,10, "  ECARTS DE CLOTURE (Reel - Theorique)", new_x="LMARGIN", new_y="NEXT", fill=True)
    pdf.set_text_color(0,0,0)
    pdf.set_font("Arial", '', 11)
    for m in METHODS_CAISSE:
        pdf.cell(0,7, f"  {m} : {stats['ecarts'][m]:,} F", new_x="LMARGIN", new_y="NEXT")
    pdf.ln(4)
    if stats['ops']:
        pdf.set_fill_color(6,41,20)
        pdf.set_text_color(255,255,255)
        pdf.set_font("Arial", 'B', 11)
        pdf.cell(0,10, "  JOURNAL DES OPERATIONS (100 premieres)", new_x="LMARGIN", new_y="NEXT", fill=True)
        pdf.set_text_color(255,255,255)
        pdf.cell(28,9, "Date", 1, 0, 'C', True)
        pdf.cell(18,9, "Heure", 1, 0, 'C', True)
        pdf.cell(32,9, "Action", 1, 0, 'C', True)
        pdf.cell(28,9, "Montant", 1, 0, 'C', True)
        pdf.cell(24,9, "Methode", 1, 0, 'C', True)
        pdf.cell(60,9, "Note", 1, 1, 'C', True)
        pdf.set_text_color(0,0,0)
        pdf.set_font("Arial", '', 9)
        for op in stats['ops'][:100]:
            pdf.cell(28,7, op["Date"], 1)
            pdf.cell(18,7, op["Heure"], 1)
            pdf.cell(32,7, op["Action"][:18], 1)
            pdf.cell(28,7, f"{op['Montant']:,} F", 1)
            pdf.cell(24,7, op["Methode"][:12], 1)
            pdf.cell(60,7, (op["Note"] or "")[:35], 1, 1)
    pdf.ln(8)
    pdf.set_font("Arial", 'I', 8)
    pdf.set_text_color(100,100,100)
    pdf.cell(0,6, "APGIV - Ango Power Group International Vision - L'Excellence au Naturel - Rapport genere par APGIV OS Gestion", align='C')
    tmp = tempfile.NamedTemporaryFile(delete=False, suffix=".pdf")
    tmp.close()
    pdf.output(tmp.name)
    return tmp.name

INVENTAIRE_FILE = "inventaire_historique.json"

def save_historique_inventaire(entree):
    hist = []
    if os.path.exists(INVENTAIRE_FILE):
        try:
            with open(INVENTAIRE_FILE, "r", encoding="utf-8") as f:
                hist = json.load(f)
        except Exception:
            hist = []
    hist.append(entree)
    with open(INVENTAIRE_FILE, "w", encoding="utf-8") as f:
        json.dump(hist, f, indent=2, ensure_ascii=False)

def charger_historique_inventaire():
    if not os.path.exists(INVENTAIRE_FILE):
        return []
    try:
        with open(INVENTAIRE_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception:
        return []

def detecter_anomalies_inventaire(df_stock):
    anomalies = []
    for _, r in df_stock.iterrows():
        nom = str(r["Produit"])
        lot = str(r.get("Lot", "-"))
        perm = str(r.get("Peremption", "-"))
        stock_val = int(r["Stock"])
        prix_val = int(r["Prix"])
        if lot == "-" or lot == "" or lot.lower() == "nan":
            anomalies.append({"Produit": nom, "Probleme": "Pas de Lot", "Gravite": "Faible"})
        if perm == "-" or perm == "" or perm.lower() == "nan":
            anomalies.append({"Produit": nom, "Probleme": "Pas de Peremption", "Gravite": "Faible"})
        if stock_val == 0:
            anomalies.append({"Produit": nom, "Probleme": "Stock a 0 - Rupture", "Gravite": "Forte"})
        if prix_val == 0:
            anomalies.append({"Produit": nom, "Probleme": "Prix a 0", "Gravite": "Forte"})
        if stock_val < 0:
            anomalies.append({"Produit": nom, "Probleme": "Stock negatif", "Gravite": "Forte"})
    return anomalies

with st.sidebar:
    if os.path.exists(LOGO_PATH):
        st.image(LOGO_PATH, width='stretch')
    st.markdown("<div style='height:12px'></div>", unsafe_allow_html=True)
    menu = st.radio("NAVIGATION", ["Dashboard", "Magasin & Restockage", "Clients & Livraison", "Codes Agents", "MLM & Reseau", "Temoignages Clients", "Inventaire", "Comptabilite Centrale", "Compta Privee"], label_visibility="collapsed")
    if st.button("🔄 Recharger Supabase"):
        st.session_state.stock = charger_produits_supabase()
        st.session_state.agents = charger_agents_supabase()
        st.session_state.temoignages = charger_temoignages_supabase()
        st.session_state.clients = charger_clients_supabase()
        st.session_state.zones = charger_zones_supabase()
        st.rerun()
    st.caption(f"Connecte : {st.session_state.get('user','')} | Role : {st.session_state.get('role','')}")

st.markdown(f"""
<div class="apgiv-header-final">
    <div class="apgiv-logo-box"><img src="data:image/jpeg;base64,{logo_b64}" /></div>
    <div class="apgiv-header-content">
        <div class="apgiv-title-line"><span class="apgiv-title-os">APGIV OS</span><span class="apgiv-title-gestion">Gestion</span></div>
        <div class="apgiv-slogan">L'Excellence au Naturel - {datetime.now().strftime('%d/%m/%Y %H:%M')}</div>
    </div>
    <div class="apgiv-waves"><div class="wave wave-3"></div><div class="wave wave-1"></div><div class="wave wave-2"></div></div>
</div>
""", unsafe_allow_html=True)

df_stock = pd.DataFrame(st.session_state.stock)

if menu == "Dashboard":
    mois_actuel = datetime.now().strftime("%m/%Y")
    ventes_mois = [v for v in st.session_state.ventes if mois_actuel in v.get("Date", "")]
    top_mois_nom = "— Aucune vente —"
    top_mois_ca = 0
    if ventes_mois:
        df_mois = pd.DataFrame(ventes_mois)
        classement_mois = df_mois.groupby("Agent")["Total"].sum().sort_values(ascending=False)
        top_mois_nom = str(classement_mois.index[0])
        top_mois_ca = int(classement_mois.iloc[0])
    jour_actuel = datetime.now().strftime("%d/%m/%Y")
    ventes_jour = [v for v in st.session_state.ventes if jour_actuel in v.get("Date", "")]
    top_jour_nom = "— Aucune vente —"
    if ventes_jour:
        df_jour = pd.DataFrame(ventes_jour)
        classement_jour = df_jour.groupby("Agent")["Total"].sum().sort_values(ascending=False)
        top_jour_nom = str(classement_jour.index[0])
    k1,k2,k3,k4 = st.columns(4, gap="medium")
    with k1:
        st.markdown(f"""<div class="kpi-card kpi-ventes"><div class="kpi-icon kpi-icon-ventes">📅</div><div style="flex:1"><div style="font-size:12px; font-weight:700">VENTES JOUR</div><div style="font-size:28px; font-weight:900">{len(ventes_jour)}</div><div style="font-size:12px; color:{OR}; font-weight:700">● Temps reel</div></div></div>""", unsafe_allow_html=True)
    with k2:
        alerte = len([s for s in st.session_state.stock if s['Stock']<20])
        st.markdown(f"""<div class="kpi-card kpi-alerte"><div class="kpi-icon kpi-icon-alerte">⚠</div><div style="flex:1"><div style="font-size:12px; font-weight:700">STOCK ALERTE</div><div style="font-size:26px; font-weight:900">{alerte} Lots</div><div style="font-size:12px; color:#EF4444; font-weight:700">● Action requise</div></div></div>""", unsafe_allow_html=True)
    with k3:
        st.markdown(f"""<div class="kpi-card kpi-top"><div class="kpi-icon kpi-icon-top">🏆</div><div style="flex:1"><div style="font-size:12px; font-weight:700">AGENT TOP JOUR</div><div style="font-size:22px; font-weight:900">{top_jour_nom}</div><div style="font-size:12px; color:{VERT}; font-weight:700">★ Meilleur aujourd'hui</div></div></div>""", unsafe_allow_html=True)
    with k4:
        st.markdown(f"""<div class="kpi-card kpi-top"><div class="kpi-icon kpi-icon-top">🥇</div><div style="flex:1"><div style="font-size:12px; font-weight:700">MEILLEUR VENDEUR DU MOIS</div><div style="font-size:22px; font-weight:900">{top_mois_nom}</div><div style="font-size:12px; color:{OR}; font-weight:700">● {top_mois_ca} F ce mois</div></div></div>""", unsafe_allow_html=True)
    st.markdown(f"""<div class="section-header"><div class="section-header-gold-bar"></div><div style="font-size:20px">📦</div><div style="color:white; font-weight:900; font-size:15px; letter-spacing:0.8px">STOCK & PEREMPTION - VUE GENERALE</div></div>""", unsafe_allow_html=True)
    st.dataframe(df_stock, width='stretch', hide_index=True, height=220)
    st.markdown("**✏ Agir sur un produit**")
    if st.session_state.stock:
        p_sel = st.selectbox("Choisir un produit :", ["-- Choisir --"] + [f"{s['Produit']} (Stock : {s['Stock']})" for s in st.session_state.stock], key="act_stock")
        if p_sel != "-- Choisir --":
            prod_act = next(s for s in st.session_state.stock if f"{s['Produit']} (Stock : {s['Stock']})" == p_sel)
            a1, a2, a3 = st.columns(3)
            with a1:
                nouveau_prix = st.number_input("Nouveau Prix", min_value=0, value=int(prod_act["Prix"]), key="act_prix")
            with a2:
                nouveau_stock = st.number_input("Nouveau Stock", min_value=0, value=int(prod_act["Stock"]), key="act_stock_val")
            with a3:
                st.write("")
                if st.button("💾 Modifier ce produit", key="btn_mod_prod"):
                    if prod_act.get("id"):
                        supa_update("produits", "id", prod_act["id"], {"prix_fcfa": int(nouveau_prix), "stock_actuel": int(nouveau_stock)})
                    prod_act["Prix"] = int(nouveau_prix)
                    prod_act["Stock"] = int(nouveau_stock)
                    st.success(f"{prod_act['Produit']} modifié !")
                    st.rerun()
                if st.button("🗑 Supprimer ce produit", key="btn_del_prod"):
                    if prod_act.get("id"):
                        supa_delete("produits", "id", prod_act["id"])
                    st.session_state.stock = [s for s in st.session_state.stock if s["Produit"] != prod_act["Produit"]]
                    st.success(f"{prod_act['Produit']} supprimé !")
                    st.rerun()
    st.markdown(f"""<div class="section-header" style="background: linear-gradient(90deg, {VERT} 0%, {VERT_FONCE} 60%, {OR} 100%);"><div class="section-header-gold-bar"></div><div style="color:white; font-weight:800; font-size:14px">CAISSE INTELLIGENTE - VENTE + LIVRAISON + FACTURE PDF + Envoie WhatsApp</div></div>""", unsafe_allow_html=True)
    col1,col2 = st.columns(2, gap="large")
    with col1:
        produit_sel = st.selectbox("Produit *", [s["Produit"] for s in st.session_state.stock])
        prod_info = next(s for s in st.session_state.stock if s["Produit"]==produit_sel)
        st.text_input("Prix Unitaire (auto)", value=f"{prod_info['Prix']} F", disabled=True)
        st.text_input("Lot (auto)", value=prod_info["Lot"], disabled=True)
        st.text_input("Peremption (auto)", value=prod_info["Peremption"], disabled=True)
        st.caption(f"Stock dispo pour {produit_sel} : {prod_info['Stock']} unites")
        quantite = st.number_input("Quantité *", min_value=1, max_value=999, value=1, key=f"qte_{produit_sel}")
        if quantite > prod_info["Stock"]:
            st.error(f"Stock insuffisant ! Il ne reste que {prod_info['Stock']} pour {produit_sel}")
        mode_paiement = st.selectbox("Mode Paiement *", ["Espèces", "Mixx by Yas", "Flooz"])
        zone_sel = st.selectbox("Zone de livraison *", [z["Nom"] for z in st.session_state.zones])
        if st.button("➕ Ajouter au panier", width='stretch'):
            if quantite > prod_info["Stock"]:
                st.error("Stock insuffisant")
            else:
                st.session_state.panier.append({"Produit": produit_sel, "Prix": prod_info["Prix"], "Qte": quantite, "Lot": prod_info["Lot"], "id": prod_info.get("id")})
                st.success(f"{produit_sel} x{quantite} ajouté au panier")
                st.rerun()
    with col2:
        nom_agent = st.text_input("Nom Agent Vendeur *", placeholder="Koffi")
        code_agent = st.text_input("Code Agent *", placeholder="APG-001")
        choix_client = st.selectbox("Client *", ["-- Nouveau client --"] + [c["Nom"] for c in st.session_state.clients])
        if choix_client == "-- Nouveau client --":
            client_nom = st.text_input("Nom Client *", placeholder="M. Kodjo")
            client_tel = st.text_input("Téléphone Client *", placeholder="90 12 34 56")
        else:
            c_ex = next(c for c in st.session_state.clients if c["Nom"]==choix_client)
            client_nom = c_ex["Nom"]
            client_tel = st.text_input("Téléphone Client *", value=c_ex.get("Telephone",""))
            st.caption(f"Quartier : {c_ex.get('Quartier','')} - {c_ex.get('Ville','')}")
        sous_total = sum(item["Prix"] * item["Qte"] for item in st.session_state.panier) if st.session_state.panier else 0
        frais_liv, msg_liv = calculer_livraison(zone_sel, sous_total, st.session_state.zones)
        total_vente = sous_total + frais_liv
        st.markdown(f"<div style='background:white; border:2.5px solid {VERT}; border-radius:14px; padding:16px; text-align:center'><p style='margin:0; font-size:11px; font-weight:700'>TOTAL A PAYER</p><p style='margin:0; font-size:30px; font-weight:900; color:{VERT_FONCE}'>{total_vente} F</p><p style='margin:0; font-size:11px; color:#667085'>Produits : {sous_total} F + Livraison : {frais_liv} F</p><p style='margin:4px 0 0 0; font-size:11px; color:{VERT}; font-weight:700'>{msg_liv}</p></div>", unsafe_allow_html=True)
        can_sell = all([nom_agent.strip(), code_agent.strip(), client_nom.strip(), client_tel.strip()]) and len(st.session_state.panier) > 0
        code_valide = any(a["Code"]==code_agent and a["Nom"].lower()==nom_agent.lower() for a in st.session_state.agents)
        if nom_agent and code_agent and not code_valide:
            st.warning("Code agent non reconnu - Voir Codes Agents")
            can_sell = False
        if st.button("✅ Confirmer Vente + Générer Facture", disabled=not can_sell, width='stretch', type="primary"):
            for item in st.session_state.panier:
                for s in st.session_state.stock:
                    if s["Produit"] == item["Produit"]:
                        s["Stock"] -= item["Qte"]
                        if s.get("id"):
                            try:
                                supa_update_stock(s["id"], s["Stock"])
                            except Exception:
                                pass
            vente = {"Date": datetime.now().strftime("%d/%m/%Y %H:%M"), "Produit": ", ".join([f"{i['Produit']} x{i['Qte']}" for i in st.session_state.panier]), "Qte": sum(i["Qte"] for i in st.session_state.panier), "SousTotal": sous_total, "Livraison": frais_liv, "Zone": zone_sel, "Total": total_vente, "Paiement": mode_paiement, "Agent": nom_agent, "Code": code_agent, "Lot": st.session_state.panier[0]["Lot"], "Client": client_nom, "Telephone": client_tel, "Lignes": list(st.session_state.panier)}
            st.session_state.ventes.append(vente)
            st.session_state.derniere_vente = vente
            for a in st.session_state.agents:
                if a["Code"]==code_agent:
                    a["Commission"] += int(total_vente * 0.10)
                    try:
                        if a.get("id"):
                            supa_update("agents", "id", a["id"], {"commission_fcfa": int(a["Commission"])})
                    except Exception:
                        pass
            if choix_client == "-- Nouveau client --":
                try:
                    supa_insert("clients", {"nom": client_nom, "telephone": client_tel, "quartier": "", "ville": "Lome", "type_client": "Particulier"})
                    st.session_state.clients = charger_clients_supabase()
                except Exception:
                    pass
            try:
                cmd = supa_insert("commandes", {"numero": f"APG-{datetime.now().strftime('%Y%m%d%H%M%S')}", "canal": "siege", "statut": "payee", "sous_total_fcfa": sous_total, "frais_livraison_fcfa": frais_liv, "total_fcfa": total_vente, "adresse": f"{client_nom} - {zone_sel}"})
                for item in st.session_state.panier:
                    supa_insert("lignes_commande", {"commande_id": cmd["id"], "produit_id": item.get("id"), "quantite": item["Qte"], "prix_unitaire_fcfa": item["Prix"]})
                supa_insert("paiements", {"commande_id": cmd["id"], "montant_fcfa": total_vente, "methode": mode_paiement, "reference": f"{code_agent}-{datetime.now().strftime('%H%M%S')}"})
            except Exception as e:
                st.warning(f"Vente sauvée en local, Supabase : {e}")
            st.session_state.panier = []
            sync_ventes_auto_caisse()
            st.success(f"Vente confirmée pour {client_nom} - {len(vente['Lignes'])} produits - Total {total_vente} F")
            st.rerun()
        if st.session_state.derniere_vente:
            v = st.session_state.derniere_vente
            pdf_path = generer_facture_pdf(v)
            if pdf_path:
                with open(pdf_path, "rb") as f:
                    st.download_button("📄 Télécharger Facture Pro PDF avec Logo Officiel", data=f, file_name=f"Facture_{v['Client']}.pdf", mime="application/pdf", width='stretch')
            tel_clean = nettoyer_numero_tel(v.get('Telephone',''))
            msg = f"Bonjour {v['Client']} - Merci chez APGIV OS Gestion - {v['Produit']} x{v['Qte']} = {v['SousTotal']}F + Livraison {v['Livraison']}F = Total {v['Total']}F CFA - Zone {v['Zone']} - Paiement {v['Paiement']}. Votre facture PDF avec logo officiel est prete. L'Excellence au Naturel"
            wa_link = f"https://wa.me/{tel_clean}?text={urllib.parse.quote(msg)}"
            st.link_button(f"📱 Envoyer Facture - {v['Telephone']}", wa_link, width='stretch')
    if st.session_state.panier:
        st.markdown("### 🛒 Panier du client")
        st.dataframe(pd.DataFrame(st.session_state.panier), width='stretch', hide_index=True)
        if st.button("🗑 Vider le panier"):
            st.session_state.panier = []
            st.rerun()
    if st.session_state.ventes:
        st.markdown(f"""<div class="section-header"><div class="section-header-gold-bar"></div><div style="color:white; font-weight:800; font-size:13px">JOURNAL DES VENTES - FACTURE</div></div>""", unsafe_allow_html=True)
        st.dataframe(pd.DataFrame(st.session_state.ventes), width='stretch', hide_index=True)

elif menu == "Magasin & Restockage":
    st.markdown(f'<div class="section-header"><div class="section-header-gold-bar"></div><div style="color:white; font-weight:800">MAGASIN & RESTOCKAGE</div></div>', unsafe_allow_html=True)
    tab1, tab2, tab3 = st.tabs(["Stock General", "Restockage Securise", "Nouveau Produit"])
    with tab1:
        st.dataframe(df_stock, width='stretch', hide_index=True)
    with tab2:
        r1,r2 = st.columns(2)
        with r1:
            restock_agent = st.text_input("Agent Restockage *")
            restock_code = st.text_input("Code *")
            fournisseur = st.text_input("Fournisseur *")
        with r2:
            prod_restock = st.selectbox("Produit *", [s["Produit"] for s in st.session_state.stock])
            qte_restock = st.number_input("Qte Entree *", min_value=1, value=10)
            lot_restock = st.text_input("Lot *", placeholder="RD-25-05")
        if st.button("Ajouter Produit / Lot", type="primary"):
            prod = next((s for s in st.session_state.stock if s["Produit"]==prod_restock), None)
            if prod:
                prod["Stock"] += qte_restock
                prod["Lot"]=lot_restock
                try:
                    if prod.get("id"):
                        supa_update_stock(prod["id"], prod["Stock"])
                except Exception as e:
                    st.warning(f"Restockage local OK, Supabase : {e}")
            st.success("Restockage OK")
            st.rerun()
        st.divider()
        st.markdown("**✏ Modifier un lot / un restockage**")
        if st.session_state.stock:
            p_rest = st.selectbox("Choisir un produit à corriger :", ["-- Choisir --"] + [s["Produit"] for s in st.session_state.stock], key="mod_restock_prod")
            if p_rest != "-- Choisir --":
                prod_r = next(s for s in st.session_state.stock if s["Produit"] == p_rest)
                rmod1, rmod2, rmod3 = st.columns(3)
                with rmod1:
                    nouveau_lot = st.text_input("Nouveau Lot", value=prod_r.get("Lot",""), key="mod_lot_restock")
                with rmod2:
                    nouvelle_peremption = st.text_input("Nouvelle Péremption", value=prod_r.get("Peremption",""), key="mod_peremption_restock")
                with rmod3:
                    nouveau_stock_restock = st.number_input("Nouveau Stock", min_value=0, value=int(prod_r["Stock"]), key="mod_stock_restock")
                c_mod1, c_mod2 = st.columns(2)
                with c_mod1:
                    if st.button("💾 Modifier ce lot", type="primary", key="btn_mod_restock"):
                        try:
                            if prod_r.get("id"):
                                supa_update("produits", "id", prod_r["id"], {"lot": nouveau_lot, "peremption": nouvelle_peremption, "stock_actuel": int(nouveau_stock_restock)})
                            prod_r["Lot"] = nouveau_lot
                            prod_r["Peremption"] = nouvelle_peremption
                            prod_r["Stock"] = int(nouveau_stock_restock)
                            st.success(f"Lot {prod_r['Produit']} modifié")
                            st.rerun()
                        except Exception as e:
                            st.error(f"Erreur : {e}")
                with c_mod2:
                    if st.button("🗑 Supprimer ce produit du magasin", key="btn_del_restock"):
                        try:
                            if prod_r.get("id"):
                                supa_delete("produits", "id", prod_r["id"])
                        except Exception:
                            pass
                        st.session_state.stock = [s for s in st.session_state.stock if s["Produit"] != prod_r["Produit"]]
                        st.success(f"{prod_r['Produit']} supprimé du magasin !")
                        st.rerun()
    with tab3:
        n_nom = st.text_input("Nom du nouveau produit *")
        n_prix = st.number_input("Prix FCFA *", min_value=100, value=10000, step=500)
        n_stock = st.number_input("Stock initial *", min_value=0, value=20)
        n_lot = st.text_input("Lot", placeholder="AP-25-01")
        n_peremption = st.text_input("Peremption", placeholder="01/2027")
        if st.button("Creer produit dans Supabase", type="primary"):
            if n_nom:
                try:
                    supa_insert("produits", {"nom": n_nom, "prix_fcfa": int(n_prix), "stock_actuel": int(n_stock), "lot": n_lot, "peremption": n_peremption, "actif": True})
                    st.session_state.stock = charger_produits_supabase()
                    st.success(f"{n_nom} cree dans Supabase !")
                    st.rerun()
                except Exception as e:
                    st.error(f"Erreur Supabase : {e}")
            else:
                st.error("Nom obligatoire")

elif menu == "Clients & Livraison":
    st.markdown(f'<div class="section-header"><div class="section-header-gold-bar"></div><div style="color:white; font-weight:800">CLIENTS & LIVRAISON - FICHIER CLIENTS + ZONES</div></div>', unsafe_allow_html=True)
    t1,t2 = st.tabs(["Liste Clients", "Nouveau Client + Zones"])
    with t1:
        st.dataframe(pd.DataFrame(st.session_state.clients), width='stretch', hide_index=True)
        st.divider()
        st.markdown("**✏ Agir sur un client**")
        if st.session_state.clients:
            c_sel = st.selectbox("Choisir un client :", ["-- Choisir --"] + [f"{c['Nom']} ({c.get('Telephone','')})" for c in st.session_state.clients], key="act_client")
            if c_sel != "-- Choisir --":
                cli_act = next(c for c in st.session_state.clients if f"{c['Nom']} ({c.get('Telephone','')})" == c_sel)
                cc1, cc2 = st.columns(2)
                with cc1:
                    if st.button("🗑 Supprimer ce client", key="btn_del_client"):
                        if cli_act.get("id"):
                            supa_delete("clients", "id", cli_act["id"])
                        st.session_state.clients = [c for c in st.session_state.clients if c["Nom"] != cli_act["Nom"]]
                        st.success(f"{cli_act['Nom']} supprimé !")
                        st.rerun()
                with cc2:
                    nouveau_tel_cli = st.text_input("Nouveau Téléphone", value=cli_act.get("Telephone",""), key="act_tel_client")
                    if st.button("💾 Modifier téléphone", key="btn_mod_client"):
                        if cli_act.get("id"):
                            supa_update("clients", "id", cli_act["id"], {"telephone": nouveau_tel_cli})
                        cli_act["Telephone"] = nouveau_tel_cli
                        st.success("Téléphone modifié !")
                        st.rerun()
        st.markdown("**✏ Agir sur une zone de livraison**")
        if st.session_state.zones:
            z_sel = st.selectbox("Choisir une zone :", ["-- Choisir --"] + [z["Nom"] for z in st.session_state.zones], key="act_zone")
            if z_sel != "-- Choisir --":
                zone_act = next(z for z in st.session_state.zones if z["Nom"] == z_sel)
                nouveau_frais = st.number_input("Nouveaux Frais", min_value=0, value=int(zone_act["Frais"]), key="act_frais_zone")
                if st.button("💾 Modifier les frais", key="btn_mod_zone"):
                    if zone_act.get("id"):
                        supa_update("zones_livraison", "id", zone_act["id"], {"frais_fcfa": int(nouveau_frais)})
                    zone_act["Frais"] = int(nouveau_frais)
                    st.success(f"Frais {zone_act['Nom']} modifiés !")
                    st.rerun()
        st.markdown("**Zones de livraison APGIV**")
        st.dataframe(pd.DataFrame(st.session_state.zones), width='stretch', hide_index=True)
        st.info("Regle : Grand Lome = 1 000 F / 24h - OFFERT des 50 000 F | Peripherie = 1 500 F / 24-48h | Autres villes = 2 500 F / 48-72h | Sous-region = Sur devis / 3-7 jours | Retrait Siege = Gratuit")
    with t2:
        c1,c2 = st.columns(2)
        with c1:
            cl_nom = st.text_input("Nom client *")
            cl_tel = st.text_input("Telephone *", placeholder="90 12 34 56")
            cl_quartier = st.text_input("Quartier", placeholder="Agoe")
        with c2:
            cl_ville = st.selectbox("Ville", ["Lome", "Atakpame", "Kara", "Sokode", "Dapaong", "Kpalime", "Autre"])
            cl_type = st.selectbox("Type", ["particulier", "distributeur", "revendeur", "grossiste"])
            if st.button("Creer Client", type="primary", width='stretch'):
                if cl_nom and cl_tel:
                    try:
                        supa_insert("clients", {"nom": cl_nom, "telephone": cl_tel, "quartier": cl_quartier, "ville": cl_ville, "type": cl_type})
                        st.session_state.clients = charger_clients_supabase()
                        st.success(f"Client {cl_nom} cree !")
                        st.rerun()
                    except Exception as e:
                        st.error(f"Erreur : {e}")
                else:
                    st.error("Nom + Telephone obligatoires")
        st.divider()
        st.markdown("**Simulateur livraison**")
        sim_total = st.number_input("Montant commande pour test", min_value=0, value=60000, step=5000)
        sim_zone = st.selectbox("Zone test", [z["Nom"] for z in st.session_state.zones])
        f, m = calculer_livraison(sim_zone, sim_total, st.session_state.zones)
        st.success(f"{m} | Total avec livraison : {sim_total + f} F")

elif menu == "Codes Agents":
    st.markdown(f'<div class="section-header"><div class="section-header-gold-bar"></div><div style="color:white; font-weight:800">CODES AGENTS - VENDEURS BOUTIQUE + AGENTS MLM</div></div>', unsafe_allow_html=True)
    boutique = [a for a in st.session_state.agents if (a.get("Type") or "MLM") == "Boutique"]
    mlm = [a for a in st.session_state.agents if (a.get("Type") or "MLM") == "MLM"]
    cb1, cb2, cb3 = st.columns(3)
    with cb1:
        st.metric("👥 Total Codes", len(st.session_state.agents))
    with cb2:
        st.metric("🏪 Vendeurs Boutique", len(boutique))
    with cb3:
        st.metric("🌐 Agents MLM", len(mlm))
    tab_tous, tab_boutique, tab_mlm = st.tabs(["Tous les codes", "🏪 Vendeurs Boutique", "🌐 Agents MLM"])
    with tab_tous:
        st.dataframe(pd.DataFrame(st.session_state.agents), width='stretch', hide_index=True)
        st.caption("Boutique = vend au siège, pas de parrain, pas de filleuls. MLM = parrain + filleuls + niveau.")
        st.markdown("**✏ Modifier un code**")
        if st.session_state.agents:
            a_mod = st.selectbox("Choisir un agent à modifier :", ["-- Choisir --"] + [f"{a['Nom']} ({a['Code']})" for a in st.session_state.agents], key="mod_agent_tous")
            if a_mod != "-- Choisir --":
                ag_act = next(a for a in st.session_state.agents if f"{a['Nom']} ({a['Code']})" == a_mod)
                nouveau_code = st.text_input("Nouveau Code", value=ag_act["Code"], key="mod_code_agent")
                nouveau_niveau_ag = st.selectbox("Nouveau Niveau", ["Starter", "Distributeur", "Leader", "Vendeur Boutique"], index=0, key="mod_niveau_agent")
                if st.button("💾 Modifier cet agent", key="btn_mod_agent_tous"):
                    if ag_act.get("id"):
                        supa_update("agents", "id", ag_act["id"], {"code": nouveau_code, "niveau": nouveau_niveau_ag})
                    ag_act["Code"] = nouveau_code
                    ag_act["Niveau"] = nouveau_niveau_ag
                    st.success(f"{ag_act['Nom']} modifié !")
                    st.rerun()
        st.divider()
        st.markdown("**🗑 Supprimer un code de test**")
        if st.session_state.agents:
            a_suppr = st.selectbox("Supprimer un code (test) :", ["-- Choisir --"] + [f"{a['Nom']} ({a['Code']})" for a in st.session_state.agents], key="suppr_agent_tous")
            if a_suppr != "-- Choisir --" and st.button("🗑 Supprimer ce code", key="btn_suppr_agent_tous"):
                a_del = next(a for a in st.session_state.agents if f"{a['Nom']} ({a['Code']})" == a_suppr)
                if a_del.get("id"):
                    try:
                        supa_delete("agents", "id", a_del["id"])
                    except Exception as e:
                        st.error(f"Erreur Supabase : {e}")
                st.session_state.agents = [a for a in st.session_state.agents if a["Code"] != a_del["Code"]]
                st.success(f"{a_del['Nom']} supprimé !")
                st.rerun()
    with tab_boutique:
        st.markdown("**Vendeurs Boutique — vente au siège Dékon, commission 10% sur ses ventes directes**")
        if boutique:
            st.dataframe(pd.DataFrame(boutique), width='stretch', hide_index=True)
        else:
            st.info("Aucun vendeur boutique pour le moment.")
    with tab_mlm:
        st.markdown("**Agents MLM — réseau, parrainage, niveau Starter / Distributeur / Leader**")
        if mlm:
            st.dataframe(pd.DataFrame(mlm), width='stretch', hide_index=True)
            for agent in mlm:
                filleuls = [a["Nom"] for a in st.session_state.agents if a.get("Parrain") == agent["Nom"]]
                if filleuls:
                    st.write(f"👑 **{agent['Nom']} ({agent['Niveau']})** → {', '.join(filleuls)} | Commission: {agent['Commission']} F")
        else:
            st.info("Aucun agent MLM pour le moment.")
    st.divider()
    c1, c2 = st.columns(2)
    with c1:
        if st.session_state.ventes:
            df_v = pd.DataFrame(st.session_state.ventes)
            best = df_v.groupby("Agent")["Total"].sum().sort_values(ascending=False)
            st.markdown("**Performance par vendeur**")
            st.bar_chart(best, width='stretch')
        else:
            st.info("Aucune vente pour le graphique.")
    with c2:
        st.markdown("**Créer un nouveau code**")
        new_type = st.selectbox("Type *", ["Boutique", "MLM"])
        new_nom = st.text_input("Nouveau Nom Agent / Vendeur")
        new_code = st.text_input("Code Unique", placeholder="APG-005")
        new_tel = st.text_input("Téléphone", placeholder="90 12 34 56")
        if new_type == "Boutique":
            new_boutique = st.selectbox("Boutique", ["Siège Dékon", "Boutique Agoè", "Boutique Autre"])
            new_parrain = "Siège"
            new_niveau = "Vendeur Boutique"
        else:
            new_boutique = "Siège Dékon"
            new_parrain = st.selectbox("Parrain", [a["Nom"] for a in st.session_state.agents] + ["Boss"])
            new_niveau = st.selectbox("Niveau", ["Starter", "Distributeur", "Leader"])
        if st.button("Attribuer Code", width='stretch'):
            if new_nom and new_code:
                if any(a["Code"] == new_code for a in st.session_state.agents):
                    st.error(f"Code {new_code} déjà utilisé !")
                else:
                    try:
                        supa_insert("agents", {"nom": new_nom, "code": new_code, "type_agent": new_type, "niveau": new_niveau, "parrain": new_parrain, "telephone": new_tel, "boutique": new_boutique, "commission_fcfa": 0})
                    except Exception:
                        supa_insert("agents", {"nom": new_nom, "code": new_code, "niveau": new_niveau, "parrain": new_parrain, "commission_fcfa": 0})
                    st.session_state.agents = charger_agents_supabase()
                    st.success(f"{new_type} {new_nom} créé : {new_code} !")
                    st.rerun()
            else:
                st.error("Nom + Code obligatoires")

elif menu == "MLM & Reseau":
    st.markdown(f'<div class="section-header"><div class="section-header-gold-bar"></div><div style="color:white; font-weight:800">MLM & RESEAU - GESTION COMPLETE</div></div>', unsafe_allow_html=True)
    agents_mlm = [a for a in st.session_state.agents if (a.get("Type") or "MLM") == "MLM"]
    ordre_niveau = {"Leader": 0, "Distributeur": 1, "Starter": 2, "Vendeur Boutique": 3}
    agents_mlm = sorted(agents_mlm, key=lambda a: (ordre_niveau.get(a.get("Niveau","Starter"), 9), (a.get("Nom") or "").lower()))
    m1, m2, m3, m4 = st.columns(4)
    with m1:
        st.metric("🌐 Agents MLM", len(agents_mlm))
    with m2:
        st.metric("👑 Leaders", len([a for a in agents_mlm if a.get("Niveau") == "Leader"]))
    with m3:
        st.metric("📦 Distributeurs", len([a for a in agents_mlm if a.get("Niveau") == "Distributeur"]))
    with m4:
        st.metric("🌱 Starters", len([a for a in agents_mlm if a.get("Niveau") == "Starter"]))
    if agents_mlm:
        if st.button("🗑 Vider tout le tableau MLM", width='stretch'):
            for a in list(agents_mlm):
                try:
                    if a.get("id"):
                        supa_delete("agents", "id", a["id"])
                except Exception:
                    pass
            st.session_state.agents = []
            st.success("Tableau MLM vidé !")
            st.rerun()
    else:
        st.info("Tableau MLM vide — prêt à remplir.")
    st.markdown("**Tableau MLM — ordonné par Niveau puis par Nom**")
    if agents_mlm:
        df_mlm = pd.DataFrame(agents_mlm)
        cols_ordre = [c for c in ["Code", "Nom", "Niveau", "Parrain", "Telephone", "Commission"] if c in df_mlm.columns]
        st.dataframe(df_mlm[cols_ordre], width='stretch', hide_index=True)
    else:
        st.info("Aucun agent MLM pour le moment.")
    st.divider()
    st.markdown("**🌳 Arbre du réseau — Parrain → Filleuls**")
    if not agents_mlm:
        st.info("Aucun réseau à afficher pour le moment.")
    else:
        for agent in agents_mlm:
            filleuls = sorted([a for a in agents_mlm if a.get("Parrain") == agent["Nom"]], key=lambda x: (x.get("Nom") or "").lower())
            nb = len(filleuls)
            texte_filleuls = ", ".join([f"{f['Nom']} ({f['Niveau']})" for f in filleuls]) if filleuls else "— Aucun filleul —"
            st.write(f"👑 **{agent['Nom']}** — {agent['Niveau']} — Code {agent['Code']} — Parrain : {agent.get('Parrain','—')} — {nb} filleul(s)")
            st.caption(f"↳ Filleuls : {texte_filleuls} | Commission : {agent['Commission']} F")
            st.write("")
    st.divider()
    g1, g2 = st.columns(2)
    with g1:
        st.markdown("**✏ 1. Corriger un agent MLM**")
        if agents_mlm:
            agent_a_corriger = st.selectbox("Choisir l'agent à corriger *", [f"{a['Nom']} ({a['Code']})" for a in agents_mlm], key="mlm_corriger")
            a_sel = next(a for a in agents_mlm if f"{a['Nom']} ({a['Code']})" == agent_a_corriger)
            nouveau_parrain = st.selectbox("Nouveau Parrain *", ["Boss"] + [a["Nom"] for a in agents_mlm if a["Nom"] != a_sel["Nom"]], index=0, key="mlm_parrain")
            nouveau_niveau = st.selectbox("Nouveau Niveau *", ["Starter", "Distributeur", "Leader"], index=["Starter", "Distributeur", "Leader"].index(a_sel.get("Niveau", "Starter")) if a_sel.get("Niveau") in ["Starter", "Distributeur", "Leader"] else 0, key="mlm_niveau")
            nouveau_tel = st.text_input("Téléphone", value=a_sel.get("Telephone", ""), key="mlm_tel")
            if st.button("💾 Enregistrer la correction", width='stretch', key="mlm_save"):
                try:
                    if a_sel.get("id"):
                        supa_update("agents", "id", a_sel["id"], {"parrain": nouveau_parrain, "niveau": nouveau_niveau, "telephone": nouveau_tel})
                    a_sel["Parrain"] = nouveau_parrain
                    a_sel["Niveau"] = nouveau_niveau
                    a_sel["Telephone"] = nouveau_tel
                    st.success(f"{a_sel['Nom']} corrigé")
                    st.rerun()
                except Exception as e:
                    st.error(f"Erreur : {e}")
        else:
            st.info("Aucun agent à corriger.")
    with g2:
        st.markdown("**➕ 2. Ajouter un filleul**")
        f_nom = st.text_input("Nom du filleul *", placeholder="Ex : Awa", key="mlm_f_nom")
        f_code = st.text_input("Code du filleul *", placeholder="Ex : APG-010", key="mlm_f_code")
        f_tel = st.text_input("Téléphone du filleul", placeholder="90 12 34 56", key="mlm_f_tel")
        f_parrain = st.selectbox("Parrain du filleul *", ["Boss"] + [a["Nom"] for a in agents_mlm], key="mlm_f_parrain")
        f_niveau = st.selectbox("Niveau de départ *", ["Starter", "Distributeur"], key="mlm_f_niveau")
        if st.button("➕ Ajouter le filleul", width='stretch', type="primary", key="mlm_f_add"):
            if f_nom and f_code:
                if any(a["Code"] == f_code for a in st.session_state.agents):
                    st.error(f"Code {f_code} déjà utilisé !")
                else:
                    try:
                        supa_insert("agents", {"nom": f_nom, "code": f_code, "type_agent": "MLM", "niveau": f_niveau, "parrain": f_parrain, "telephone": f_tel, "boutique": "—", "commission_fcfa": 0})
                    except Exception:
                        supa_insert("agents", {"nom": f_nom, "code": f_code, "niveau": f_niveau, "parrain": f_parrain, "commission_fcfa": 0})
                    st.session_state.agents = charger_agents_supabase()
                    st.success(f"Filleul {f_nom} ({f_code}) ajouté sous {f_parrain} !")
                    st.rerun()
            else:
                st.error("Nom + Code obligatoires")

elif menu == "Temoignages Clients":
    st.markdown(f'<div class="section-header"><div class="section-header-gold-bar"></div><div style="color:white; font-weight:800">TEMOIGNAGES CLIENTS - PREUVE SOCIALE</div></div>', unsafe_allow_html=True)
    for t in st.session_state.temoignages:
        st.markdown(f"<div style='border:2px solid {VERT}; border-left:6px solid {OR}; padding:14px; margin:10px 0; background:white; border-radius:12px'><b>{t['Client']}</b> - {t['Produit']} - {'⭐'*int(t['Note'])}<br><i>\"{t['Message']}\"</i><br><small>{t['Date']}</small></div>", unsafe_allow_html=True)
    tc1,tc2 = st.columns(2)
    with tc1:
        t_client = st.text_input("Nom Client *")
        t_produit = st.selectbox("Produit Concerne *", [s["Produit"] for s in st.session_state.stock])
        t_note = st.slider("Note *", 1, 5, 5)
    with tc2:
        t_msg = st.text_area("Temoignage *")
        if st.button("Publier Temoignage", type="primary", width='stretch'):
            if t_client and t_msg:
                try:
                    supa_insert("temoignages", {"client": t_client, "produit": t_produit, "note": int(t_note), "message": t_msg, "date": datetime.now().strftime("%d/%m/%Y")})
                    st.session_state.temoignages = charger_temoignages_supabase()
                    st.success("Temoignage sauve !")
                    st.rerun()
                except Exception as e:
                    st.warning(f"Sauve en local : {e}")
    st.divider()
    st.markdown("**✏ Modifier un témoignage**")
    if st.session_state.temoignages:
        t_mod = st.selectbox("Choisir un témoignage à modifier :", ["-- Choisir --"] + [f"{t['Client']} - {t['Produit']}" for t in st.session_state.temoignages], key="mod_temoignage")
        if t_mod != "-- Choisir --":
            tem_act = next(t for t in st.session_state.temoignages if f"{t['Client']} - {t['Produit']}" == t_mod)
            m1, m2 = st.columns(2)
            with m1:
                nouveau_msg = st.text_area("Nouveau Message", value=tem_act.get("Message",""), key="mod_msg_tem")
                nouvelle_note = st.slider("Nouvelle Note", 1, 5, int(tem_act.get("Note", 5)), key="mod_note_tem")
            with m2:
                nouveau_produit_tem = st.selectbox("Nouveau Produit", [s["Produit"] for s in st.session_state.stock], key="mod_produit_tem")
                if st.button("💾 Enregistrer la modification", key="btn_mod_tem"):
                    try:
                        if tem_act.get("id"):
                            supa_update("temoignages", "id", tem_act["id"], {"message": nouveau_msg, "note": int(nouvelle_note), "produit": nouveau_produit_tem})
                        tem_act["Message"] = nouveau_msg
                        tem_act["Note"] = int(nouvelle_note)
                        tem_act["Produit"] = nouveau_produit_tem
                        st.success(f"Témoignage de {tem_act['Client']} modifié !")
                        st.rerun()
                    except Exception as e:
                        st.error(f"Erreur : {e}")
    st.divider()
    st.markdown("**🗑 Supprimer un témoignage**")
    if st.session_state.temoignages:
        t_sel = st.selectbox("Choisir un témoignage :", ["-- Choisir --"] + [f"{t['Client']} - {t['Produit']}" for t in st.session_state.temoignages], key="act_temoignage")
        if t_sel != "-- Choisir --" and st.button("🗑 Supprimer ce témoignage", key="btn_del_temoignage"):
            tem_del = next((t for t in st.session_state.temoignages if f"{t['Client']} - {t['Produit']}" == t_sel), None)
            try:
                if tem_del and tem_del.get("id"):
                    supa_delete("temoignages", "id", tem_del["id"])
            except Exception as e:
                st.warning(f"Supprimé de l'affichage, Supabase : {e}")
            st.session_state.temoignages = [t for t in st.session_state.temoignages if f"{t['Client']} - {t['Produit']}" != t_sel]
            st.success("Témoignage supprimé !")
            st.rerun()

elif menu == "Inventaire":
    st.markdown(f'<div class="section-header"><div class="section-header-gold-bar"></div><div style="color:white; font-weight:800">📦 INVENTAIRE - COMPTAGE PHYSIQUE APGIV</div></div>', unsafe_allow_html=True)
    st.caption(f"Comptage du {date.today().strftime('%d/%m/%Y')} - Produits APGIV depuis Supabase, pas de fichier Excel.")
    tab_inventaire, tab_auto, tab_histo, tab_params = st.tabs(["📋 Comptage Manuel", "🤖 Auto Inventaire", "📜 Historique", "⚙ PIN"])
    with tab_inventaire:
        if not st.session_state.stock:
            st.error("Aucun stock trouvé")
            st.stop()
        df_theo = pd.DataFrame(st.session_state.stock)
        valeur_theo = int((df_theo["Prix"] * df_theo["Stock"]).sum()) if len(df_theo) else 0
        st.info(f"Theorique : {len(df_theo)} produits | Stock total : {int(df_theo['Stock'].sum())} unites | Valeur : {valeur_theo:,} F")
        seuil_bas = st.slider("Seuil alerte stock bas par produit", 1, 50, 20)
        faibles = df_theo[df_theo["Stock"] <= seuil_bas]
        if not faibles.empty:
            texte_faibles = ", ".join([str(r["Produit"]) + " (" + str(r["Stock"]) + ")" for _, r in faibles.iterrows()])
            st.warning("Stock faible : " + texte_faibles)
        st.subheader("1. Comptage physique")
        inventaire_rows = []
        for _, row in df_theo.iterrows():
            inventaire_rows.append({"Produit": row["Produit"], "Lot": row.get("Lot","-"), "Peremption": row.get("Peremption","-"), "Prix Achat": int(row["Prix"]), "Theorique": int(row["Stock"]), "Reel": int(row["Stock"]), "Etat": "Bon", "Raison ecart": ""})
        df_edit = pd.DataFrame(inventaire_rows)
        edited = st.data_editor(df_edit, column_config={"Produit": st.column_config.TextColumn(disabled=True), "Lot": st.column_config.TextColumn(disabled=True), "Peremption": st.column_config.TextColumn(disabled=True), "Prix Achat": st.column_config.NumberColumn(disabled=True, format="%d F"), "Theorique": st.column_config.NumberColumn(disabled=True), "Reel": st.column_config.NumberColumn(min_value=0, step=1), "Etat": st.column_config.SelectboxColumn(options=["Bon", "Endommagé", "Ecran cassé", "Incomplet", "Volé", "Perdu"], required=True), "Raison ecart": st.column_config.TextColumn()}, hide_index=True, width='stretch', height=350, key="inventaire_editor")
        st.subheader("2. Validation et calcul")
        col1, col2 = st.columns(2)
        user_compte = col1.text_input("Qui a compté ? *", placeholder="ENAM")
        photo_preuve = col2.file_uploader("Photo preuve (optionnel)", type=["jpg", "png"])
        if st.button("Calculer écarts", type="primary", width='stretch'):
            if not user_compte:
                st.error("Nom obligatoire")
            else:
                edited["Ecart"] = edited["Reel"] - edited["Theorique"]
                manquants = edited[edited["Reel"] < edited["Theorique"]].copy()
                manquants["Qte manquante"] = manquants["Theorique"] - manquants["Reel"]
                endommages = edited[edited["Etat"] != "Bon"]
                perte_manquants = int((manquants["Qte manquante"] * manquants["Prix Achat"]).sum()) if len(manquants) else 0
                perte_endommages = int((endommages["Prix Achat"] * endommages["Reel"]).sum() * 0.5) if len(endommages) else 0
                perte_totale = perte_manquants + perte_endommages
                nb_theo = int(edited["Theorique"].sum())
                nb_reel = int(edited["Reel"].sum())
                fiabilite = (nb_reel / nb_theo * 100) if nb_theo else 100.0
                c1, c2, c3, c4 = st.columns(4)
                c1.metric("Manquants (unites)", f"{int(manquants['Qte manquante'].sum()) if len(manquants) else 0}")
                c2.metric("Endommages (lignes)", f"{len(endommages)}")
                c3.metric("Perte estimee", f"{perte_totale:,.0f} F")
                c4.metric("Fiabilite", f"{fiabilite:.1f} %")
                if not manquants.empty:
                    st.error("Manquants :")
                    st.dataframe(manquants[["Produit", "Lot", "Theorique", "Reel", "Qte manquante", "Prix Achat", "Raison ecart"]], width='stretch', hide_index=True)
                if not endommages.empty:
                    st.warning("Endommages :")
                    st.dataframe(endommages, width='stretch', hide_index=True)
                st.session_state["last_edited"] = edited
                st.session_state["last_perte"] = perte_totale
                st.session_state["last_user_compte"] = user_compte
        st.divider()
        if "last_edited" in st.session_state:
            st.subheader("3. Cloture inventaire")
            pin_inv = st.text_input("PIN Proprietaire pour valider ajustement", type="password", key="pin_inv_cloture")
            if st.button("Valider et ajuster stock", width='stretch'):
                if hashlib.sha256(pin_inv.encode()).hexdigest() != hashlib.sha256(st.session_state.pin.encode()).hexdigest():
                    st.error("PIN incorrect")
                else:
                    edited_final = st.session_state["last_edited"]
                    manquants = edited_final[edited_final["Reel"] < edited_final["Theorique"]]
                    for _, r in edited_final.iterrows():
                        prod = next((s for s in st.session_state.stock if s["Produit"] == r["Produit"]), None)
                        if prod:
                            prod["Stock"] = int(r["Reel"])
                            try:
                                if prod.get("id"):
                                    supa_update_stock(prod["id"], int(r["Reel"]))
                            except Exception:
                                pass
                    save_historique_inventaire({"date": str(date.today()), "heure": datetime.now().strftime("%H:%M:%S"), "par": st.session_state.get("last_user_compte",""), "type": "Manuel", "manquants": int(manquants["Theorique"].sum() - manquants["Reel"].sum()) if len(manquants) else 0, "endommages": int(len(edited_final[edited_final["Etat"] != "Bon"])), "perte": int(st.session_state["last_perte"]), "details": edited_final.to_dict(orient="records")})
                    st.success("Inventaire validé et stock ajusté")
                    st.balloons()
                    del st.session_state["last_edited"]
                    st.rerun()
    with tab_auto:
        st.title("📦 Inventaire - Automatique")
        st.caption("Comptage du " + date.today().strftime("%d/%m/%Y") + " - Version Auto")
        st.subheader("🤖 Inventaire 100% Automatique")
        st.caption("Le systeme compare automatiquement ton stock theorique avec la realite")
        df_auto = pd.DataFrame(st.session_state.stock)
        stock_theo_total = int(df_auto["Stock"].sum()) if len(df_auto) else 0
        valeur_theo_auto = int((df_auto["Prix"] * df_auto["Stock"]).sum()) if len(df_auto) else 0
        avec_fiche = 0
        for _, r in df_auto.iterrows():
            if str(r.get("Lot", "-")) != "-" and str(r.get("Peremption", "-")) != "-":
                avec_fiche += 1
        a1, a2, a3 = st.columns(3)
        with a1:
            st.metric("📦 En Stock Theorique", str(stock_theo_total))
        with a2:
            st.metric("💰 Valeur Theorique Achat", f"{valeur_theo_auto:,} F")
        with a3:
            st.metric("🖼 Avec Fiche Complete", str(avec_fiche) + " / " + str(len(df_auto)))
        st.divider()
        st.subheader("🔍 Detection automatique d'anomalies")
        anomalies = detecter_anomalies_inventaire(df_auto)
        if anomalies:
            st.error(str(len(anomalies)) + " anomalies detectees automatiquement")
            st.dataframe(pd.DataFrame(anomalies), width='stretch', hide_index=True)
        else:
            st.success("Aucune anomalie - Stock propre")
        st.divider()
        st.subheader("📉 Alertes Stock Bas Automatiques")
        seuil_auto = st.slider("Seuil alerte auto", 1, 50, 20, key="seuil_auto_inv")
        faibles_auto = df_auto[df_auto["Stock"] <= seuil_auto].copy()
        if not faibles_auto.empty:
            faibles_auto["Alerte"] = "🔴 A COMMANDER"
            st.dataframe(faibles_auto[["Produit", "Stock", "Alerte"]].rename(columns={"Stock": "Qte"}), width='stretch', hide_index=True)
            liste_reco = ", ".join([str(x) for x in faibles_auto["Produit"].tolist()])
            st.warning("Il faut recommander : " + liste_reco)
        else:
            st.success("Aucun produit sous le seuil - Stock OK")
        st.divider()
        st.subheader("⚡ Inventaire Flash en 1 Clic")
        st.caption("Au lieu de cocher ligne par ligne, clique ici pour dire que tout le stock theorique est bien la")
        user_auto = st.text_input("Qui valide l'auto inventaire ?", placeholder="ENAM", key="user_auto_inv")
        if st.button("🤖 LANCER INVENTAIRE AUTOMATIQUE", type="primary", width='stretch'):
            if not user_auto:
                st.error("Nom obligatoire - Qui valide ?")
            elif anomalies:
                st.warning("Il y a des anomalies ci-dessus. Corrige-les d'abord dans Magasin & Restockage (Lot / Peremption / Prix), puis relance.")
            else:
                lignes_auto = []
                for _, r in df_auto.iterrows():
                    lignes_auto.append({"Produit": r["Produit"], "Lot": r.get("Lot", "-"), "Peremption": r.get("Peremption", "-"), "Prix Achat": int(r["Prix"]), "Theorique": int(r["Stock"]), "Reel": int(r["Stock"]), "Etat": "Bon", "Raison ecart": "Auto - Flash"})
                save_historique_inventaire({"date": str(date.today()), "heure": datetime.now().strftime("%H:%M:%S"), "par": user_auto, "type": "Auto Flash", "manquants": 0, "endommages": 0, "perte": 0, "details": lignes_auto})
                st.success("Inventaire Auto valide - Tout le stock theorique est confirme present : " + str(stock_theo_total) + " unites")
                st.balloons()
                st.rerun()
    with tab_histo:
        st.subheader("Historique")
        hist = charger_historique_inventaire()
        if hist:
            st.dataframe(pd.DataFrame([{"Date": h["date"], "Heure": h.get("heure",""), "Par": h["par"], "Type": h.get("type", "Manuel"), "Manquants": h["manquants"], "Endommages": h.get("endommages", 0), "Perte": h["perte"]} for h in hist[-20:]]), width='stretch', hide_index=True)
            if st.button("Voir le dernier detail complet"):
                st.json(hist[-1].get("details", []))
        else:
            st.info("Aucun historique")
    with tab_params:
        st.caption("🔒 Zone proprietaire - PIN commun / Inventaire")
        st.subheader("⚙ Modifier PIN Proprietaire")
        st.info("Ce PIN est le meme que Compta Privee et Comptabilite Centrale. PIN actuel : " + st.session_state.pin)
        with st.form("change_pin_inv"):
            old_pin = st.text_input("Ancien code PIN *", type="password")
            new_pin = st.text_input("Nouveau code PIN (4 chiffres) *", type="password")
            confirm_pin = st.text_input("Confirmer nouveau PIN *", type="password")
            submit = st.form_submit_button("Changer le code PIN", type="primary", width='stretch')
            if submit:
                if hashlib.sha256(old_pin.encode()).hexdigest() != hashlib.sha256(st.session_state.pin.encode()).hexdigest():
                    st.error("Ancien code PIN incorrect")
                elif len(new_pin) < 4:
                    st.error("PIN trop court, min 4 chiffres")
                elif new_pin != confirm_pin:
                    st.error("Confirmation differente")
                else:
                    st.session_state.pin = new_pin
                    st.success("✅ PIN change avec succes ! Nouveau PIN : " + new_pin)
                    st.balloons()

elif menu == "Comptabilite Centrale":
    st.markdown(f'<div class="section-header"><div class="section-header-gold-bar"></div><div style="color:white; font-weight:800">COMPTABILITE CENTRALE - CAISSE INTELLIGENTE</div></div>', unsafe_allow_html=True)
    sync_ventes_auto_caisse()
    all_data = load_caisse()
    today_str = str(date.today())
    today_data = get_today_data_caisse(all_data, today_str)
    soldes_theoriques = {}
    for m in METHODS_CAISSE:
        soldes_theoriques[m] = today_data["ouverture"].get(m, 0) + today_data["ventes_auto"].get(m, 0) + sum([v["montant"] for v in today_data["ventes_manuelles"] if v["methode"] == m]) - sum([d["montant"] for d in today_data["depenses"] if d["methode"] == m]) + sum([t["montant"] if t["vers"] == m else -t["montant"] for t in today_data["transferts"]])
    c1, c2, c3, c4, c5 = st.columns(5)
    c1.metric("Espèces", f"{soldes_theoriques['Espèces']:,} F")
    c2.metric("Flooz", f"{soldes_theoriques['Flooz']:,} F")
    c3.metric("TMoney", f"{soldes_theoriques['TMoney']:,} F")
    c4.metric("Mixx", f"{soldes_theoriques['Mixx']:,} F")
    c5.metric("TOTAL", f"{sum(soldes_theoriques.values()):,} F")
    st.caption(f"Journée du {date.today().strftime('%d/%m/%Y')} | Ventes auto Dashboard : {sum(today_data['ventes_auto'].values()):,} F")
    alertes = []
    if sum([d["montant"] for d in today_data["depenses"] if d["montant"] >= SEUIL_ALERTE_CAISSE]):
        alertes.append(f"Dépense > {SEUIL_ALERTE_CAISSE:,}F")
    if today_data["ouverture"] == {m: 0 for m in METHODS_CAISSE} and sum(today_data["ventes_auto"].values()) > 0:
        alertes.append("Ventes sans ouverture")
    if alertes:
        st.error(" | ".join(alertes))
    st.divider()
    tabs = st.tabs(["Ouverture", "Opérations", "Transfert", "Clôture", "Contrôle", "📄 Rapports PDF Boss"])
    with tabs[0]:
        if today_data["ouverture_par"]:
            st.success(f"Ouvert à {today_data['heure_ouverture']} par {today_data['ouverture_par']}")
            st.json(today_data["ouverture"])
        else:
            with st.form("ouverture"):
                c1, c2 = st.columns(2)
                user_ouv = c1.text_input("Qui ouvre ? *")
                o_espece = c1.number_input("Espèces", 0, step=1000)
                o_flooz = c2.number_input("Flooz", 0, step=1000)
                o_tmoney = c1.number_input("TMoney", 0, step=1000)
                o_mixx = c2.number_input("Mixx", 0, step=1000)
                if st.form_submit_button("Valider Ouverture", use_container_width=True):
                    if not user_ouv:
                        st.error("Nom obligatoire")
                    else:
                        today_data["ouverture"] = {"Espèces": o_espece, "Flooz": o_flooz, "TMoney": o_tmoney, "Mixx": o_mixx}
                        today_data["ouverture_par"] = user_ouv
                        today_data["heure_ouverture"] = datetime.now().strftime("%H:%M:%S")
                        add_log_caisse(today_data, "OUVERTURE", user_ouv, sum([o_espece, o_flooz, o_tmoney, o_mixx]), "TOUS", "")
                        all_data[today_str] = today_data
                        save_caisse(all_data)
                        st.rerun()
    with tabs[1]:
        col_a, col_b = st.columns(2)
        with col_a:
            st.markdown("**Sortie**")
            with st.form("depense"):
                user_dep = st.text_input("Qui sort ? *")
                montant = st.number_input("Montant", 100, step=500)
                methode = st.selectbox("Méthode", METHODS_CAISSE)
                motif = st.selectbox("Motif", ["Retrait proprio", "Achat stock", "Crédit", "Loyer", "Transport", "Autre"])
                note = st.text_area("Justification *")
                pin = st.text_input("PIN si >50k", type="password") if montant >= SEUIL_ALERTE_CAISSE else ""
                if st.form_submit_button("Enregistrer Dépense", type="primary"):
                    if not user_dep or not note:
                        st.error("User + justification obligatoires")
                    elif montant >= SEUIL_ALERTE_CAISSE and hashlib.sha256(pin.encode()).hexdigest() != hashlib.sha256(st.session_state.pin.encode()).hexdigest():
                        st.error("PIN incorrect")
                    else:
                        today_data["depenses"].append({"heure": datetime.now().strftime("%H:%M:%S"), "user": user_dep, "montant": montant, "methode": methode, "motif": motif, "note": note})
                        add_log_caisse(today_data, "DEPENSE", user_dep, montant, methode, f"{motif} - {note}")
                        all_data[today_str] = today_data
                        save_caisse(all_data)
                        st.rerun()
        with col_b:
            st.markdown("**Vente manuelle**")
            with st.form("vente_man"):
                user_v = st.text_input("Vendeur *", key="user_v")
                montant_v = st.number_input("Montant", 100, step=1000, key="mont_v")
                methode_v = st.selectbox("Méthode", METHODS_CAISSE, key="meth_v")
                note_v = st.text_input("Produit / Raison")
                if st.form_submit_button("Ajouter Vente"):
                    today_data["ventes_manuelles"].append({"heure": datetime.now().strftime("%H:%M:%S"), "user": user_v, "montant": montant_v, "methode": methode_v, "note": note_v})
                    add_log_caisse(today_data, "VENTE_MANUELLE", user_v, montant_v, methode_v, note_v)
                    all_data[today_str] = today_data
                    save_caisse(all_data)
                    st.rerun()
    with tabs[2]:
        with st.form("transfert"):
            user_t = st.text_input("Qui transfère ?")
            de = st.selectbox("De", METHODS_CAISSE)
            vers = st.selectbox("Vers", [m for m in METHODS_CAISSE if m != de])
            mont_t = st.number_input("Montant", 1000, step=1000)
            if st.form_submit_button("Transférer"):
                today_data["transferts"].append({"heure": datetime.now().strftime("%H:%M:%S"), "user": user_t, "de": de, "vers": vers, "montant": mont_t})
                add_log_caisse(today_data, "TRANSFERT", user_t, mont_t, f"{de}->{vers}", "")
                all_data[today_str] = today_data
                save_caisse(all_data)
                st.success(f"{mont_t}F {de}->{vers}")
                st.rerun()
    with tabs[3]:
        if today_data["cloture"]:
            st.success(f"Clôturé à {today_data['heure_cloture']} par {today_data['cloture_par']}")
            st.json(today_data["ecarts"])
        else:
            with st.form("cloture_form"):
                user_clot = st.text_input("Qui clôture ? *")
                c1, c2 = st.columns(2)
                reel_espece = c1.number_input("Réel Espèces", 0, step=500)
                reel_flooz = c2.number_input("Réel Flooz", 0, step=500)
                reel_tmoney = c1.number_input("Réel TMoney", 0, step=500)
                reel_mixx = c2.number_input("Réel Mixx", 0, step=500)
                pin_clot = st.text_input("PIN Propriétaire", type="password")
                if st.form_submit_button("Clôturer", use_container_width=True):
                    if hashlib.sha256(pin_clot.encode()).hexdigest() != hashlib.sha256(st.session_state.pin.encode()).hexdigest():
                        st.error("PIN incorrect")
                    elif not user_clot:
                        st.error("Nom obligatoire")
                    else:
                        comptage = {"Espèces": reel_espece, "Flooz": reel_flooz, "TMoney": reel_tmoney, "Mixx": reel_mixx}
                        ecarts = {m: comptage[m] - soldes_theoriques[m] for m in METHODS_CAISSE}
                        today_data["comptage_reel"] = comptage
                        today_data["ecarts"] = ecarts
                        today_data["cloture"] = True
                        today_data["heure_cloture"] = datetime.now().strftime("%H:%M:%S")
                        today_data["cloture_par"] = user_clot
                        add_log_caisse(today_data, "CLOTURE", user_clot, sum(comptage.values()), "TOUS", f"Ecarts:{ecarts}")
                        all_data[today_str] = today_data
                        save_caisse(all_data)
                        if any(v != 0 for v in ecarts.values()):
                            st.error(f"ÉCARTS: {ecarts}")
                        else:
                            st.success("Caisse équilibrée")
                        st.balloons()
                        st.rerun()
    with tabs[4]:
        pin_view = st.text_input("PIN Propriétaire", type="password", key="pin_view")
        if hashlib.sha256(pin_view.encode()).hexdigest() == hashlib.sha256(st.session_state.pin.encode()).hexdigest():
            st.success("Accès propriétaire")
            dates = sorted(all_data.keys(), reverse=True)
            sel_date = st.selectbox("Date", dates, index=0) if dates else today_str
            d = all_data.get(sel_date, today_data)
            k1, k2, k3 = st.columns(3)
            k1.metric("Ventes", f"{sum(d['ventes_auto'].values()) + sum([v['montant'] for v in d['ventes_manuelles']]):,} F")
            k2.metric("Dépenses", f"{sum([x['montant'] for x in d['depenses']]):,} F")
            k3.metric("Opérations", len(d.get('logs', [])))
            if d.get('logs'):
                st.dataframe(pd.DataFrame(d['logs']), use_container_width=True)
            hist = []
            for dt in dates[:7]:
                dd = all_data[dt]
                hist.append({"Date": dt, "Ventes": sum(dd["ventes_auto"].values()), "Dépenses": sum([x["montant"] for x in dd["depenses"]]), "Clôturé": dd["cloture"]})
            if hist:
                st.dataframe(pd.DataFrame(hist), use_container_width=True)
        else:
            if pin_view:
                st.error("PIN incorrect")
            st.info("PIN Boss actuel — même que Compta Privée")
    with tabs[5]:
        st.markdown("**📄 Rapports PDF pour le Patron — Journalier / Mensuel / Annuel — Prêt à envoyer sur WhatsApp**")
        pin_rapport = st.text_input("PIN Propriétaire pour voir les rapports", type="password", key="pin_rapport")
        if hashlib.sha256(pin_rapport.encode()).hexdigest() != hashlib.sha256(st.session_state.pin.encode()).hexdigest():
            if pin_rapport:
                st.error("PIN incorrect")
            st.info("Entre le PIN Boss pour débloquer les rapports PDF.")
        else:
            st.success("Accès rapports débloqué")
            rc1, rc2, rc3 = st.columns(3)
            with rc1:
                type_rapport = st.selectbox("Type de rapport *", ["Journalier", "Mensuel", "Annuel"], key="type_rapport")
            with rc2:
                ref_date_rapport = st.date_input("Date de référence *", value=date.today(), key="ref_date_rapport")
            with rc3:
                auteur_rapport = st.text_input("Préparé par *", value=st.session_state.get("user", ""), key="auteur_rapport")
            tel_patron_input = st.text_input("Numéro WhatsApp du Patron *", value=st.session_state.get("tel_patron", ""), placeholder="90 12 34 56", key="tel_patron_input")
            if tel_patron_input:
                st.session_state.tel_patron = tel_patron_input
            stats_rapport = calculer_stats_periode(all_data, type_rapport, ref_date_rapport)
            k1, k2, k3, k4 = st.columns(4)
            with k1:
                st.metric("Ventes totales", f"{stats_rapport['total_ventes']:,} F")
            with k2:
                st.metric("Dépenses", f"{stats_rapport['total_depenses']:,} F")
            with k3:
                st.metric("Solde théorique", f"{stats_rapport['solde_theorique']:,} F")
            with k4:
                st.metric("Bénéfice estimé 42%", f"{stats_rapport['benefice_estime']:,} F")
            st.caption(f"Période : {stats_rapport['libelle']} | Jours avec activité : {stats_rapport['nb_jours']} | Jours clôturés : {stats_rapport['nb_clotures']} | Opérations : {len(stats_rapport['ops'])}")
            if stats_rapport['lignes_jours']:
                st.dataframe(pd.DataFrame(stats_rapport['lignes_jours']), use_container_width=True, hide_index=True)
            else:
                st.info("Aucune activité enregistrée pour cette période dans la Caisse.")
            if st.button("📄 Générer le Rapport PDF Patron", type="primary", use_container_width=True, key="btn_gen_rapport"):
                chemin_pdf = generer_rapport_pdf_caisse(type_rapport, ref_date_rapport, stats_rapport, auteur_rapport)
                if chemin_pdf:
                    st.session_state["dernier_rapport_pdf"] = chemin_pdf
                    st.session_state["dernier_stats_rapport"] = stats_rapport
                    st.session_state["dernier_type_rapport"] = type_rapport
                    st.success("Rapport PDF généré ! Télécharge-le ci-dessous, puis envoie-le sur WhatsApp.")
                else:
                    st.error("Installe fpdf2 : pip install fpdf2")
            if st.session_state.get("dernier_rapport_pdf") and os.path.exists(st.session_state["dernier_rapport_pdf"]):
                s_rap = st.session_state.get("dernier_stats_rapport", stats_rapport)
                t_rap = st.session_state.get("dernier_type_rapport", type_rapport)
                nom_fichier = f"Rapport_{t_rap}_{s_rap['libelle'].replace('/','-')}_APGIV.pdf"
                with open(st.session_state["dernier_rapport_pdf"], "rb") as f:
                    st.download_button("📥 Télécharger le Rapport PDF Patron", data=f, file_name=nom_fichier, mime="application/pdf", use_container_width=True)
                msg_wa = f"Bonjour Patron - Rapport {t_rap} APGIV - Comptabilite Centrale - Periode : {s_rap['libelle']} - Ventes : {s_rap['total_ventes']:,} F - Depenses : {s_rap['total_depenses']:,} F - Solde theorique : {s_rap['solde_theorique']:,} F - Benefice estime 42% : {s_rap['benefice_estime']:,} F - Jours actifs : {s_rap['nb_jours']} - Jours clotures : {s_rap['nb_clotures']} - PDF complet en piece jointe. L'Excellence au Naturel - APGIV"
                st.text_area("Message WhatsApp prêt à copier", value=msg_wa, height=110, key="msg_wa_rapport")
                tel_p = nettoyer_numero_tel(st.session_state.get("tel_patron", ""))
                if tel_p:
                    wa_rap = f"https://wa.me/{tel_p}?text={urllib.parse.quote(msg_wa)}"
                    st.link_button(f"📱 Ouvrir WhatsApp du Patron ({st.session_state.get('tel_patron','')}) + coller le message", wa_rap, use_container_width=True)
                else:
                    st.warning("Entre le numéro WhatsApp du Patron ci-dessus pour activer le bouton WhatsApp.")

elif menu == "Compta Privee":
    st.markdown(f'<div class="section-header"><div class="section-header-gold-bar"></div><div style="color:white; font-weight:900; font-size:15px; letter-spacing:0.6px">COMPTA PRIVEE - BILAN - RAPPORT</div></div>', unsafe_allow_html=True)
    if not st.session_state.auth_compta:
        st.markdown(f"<div style='background:white; border:2px solid {VERT}; border-radius:14px; padding:20px; text-align:center'><p style='font-weight:800; color:{VERT_FONCE}'>🔒 ACCES RESERVE BOSS</p><p style='font-size:12px; color:#667085'>Entrez le PIN Boss pour acceder au Bilan complet</p></div>", unsafe_allow_html=True)
        st.write("")
        pin_input = st.text_input("PIN Boss", type="password", placeholder="••••")
        col_p1, col_p2 = st.columns([2,1])
        with col_p1:
            if st.button("🔓 Deverrouiller Compta Privee", type="primary", width='stretch'):
                if pin_input == st.session_state.pin:
                    st.session_state.auth_compta=True
                    st.rerun()
                else:
                    st.error("PIN incorrect - Acces refuse")
        with col_p2:
            st.caption("PIN par defaut: 1234")
    else:
        total_ca = sum(v["Total"] for v in st.session_state.ventes) if st.session_state.ventes else 0
        valeur_stock = sum(s['Prix']*s['Stock'] for s in st.session_state.stock)
        benefice = int(total_ca*0.42)
        c1,c2,c3 = st.columns(3, gap="medium")
        with c1:
            st.markdown(f"<div style='background:white; border-left:6px solid {VERT}; border-radius:14px; padding:16px; box-shadow:0 4px 12px rgba(0,0,0,0.08)'><p style='margin:0; font-size:11px; font-weight:700; color:#667085'>CA TOTAL</p><p style='margin:4px 0 0 0; font-size:26px; font-weight:900; color:{VERT_FONCE}'>{total_ca} F</p><p style='margin:4px 0 0 0; font-size:11px; color:{OR}'>● Cumul ventes</p></div>", unsafe_allow_html=True)
        with c2:
            st.markdown(f"<div style='background:white; border-left:6px solid #F97316; border-radius:14px; padding:16px; box-shadow:0 4px 12px rgba(0,0,0,0.08)'><p style='margin:0; font-size:11px; font-weight:700; color:#667085'>VALEUR STOCK</p><p style='margin:4px 0 0 0; font-size:26px; font-weight:900; color:{VERT_FONCE}'>{valeur_stock} F</p><p style='margin:4px 0 0 0; font-size:11px; color:#F97316'>● Inventaire auto</p></div>", unsafe_allow_html=True)
        with c3:
            st.markdown(f"<div style='background:white; border-left:6px solid {OR}; border-radius:14px; padding:16px; box-shadow:0 4px 12px rgba(0,0,0,0.08)'><p style='margin:0; font-size:11px; font-weight:700; color:#667085'>BENEFICE (42%)</p><p style='margin:4px 0 0 0; font-size:26px; font-weight:900; color:{VERT_FONCE}'>{benefice} F</p><p style='margin:4px 0 0 0; font-size:11px; color:{OR}'>● Marge nette</p></div>", unsafe_allow_html=True)
        st.write("")
        if st.session_state.ventes:
            df_v = pd.DataFrame(st.session_state.ventes)
            st.markdown(f'<div class="section-header" style="margin-top:10px"><div class="section-header-gold-bar"></div><div style="color:white; font-weight:800; font-size:13px">📊 BILAN DES VENTES PAR PRODUIT</div></div>', unsafe_allow_html=True)
            b1,b2 = st.columns([2,1], gap="large")
            with b1:
                bilan_produit = df_v.groupby("Produit")[["Qte","Total"]].sum().sort_values("Total", ascending=False)
                bilan_produit.columns = ["Quantite Vendue","CA Produit"]
                st.bar_chart(bilan_produit["CA Produit"], width='stretch')
            with b2:
                st.dataframe(bilan_produit, width='stretch')
            st.markdown(f'<div class="section-header"><div class="section-header-gold-bar"></div><div style="color:white; font-weight:800; font-size:13px">👤 BILAN PAR AGENT VENDEUR</div></div>', unsafe_allow_html=True)
            a1,a2 = st.columns([2,1], gap="large")
            with a1:
                bilan_agent = df_v.groupby("Agent")[["Qte","Total"]].sum().sort_values("Total", ascending=False)
                bilan_agent.columns = ["Qte Vendue","CA Agent"]
                bilan_agent["Commission 10%"] = (bilan_agent["CA Agent"]*0.10).astype(int)
                st.bar_chart(bilan_agent["CA Agent"], width='stretch')
            with a2:
                st.dataframe(bilan_agent, width='stretch')
            st.markdown(f'<div class="section-header"><div class="section-header-gold-bar"></div><div style="color:white; font-weight:800; font-size:13px">📦 INVENTAIRE AUTO - STOCK RESTANT + VALEUR</div></div>', unsafe_allow_html=True)
            df_inv = df_stock.copy()
            df_inv["Valeur Stock"] = df_inv["Prix"]*df_inv["Stock"]
            df_inv["Statut"] = df_inv["Stock"].apply(lambda x: "🔴 ALERTE" if x<20 else "🟢 OK")
            st.dataframe(df_inv[["Produit","Stock","Lot","Peremption","Valeur Stock","Statut"]], width='stretch', hide_index=True)
            st.markdown(f'<div class="section-header"><div class="section-header-gold-bar"></div><div style="color:white; font-weight:800; font-size:13px">📝 RAPPORT AUTO JOURNALIER - {datetime.now().strftime("%d/%m/%Y")}</div></div>', unsafe_allow_html=True)
            today = datetime.now().strftime("%d/%m/%Y")
            ventes_jour = [v for v in st.session_state.ventes if today in v["Date"]]
            ca_jour = sum(v["Total"] for v in ventes_jour)
            st.markdown(f"""
            <div style='background:white; border:2px solid {VERT}; border-radius:14px; padding:18px'>
                <p style='margin:0; font-weight:900; color:{VERT_FONCE}'>Rapport du {today}</p>
                <p style='margin:6px 0 0 0; font-size:13px'>• Nombre de ventes aujourd'hui : <b>{len(ventes_jour)}</b><br>
                - Chiffre d'affaires du jour : <b>{ca_jour} F CFA</b><br>
                - Benefice jour (42%) : <b>{int(ca_jour*0.42)} F</b><br>
                - Produits les plus vendus : <b>{', '.join(bilan_produit.index[:2]) if len(bilan_produit)>0 else 'Aucun'}</b><br>
                - Top vendeur du jour : <b>{bilan_agent.index[0] if len(bilan_agent)>0 else 'Aucun'}</b><br>
                - Stock critique (&lt;20) : <b>{len([s for s in st.session_state.stock if s['Stock']<20])} lots</b></p>
            </div>
            """, unsafe_allow_html=True)
            st.write("")
            st.dataframe(pd.DataFrame(ventes_jour) if ventes_jour else pd.DataFrame([{"Info":"Aucune vente aujourd'hui"}]), width='stretch', hide_index=True)
            if ventes_jour:
                csv = pd.DataFrame(ventes_jour).to_csv(index=False).encode('utf-8')
                st.download_button("📥 Télécharger Rapport Journalier CSV", data=csv, file_name=f"Rapport_{today.replace('/','-')}.csv", mime="text/csv", width='stretch')
        else:
            st.info("Aucune vente encore - Bilan vide")
        st.divider()
        c_sec1, c_sec2 = st.columns(2, gap="large")
        with c_sec1:
            with st.expander("🔑 Modifier PIN Boss (Securite)"):
                new_pin = st.text_input("Nouveau PIN", type="password", placeholder="Nouveau code")
                if st.button("Changer PIN", type="primary"):
                    if new_pin and len(new_pin)>=4:
                        st.session_state.pin = new_pin
                        st.success(f"PIN modifie avec succes ! Nouveau PIN : {new_pin}")
                    else:
                        st.error("PIN trop court (4 chiffres min)")
                st.caption(f"PIN actuel : {st.session_state.pin}")
        with c_sec2:
            st.write("")
            if st.button("🔒 Verrouiller Compta Privee", width='stretch'):
                st.session_state.auth_compta=False
                st.rerun()
