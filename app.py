import os
import base64
import urllib.parse
from datetime import datetime
from io import BytesIO

import pandas as pd
import streamlit as st
from fpdf import FPDF


# ============================================================
# APGIV OS GESTION — VERSION PREMIUM
# ============================================================

LOGO_PATH = "assets/Logo.jpeg"

VERT_FONCE = "#062914"
VERT = "#0E4D2E"
VERT_CLAIR = "#1D7A45"
OR = "#C8A040"
FOND = "#F4F7F3"
BLANC = "#FFFFFF"
TEXTE = "#17251C"


# ============================================================
# CONFIGURATION STREAMLIT
# ============================================================

st.set_page_config(
    page_title="APGIV OS Gestion",
    page_icon="🌿",
    layout="wide",
    initial_sidebar_state="expanded"
)


def get_logo_b64():
    if os.path.exists(LOGO_PATH):
        with open(LOGO_PATH, "rb") as fichier:
            return base64.b64encode(fichier.read()).decode("utf-8")
    return ""


logo_b64 = get_logo_b64()


# ============================================================
# DESIGN PREMIUM — CSS
# ============================================================

st.markdown(
    f"""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=DM+Sans:wght@400;500;600;700;800&family=Manrope:wght@400;500;600;700;800&display=swap');

    html, body, [class*="css"] {{
        font-family: 'DM Sans', 'Manrope', sans-serif;
    }}

    .stApp {{
        background:
            radial-gradient(circle at 95% 0%, rgba(200,160,64,.08), transparent 25%),
            linear-gradient(135deg, #F7F9F6 0%, #EEF3ED 100%);
        color: {TEXTE};
    }}

    [data-testid="stHeader"] {{
        background: transparent;
        height: 2.2rem;
    }}

    .block-container {{
        max-width: 1600px;
        padding-top: 1.1rem;
        padding-bottom: 2rem;
    }}

    [data-testid="stSidebar"] {{
        background: linear-gradient(
            180deg,
            #041D10 0%,
            #07351D 58%,
            #0B4727 100%
        );
        border-right: 3px solid {OR};
    }}

    [data-testid="stSidebar"] > div:first-child {{
        padding-top: 1.1rem;
    }}

    [data-testid="stSidebar"] * {{
        color: white;
    }}

    [data-testid="stSidebar"] .stRadio > label {{
        display: none;
    }}

    [data-testid="stSidebar"] div[role="radiogroup"] {{
        gap: 9px;
    }}

    [data-testid="stSidebar"] div[role="radiogroup"] label {{
        background: rgba(255,255,255,.045);
        border: 1px solid rgba(255,255,255,.58);
        border-radius: 28px;
        padding: 10px 13px;
        min-height: 42px;
        transition: all .2s ease;
    }}

    [data-testid="stSidebar"] div[role="radiogroup"] label:hover {{
        background: rgba(255,255,255,.14);
        border-color: {OR};
    }}

    [data-testid="stSidebar"] div[role="radiogroup"] label:has(input:checked) {{
        background: linear-gradient(90deg, #238D49, #55B95D);
        border: 1px solid {OR};
        box-shadow: 0 4px 14px rgba(0,0,0,.22);
        font-weight: 800;
    }}

    [data-testid="stSidebar"] div[role="radiogroup"] label p {{
        font-size: 13px;
        font-weight: 650;
    }}

    .brand-card {{
        padding: 13px 10px 17px;
        margin-bottom: 20px;
        border-bottom: 1px solid rgba(200,160,64,.65);
        text-align: center;
    }}

    .brand-card img {{
        max-width: 76px;
        max-height: 76px;
        object-fit: contain;
        border-radius: 50%;
        background: white;
        padding: 4px;
        margin-bottom: 8px;
    }}

    .brand-name {{
        color: white;
        font-size: 20px;
        font-weight: 850;
        line-height: 1.05;
    }}

    .brand-sub {{
        color: #E5C879;
        font-size: 10px;
        font-style: italic;
        margin-top: 5px;
    }}

    .main-hero {{
        position: relative;
        overflow: hidden;
        display: flex;
        align-items: center;
        min-height: 104px;
        padding: 17px 24px;
        margin-bottom: 18px;
        border: 1px solid rgba(200,160,64,.55);
        border-radius: 18px;
        background: linear-gradient(
            105deg,
            #FFFFFF 0%,
            #F5F8F3 54%,
            #E5EEE3 100%
        );
        box-shadow: 0 5px 18px rgba(12,45,24,.08);
    }}

    .hero-logo {{
        width: 66px;
        height: 66px;
        border-radius: 15px;
        object-fit: contain;
        background: white;
        padding: 5px;
        border: 1px solid #E4E9E2;
        margin-right: 17px;
    }}

    .hero-title {{
        font-size: clamp(22px, 2.5vw, 32px);
        color: {VERT_FONCE};
        font-weight: 900;
        letter-spacing: -1px;
        line-height: 1.1;
    }}

    .hero-subtitle {{
        color: #69776C;
        font-size: 12px;
        font-weight: 600;
        margin-top: 6px;
    }}

    .hero-accent {{
        position: absolute;
        right: -35px;
        top: -65px;
        width: 250px;
        height: 155px;
        transform: rotate(-18deg);
        border-bottom: 9px solid {OR};
        border-radius: 0 0 0 100%;
        opacity: .9;
        pointer-events: none;
    }}

    .hero-accent:after {{
        content: "";
        position: absolute;
        right: 20px;
        top: 16px;
        width: 240px;
        height: 150px;
        border-bottom: 18px solid {VERT};
        border-radius: 0 0 0 100%;
    }}

    .section-header {{
        display: flex;
        align-items: center;
        gap: 11px;
        color: white;
        background: linear-gradient(
            100deg,
            #062914 0%,
            #0E4D2E 66%,
            #287343 100%
        );
        border: 1px solid rgba(200,160,64,.8);
        border-radius: 11px;
        padding: 12px 15px;
        margin: 18px 0 12px;
        box-shadow: 0 4px 11px rgba(6,41,20,.12);
        font-size: 13px;
        font-weight: 850;
        letter-spacing: .45px;
    }}

    .gold-bar {{
        width: 5px;
        align-self: stretch;
        min-height: 20px;
        background: {OR};
        border-radius: 8px;
    }}

    .kpi-card {{
        display: flex;
        align-items: center;
        gap: 13px;
        min-height: 94px;
        background: white;
        border: 1px solid #E2E9E1;
        border-left: 5px solid {VERT};
        border-radius: 15px;
        padding: 15px 16px;
        box-shadow: 0 5px 16px rgba(12,45,24,.07);
        margin-bottom: 10px;
    }}

    .kpi-card.orange {{
        border-left-color: #E0782F;
    }}

    .kpi-card.gold {{
        border-left-color: {OR};
    }}

    .kpi-icon {{
        display: flex;
        align-items: center;
        justify-content: center;
        flex: 0 0 43px;
        width: 43px;
        height: 43px;
        border-radius: 50%;
        background: #E8F2E9;
        font-size: 21px;
    }}

    .kpi-card.orange .kpi-icon {{
        background: #FFF0E6;
    }}

    .kpi-card.gold .kpi-icon {{
        background: #FBF4DF;
    }}

    .kpi-label {{
        font-size: 10px;
        color: #59675D;
        font-weight: 850;
        letter-spacing: .5px;
    }}

    .kpi-value {{
        color: {VERT_FONCE};
        font-size: 25px;
        font-weight: 900;
        line-height: 1.2;
        margin-top: 3px;
    }}

    .kpi-note {{
        font-size: 10px;
        color: #77847A;
        margin-top: 4px;
        font-weight: 650;
    }}

    div[data-testid="stDataFrame"] {{
        border: 1px solid #E0E7DF;
        border-radius: 11px;
        overflow: hidden;
        box-shadow: 0 3px 12px rgba(12,45,24,.045);
    }}

    div[data-testid="stTextInput"] input,
    div[data-testid="stNumberInput"] input,
    div[data-testid="stSelectbox"] > div,
    div[data-testid="stTextArea"] textarea {{
        border-radius: 9px;
    }}

    .stButton > button,
    .stDownloadButton > button,
    .stLinkButton > a {{
        border-radius: 10px;
        font-weight: 750;
        min-height: 42px;
    }}

    .stButton > button[kind="primary"] {{
        background: linear-gradient(90deg, {VERT}, #218449);
        border: 1px solid {OR};
    }}

    .total-box {{
        background: linear-gradient(135deg, #FFFFFF, #F0F6EF);
        border: 2px solid {VERT};
        border-radius: 14px;
        padding: 15px;
        text-align: center;
        box-shadow: 0 4px 12px rgba(6,41,20,.06);
        margin: 8px 0 14px;
    }}

    .total-label {{
        color: #657268;
        font-size: 10px;
        font-weight: 850;
        letter-spacing: .6px;
    }}

    .total-value {{
        color: {VERT_FONCE};
        font-size: 29px;
        font-weight: 950;
        margin: 2px 0;
    }}

    .private-box {{
        background: white;
        border: 1px solid #DCE6DC;
        border-left: 5px solid {OR};
        border-radius: 13px;
        padding: 17px;
        box-shadow: 0 4px 13px rgba(6,41,20,.05);
    }}

    .stTabs [data-baseweb="tab-list"] {{
        gap: 7px;
    }}

    .stTabs [data-baseweb="tab"] {{
        border-radius: 9px 9px 0 0;
        padding: 9px 15px;
        font-weight: 700;
    }}

    hr {{
        border-color: #DCE5DA;
    }}

    @media (max-width: 700px) {{
        .block-container {{
            padding-left: .8rem;
            padding-right: .8rem;
        }}

        .main-hero {{
            padding: 13px;
            min-height: 84px;
        }}

        .hero-logo {{
            width: 49px;
            height: 49px;
            margin-right: 10px;
        }}

        .hero-subtitle {{
            font-size: 10px;
        }}

        .kpi-value {{
            font-size: 21px;
        }}
    }}
    </style>
    """,
    unsafe_allow_html=True
)


