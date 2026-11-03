import streamlit as st
import pandas as pd
from datetime import datetime
import os
from fpdf import FPDF
import urllib.parse
import base64

LOGO_PATH = "assets/Logo.jpeg"
VERT_FONCE = "#062914"
VERT = "#0E4D2E"
OR = "#C8A040"
FOND = "#F7F8F5"

def get_logo_b64():
    if os.path.exists(LOGO_PATH):
        with open(LOGO_PATH, "rb") as f:
            return base64.b64encode(f.read()).decode()
    return ""

logo_b64 = get_logo_b64()

st.set_page_config(
    page_title="APGIV OS Gestion",
    page_icon=LOGO_PATH,
    layout="wide",
    initial_sidebar_state="expanded"
)

st.markdown(f"""
<style>
    .stApp {{ background:{FOND}; }}
    .block-container {{ padding-top: 0.5rem !important; }}
    header[data-testid="stHeader"] {{ background: transparent !important; height: 0px !important; }}
    [data-testid="collapsedControl"] {{
        display: block !important; visibility: visible !important;
        color: {VERT_FONCE} !important; z-index: 99999 !important;
    }}
    [data-testid="stSidebar"] {{
        background: linear-gradient(180deg, {VERT_FONCE} 0%, #0A3D1F 100%) !important;
        border-right: 3px solid {OR} !important;
    }}
    div[data-testid="stRadio"] {{ gap:12px; }}
    div[data-testid="stRadio"] > div {{ gap:12px; }}
    div[data-testid="stRadio"] label {{
        background: transparent !important;
        border: 1.5px solid rgba(255,255,255,0.7) !important;
        border-radius: 22px !important;
        padding: 12px 18px !important;
        color: white !important;
        font-weight: 600 !important;
    }}
    div[data-testid="stRadio"] label[data-checked="true"] {{
        background: linear-gradient(90deg, #1DB954, #0E8A3E) !important;
        border-left: 5px solid {OR} !important;
        font-weight: 800 !important;
    }}
    .apgiv-header-final {{
        width: 100vw; margin-left: -5rem; margin-right: -5rem; height: 92px;
        background: #FFFFFF; display: flex; position: relative; overflow: hidden;
        box-shadow: 0 4px 24px rgba(0,0,0,0.07); border-bottom: 1px solid #E8EAEF; margin-bottom: 24px;
    }}
    .apgiv-logo-box {{
        width: 88px; background: #062914; display: flex; align-items: center; justify-content: center; flex-shrink: 0; z-index: 5;
    }}
    .apgiv-logo-box img {{
        width: 52px; height: 52px; border-radius: 50%; object-fit: cover; background: white; padding: 2px;
        box-shadow: 0 0 12px rgba(255,255,255,0.25);
    }}
    .apgiv-header-content {{
        flex: 1; background: white; display: flex; flex-direction: column; justify-content: center; padding-left: 22px; z-index: 3;
    }}
    .apgiv-title-line {{ display: flex; align-items: baseline; gap: 8px; line-height: 1; }}
    .apgiv-title-os {{ font-weight: 900; font-size: 26px; color: #0E4D2E; }}
    .apgiv-title-gestion {{ font-weight: 800; font-size: 26px; color: #C8A040; }}
    .apgiv-slogan {{
        font-size: 12.5px; color: #000000; font-style: italic; font-weight: 500; margin-top: 6px;
        border-top: 1px solid #EDEEF2; padding-top: 5px; display: inline-block; width: fit-content; padding-right: 20px;
    }}
    .apgiv-waves {{ position: absolute; right: 0; top: 0; width: 58%; height: 100%; z-index: 2; pointer-events: none; }}
    .wave {{ position: absolute; right: -10%; width: 110%; height: 55px; border-radius: 100% 0 0 0; }}
    .wave-1 {{ bottom: -18px; background: #0E4D2E; transform: rotate(-6deg) skewX(-12deg); opacity: 0.95; }}
    .wave-2 {{
        bottom: -2px; background: linear-gradient(90deg, #C8A040 0%, #E8C86A 50%, #C8A040 100%);
        height: 22px; transform: rotate(-7deg) skewX(-12deg); box-shadow: 0 2px 10px rgba(200,160,64,0.4); z-index: 3;
    }}
    .wave-3 {{
        top: -8px; right: -15%; width: 115%; height: 68px;
        background: linear-gradient(105deg, #062914 0%, #0E4D2E 40%, #1A6B3C 65%, #C8A040 90%, #E8C86A 100%);
        transform: rotate(-8deg) skewX(-10deg); opacity: 0.98; clip-path: ellipse(90% 80% at 80% 20%);
    }}
    .kpi-card {{
        background:white; border-radius:18px; padding:18px 20px;
        box-shadow: 0 8px 24px rgba(0,0,0,0.08); display:flex; align-items:flex-start; gap:16px;
        position:relative; overflow:hidden; height:115px; border:1px solid #EAECF0;
    }}
    .kpi-card::before {{ content:''; position:absolute; top:0; left:0; width:6px; height:100%; }}
    .kpi-ventes::before {{ background: #0E4D2E; }}
    .kpi-alerte::before {{ background: linear-gradient(180deg, #F97316, #EF4444); }}
    .kpi-top::before {{ background: #0E4D2E; }}
    .kpi-icon {{ width:48px; height:48px; border-radius:50%; display:flex; align-items:center; justify-content:center; font-size:22px; flex-shrink:0; color:white; }}
    .kpi-icon-ventes {{ background: #0E4D2E; }}
    .kpi-icon-alerte {{ background: #F97316; }}
    .kpi-icon-top {{ background: #0E4D2E; }}
    .section-header {{
        background: linear-gradient(90deg, #062914 0%, #0E4D2E 55%, #C8A040 100%);
        border-radius:14px; padding:14px 20px; display:flex; align-items:center; gap:14px;
        box-shadow: 0 6px 18px rgba(10,46,28,0.25); border:1.5px solid #C8A040;
        margin:18px 0 14px 0;
    }}
    .section-header-gold-bar {{ width:5px; height:22px; background:#C8A040; border-radius:10px; }}
</style>
""", unsafe_allow_html=True)

