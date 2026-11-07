# -*- coding: utf-8 -*-
# TÜBİTAK 2209-A Araştırma Projesi - Yüksek Kontrastlı Kurumsal KDS Prototipi
# Proje: Kimya Sektöründe Üretim Reçetesi Tabanlı Otomatik Stok Takibi ve Dinamik Depo Yerleşim KDS

from datetime import datetime, timedelta
import math
import numpy as np
import pandas as pd
import streamlit as st

st.set_page_config(
    page_title="KİM-KDS | Kurumsal Stok ve Depo Optimizasyon Sistemi",
    layout="wide",
    initial_sidebar_state="expanded",
)

# -------------------------------------------------------------------------
# YÜKSEK KONTRASTLI (WCAG ERİŞİLEBİLİR) KURUMSAL ERP CSS TASARIMI
# Koyu tema (Dark Mode) cihazlarda bile tüm metinleri ve kutuları net okunur kılar
# -------------------------------------------------------------------------
st.markdown(
    """
<style>
    /* Ana arka plan ve genel metin kontrast kilidi */
    .stApp, [data-testid="stAppViewContainer"], [data-testid="stHeader"] {
        background-color: #f1f5f9 !important;
        color: #0f172a !important;
    }
    
    /* Tüm başlıklar, paragraflar ve etiketler için koyu lacivert/antrasit renk zorlaması */
    .main h1, .main h2, .main h3, .main h4, .main h5, .main h6,
    .main p, .main span, .main label, .main div[data-testid="stMarkdownContainer"] p,
    div[data-testid="stWidgetLabel"] p, div[data-testid="stWidgetLabel"] label,
    .stSelectbox label, .stNumberInput label, .stTextInput label, .stDateInput label, .stSlider label {
        color: #0f172a !important;
        font-weight: 600 !important;
    }

    /* Alt başlık (st.subheader) görünümü */
    .section-title {
        background-color: #ffffff;
        color: #0f172a !important;
        padding: 12px 16px;
        border-radius: 6px;
        border-left: 5px solid #1d4ed8;
        border-top: 1px solid #cbd5e1;
        border-right: 1px solid #cbd5e1;
        border-bottom: 1px solid #cbd5e1;
        font-size: 1.08rem;
        font-weight: 700;
        margin: 16px 0 12px 0;
        box-shadow: 0 1px 2px rgba(15, 23, 42, 0.05);
    }

    /* Form kutuları ve kartlar */
    div[data-testid="stForm"] {
        background-color: #ffffff !important;
        border: 1px solid #cbd5e1 !important;
        border-radius: 8px !important;
        padding: 18px !important;
        box-shadow: 0 2px 4px rgba(15, 23, 42, 0.04) !important;
    }

    /* Input, Selectbox ve Sayı kutularını beyaz zemin + koyu yazı yapma */
    div[data-baseweb="select"] > div,
    div[data-baseweb="input"] > div,
    div[data-baseweb="base-input"],
    input[type="number"], input[type="text"], input[type="date"] {
        background-color: #ffffff !important;
        color: #0f172a !important;
        border: 1px solid #94a3b8 !important;
        border-radius: 5px !important;
        font-weight: 600 !important;
    }
    div[data-baseweb="select"] span,
    div[data-baseweb="select"] div {
        color: #0f172a !important;
    }
    /* Sayı artırma/azaltma (+/-) butonları */
    button[data-testid="stNumberInputStepDown"],
    button[data-testid="stNumberInputStepUp"] {
        background-color: #e2e8f0 !important;
        color: #0f172a !important;
    }

    /* Birincil Aksiyon Butonları (Kurumsal Mavi) */
    .stButton > button, .stFormSubmitButton > button {
        background: linear-gradient(180deg, #2563eb 0%, #1d4ed8 100%) !important;
        color: #ffffff !important;
        border: 1px solid #1e40af !important;
        border-radius: 6px !important;
        padding: 10px 18px !important;
        font-weight: 700 !important;
        font-size: 0.92rem !important;
        width: 100%;
        box-shadow: 0 2px 4px rgba(29, 78, 216, 0.2) !important;
    }
    .stButton > button:hover, .stFormSubmitButton > button:hover {
        background: linear-gradient(180deg, #1d4ed8 0%, #1e3a8a 100%) !important;
        color: #ffffff !important;
    }
    .stButton > button *, .stFormSubmitButton > button * {
        color: #ffffff !important;
    }

    /* Sol Menü (Sidebar) Tasarımı */
    section[data-testid="stSidebar"] {
        background-color: #0f172a !important;
        border-right: 2px solid #1e293b !important;
    }
    section[data-testid="stSidebar"] h1,
    section[data-testid="stSidebar"] h2,
    section[data-testid="stSidebar"] h3,
    section[data-testid="stSidebar"] p,
    section[data-testid="stSidebar"] span,
    section[data-testid="stSidebar"] label {
        color: #f8fafc !important;
    }
    section[data-testid="stSidebar"] div[data-baseweb="select"] > div {
        background-color: #1e293b !important;
        border-color: #475569 !important;
    }
    section[data-testid="stSidebar"] div[data-baseweb="select"] span,
    section[data-testid="stSidebar"] div[data-baseweb="select"] div {
        color: #f8fafc !important;
    }

    /* Üst Kurumsal Başlık Bandı */
    .top-banner {
        background: linear-gradient(90deg, #0f172a 0%, #1e3a8a 100%);
        color: #ffffff !important;
        padding: 18px 24px;
        border-radius: 8px;
        border-left: 6px solid #38bdf8;
        box-shadow: 0 4px 10px rgba(15, 23, 42, 0.12);
        margin-bottom: 18px;
        display: flex;
        justify-content: space-between;
        align-items: center;
    }
    .top-banner h1 { margin: 0; font-size: 1.3rem; font-weight: 800; color: #ffffff !important; }
    .top-banner p { margin: 5px 0 0 0; font-size: 0.84rem; color: #e2e8f0 !important; font-weight: 400 !important; }
    .badge-box {
        background-color: rgba(56, 189, 248, 0.2);
        border: 1px solid #38bdf8;
        color: #ffffff !important;
        padding: 6px 14px;
        border-radius: 6px;
        font-size: 0.8rem;
        font-weight: 700;
        text-align: right;
        white-space: nowrap;
    }

    /* KPI Kartları */
    .kpi-card {
        background: #ffffff;
        border: 1px solid #cbd5e1;
        border-top: 4px solid #1d4ed8;
        border-radius: 8px;
        padding: 14px 16px;
        box-shadow: 0 2px 4px rgba(15, 23, 42, 0.04);
    }
    .kpi-title { font-size: 0.78rem; font-weight: 700; color: #475569 !important; text-transform: uppercase; }
    .kpi-val { font-size: 1.5rem; font-weight: 800; color: #0f172a !important; margin-top: 4px; }
    .kpi-sub { font-size: 0.76rem; color: #64748b !important; margin-top: 2px; }

    /* Matematiksel Formül Kutusu */
    .formula-bar {
        background-color: #eff6ff;
        border: 1px solid #93c5fd;
        border-left: 5px solid #1d4ed8;
        padding: 12px 16px;
        border-radius: 6px;
        font-family: 'Segoe UI', 'Consolas', monospace;
        font-size: 0.9rem;
        color: #0f172a !important;
        margin-bottom: 14px;
    }

    /* Yüksek Kontrastlı Kurumsal HTML Tablo Tasarımı */
    .erp-table-wrap {
        background: #ffffff;
        border: 1px solid #cbd5e1;
        border-radius: 8px;
        overflow-x: auto;
        box-shadow: 0 1px 3px rgba(15, 23, 42, 0.05);
        margin-bottom: 16px;
    }
    .erp-table {
        width: 100%;
        border-collapse: collapse;
        font-size: 0.86rem;
        color: #0f172a !important;
        background-color: #ffffff !important;
    }
    .erp-table th {
        background-color: #1e293b !important;
        color: #ffffff !important;
        font-weight: 700 !important;
        text-align: left;
        padding: 10px 12px;
        border-bottom: 2px solid #0f172a;
        white-space: nowrap;
    }
    .erp-table td {
        padding: 9px 12px;
        border-bottom: 1px solid #e2e8f0;
        color: #0f172a !important;
        font-weight: 500;
    }
    .erp-table tr:nth-child(even) td {
        background-color: #f8fafc !important;
    }
    .erp-table tr:hover td {
        background-color: #eff6ff !important;
    }
    .badge-crit {
        background-color: #fee2e2;
        color: #991b1b !important;
        border: 1px solid #f87171;
        padding: 3px 8px;
        border-radius: 4px;
        font-weight: 700;
        font-size: 0.76rem;
    }
    .badge-ok {
        background-color: #dcfce7;
        color: #166534 !important;
        border: 1px solid #4ade80;
        padding: 3px 8px;
        border-radius: 4px;
        font-weight: 700;
        font-size: 0.76rem;
    }

    /* 2B Depo Izgara (Grid) Haritası */
    .grid-map { border-collapse: collapse; width: 100%; font-family: 'Segoe UI', monospace; font-size: 12px; margin-top: 8px; }
    .grid-map td {
        border: 1px solid #64748b;
        text-align: center;
        padding: 6px 4px;
        height: 58px;
        width: 82px;
        vertical-align: middle;
        line-height: 1.25;
    }
</style>
""",
    unsafe_allow_html=True,
)