# ============================================================
# DONNÉES INITIALES
# ============================================================

def init_state():

    defaults = {
        "stock": [
            {
                "Produit": "Ramdan Gourmet",
                "Prix": 23000,
                "Stock": 42,
                "Lot": "RD-24-09",
                "Peremption": "09/2026"
            },
            {
                "Produit": "Vidangeur",
                "Prix": 8000,
                "Stock": 18,
                "Lot": "VD-24-11",
                "Peremption": "11/2025"
            },
            {
                "Produit": "Ango Power",
                "Prix": 14000,
                "Stock": 65,
                "Lot": "AP-25-01",
                "Peremption": "01/2027"
            },
            {
                "Produit": "Soyayya Ladies",
                "Prix": 16000,
                "Stock": 12,
                "Lot": "SY-24-10",
                "Peremption": "10/2026"
            },
            {
                "Produit": "Lait Ango",
                "Prix": 11000,
                "Stock": 35,
                "Lot": "LA-25-02",
                "Peremption": "02/2027"
            }
        ],

        "ventes": [],

        "agents": [
            {
                "Nom": "Koffi",
                "Code": "APG-001",
                "Niveau": "Leader",
                "Parrain": "Boss",
                "Commission": 0
            },
            {
                "Nom": "Afi",
                "Code": "APG-002",
                "Niveau": "Distributeur",
                "Parrain": "Koffi",
                "Commission": 0
            },
            {
                "Nom": "Yawovi",
                "Code": "APG-003",
                "Niveau": "Starter",
                "Parrain": "Koffi",
                "Commission": 0
            }
        ],

        "temoignages": [
            {
                "Client": "Maman Chantal",
                "Produit": "Ango Power",
                "Note": 5,
                "Message": "Mon mari est redevenu jeune, merci APGIV!",
                "Date": "01/11/2026"
            }
        ],

        "pin": "1234",
        "auth_compta": False,
        "derniere_vente": None
    }

    for key, value in defaults.items():
        if key not in st.session_state:
            st.session_state[key] = value