if 'stock' not in st.session_state:
    st.session_state.stock = [
        {"Produit": "Ramdan Gourmet", "Prix": 23000, "Stock": 42, "Lot": "RD-24-09", "Peremption": "09/2026"},
        {"Produit": "Vidangeur", "Prix": 8000, "Stock": 18, "Lot": "VD-24-11", "Peremption": "11/2025"},
        {"Produit": "Ango Power", "Prix": 14000, "Stock": 65, "Lot": "AP-25-01", "Peremption": "01/2027"},
        {"Produit": "Soyayya Ladies", "Prix": 16000, "Stock": 12, "Lot": "SY-24-10", "Peremption": "10/2026"},
        {"Produit": "Lait Ango", "Prix": 11000, "Stock": 35, "Lot": "LA-25-02", "Peremption": "02/2027"},
    ]
if 'ventes' not in st.session_state: st.session_state.ventes = []
if 'agents' not in st.session_state:
    st.session_state.agents = [
        {"Nom": "Koffi", "Code": "APG-001", "Niveau": "Leader", "Parrain": "Boss", "Commission": 0},
        {"Nom": "Afi", "Code": "APG-002", "Niveau": "Distributeur", "Parrain": "Koffi", "Commission": 0},
        {"Nom": "Yawovi", "Code": "APG-003", "Niveau": "Starter", "Parrain": "Koffi", "Commission": 0},
    ]
if 'temoignages' not in st.session_state:
    st.session_state.temoignages = [
        {"Client": "Maman Chantal", "Produit": "Ango Power", "Note": 5, "Message": "Mon mari est redevenu jeune, merci APGIV!", "Date": "01/11/2026"},
    ]