# -------------------------------------------------------------------------
# YARDIMCI GÖRSEL BİLEŞEN FONKSİYONLARI
# -------------------------------------------------------------------------
def baslik_karti(metin):
    st.markdown(f'<div class="section-title">{metin}</div>', unsafe_allow_html=True)


def erp_tablo_goster(df):
    html = '<div class="erp-table-wrap"><table class="erp-table"><thead><tr>'
    for col in df.columns:
        html += f"<th>{col}</th>"
    html += "</tr></thead><tbody>"

    for _, row in df.iterrows():
        html += "<tr>"
        for col in df.columns:
            val = row[col]
            if col == "Durum":
                if "KRİTİK" in str(val):
                    html += f'<td><span class="badge-crit">{val}</span></td>'
                else:
                    html += f'<td><span class="badge-ok">{val}</span></td>'
            elif isinstance(val, float):
                if col in ["Alpha_Fire", "Oran_r", "COI_Indeksi"]:
                    html += f"<td>{val:.4f}</td>"
                else:
                    html += f"<td>{val:,.2f}</td>"
            else:
                html += f"<td>{val}</td>"
        html += "</tr>"
    html += "</tbody></table></div>"
    st.markdown(html, unsafe_allow_html=True)


# -------------------------------------------------------------------------
# İLİŞKİSEL VERİTABANI BAŞLANGIÇ TABLOLARI (SESSION STATE)
# -------------------------------------------------------------------------
def init_db():
    if "hammaddeler" not in st.session_state:
        st.session_state.hammaddeler = pd.DataFrame(
            [
                {
                    "Kod": "HM-01",
                    "Ad": "Titanyum Dioksit (TiO2)",
                    "GHS": "GHS07 - Normal/Tahriş",
                    "Birim_Hacim_m3": 0.80,
                    "L_Gun": 7,
                    "Talep_Std_Sapma": 12.0,
                    "Alpha_Fire": 0.020,
                    "Birim_Tasima_kg": 250.0,
                },
                {
                    "Kod": "HM-02",
                    "Ad": "Stiren Akrilik Emülsiyon",
                    "GHS": "GHS07 - Normal/Tahriş",
                    "Birim_Hacim_m3": 1.10,
                    "L_Gun": 5,
                    "Talep_Std_Sapma": 18.5,
                    "Alpha_Fire": 0.015,
                    "Birim_Tasima_kg": 300.0,
                },
                {
                    "Kod": "HM-03",
                    "Ad": "Mikronize Kalsit (CaCO3)",
                    "GHS": "GHS07 - Normal/Tahriş",
                    "Birim_Hacim_m3": 1.40,
                    "L_Gun": 3,
                    "Talep_Std_Sapma": 25.0,
                    "Alpha_Fire": 0.010,
                    "Birim_Tasima_kg": 400.0,
                },
                {
                    "Kod": "HM-04",
                    "Ad": "Ksilen (Aromatik Solvent)",
                    "GHS": "GHS02 - Yanıcı Sıvı",
                    "Birim_Hacim_m3": 0.90,
                    "L_Gun": 6,
                    "Talep_Std_Sapma": 14.0,
                    "Alpha_Fire": 0.035,
                    "Birim_Tasima_kg": 200.0,
                },
                {
                    "Kod": "HM-05",
                    "Ad": "Poliüretan Reçine Bazı",
                    "GHS": "GHS02 - Yanıcı Sıvı",
                    "Birim_Hacim_m3": 1.00,
                    "L_Gun": 8,
                    "Talep_Std_Sapma": 10.5,
                    "Alpha_Fire": 0.025,
                    "Birim_Tasima_kg": 250.0,
                },
                {
                    "Kod": "HM-06",
                    "Ad": "Hidrojen Peroksit (%50)",
                    "GHS": "GHS03 - Oksitleyici",
                    "Birim_Hacim_m3": 0.75,
                    "L_Gun": 5,
                    "Talep_Std_Sapma": 9.0,
                    "Alpha_Fire": 0.020,
                    "Birim_Tasima_kg": 200.0,
                },
                {
                    "Kod": "HM-07",
                    "Ad": "Sodyum Hidroksit Çözeltisi",
                    "GHS": "GHS05 - Aşındırıcı",
                    "Birim_Hacim_m3": 0.85,
                    "L_Gun": 4,
                    "Talep_Std_Sapma": 8.0,
                    "Alpha_Fire": 0.015,
                    "Birim_Tasima_kg": 250.0,
                },
            ]
        )

    if "partiler" not in st.session_state:
        st.session_state.partiler = pd.DataFrame(
            [
                {
                    "Parti_ID": "LOT-2601A",
                    "HM_Kodu": "HM-01",
                    "Giris_Tarihi": "2026-09-10",
                    "SKT": "2026-12-15",
                    "Miktar_kg": 650.0,
                },
                {
                    "Parti_ID": "LOT-2608B",
                    "HM_Kodu": "HM-01",
                    "Giris_Tarihi": "2026-10-12",
                    "SKT": "2027-04-20",
                    "Miktar_kg": 900.0,
                },
                {
                    "Parti_ID": "LOT-2602A",
                    "HM_Kodu": "HM-02",
                    "Giris_Tarihi": "2026-09-18",
                    "SKT": "2027-01-10",
                    "Miktar_kg": 800.0,
                },
                {
                    "Parti_ID": "LOT-2609C",
                    "HM_Kodu": "HM-02",
                    "Giris_Tarihi": "2026-10-25",
                    "SKT": "2027-05-15",
                    "Miktar_kg": 1350.0,
                },
                {
                    "Parti_ID": "LOT-2603A",
                    "HM_Kodu": "HM-03",
                    "Giris_Tarihi": "2026-10-01",
                    "SKT": "2028-01-01",
                    "Miktar_kg": 3400.0,
                },
                {
                    "Parti_ID": "LOT-2604X",
                    "HM_Kodu": "HM-04",
                    "Giris_Tarihi": "2026-10-05",
                    "SKT": "2026-11-28",
                    "Miktar_kg": 420.0,
                },
                {
                    "Parti_ID": "LOT-2605A",
                    "HM_Kodu": "HM-05",
                    "Giris_Tarihi": "2026-10-14",
                    "SKT": "2027-02-28",
                    "Miktar_kg": 980.0,
                },
                {
                    "Parti_ID": "LOT-2606P",
                    "HM_Kodu": "HM-06",
                    "Giris_Tarihi": "2026-10-02",
                    "SKT": "2026-11-19",
                    "Miktar_kg": 390.0,
                },
                {
                    "Parti_ID": "LOT-2607K",
                    "HM_Kodu": "HM-07",
                    "Giris_Tarihi": "2026-10-19",
                    "SKT": "2027-06-30",
                    "Miktar_kg": 720.0,
                },
            ]
        )

    if "mamuller" not in st.session_state:
        st.session_state.mamuller = pd.DataFrame(
            [
                {
                    "Mamul_Kodu": "M-101",
                    "Mamul_Adi": "Akrilik Dış Cephe Boyası",
                    "Stok_kg": 1400.0,
                    "Gelecek_Ay_MPS_kg": 9000.0,
                },
                {
                    "Mamul_Kodu": "M-102",
                    "Mamul_Adi": "Endüstriyel Poliüretan Kaplama",
                    "Stok_kg": 750.0,
                    "Gelecek_Ay_MPS_kg": 4500.0,
                },
                {
                    "Mamul_Kodu": "M-103",
                    "Mamul_Adi": "Aktif Oksijenli Endüstriyel Dezenfektan",
                    "Stok_kg": 520.0,
                    "Gelecek_Ay_MPS_kg": 3200.0,
                },
            ]
        )

    if "bom" not in st.session_state:
        st.session_state.bom = pd.DataFrame(
            [
                {"Mamul_Kodu": "M-101", "HM_Kodu": "HM-01", "Oran_r": 0.25},