init_state()


# ============================================================
# FONCTIONS UTILITAIRES
# ============================================================

def section(titre, emoji=""):
    st.markdown(
        f'<div class="section-header">'
        f'<span class="gold-bar"></span>'
        f'<span>{emoji}</span>'
        f'<span>{titre}</span>'
        f'</div>',
        unsafe_allow_html=True
    )


def fcfa(valeur):
    return f"{int(valeur):,}".replace(",", " ") + " F CFA"


def nettoyer_numero_tel(tel):

    tel = "".join(filter(str.isdigit, str(tel)))

    if tel.startswith("0"):
        tel = "228" + tel[1:]

    elif len(tel) == 8 and not tel.startswith("228"):
        tel = "228" + tel

    return tel


def pdf_text(value):
    return str(value).encode(
        "latin-1",
        "replace"
    ).decode("latin-1")


# ============================================================
# FACTURE PDF — GÉNÉRATION EN MÉMOIRE
# CORRECTION FILE NOT FOUND ERROR
# ============================================================

def generer_facture_pdf(vente):

    pdf = FPDF()
    pdf.set_auto_page_break(auto=True, margin=15)
    pdf.add_page()

    if os.path.exists(LOGO_PATH):
        pdf.image(LOGO_PATH, x=10, y=8, w=28)

    pdf.set_y(12)

    pdf.set_font("Arial", "B", 17)
    pdf.set_text_color(6, 41, 20)

    pdf.cell(
        0,
        10,
        "APGIV OS Gestion",
        ln=True,
        align="C"
    )

    pdf.set_font("Arial", "B", 10)
    pdf.set_text_color(200, 160, 64)

    pdf.cell(
        0,
        7,
        "Facture professionnelle - L'Excellence au Naturel",
        ln=True,
        align="C"
    )

    pdf.ln(12)

    pdf.set_text_color(25, 35, 28)
    pdf.set_font("Arial", "B", 10)

    pdf.cell(
        0,
        7,
        pdf_text(
            f"Client : {vente['Client']} | "
            f"Téléphone : {vente.get('Telephone', '')}"
        ),
        ln=True
    )

    pdf.cell(
        0,
        7,
        pdf_text(
            f"Date : {vente['Date']} | "
            f"Vendeur : {vente['Agent']} ({vente['Code']})"
        ),
        ln=True
    )

    pdf.ln(5)

    pdf.set_fill_color(6, 41, 20)
    pdf.set_text_color(255, 255, 255)
    pdf.set_font("Arial", "B", 9)

    widths = [58, 28, 18, 37, 49]

    headers = [
        "Produit",
        "Lot",
        "Qte",
        "Prix unitaire",
        "Total"
    ]

    for i, header in enumerate(headers):
        pdf.cell(
            widths[i],
            10,
            pdf_text(header),
            border=1,
            align="C",
            fill=True
        )

    pdf.ln()

    prix_unitaire = (
        int(vente["Total"]) //
        max(int(vente["Qte"]), 1)
    )

    values = [
        vente["Produit"],
        vente["Lot"],
        str(vente["Qte"]),
        fcfa(prix_unitaire),
        fcfa(vente["Total"])
    ]

    pdf.set_text_color(20, 20, 20)
    pdf.set_font("Arial", "", 9)

    for i, value in enumerate(values):
        pdf.cell(
            widths[i],
            12,
            pdf_text(value),
            border=1,
            align="C"
        )

    pdf.ln(18)

    pdf.set_font("Arial", "B", 14)
    pdf.set_text_color(6, 41, 20)

    pdf.cell(
        0,
        10,
        pdf_text(
            f"TOTAL : {fcfa(vente['Total'])} | "
            f"{vente['Paiement']}"
        ),
        ln=True,
        align="R"
    )

    pdf.ln(14)

    pdf.set_font("Arial", "I", 9)
    pdf.set_text_color(100, 100, 100)

    pdf.cell(
        0,
        7,
        "Merci pour votre confiance - APGIV OS - L'Excellence au Naturel",
        align="C"
    )

    # IMPORTANT :
    # Aucun fichier temporaire n'est créé sur le serveur.
    # Le PDF est directement généré en mémoire.
    output = pdf.output(dest="S")

    if isinstance(output, str):
        return output.encode("latin-1")

    return bytes(output)


# ============================================================
# WHATSAPP
# ============================================================

def lien_whatsapp(vente):

    telephone = nettoyer_numero_tel(
        vente.get("Telephone", "")
    )

    message = (
        f"Bonjour {vente['Client']} 👋 "
        f"Merci pour votre confiance chez APGIV OS. "
        f"{vente['Produit']} x{vente['Qte']} = "
        f"{fcfa(vente['Total'])}. "
        f"Lot {vente['Lot']} - "
        f"Paiement : {vente['Paiement']}. "
        "Votre facture est disponible. "
        "L'Excellence au Naturel 🌿"
    )

    return (
        f"https://wa.me/{telephone}"
        f"?text={urllib.parse.quote(message)}"
    )


# ============================================================
# MEILLEUR AGENT
# ============================================================

def top_agent():

    if not st.session_state.ventes:
        return "Koffi"

    ventes_df = pd.DataFrame(
        st.session_state.ventes
    )

    classement = (
        ventes_df.groupby("Agent")["Total"]
        .sum()
        .sort_values(ascending=False)
    )

    return (
        str(classement.index[0])
        if not classement.empty
        else "Koffi"
    )