if 'pin' not in st.session_state: st.session_state.pin = "1234"
if 'auth_compta' not in st.session_state: st.session_state.auth_compta = False
if 'derniere_vente' not in st.session_state: st.session_state.derniere_vente = None

def generer_facture_pdf(vente):
    pdf = FPDF()
    pdf.add_page()
    if os.path.exists(LOGO_PATH):
        pdf.image(LOGO_PATH, x=10, y=8, w=40)
    pdf.set_font("Arial", 'B', 16)
    pdf.set_text_color(6,41,20)
    pdf.cell(0,12,'APGIV OS Gestion', ln=True, align='C')
    pdf.set_font("Arial", 'B', 11)
    pdf.set_text_color(200,160,64)
    pdf.cell(0,7,'Facture Professionnelle - L\'Excellence au Naturel', ln=True, align='C')
    pdf.ln(10)
    pdf.set_font("Arial", 'B', 11)
    pdf.set_text_color(0,0,0)
    pdf.cell(0,7,f"Client: {vente['Client']} - Tel: {vente.get('Telephone','')}", ln=True)
    pdf.cell(0,7,f"Date: {vente['Date']} | Vendeur: {vente['Agent']} ({vente['Code']})", ln=True)
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
    pdf.cell(55,11,vente['Produit'],1)
    pdf.cell(25,11,vente['Lot'],1)
    pdf.cell(15,11,str(vente['Qte']),1)
    pdf.cell(35,11,f"{vente['Total']//vente['Qte']} F",1)
    pdf.cell(50,11,f"{vente['Total']} F CFA",1,1)
    pdf.ln(6)
    pdf.set_font("Arial", 'B', 14)
    pdf.set_text_color(6,41,20)
    pdf.cell(0,12,f"TOTAL: {vente['Total']} F CFA - {vente['Paiement']}", ln=True, align='R')
    pdf.ln(10)
    pdf.set_font("Arial", 'I', 8)
    pdf.set_text_color(100,100,100)
    pdf.cell(0,6,"Merci pour votre confiance - APGIV OS - Produits 100% Naturels", align='C')
    path = f"/tmp/facture_{vente['Client'].replace(' ','_')}_{datetime.now().strftime('%H%M%S')}.pdf"
    pdf.output(path)
    return path

def nettoyer_numero_tel(tel):
    tel = ''.join(filter(str.isdigit, tel))
    if tel.startswith('0'):
        tel = '228' + tel[1:]
    if not tel.startswith('228') and len(tel)==8:
        tel = '228' + tel
    return tel

with st.sidebar:
    st.image(LOGO_PATH, width='stretch')
    st.markdown("<div style='height:12px'></div>", unsafe_allow_html=True)
    menu = st.radio("NAVIGATION", ["Dashboard", "Magasin & Restockage", "Codes Agents", "MLM & Reseau", "Temoignages Clients", "Compta Privee"], label_visibility="collapsed")

st.markdown(f"""
<div class="apgiv-header-final">
    <div class="apgiv-logo-box">
        <img src="data:image/jpeg;base64,{logo_b64}" />
    </div>
    <div class="apgiv-header-content">
        <div class="apgiv-title-line">
            <span class="apgiv-title-os">APGIV OS</span>
            <span class="apgiv-title-gestion">Gestion</span>
        </div>
        <div class="apgiv-slogan">L'Excellence au Naturel - {datetime.now().strftime('%d/%m/%Y %H:%M')}</div>
    </div>
    <div class="apgiv-waves">
        <div class="wave wave-3"></div>
        <div class="wave wave-1"></div>
        <div class="wave wave-2"></div>
    </div>
</div>
""", unsafe_allow_html=True)

df_stock = pd.DataFrame(st.session_state.stock)