# ============================================================
# SIDEBAR
# ============================================================

with st.sidebar:

    if logo_b64:

        st.markdown(
            f"""
            <div class="brand-card">
                <img src="data:image/jpeg;base64,{logo_b64}">
                <div class="brand-name">
                    APGIV OS<br>Gestion
                </div>
                <div class="brand-sub">
                    L’Excellence au Naturel
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )

    else:

        st.markdown(
            """
            <div class="brand-card">
                <div class="brand-name">
                    🌿 APGIV OS<br>Gestion
                </div>
                <div class="brand-sub">
                    L’Excellence au Naturel
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )

    menu = st.radio(
        "NAVIGATION",
        [
            "Dashboard",
            "Magasin & Restockage",
            "Codes Agents",
            "MLM & Réseau",
            "Témoignages Clients",
            "Compta Privée"
        ],
        label_visibility="collapsed"
    )

    st.markdown("---")
    st.caption("APGIV OS • Gestion Premium")


# ============================================================
# EN-TÊTE PRINCIPAL
# ============================================================

logo_html = (
    f'<img class="hero-logo" '
    f'src="data:image/jpeg;base64,{logo_b64}">'
    if logo_b64
    else
    '<div class="hero-logo" '
    'style="display:flex;align-items:center;'
    'justify-content:center">🌿</div>'
)

st.markdown(
    f"""
    <div class="main-hero">
        {logo_html}

        <div>
            <div class="hero-title">
                APGIV OS Gestion
            </div>

            <div class="hero-subtitle">
                L’Excellence au Naturel ·
                {datetime.now().strftime("%d/%m/%Y %H:%M")}
            </div>
        </div>

        <div class="hero-accent"></div>
    </div>
    """,
    unsafe_allow_html=True
)

df_stock = pd.DataFrame(
    st.session_state.stock
)


# ============================================================
# 1. DASHBOARD
# ============================================================

if menu == "Dashboard":

    ventes_jour = [
        v for v in st.session_state.ventes
        if v["Date"].startswith(
            datetime.now().strftime("%d/%m/%Y")
        )
    ]

    alertes = sum(
        1 for s in st.session_state.stock
        if int(s["Stock"]) < 20
    )

    k1, k2, k3 = st.columns(3, gap="medium")

    with k1:

        st.markdown(
            f"""
            <div class="kpi-card">
                <div class="kpi-icon">📅</div>
                <div>
                    <div class="kpi-label">
                        VENTES DU JOUR
                    </div>
                    <div class="kpi-value">
                        {len(ventes_jour)}
                    </div>
                    <div class="kpi-note">
                        ● Activité en temps réel
                    </div>
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )

    with k2:

        st.markdown(
            f"""
            <div class="kpi-card orange">
                <div class="kpi-icon">⚠️</div>
                <div>
                    <div class="kpi-label">
                        STOCK EN ALERTE
                    </div>
                    <div class="kpi-value">
                        {alertes} Lots
                    </div>
                    <div class="kpi-note">
                        ● Action requise
                    </div>
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )

    with k3:

        st.markdown(
            f"""
            <div class="kpi-card gold">
                <div class="kpi-icon">🏆</div>
                <div>
                    <div class="kpi-label">
                        AGENT TOP
                    </div>
                    <div class="kpi-value">
                        {top_agent()}
                    </div>
                    <div class="kpi-note">
                        ★ Meilleur chiffre d’affaires
                    </div>
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )

    section(
        "STOCK & PÉREMPTION — VUE GÉNÉRALE",
        "📦"
    )

    st.dataframe(
        df_stock,
        use_container_width=True,
        hide_index=True,
        height=220
    )

    section(
        "CAISSE INTELLIGENTE — VENTE, FACTURE PDF & WHATSAPP",
        "🧾"
    )

    col1, col2 = st.columns(2, gap="large")

    with col1:

        produits = [
            s["Produit"]
            for s in st.session_state.stock
        ]

        produit_sel = st.selectbox(
            "Produit *",
            produits
        )

        prod_info = next(
            s for s in st.session_state.stock
            if s["Produit"] == produit_sel
        )

        st.text_input(
            "Prix unitaire",
            value=fcfa(prod_info["Prix"]),
            disabled=True
        )

        st.text_input(
            "Numéro de lot",
            value=prod_info["Lot"],
            disabled=True
        )

        st.text_input(
            "Date de péremption",
            value=prod_info["Peremption"],
            disabled=True
        )

        quantite = st.number_input(
            "Quantité *",
            min_value=1,
            max_value=max(1, int(prod_info["Stock"])),
            value=1,
            step=1
        )

        mode_paiement = st.selectbox(
            "Mode de paiement *",
            [
                "Espèces",
                "Mixx by Yas",
                "Flooz"
            ]
        )

    with col2:

        nom_agent = st.text_input(
            "Nom de l’agent vendeur *",
            placeholder="Koffi"
        )

        code_agent = st.text_input(
            "Code agent *",
            placeholder="APG-001"
        )

        client_nom = st.text_input(
            "Nom du client *",
            placeholder="M. Kodjo"
        )

        client_tel = st.text_input(
            "Téléphone WhatsApp du client *",
            placeholder="90 12 34 56"
        )

        total_vente = (
            int(prod_info["Prix"]) *
            int(quantite)
        )

        st.markdown(
            f"""
            <div class="total-box">
                <div class="total-label">
                    TOTAL À PAYER
                </div>

                <div class="total-value">
                    {fcfa(total_vente)}
                </div>

                <div class="kpi-note">
                    Stock disponible : {prod_info["Stock"]}
                    · {mode_paiement}
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )

        champs_ok = all([
            nom_agent.strip(),
            code_agent.strip(),
            client_nom.strip(),
            client_tel.strip()
        ])

        code_valide = any(
            a["Code"].strip().upper()
            == code_agent.strip().upper()
            and
            a["Nom"].strip().lower()
            == nom_agent.strip().lower()
            for a in st.session_state.agents
        )

        if nom_agent and code_agent and not code_valide:

            st.warning(
                "Code agent non reconnu. "
                "Vérifiez les informations dans Codes Agents."
            )

        can_sell = (
            champs_ok
            and code_valide
            and int(prod_info["Stock"]) >= int(quantite)
        )

        if st.button(
            "✅ CONFIRMER LA VENTE ET GÉNÉRER LA FACTURE",
            disabled=not can_sell,
            use_container_width=True,
            type="primary"
        ):

            prod_info["Stock"] -= int(quantite)

            vente = {
                "Date": datetime.now().strftime(
                    "%d/%m/%Y %H:%M"
                ),
                "Produit": produit_sel,
                "Qte": int(quantite),
                "Total": total_vente,
                "Paiement": mode_paiement,
                "Agent": nom_agent.strip(),
                "Code": code_agent.strip().upper(),
                "Lot": prod_info["Lot"],
                "Client": client_nom.strip(),
                "Telephone": client_tel.strip()
            }

            st.session_state.ventes.append(vente)

            st.session_state.derniere_vente = vente

            for agent in st.session_state.agents:

                if (
                    agent["Code"].upper()
                    == code_agent.strip().upper()
                ):

                    agent["Commission"] += int(
                        total_vente * 0.10
                    )

                    break

            st.success(
                f"Vente confirmée pour {client_nom}."
            )

            st.rerun()

    # DERNIÈRE FACTURE

    if st.session_state.derniere_vente:

        vente = st.session_state.derniere_vente

        pdf_data = generer_facture_pdf(vente)

        safe_client = "".join(
            c if c.isalnum() else "_"
            for c in vente["Client"]
        )

        st.download_button(
            "📄 Télécharger la dernière facture PDF",
            data=pdf_data,
            file_name=f"Facture_APGIV_{safe_client}.pdf",
            mime="application/pdf",
            use_container_width=True
        )

        st.link_button(
            f"📱 Préparer l’envoi WhatsApp — {vente['Telephone']}",
            lien_whatsapp(vente),
            use_container_width=True
        )

    # JOURNAL DES VENTES

    if st.session_state.ventes:

        section(
            "JOURNAL DES VENTES — FACTURES & WHATSAPP",
            "📚"
        )

        st.dataframe(
            pd.DataFrame(st.session_state.ventes),
            use_container_width=True,
            hide_index=True
        )

        for idx, vente in enumerate(
            reversed(st.session_state.ventes)
        ):

            real_idx = (
                len(st.session_state.ventes)
                - 1
                - idx
            )

            with st.expander(
                f"🧾 {vente['Date']} | "
                f"{vente['Client']} | "
                f"{vente['Produit']} | "
                f"{fcfa(vente['Total'])}"
            ):

                c1, c2 = st.columns(2)

                with c1:

                    safe_client = "".join(
                        c if c.isalnum() else "_"
                        for c in vente["Client"]
                    )

                    st.download_button(
                        "📄 Télécharger la facture PDF",
                        data=generer_facture_pdf(vente),
                        file_name=(
                            f"Facture_APGIV_{safe_client}_"
                            f"{real_idx + 1}.pdf"
                        ),
                        mime="application/pdf",
                        key=f"pdf_{real_idx}",
                        use_container_width=True
                    )

                with c2:

                    st.link_button(
                        "📱 WhatsApp Client",
                        lien_whatsapp(vente),
                        use_container_width=True
                    )


# ============================================================
# 2. MAGASIN & RESTOCKAGE
# ============================================================

elif menu == "Magasin & Restockage":

    section(
        "MAGASIN & RESTOCKAGE",
        "📦"
    )

    tab1, tab2 = st.tabs([
        "Stock général",
        "Restockage sécurisé"
    ])

    with tab1:

        df_stock = pd.DataFrame(
            st.session_state.stock
        )

        st.dataframe(
            df_stock,
            use_container_width=True,
            hide_index=True
        )

        st.metric(
            "Références produits",
            len(st.session_state.stock)
        )

        st.metric(
            "Unités en stock",
            sum(
                int(s["Stock"])
                for s in st.session_state.stock
            )
        )

    with tab2:

        r1, r2 = st.columns(2, gap="large")

        with r1:

            restock_agent = st.text_input(
                "Agent responsable *"
            )

            restock_code = st.text_input(
                "Code agent *"
            )

            fournisseur = st.text_input(
                "Fournisseur *"
            )

        with r2:

            produits = [
                s["Produit"]
                for s in st.session_state.stock
            ]

            prod_restock = st.selectbox(
                "Produit concerné *",
                produits
            )

            qte_restock = st.number_input(
                "Quantité entrée *",
                min_value=1,
                value=10,
                step=1
            )

            lot_restock = st.text_input(
                "Nouveau numéro de lot *",
                placeholder="RD-25-05"
            )

            peremption_restock = st.text_input(
                "Péremption (MM/AAAA)",
                placeholder="05/2027"
            )

        if st.button(
            "➕ VALIDER LE RESTOCKAGE",
            type="primary",
            use_container_width=True
        ):

            agent_valide = any(
                a["Code"].upper()
                == restock_code.strip().upper()
                and
                a["Nom"].lower()
                == restock_agent.strip().lower()
                for a in st.session_state.agents
            )

            if not all([
                restock_agent.strip(),
                restock_code.strip(),
                fournisseur.strip(),
                lot_restock.strip()
            ]):

                st.error(
                    "Veuillez renseigner tous les champs obligatoires."
                )

            elif not agent_valide:

                st.error(
                    "Agent ou code agent non reconnu."
                )

            else:

                produit = next(
                    s for s in st.session_state.stock
                    if s["Produit"] == prod_restock
                )

                produit["Stock"] += int(qte_restock)

                produit["Lot"] = lot_restock.strip()

                if peremption_restock.strip():
                    produit["Peremption"] = (
                        peremption_restock.strip()
                    )

                st.success(
                    f"Restockage validé : "
                    f"{qte_restock} unité(s) de {prod_restock}."
                )

                st.rerun()