if "Dashboard" in menu:
    k1,k2,k3 = st.columns(3, gap="medium")
    with k1:
        st.markdown(f"""<div class="kpi-card kpi-ventes"><div class="kpi-icon kpi-icon-ventes">📅</div><div style="flex:1"><div style="font-size:12px; font-weight:700">VENTES JOUR</div><div style="font-size:28px; font-weight:900">{len(st.session_state.ventes)}</div><div style="font-size:12px; color:{OR}; font-weight:700">● Temps reel</div></div></div>""", unsafe_allow_html=True)
    with k2:
        alerte = len([s for s in st.session_state.stock if s['Stock']<20])
        st.markdown(f"""<div class="kpi-card kpi-alerte"><div class="kpi-icon kpi-icon-alerte">⚠️</div><div style="flex:1"><div style="font-size:12px; font-weight:700">STOCK ALERTE</div><div style="font-size:26px; font-weight:900">{alerte} Lots</div><div style="font-size:12px; color:#EF4444; font-weight:700">● Action requise</div></div></div>""", unsafe_allow_html=True)
    with k3:
        st.markdown(f"""<div class="kpi-card kpi-top"><div class="kpi-icon kpi-icon-top">🏆</div><div style="flex:1"><div style="font-size:12px; font-weight:700">AGENT TOP</div><div style="font-size:24px; font-weight:900">{st.session_state.ventes[0]['Agent'] if st.session_state.ventes else 'Koffi'}</div><div style="font-size:12px; color:{VERT}; font-weight:700">★ Meilleur du mois</div></div></div>""", unsafe_allow_html=True)
    st.markdown(f"""<div class="section-header"><div class="section-header-gold-bar"></div><div style="font-size:20px">📦</div><div style="color:white; font-weight:900; font-size:15px; letter-spacing:0.8px">STOCK & PEREMPTION - VUE GENERALE</div></div>""", unsafe_allow_html=True)
    st.dataframe(df_stock, width='stretch', hide_index=True, height=220)
    st.markdown(f"""<div class="section-header" style="background: linear-gradient(90deg, {VERT} 0%, {VERT_FONCE} 60%, {OR} 100%);"><div class="section-header-gold-bar"></div><div style="color:white; font-weight:800; font-size:14px">CAISSE INTELLIGENTE - VENTE + FACTURE PDF LOGO + WHATSAPP</div></div>""", unsafe_allow_html=True)
    col1,col2 = st.columns(2, gap="large")
    with col1:
        produit_sel = st.selectbox("Produit *", [s["Produit"] for s in st.session_state.stock])
        prod_info = next(s for s in st.session_state.stock if s["Produit"]==produit_sel)
        st.text_input("Prix Unitaire (auto)", value=f"{prod_info['Prix']} F", disabled=True)
        st.text_input("Lot (auto)", value=prod_info["Lot"], disabled=True)
        st.text_input("Peremption (auto)", value=prod_info["Peremption"], disabled=True)
        quantite = st.number_input("Quantité *", min_value=1, max_value=prod_info["Stock"], value=1)
        mode_paiement = st.selectbox("Mode Paiement *", ["Espèces", "Mixx by Yas", "Flooz"])
    with col2:
        nom_agent = st.text_input("Nom Agent Vendeur *", placeholder="Koffi")
        code_agent = st.text_input("Code Agent *", placeholder="APG-001")
        client_nom = st.text_input("Nom Client *", placeholder="M. Kodjo")
        client_tel = st.text_input("Téléphone WhatsApp Client *", placeholder="90 12 34 56")
        total_vente = prod_info['Prix']*quantite
        st.markdown(f"<div style='background:white; border:2.5px solid {VERT}; border-radius:14px; padding:16px; text-align:center'><p style='margin:0; font-size:11px; font-weight:700'>TOTAL A PAYER</p><p style='margin:0; font-size:30px; font-weight:900; color:{VERT_FONCE}'>{total_vente} F</p><p style='margin:0; font-size:11px; color:#667085'>Stock: {prod_info['Stock']} | {mode_paiement}</p></div>", unsafe_allow_html=True)
        can_sell = all([nom_agent.strip(), code_agent.strip(), client_nom.strip(), client_tel.strip()])
        code_valide = any(a["Code"]==code_agent and a["Nom"].lower()==nom_agent.lower() for a in st.session_state.agents)
        if nom_agent and code_agent and not code_valide:
            st.warning("Code agent non reconnu - Voir Codes Agents")
            can_sell = False
        if st.button("✅ Confirmer Vente + Générer Facture", disabled=not can_sell, width='stretch', type="primary"):
            prod_info["Stock"] -= quantite
            vente = {"Date": datetime.now().strftime("%d/%m/%Y %H:%M"), "Produit": produit_sel, "Qte": quantite, "Total": total_vente, "Paiement": mode_paiement, "Agent": nom_agent, "Code": code_agent, "Lot": prod_info["Lot"], "Client": client_nom, "Telephone": client_tel}
            st.session_state.ventes.append(vente)
            st.session_state.derniere_vente = vente
            for a in st.session_state.agents:
                if a["Code"]==code_agent:
                    a["Commission"] += int(total_vente * 0.10)
            st.success(f"Vente confirmée pour {client_nom}")
            st.rerun()
        if st.session_state.derniere_vente:
            v = st.session_state.derniere_vente
            pdf_path = generer_facture_pdf(v)
            with open(pdf_path, "rb") as f:
                st.download_button("📄 Télécharger Facture Pro PDF avec Logo Officiel", data=f, file_name=f"Facture_{v['Client']}.pdf", mime="application/pdf", width='stretch')
            tel_clean = nettoyer_numero_tel(v.get('Telephone',''))
            msg = f"Bonjour {v['Client']} 👋 Merci chez APGIV OS Gestion - {v['Produit']} x{v['Qte']} = {v['Total']}F CFA - Lot {v['Lot']} - Paiement {v['Paiement']}. Votre facture PDF avec logo officiel est prête. L'Excellence au Naturel 🌿"
            wa_link = f"https://wa.me/{tel_clean}?text={urllib.parse.quote(msg)}"
            st.link_button(f"📱 Envoyer Facture sur WhatsApp {v['Telephone']}", wa_link, width='stretch')
    if st.session_state.ventes:
        st.markdown(f"""<div class="section-header"><div class="section-header-gold-bar"></div><div style="color:white; font-weight:800; font-size:13px">JOURNAL DES VENTES - FACTURE & WHATSAPP</div></div>""", unsafe_allow_html=True)
        st.dataframe(pd.DataFrame(st.session_state.ventes), width='stretch', hide_index=True)
        for idx, vente in enumerate(reversed(st.session_state.ventes)):
            real_idx = len(st.session_state.ventes) - 1 - idx
            with st.expander(f"🧾 {vente['Date']} | {vente['Client']} | {vente['Produit']} | {vente['Total']} F"):
                c1,c2 = st.columns(2)
                with c1:
                    pdf_path = generer_facture_pdf(vente)
                    with open(pdf_path, "rb") as f:
                        st.download_button("📄 Facture PDF Logo", data=f, file_name=f"Facture_{vente['Client']}.pdf", mime="application/pdf", key=f"pdf_{real_idx}", width='stretch')
                with c2:
                    tel_clean = nettoyer_numero_tel(vente.get('Telephone',''))
                    wa_link = f"https://wa.me/{tel_clean}?text={urllib.parse.quote(f'Bonjour {vente['Client']}, facture APGIV {vente['Total']}F')}"
                    st.link_button("📱 WhatsApp Client", wa_link, key=f"wa_{real_idx}", width='stretch')