# ============================================================
# 3. CODES AGENTS
# ============================================================

elif menu == "Codes Agents":

    section(
        "CODES AGENTS — ATTRIBUTION & PERFORMANCE",
        "👥"
    )

    st.dataframe(
        pd.DataFrame(st.session_state.agents),
        use_container_width=True,
        hide_index=True
    )

    c1, c2 = st.columns(2, gap="large")

    with c1:

        section(
            "PERFORMANCE COMMERCIALE",
            "📊"
        )

        if st.session_state.ventes:

            df_v = pd.DataFrame(
                st.session_state.ventes
            )

            performance = (
                df_v.groupby("Agent")["Total"]
                .sum()
                .sort_values(ascending=False)
            )

            st.bar_chart(
                performance,
                use_container_width=True
            )

        else:

            st.info(
                "Les performances apparaîtront "
                "après les premières ventes."
            )

    with c2:

        section(
            "ATTRIBUER UN NOUVEAU CODE",
            "🔐"
        )

        new_nom = st.text_input(
            "Nom du nouvel agent"
        )

        new_code = st.text_input(
            "Code unique",
            placeholder="APG-004"
        )

        parrains = (
            ["Boss"]
            + [
                a["Nom"]
                for a in st.session_state.agents
            ]
        )

        new_parrain = st.selectbox(
            "Parrain",
            parrains
        )

        if st.button(
            "➕ ATTRIBUER LE CODE AGENT",
            use_container_width=True,
            type="primary"
        ):

            code_existant = any(
                a["Code"].upper()
                == new_code.strip().upper()
                for a in st.session_state.agents
            )

            nom_existant = any(
                a["Nom"].lower()
                == new_nom.strip().lower()
                for a in st.session_state.agents
            )

            if not new_nom.strip() or not new_code.strip():

                st.error(
                    "Le nom et le code sont obligatoires."
                )

            elif code_existant or nom_existant:

                st.error(
                    "Ce nom ou ce code existe déjà."
                )

            else:

                st.session_state.agents.append({
                    "Nom": new_nom.strip(),
                    "Code": new_code.strip().upper(),
                    "Niveau": "Starter",
                    "Parrain": new_parrain,
                    "Commission": 0
                })

                st.success(
                    "Code agent attribué."
                )

                st.rerun()


# ============================================================
# 4. MLM & RÉSEAU
# ============================================================

elif menu == "MLM & Réseau":

    section(
        "MLM & RÉSEAU — GESTION DE L'ÉQUIPE",
        "🌐"
    )

    st.dataframe(
        pd.DataFrame(st.session_state.agents),
        use_container_width=True,
        hide_index=True
    )

    section(
        "ORGANISATION DU RÉSEAU",
        "🌳"
    )

    for agent in st.session_state.agents:

        filleuls = [
            a["Nom"]
            for a in st.session_state.agents
            if (
                a["Parrain"].strip().lower()
                == agent["Nom"].strip().lower()
            )
        ]

        if filleuls:

            st.markdown(
                f"""
                <div class="private-box"
                     style="margin-bottom:9px">

                    <b>👑 {agent["Nom"]}</b>
                    — {agent["Niveau"]}

                    <br>

                    <span style="color:#637267;font-size:13px">
                        Filleuls : {", ".join(filleuls)}
                    </span>

                    <br>

                    <b style="color:{VERT}">
                        Commission cumulée :
                        {fcfa(agent["Commission"])}
                    </b>

                </div>
                """,
                unsafe_allow_html=True
            )

    section(
        "COMMISSIONS DES AGENTS",
        "💰"
    )

    df_agents = pd.DataFrame(
        st.session_state.agents
    )

    st.dataframe(
        df_agents[
            ["Nom", "Code", "Niveau", "Commission"]
        ],
        use_container_width=True,
        hide_index=True
    )


# ============================================================
# 5. TÉMOIGNAGES CLIENTS
# ============================================================

elif menu == "Témoignages Clients":

    section(
        "TÉMOIGNAGES CLIENTS — PREUVE SOCIALE",
        "⭐"
    )

    for temoignage in reversed(
        st.session_state.temoignages
    ):

        etoiles = (
            "★" * int(temoignage["Note"])
            + "☆" * (5 - int(temoignage["Note"]))
        )

        st.markdown(
            f"""
            <div class="private-box"
                 style="margin-bottom:11px">

                <div style="
                    display:flex;
                    justify-content:space-between;
                    gap:10px;
                    flex-wrap:wrap
                ">

                    <b>{temoignage["Client"]}</b>

                    <span style="
                        color:{OR};
                        font-weight:900
                    ">
                        {etoiles}
                    </span>

                </div>

                <div style="
                    font-size:12px;
                    color:#66736A;
                    margin:5px 0
                ">
                    {temoignage["Produit"]}
                    · {temoignage["Date"]}
                </div>

                <div style="
                    font-style:italic;
                    color:#29372D
                ">
                    “{temoignage["Message"]}”
                </div>

            </div>
            """,
            unsafe_allow_html=True
        )

    section(
        "PUBLIER UN NOUVEAU TÉMOIGNAGE",
        "✍️"
    )

    tc1, tc2 = st.columns(2, gap="large")

    with tc1:

        t_client = st.text_input(
            "Nom du client *"
        )

        produits = [
            s["Produit"]
            for s in st.session_state.stock
        ]

        t_produit = st.selectbox(
            "Produit concerné *",
            produits
        )

        t_note = st.slider(
            "Note attribuée",
            1,
            5,
            5
        )

    with tc2:

        t_msg = st.text_area(
            "Témoignage du client *",
            height=125
        )

    if st.button(
        "📢 PUBLIER LE TÉMOIGNAGE",
        type="primary",
        use_container_width=True
    ):

        if t_client.strip() and t_msg.strip():

            st.session_state.temoignages.append({

                "Client": t_client.strip(),

                "Produit": t_produit,

                "Note": int(t_note),

                "Message": t_msg.strip(),

                "Date": datetime.now().strftime(
                    "%d/%m/%Y"
                )

            })

            st.success(
                "Témoignage publié."
            )

            st.rerun()

        else:

            st.error(
                "Le nom du client et le témoignage sont obligatoires."
            )


# ============================================================
# 6. COMPTABILITÉ PRIVÉE
# ============================================================

elif menu == "Compta Privée":

    section(
        "COMPTA PRIVÉE — BILAN & RAPPORT",
        "🔒"
    )

    if not st.session_state.auth_compta:

        st.markdown(
            f"""
            <div class="private-box"
                 style="text-align:center">

                <div style="font-size:27px">
                    🔐
                </div>

                <div style="
                    font-size:16px;
                    font-weight:900;
                    color:{VERT_FONCE}
                ">
                    ACCÈS RÉSERVÉ BOSS
                </div>

                <div style="
                    font-size:12px;
                    color:#66736A;
                    margin-top:5px
                ">
                    Entrez votre code confidentiel
                    pour accéder au bilan complet.
                </div>

            </div>
            """,
            unsafe_allow_html=True
        )

        st.write("")

        pin_input = st.text_input(
            "PIN Boss",
            type="password",
            placeholder="Code confidentiel"
        )

        if st.button(
            "🔓 DÉVERROUILLER LA COMPTABILITÉ",
            type="primary",
            use_container_width=True
        ):

            if pin_input == st.session_state.pin:

                st.session_state.auth_compta = True

                st.rerun()

            else:

                st.error(
                    "PIN incorrect — accès refusé."
                )

    else:

        total_ca = sum(
            int(v["Total"])
            for v in st.session_state.ventes
        )

        valeur_stock = sum(
            int(s["Prix"]) * int(s["Stock"])
            for s in st.session_state.stock
        )

        # Estimation indicative conservée selon le taux initial.
        benefice = int(total_ca * 0.42)

        c1, c2, c3 = st.columns(3, gap="medium")

        with c1:

            st.markdown(
                f"""
                <div class="kpi-card">
                    <div class="kpi-icon">💳</div>
                    <div>
                        <div class="kpi-label">
                            CHIFFRE D’AFFAIRES TOTAL
                        </div>
                        <div class="kpi-value">
                            {fcfa(total_ca)}
                        </div>
                        <div class="kpi-note">
                            ● Cumul des ventes enregistrées
                        </div>
                    </div>
                </div>
                """,
                unsafe_allow_html=True
            )

        with c2:

            st.markdown(
                f"""
                <div class="kpi-card orange">
                    <div class="kpi-icon">📦</div>
                    <div>
                        <div class="kpi-label">
                            VALEUR DU STOCK
                        </div>
                        <div class="kpi-value">
                            {fcfa(valeur_stock)}
                        </div>
                        <div class="kpi-note">
                            ● Inventaire au prix de vente
                        </div>
                    </div>
                </div>
                """,
                unsafe_allow_html=True
            )

        with c3:

            st.markdown(
                f"""
                <div class="kpi-card gold">
                    <div class="kpi-icon">📈</div>
                    <div>
                        <div class="kpi-label">
                            BÉNÉFICE ESTIMÉ (42 %)
                        </div>
                        <div class="kpi-value">
                            {fcfa(benefice)}
                        </div>
                        <div class="kpi-note">
                            ● Estimation selon le taux configuré
                        </div>
                    </div>
                </div>
                """,
                unsafe_allow_html=True
            )

        # ----------------------------------------------------
        # BILAN DES VENTES
        # ----------------------------------------------------

        if st.session_state.ventes:

            df_v = pd.DataFrame(
                st.session_state.ventes
            )

            section(
                "BILAN DES VENTES PAR PRODUIT",
                "📊"
            )

            b1, b2 = st.columns(
                [2, 1],
                gap="large"
            )

            with b1:

                bilan_produit = (
                    df_v.groupby("Produit")[["Qte", "Total"]]
                    .sum()
                    .sort_values(
                        "Total",
                        ascending=False
                    )
                )

                bilan_produit.columns = [
                    "Quantité vendue",
                    "CA produit"
                ]

                st.bar_chart(
                    bilan_produit["CA produit"],
                    use_container_width=True
                )

            with b2:

                st.dataframe(
                    bilan_produit,
                    use_container_width=True
                )

            # ------------------------------------------------
            # BILAN PAR AGENT
            # ------------------------------------------------

            section(
                "BILAN PAR AGENT VENDEUR",
                "👤"
            )

            a1, a2 = st.columns(
                [2, 1],
                gap="large"
            )

            with a1:

                bilan_agent = (
                    df_v.groupby("Agent")[["Qte", "Total"]]
                    .sum()
                    .sort_values(
                        "Total",
                        ascending=False
                    )
                )

                bilan_agent.columns = [
                    "Quantité vendue",
                    "CA agent"
                ]

                bilan_agent["Commission 10 %"] = (
                    bilan_agent["CA agent"] * 0.10
                ).astype(int)

                st.bar_chart(
                    bilan_agent["CA agent"],
                    use_container_width=True
                )

            with a2:

                st.dataframe(
                    bilan_agent,
                    use_container_width=True
                )

            # ------------------------------------------------
            # INVENTAIRE AUTOMATIQUE
            # ------------------------------------------------

            section(
                "INVENTAIRE AUTOMATIQUE — STOCK RESTANT & VALEUR",
                "📦"
            )

            df_inv = pd.DataFrame(
                st.session_state.stock
            ).copy()

            df_inv["Valeur stock"] = (
                df_inv["Prix"] * df_inv["Stock"]
            )

            df_inv["Statut"] = df_inv["Stock"].apply(
                lambda x:
                "🔴 ALERTE"
                if int(x) < 20
                else "🟢 OK"
            )

            st.dataframe(
                df_inv[
                    [
                        "Produit",
                        "Stock",
                        "Lot",
                        "Peremption",
                        "Valeur stock",
                        "Statut"
                    ]
                ],
                use_container_width=True,
                hide_index=True
            )

            # ------------------------------------------------
            # RAPPORT JOURNALIER
            # ------------------------------------------------

            today = datetime.now().strftime(
                "%d/%m/%Y"
            )

            section(
                f"RAPPORT AUTOMATIQUE JOURNALIER — {today}",
                "📝"
            )

            ventes_du_jour = [
                v for v in st.session_state.ventes
                if v["Date"].startswith(today)
            ]

            ca_jour = sum(
                int(v["Total"])
                for v in ventes_du_jour
            )

            qte_jour = sum(
                int(v["Qte"])
                for v in ventes_du_jour
            )

            if ventes_du_jour:

                produits_jour = (
                    pd.DataFrame(ventes_du_jour)
                    .groupby("Produit")["Qte"]
                    .sum()
                    .sort_values(ascending=False)
                )

                agents_jour = (
                    pd.DataFrame(ventes_du_jour)
                    .groupby("Agent")["Total"]
                    .sum()
                    .sort_values(ascending=False)
                )

                produits_vedettes = ", ".join(
                    produits_jour.index[:2]
                )

                meilleur_agent = agents_jour.index[0]

            else:

                produits_vedettes = "Aucun"
                meilleur_agent = "Aucun"

            stock_critique = sum(
                1 for s in st.session_state.stock
                if int(s["Stock"]) < 20
            )

            st.markdown(
                f"""
                <div class="private-box">

                    <b style="color:{VERT_FONCE}">
                        Rapport du {today}
                    </b>

                    <br><br>

                    • Nombre de ventes :
                    <b>{len(ventes_du_jour)}</b>

                    <br>

                    • Quantité totale vendue :
                    <b>{qte_jour}</b>

                    <br>

                    • Chiffre d’affaires du jour :
                    <b>{fcfa(ca_jour)}</b>

                    <br>

                    • Bénéfice estimé (42 %) :
                    <b>{fcfa(int(ca_jour * 0.42))}</b>

                    <br>

                    • Produits les plus vendus :
                    <b>{produits_vedettes}</b>

                    <br>

                    • Meilleur vendeur du jour :
                    <b>{meilleur_agent}</b>

                    <br>

                    • Références en stock critique (&lt; 20) :
                    <b>{stock_critique}</b>

                </div>
                """,
                unsafe_allow_html=True
            )

            st.write("")

            st.dataframe(
                pd.DataFrame(ventes_du_jour)
                if ventes_du_jour
                else pd.DataFrame([
                    {
                        "Information":
                        "Aucune vente aujourd’hui"
                    }
                ]),
                use_container_width=True,
                hide_index=True
            )

            # ------------------------------------------------
            # EXPORT CSV EN MÉMOIRE
            # CORRECTION FILE NOT FOUND ERROR
            # ------------------------------------------------

            if ventes_du_jour:

                csv_buffer = BytesIO()

                csv_buffer.write(
                    pd.DataFrame(ventes_du_jour)
                    .to_csv(index=False)
                    .encode("utf-8-sig")
                )

                csv_data = csv_buffer.getvalue()

                st.download_button(
                    "📥 TÉLÉCHARGER LE RAPPORT JOURNALIER CSV",
                    data=csv_data,
                    file_name=(
                        f"Rapport_APGIV_"
                        f"{today.replace('/', '-')}.csv"
                    ),
                    mime="text/csv",
                    use_container_width=True
                )

        else:

            st.info(
                "Aucune vente enregistrée pour le moment. "
                "Le bilan apparaîtra après les premières ventes."
            )

        # ----------------------------------------------------
        # SÉCURITÉ — MODIFIER LE PIN
        # ----------------------------------------------------

        st.divider()

        sec1, sec2 = st.columns(
            2,
            gap="large"
        )

        with sec1:

            with st.expander(
                "🔑 Modifier le PIN Boss"
            ):

                new_pin = st.text_input(
                    "Nouveau PIN",
                    type="password",
                    placeholder="4 caractères minimum"
                )

                confirm_pin = st.text_input(
                    "Confirmer le nouveau PIN",
                    type="password"
                )

                if st.button(
                    "ENREGISTRER LE NOUVEAU PIN",
                    use_container_width=True
                ):

                    if len(new_pin) < 4:

                        st.error(
                            "Le PIN doit contenir au moins 4 caractères."
                        )

                    elif new_pin != confirm_pin:

                        st.error(
                            "Les deux codes ne correspondent pas."
                        )

                    else:

                        st.session_state.pin = new_pin

                        st.success(
                            "PIN modifié pour cette session."
                        )

        with sec2:

            st.write("")

            if st.button(
                "🔒 VERROUILLER LA COMPTABILITÉ",
                use_container_width=True
            ):

                st.session_state.auth_compta = False

                st.rerun()


# ============================================================
# PIED DE PAGE
# ============================================================

st.markdown(
    f"""
    <div style="
        text-align:center;
        padding:22px 5px 4px;
        color:#829087;
        font-size:10px
    ">

        <span style="
            color:{VERT};
            font-weight:800
        ">
            APGIV OS GESTION
        </span>

        &nbsp;·&nbsp;
        L’Excellence au Naturel

        &nbsp;·&nbsp;
        Interface de gestion

    </div>
    """,
    unsafe_allow_html=True
)