elif "Magasin" in menu:
    st.markdown(f'<div class="section-header"><div class="section-header-gold-bar"></div><div style="color:white; font-weight:800">MAGASIN & RESTOCKAGE</div></div>', unsafe_allow_html=True)
    tab1, tab2 = st.tabs(["Stock Général", "Restockage Sécurisé"])
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
            qte_restock = st.number_input("Qté Entrée *", min_value=1, value=10)
            lot_restock = st.text_input("Lot *", placeholder="RD-25-05")
        if st.button("Ajouter Produit / Lot", type="primary"):
            prod = next((s for s in st.session_state.stock if s["Produit"]==prod_restock), None)
            if prod:
                prod["Stock"] += qte_restock
                prod["Lot"]=lot_restock
            st.success("Restockage OK")
            st.rerun()

elif "Codes Agents" in menu:
    st.markdown(f'<div class="section-header"><div class="section-header-gold-bar"></div><div style="color:white; font-weight:800">CODES AGENTS - ATTRIBUTION + PERFORMANCE</div></div>', unsafe_allow_html=True)
    st.dataframe(pd.DataFrame(st.session_state.agents), width='stretch', hide_index=True)
    c1,c2 = st.columns(2)
    with c1:
        if st.session_state.ventes:
            df_v = pd.DataFrame(st.session_state.ventes)
            best = df_v.groupby("Agent")["Total"].sum().sort_values(ascending=False)
            st.bar_chart(best, width='stretch')
    with c2:
        new_nom = st.text_input("Nouveau Nom Agent")
        new_code = st.text_input("Code Unique", placeholder="APG-004")
        new_parrain = st.selectbox("Parrain", [a["Nom"] for a in st.session_state.agents])
        if st.button("Attribuer Code", width='stretch'):
            if new_nom and new_code:
                st.session_state.agents.append({"Nom": new_nom, "Code": new_code, "Niveau": "Starter", "Parrain": new_parrain, "Commission": 0})
                st.rerun()

elif "MLM" in menu:
    st.markdown(f'<div class="section-header"><div class="section-header-gold-bar"></div><div style="color:white; font-weight:800">MLM & RÉSEAU - GESTION COMPLÈTE</div></div>', unsafe_allow_html=True)
    st.dataframe(pd.DataFrame(st.session_state.agents), width='stretch', hide_index=True)
    for agent in st.session_state.agents:
        filleuls = [a["Nom"] for a in st.session_state.agents if a["Parrain"]==agent["Nom"]]
        if filleuls:
            st.write(f"👑 **{agent['Nom']} ({agent['Niveau']})** → {', '.join(filleuls)} | Commission: {agent['Commission']} F")

elif "Temoignages" in menu:
    st.markdown(f'<div class="section-header"><div class="section-header-gold-bar"></div><div style="color:white; font-weight:800">TÉMOIGNAGES CLIENTS - PREUVE SOCIALE</div></div>', unsafe_allow_html=True)
    for t in st.session_state.temoignages:
        st.markdown(f"<div style='border:2px solid {VERT}; border-left:6px solid {OR}; padding:14px; margin:10px 0; background:white; border-radius:12px'><b>{t['Client']}</b> - {t['Produit']} - {'⭐'*t['Note']}<br><i>\"{t['Message']}\"</i><br><small>{t['Date']}</small></div>", unsafe_allow_html=True)
    tc1,tc2 = st.columns(2)
    with tc1:
        t_client = st.text_input("Nom Client *")
        t_produit = st.selectbox("Produit Concerné *", [s["Produit"] for s in st.session_state.stock])
        t_note = st.slider("Note *", 1, 5, 5)
    with tc2:
        t_msg = st.text_area("Témoignage *")
        if st.button("Publier Témoignage", type="primary", width='stretch'):
            if t_client and t_msg:
                st.session_state.temoignages.append({"Client": t_client, "Produit": t_produit, "Note": t_note, "Message": t_msg, "Date": datetime.now().strftime("%d/%m/%Y")})
                st.rerun()

elif "Compta" in menu:
    # TITRE CORRIGÉ SANS PIN COMME DEMANDÉ
    st.markdown(f'<div class="section-header"><div class="section-header-gold-bar"></div><div style="color:white; font-weight:900; font-size:15px; letter-spacing:0.6px">COMPTA PRIVÉE - BILAN - RAPPORT</div></div>', unsafe_allow_html=True)
    
    if not st.session_state.auth_compta:
        st.markdown(f"<div style='background:white; border:2px solid {VERT}; border-radius:14px; padding:20px; text-align:center'><p style='font-weight:800; color:{VERT_FONCE}'>🔒 ACCÈS RÉSERVÉ BOSS</p><p style='font-size:12px; color:#667085'>Entrez le PIN Boss pour accéder au Bilan complet</p></div>", unsafe_allow_html=True)
        st.write("")
        pin_input = st.text_input("PIN Boss", type="password", placeholder="••••")
        col_p1, col_p2 = st.columns([2,1])
        with col_p1:
            if st.button("🔓 Déverrouiller Compta Privée", type="primary", width='stretch'):
                if pin_input == st.session_state.pin:
                    st.session_state.auth_compta=True
                    st.rerun()
                else:
                    st.error("PIN incorrect - Accès refusé")
        with col_p2:
            st.caption(f"PIN par défaut: 1234")
    else:
        total_ca = sum(v["Total"] for v in st.session_state.ventes) if st.session_state.ventes else 0
        valeur_stock = sum(s['Prix']*s['Stock'] for s in st.session_state.stock)
        benefice = int(total_ca*0.42)

        # LIGNE 1 - KPI COMPTA
        c1,c2,c3 = st.columns(3, gap="medium")
        with c1:
            st.markdown(f"<div style='background:white; border-left:6px solid {VERT}; border-radius:14px; padding:16px; box-shadow:0 4px 12px rgba(0,0,0,0.08)'><p style='margin:0; font-size:11px; font-weight:700; color:#667085'>CA TOTAL</p><p style='margin:4px 0 0 0; font-size:26px; font-weight:900; color:{VERT_FONCE}'>{total_ca} F</p><p style='margin:4px 0 0 0; font-size:11px; color:{OR}'>● Cumul ventes</p></div>", unsafe_allow_html=True)
        with c2:
            st.markdown(f"<div style='background:white; border-left:6px solid #F97316; border-radius:14px; padding:16px; box-shadow:0 4px 12px rgba(0,0,0,0.08)'><p style='margin:0; font-size:11px; font-weight:700; color:#667085'>VALEUR STOCK</p><p style='margin:4px 0 0 0; font-size:26px; font-weight:900; color:{VERT_FONCE}'>{valeur_stock} F</p><p style='margin:4px 0 0 0; font-size:11px; color:#F97316'>● Inventaire auto</p></div>", unsafe_allow_html=True)
        with c3:
            st.markdown(f"<div style='background:white; border-left:6px solid {OR}; border-radius:14px; padding:16px; box-shadow:0 4px 12px rgba(0,0,0,0.08)'><p style='margin:0; font-size:11px; font-weight:700; color:#667085'>BÉNÉFICE (42%)</p><p style='margin:4px 0 0 0; font-size:26px; font-weight:900; color:{VERT_FONCE}'>{benefice} F</p><p style='margin:4px 0 0 0; font-size:11px; color:{OR}'>● Marge nette</p></div>", unsafe_allow_html=True)

        st.write("")
        if st.session_state.ventes:
            df_v = pd.DataFrame(st.session_state.ventes)
            
            # BILAN DES VENTES PAR PRODUIT
            st.markdown(f'<div class="section-header" style="margin-top:10px"><div class="section-header-gold-bar"></div><div style="color:white; font-weight:800; font-size:13px">📊 BILAN DES VENTES PAR PRODUIT</div></div>', unsafe_allow_html=True)
            b1,b2 = st.columns([2,1], gap="large")
            with b1:
                bilan_produit = df_v.groupby("Produit")[["Qte","Total"]].sum().sort_values("Total", ascending=False)
                bilan_produit.columns = ["Quantité Vendue","CA Produit"]
                st.bar_chart(bilan_produit["CA Produit"], width='stretch')
            with b2:
                st.dataframe(bilan_produit, width='stretch')

            # BILAN SELON L'AGENT QUI A VENDU
            st.markdown(f'<div class="section-header"><div class="section-header-gold-bar"></div><div style="color:white; font-weight:800; font-size:13px">👤 BILAN PAR AGENT VENDEUR</div></div>', unsafe_allow_html=True)
            a1,a2 = st.columns([2,1], gap="large")
            with a1:
                bilan_agent = df_v.groupby("Agent")[["Qte","Total"]].sum().sort_values("Total", ascending=False)
                bilan_agent.columns = ["Qté Vendue","CA Agent"]
                # Ajoute commission
                bilan_agent["Commission 10%"] = (bilan_agent["CA Agent"]*0.10).astype(int)
                st.bar_chart(bilan_agent["CA Agent"], width='stretch')
            with a2:
                st.dataframe(bilan_agent, width='stretch')

            # INVENTAIRE AUTO QUI SUIT
            st.markdown(f'<div class="section-header"><div class="section-header-gold-bar"></div><div style="color:white; font-weight:800; font-size:13px">📦 INVENTAIRE AUTO - STOCK RESTANT + VALEUR</div></div>', unsafe_allow_html=True)
            df_inv = df_stock.copy()
            df_inv["Valeur Stock"] = df_inv["Prix"]*df_inv["Stock"]
            df_inv["Statut"] = df_inv["Stock"].apply(lambda x: "🔴 ALERTE" if x<20 else "🟢 OK")
            st.dataframe(df_inv[["Produit","Stock","Lot","Peremption","Valeur Stock","Statut"]], width='stretch', hide_index=True)

            # RAPPORT AUTO JOURNALIER
            st.markdown(f'<div class="section-header"><div class="section-header-gold-bar"></div><div style="color:white; font-weight:800; font-size:13px">📝 RAPPORT AUTO JOURNALIER - {datetime.now().strftime("%d/%m/%Y")}</div></div>', unsafe_allow_html=True)
            today = datetime.now().strftime("%d/%m/%Y")
            ventes_jour = [v for v in st.session_state.ventes if today in v["Date"]]
            ca_jour = sum(v["Total"] for v in ventes_jour)
            st.markdown(f"""
            <div style='background:white; border:2px solid {VERT}; border-radius:14px; padding:18px'>
                <p style='margin:0; font-weight:900; color:{VERT_FONCE}'>Rapport du {today}</p>
                <p style='margin:6px 0 0 0; font-size:13px'>• Nombre de ventes aujourd'hui : <b>{len(ventes_jour)}</b><br>
                • Chiffre d'affaires du jour : <b>{ca_jour} F CFA</b><br>
                • Bénéfice jour (42%) : <b>{int(ca_jour*0.42)} F</b><br>
                • Produits les plus vendus : <b>{', '.join(bilan_produit.index[:2]) if len(bilan_produit)>0 else 'Aucun'}</b><br>
                • Top vendeur du jour : <b>{bilan_agent.index[0] if len(bilan_agent)>0 else 'Aucun'}</b><br>
                • Stock critique (&lt;20) : <b>{len([s for s in st.session_state.stock if s['Stock']<20])} lots</b></p>
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
        # SÉCURITÉ - MODIFIER PIN + VERROUILLER
        c_sec1, c_sec2 = st.columns(2, gap="large")
        with c_sec1:
            with st.expander("🔑 Modifier PIN Boss (Sécurité)"):
                new_pin = st.text_input("Nouveau PIN", type="password", placeholder="Nouveau code")
                if st.button("Changer PIN", type="primary"):
                    if new_pin and len(new_pin)>=4:
                        st.session_state.pin = new_pin
                        st.success(f"PIN modifié avec succès ! Nouveau PIN : {new_pin}")
                    else:
                        st.error("PIN trop court (4 chiffres min)")
                st.caption(f"PIN actuel : {st.session_state.pin}")
        with c_sec2:
            st.write("")
            if st.button("🔒 Verrouiller Compta Privée", width='stretch'):
                st.session_state.auth_compta=False
                st.rerun()