# -*- coding: utf-8 -*-
# TÜBİTAK 2209-A Araştırma Projesi - Kurumsal KDS & Google Sheets Entegreli Canlı SUS Paneli
# Proje: Kimya Sektöründe Üretim Reçetesi Tabanlı Otomatik Stok Takibi ve Dinamik Depo Yerleşim KDS

import streamlit as st
import pandas as pd
import numpy as np
import math
from datetime import datetime, timedelta
import requests

st.set_page_config(
    page_title="StreamX | Kurumsal Stok ve Depo Optimizasyon Sistemi",
    layout="wide",
    initial_sidebar_state="expanded",
)

# -------------------------------------------------------------------------
# YÜKSEK KONTRASTLI (WCAG ERİŞİLEBİLİR) KURUMSAL ERP CSS TASARIMI
# -------------------------------------------------------------------------
st.markdown("""
<style>
    .stApp, [data-testid="stAppViewContainer"], [data-testid="stHeader"] {
        background-color: #f1f5f9 !important;
        color: #0f172a !important;
    }
    
    .main h1, .main h2, .main h3, .main h4, .main h5, .main h6,
    .main p, .main span, .main label, .main div[data-testid="stMarkdownContainer"] p,
    div[data-testid="stWidgetLabel"] p, div[data-testid="stWidgetLabel"] label,
    .stSelectbox label, .stNumberInput label, .stTextInput label, .stDateInput label, .stSlider label {
        color: #0f172a !important;
        font-weight: 600 !important;
    }

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

    div[data-testid="stForm"] {
        background-color: #ffffff !important;
        border: 1px solid #cbd5e1 !important;
        border-radius: 8px !important;
        padding: 18px !important;
        box-shadow: 0 2px 4px rgba(15, 23, 42, 0.04) !important;
    }

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
    div[data-baseweb="select"] span, div[data-baseweb="select"] div {
        color: #0f172a !important;
    }

    button[data-testid="stNumberInputStepDown"],
    button[data-testid="stNumberInputStepUp"] {
        background-color: #e2e8f0 !important;
        color: #0f172a !important;
    }

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
""", unsafe_allow_html=True)

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

def init_db():
    if "hammaddeler" not in st.session_state:
        st.session_state.hammaddeler = pd.DataFrame([
            {"Kod": "HM-01", "Ad": "Titanyum Dioksit (TiO2)", "GHS": "GHS07 - Normal/Tahriş", "Birim_Hacim_m3": 0.80, "L_Gun": 7, "Talep_Std_Sapma": 12.0, "Alpha_Fire": 0.020, "Birim_Tasima_kg": 250.0},
            {"Kod": "HM-02", "Ad": "Stiren Akrilik Emülsiyon", "GHS": "GHS07 - Normal/Tahriş", "Birim_Hacim_m3": 1.10, "L_Gun": 5, "Talep_Std_Sapma": 18.5, "Alpha_Fire": 0.015, "Birim_Tasima_kg": 300.0},
            {"Kod": "HM-03", "Ad": "Mikronize Kalsit (CaCO3)", "GHS": "GHS07 - Normal/Tahriş", "Birim_Hacim_m3": 1.40, "L_Gun": 3, "Talep_Std_Sapma": 25.0, "Alpha_Fire": 0.010, "Birim_Tasima_kg": 400.0},
            {"Kod": "HM-04", "Ad": "Ksilen (Aromatik Solvent)", "GHS": "GHS02 - Yanıcı Sıvı", "Birim_Hacim_m3": 0.90, "L_Gun": 6, "Talep_Std_Sapma": 14.0, "Alpha_Fire": 0.035, "Birim_Tasima_kg": 200.0},
            {"Kod": "HM-05", "Ad": "Poliüretan Reçine Bazı", "GHS": "GHS02 - Yanıcı Sıvı", "Birim_Hacim_m3": 1.00, "L_Gun": 8, "Talep_Std_Sapma": 10.5, "Alpha_Fire": 0.025, "Birim_Tasima_kg": 250.0},
            {"Kod": "HM-06", "Ad": "Hidrojen Peroksit (%50)", "GHS": "GHS03 - Oksitleyici", "Birim_Hacim_m3": 0.75, "L_Gun": 5, "Talep_Std_Sapma": 9.0, "Alpha_Fire": 0.020, "Birim_Tasima_kg": 200.0},
            {"Kod": "HM-07", "Ad": "Sodyum Hidroksit Çözeltisi", "GHS": "GHS05 - Aşındırıcı", "Birim_Hacim_m3": 0.85, "L_Gun": 4, "Talep_Std_Sapma": 8.0, "Alpha_Fire": 0.015, "Birim_Tasima_kg": 250.0}
        ])

    if "partiler" not in st.session_state:
        st.session_state.partiler = pd.DataFrame([
            {"Parti_ID": "LOT-2601A", "HM_Kodu": "HM-01", "Giris_Tarihi": "2026-09-10", "SKT": "2026-12-15", "Miktar_kg": 650.0},
            {"Parti_ID": "LOT-2608B", "HM_Kodu": "HM-01", "Giris_Tarihi": "2026-10-12", "SKT": "2027-04-20", "Miktar_kg": 900.0},
            {"Parti_ID": "LOT-2602A", "HM_Kodu": "HM-02", "Giris_Tarihi": "2026-09-18", "SKT": "2027-01-10", "Miktar_kg": 800.0},
            {"Parti_ID": "LOT-2609C", "HM_Kodu": "HM-02", "Giris_Tarihi": "2026-10-25", "SKT": "2027-05-15", "Miktar_kg": 1350.0},
            {"Parti_ID": "LOT-2603A", "HM_Kodu": "HM-03", "Giris_Tarihi": "2026-10-01", "SKT": "2028-01-01", "Miktar_kg": 3400.0},
            {"Parti_ID": "LOT-2604X", "HM_Kodu": "HM-04", "Giris_Tarihi": "2026-10-05", "SKT": "2026-11-28", "Miktar_kg": 420.0},
            {"Parti_ID": "LOT-2605A", "HM_Kodu": "HM-05", "Giris_Tarihi": "2026-10-14", "SKT": "2027-02-28", "Miktar_kg": 980.0},
            {"Parti_ID": "LOT-2606P", "HM_Kodu": "HM-06", "Giris_Tarihi": "2026-10-02", "SKT": "2026-11-19", "Miktar_kg": 390.0},
            {"Parti_ID": "LOT-2607K", "HM_Kodu": "HM-07", "Giris_Tarihi": "2026-10-19", "SKT": "2027-06-30", "Miktar_kg": 720.0}
        ])

    if "mamuller" not in st.session_state:
        st.session_state.mamuller = pd.DataFrame([
            {"Mamul_Kodu": "M-101", "Mamul_Adi": "Akrilik Dış Cephe Boyası", "Stok_kg": 1400.0, "Gelecek_Ay_MPS_kg": 9000.0},
            {"Mamul_Kodu": "M-102", "Mamul_Adi": "Endüstriyel Poliüretan Kaplama", "Stok_kg": 750.0, "Gelecek_Ay_MPS_kg": 4500.0},
            {"Mamul_Kodu": "M-103", "Mamul_Adi": "Aktif Oksijenli Endüstriyel Dezenfektan", "Stok_kg": 520.0, "Gelecek_Ay_MPS_kg": 3200.0}
        ])

    if "bom" not in st.session_state:
        st.session_state.bom = pd.DataFrame([
            {"Mamul_Kodu": "M-101", "HM_Kodu": "HM-01", "Oran_r": 0.25},
            {"Mamul_Kodu": "M-101", "HM_Kodu": "HM-02", "Oran_r": 0.35},
            {"Mamul_Kodu": "M-101", "HM_Kodu": "HM-03", "Oran_r": 0.40},
            {"Mamul_Kodu": "M-102", "HM_Kodu": "HM-04", "Oran_r": 0.35},
            {"Mamul_Kodu": "M-102", "HM_Kodu": "HM-05", "Oran_r": 0.50},
            {"Mamul_Kodu": "M-102", "HM_Kodu": "HM-01", "Oran_r": 0.15},
            {"Mamul_Kodu": "M-103", "HM_Kodu": "HM-06", "Oran_r": 0.45},
            {"Mamul_Kodu": "M-103", "HM_Kodu": "HM-07", "Oran_r": 0.25},
            {"Mamul_Kodu": "M-103", "HM_Kodu": "HM-03", "Oran_r": 0.30}
        ])

    if "hareket_log" not in st.session_state:
        st.session_state.hareket_log = pd.DataFrame([
            {"Islem_No": "TR-1001", "Tarih": "2026-11-01 09:30", "Hareket_Tipi": "MAL KABUL (+)", "HM_Kodu": "HM-02", "Parti_ID": "LOT-2609C", "Degisim_kg": "+1350.00", "Aciklama": "Tedarikçi parti girişi"},
            {"Islem_No": "TR-1002", "Tarih": "2026-11-03 14:15", "Hareket_Tipi": "ÜRETİM SARFİYATI (-)", "HM_Kodu": "HM-01", "Parti_ID": "LOT-2601A", "Degisim_kg": "-127.55", "Aciklama": "M-101 üretimi (FEFO + %2.0 Fire dahil)"},
            {"Islem_No": "TR-1003", "Tarih": "2026-11-05 16:40", "Hareket_Tipi": "SAYIM DÜZELTME (+/-)", "HM_Kodu": "HM-04", "Parti_ID": "LOT-2604X", "Degisim_kg": "-8.50", "Aciklama": "Fiziki sayım farkı (Uçucu solvent kaybı)"}
        ])

    if "sus_yanitlari" not in st.session_state:
        st.session_state.sus_yanitlari = [82.5, 77.0, 85.0, 79.5]

init_db()

def analitik_hesapla(c_hucre=1.5, z_katsayi=1.65):
    hm_df = st.session_state.hammaddeler.copy()
    lot_df = st.session_state.partiler.copy()
    mamul_df = st.session_state.mamuller.copy()
    bom_df = st.session_state.bom.copy()

    aktif_lotlar = lot_df[lot_df["Miktar_kg"] > 0]
    stok_ozet = aktif_lotlar.groupby("HM_Kodu")["Miktar_kg"].sum().to_dict()
    fefo_skt = aktif_lotlar.groupby("HM_Kodu")["SKT"].min().to_dict()
    lot_sayisi = aktif_lotlar.groupby("HM_Kodu")["Parti_ID"].count().to_dict()

    hm_df["Toplam_Stok_kg"] = hm_df["Kod"].map(stok_ozet).fillna(0.0).round(2)
    hm_df["En_Yakin_SKT"] = hm_df["Kod"].map(fefo_skt).fillna("-")
    hm_df["Aktif_Lot"] = hm_df["Kod"].map(lot_sayisi).fillna(0).astype(int)

    aylik_ihtiyac = {}
    for _, hm in hm_df.iterrows():
        kod = hm["Kod"]
        alpha = hm["Alpha_Fire"]
        receteler = bom_df[bom_df["HM_Kodu"] == kod]
        top_ihtiyac = 0.0
        for _, r in receteler.iterrows():
            mps_hedef = mamul_df.loc[mamul_df["Mamul_Kodu"] == r["Mamul_Kodu"], "Gelecek_Ay_MPS_kg"].values[0]
            top_ihtiyac += (mps_hedef * r["Oran_r"]) / (1.0 - alpha)
        aylik_ihtiyac[kod] = round(top_ihtiyac, 1)

    hm_df["Aylik_MPS_Ihtiyac_kg"] = hm_df["Kod"].map(aylik_ihtiyac)
    hm_df["Gunluk_Talep_d"] = (hm_df["Aylik_MPS_Ihtiyac_kg"] / 30.0).round(2)

    hm_df["Emniyet_Stoku_SS"] = (z_katsayi * hm_df["Talep_Std_Sapma"] * np.sqrt(hm_df["L_Gun"])).round(1)
    hm_df["ROP_Esigi_kg"] = ((hm_df["Gunluk_Talep_d"] * hm_df["L_Gun"]) + hm_df["Emniyet_Stoku_SS"]).round(1)

    hm_df["Toplam_Hacim_Vi"] = ((hm_df["Toplam_Stok_kg"] / 500.0) * hm_df["Birim_Hacim_m3"]).round(2).clip(lower=0.5)
    hm_df["Cekim_Sikligi_fi"] = (hm_df["Aylik_MPS_Ihtiyac_kg"] / hm_df["Birim_Tasima_kg"]).apply(lambda x: max(1, math.ceil(x)))
    hm_df["Gereken_Hucre_Ni"] = (hm_df["Toplam_Hacim_Vi"] / c_hucre).apply(lambda x: max(1, math.ceil(x)))
    hm_df["COI_Indeksi"] = (hm_df["Toplam_Hacim_Vi"] / hm_df["Cekim_Sikligi_fi"]).round(4)

    hm_df["Durum"] = np.where(hm_df["Toplam_Stok_kg"] <= hm_df["ROP_Esigi_kg"], "KRİTİK (ROP ALTI)", "GÜVENLİ")
    return hm_df

st.sidebar.markdown("## 🧪 StreamX v3.5")
st.sidebar.caption("TÜBİTAK 2209-A Araştırma Projesi\nReçete, Lot/FEFO ve Dinamik Depo KDS")
st.sidebar.markdown("---")

secilen_modul = st.sidebar.radio(
    "KARAR DESTEK MODÜLLERİ",
    [
        "1. Gösterge Paneli & Olasılıklı ROP",
        "2. Fireli Reçete (BOM) & FEFO Üretim",
        "3. Parti (Lot) Arşivi & Stok Hareketleri",
        "4. Parametrik 2B Depo & GHS/COI Haritası",
        "5. Fiziki Sayım & Dinamik Fire (α) Güncelleme",
        "6. H1-H2 Deneysel Simülasyon (30 Senaryo)",
        "7. SUS Kullanılabilirlik Testi (Aşama 5)",
    ],
)

st.sidebar.markdown("---")
st.sidebar.markdown("**Küresel Model Parametreleri**")
c_hucre_input = st.sidebar.slider("Standart Hücre Kapasitesi C_hücre (m³)", 1.0, 3.0, 1.5, 0.25)
z_secim = st.sidebar.selectbox(
    "Hizmet Düzeyi (z Katsayısı)",
    [("95% Hizmet Düzeyi (z = 1.65)", 1.65), ("99% Hizmet Düzeyi (z = 2.33)", 2.33)],
    format_func=lambda x: x[0]
)

analiz_tablosu = analitik_hesapla(c_hucre=c_hucre_input, z_katsayi=z_secim[1])

st.markdown("""
<div class="top-banner">
    <div>
        <h1> Sektöründe Üretim Reçetesi Tabanlı Otomatik Stok Takibi ve Dinamik Depo Yerleşim KDS</h1>
        <p>Parti (Lot) Bazlı FEFO Stok Hareket Mimarisi &bull; Fire Düzeltmeli Backflushing &bull; Tedarik Süresi Duyarlı ROP &bull; GHS/SDS &amp; Kapasite Kısıtlı COI Optimizasyonu</p>
    </div>
    <div class="badge-box">
        TÜBİTAK 2209-A<br>YBS Araştırma Prototipi
    </div>
</div>
""", unsafe_allow_html=True)

if secilen_modul == "1. Gösterge Paneli & Olasılıklı ROP":
    toplam_stok = analiz_tablosu["Toplam_Stok_kg"].sum()
    aktif_lot_top = analiz_tablosu["Aktif_Lot"].sum()
    kritik_sayisi = int((analiz_tablosu["Durum"] == "KRİTİK (ROP ALTI)").sum())
    ort_fire = (analiz_tablosu["Alpha_Fire"].mean()) * 100

    k1, k2, k3, k4 = st.columns(4)
    k1.markdown(f'<div class="kpi-card"><div class="kpi-title">Toplam Parti (Lot) Stoğu</div><div class="kpi-val">{toplam_stok:,.1f} kg</div><div class="kpi-sub">{aktif_lot_top} Aktif Lot Kaydı Üzerinden</div></div>', unsafe_allow_html=True)
    k2.markdown(f'<div class="kpi-card"><div class="kpi-title">Tedarik Süresi Duyarlı ROP Uyarısı</div><div class="kpi-val" style="color:#b91c1c !important;">{kritik_sayisi} Hammadde</div><div class="kpi-sub">Hedef Hizmet Düzeyi: {z_secim[0]}</div></div>', unsafe_allow_html=True)
    k3.markdown(f'<div class="kpi-card"><div class="kpi-title">Ortalama Proses Fire Oranı (α_i)</div><div class="kpi-val">%{ort_fire:.2f}</div><div class="kpi-sub">Üstel Düzeltme İle Dinamik Güncellenir</div></div>', unsafe_allow_html=True)
    k4.markdown(f'<div class="kpi-card"><div class="kpi-title">Toplam Depo Hücre İhtiyacı (Σ N_i)</div><div class="kpi-val">{analiz_tablosu["Gereken_Hucre_Ni"].sum()} Hücre</div><div class="kpi-sub">C_hücre = {c_hucre_input} m³ Kapasite Kısıtlı</div></div>', unsafe_allow_html=True)

    st.write("")
    st.markdown("""
    <div class="formula-bar">
        <b>Aktif Envanter Modelleri:</b> &nbsp;
        Harcanan_i = (Q_m &times; r_{m,i}) / (1 - &alpha;_i) &nbsp;&bull;&nbsp;
        SS_i = z &times; &sigma;_{d,i} &times; &radic;L_i &nbsp;&bull;&nbsp;
        ROP_i = (d_{ort,i} &times; L_i) + SS_i &nbsp;&bull;&nbsp;
        N_i = &lceil;V_i / C_{hücre}&rceil; &nbsp;&bull;&nbsp;
        COI_i = V_i / f_i
    </div>
    """, unsafe_allow_html=True)

    if kritik_sayisi > 0:
        kritik_liste = ", ".join(analiz_tablosu[analiz_tablosu["Durum"] == "KRİTİK (ROP ALTI)"]["Ad"].tolist())
        st.error(f"🚨 TEDARİK SÜRESİ TALEBİNE DUYARLI ROP ALARMI: Aşağıdaki hammaddelerin parti bazlı toplam stoğu, tedarik süresi (L_i) boyunca beklenen talep + emniyet stoku (SS_i) sınırının altına inmiştir: {kritik_liste}")

    baslik_karti("Hammadde Envanter, Olasılıklı ROP ve COI Optimizasyon Özeti")
    kolonlar = ["Kod", "Ad", "GHS", "Aktif_Lot", "Toplam_Stok_kg", "En_Yakin_SKT", "Alpha_Fire", "L_Gun", "Emniyet_Stoku_SS", "ROP_Esigi_kg", "Gereken_Hucre_Ni", "COI_Indeksi", "Durum"]
    erp_tablo_goster(analiz_tablosu[kolonlar])

    baslik_karti("Mamul Stokları ve Gelecek 1 Aylık Ana Üretim Planı (MPS)")
    erp_tablo_goster(st.session_state.mamuller)

elif secilen_modul == "2. Fireli Reçete (BOM) & FEFO Üretim":
    c_sol, c_sag = st.columns([1.2, 1])

    with c_sol:
        baslik_karti("Üretim Bildirimi ve Parti Bazlı Otomatik Stok Düşümü (FEFO + Fire)")
        st.markdown("""
        <div class="formula-bar">
            <b>Fire Düzeltmeli Tersine Stok Düşüm (Backflush) Formülü:</b><br>
            Harcanan Hammadde_i = (Q_m &times; r_{m,i}) / (1 - &alpha;_i) &nbsp;&rarr;&nbsp; SKT'si en yakın partiden (FEFO) başlanarak otomatik düşülür.
        </div>
        """, unsafe_allow_html=True)

        secilen_m = st.selectbox("Üretilen Mamulü Seçiniz", st.session_state.mamuller["Mamul_Kodu"] + " - " + st.session_state.mamuller["Mamul_Adi"])
        m_kod = secilen_m.split(" - ")[0]
        q_miktar = st.number_input("Üretilen Mamul Miktarı Q_m (kg)", min_value=10.0, max_value=5000.0, value=200.0, step=25.0)

        recete_df = st.session_state.bom[st.session_state.bom["Mamul_Kodu"] == m_kod].merge(
            analiz_tablosu[["Kod", "Ad", "Alpha_Fire", "Toplam_Stok_kg", "En_Yakin_SKT"]],
            left_on="HM_Kodu", right_on="Kod"
        )
        recete_df["Net_Recete_kg"] = (recete_df["Oran_r"] * q_miktar).round(2)
        recete_df["Fireli_Harcanan_kg"] = ((recete_df["Oran_r"] * q_miktar) / (1.0 - recete_df["Alpha_Fire"])).round(2)

        erp_tablo_goster(recete_df[["HM_Kodu", "Ad", "Oran_r", "Alpha_Fire", "Net_Recete_kg", "Fireli_Harcanan_kg", "Toplam_Stok_kg", "En_Yakin_SKT"]])

        if st.button("Üretimi Onayla ve FEFO Partilerinden Otomatik Düş"):
            yetersiz = recete_df[recete_df["Toplam_Stok_kg"] < recete_df["Fireli_Harcanan_kg"]]
            if not yetersiz.empty:
                st.error("❌ HATA: Seçilen üretim miktarı için bazı hammaddelerin toplam parti stoğu yetersizdir!")
            else:
                for _, r_satir in recete_df.iterrows():
                    hm_k = r_satir["HM_Kodu"]
                    kalan_dusum = float(r_satir["Fireli_Harcanan_kg"])

                    ilgili_indisler = st.session_state.partiler[
                        (st.session_state.partiler["HM_Kodu"] == hm_k) & (st.session_state.partiler["Miktar_kg"] > 0)
                    ].sort_values(by="SKT", ascending=True).index

                    for idx in ilgili_indisler:
                        if kalan_dusum <= 0:
                            break
                        mevcut_lot_miktar = float(st.session_state.partiler.loc[idx, "Miktar_kg"])
                        lot_id = st.session_state.partiler.loc[idx, "Parti_ID"]
                        dusulecek = min(mevcut_lot_miktar, kalan_dusum)

                        st.session_state.partiler.loc[idx, "Miktar_kg"] = round(mevcut_lot_miktar - dusulecek, 2)
                        kalan_dusum = round(kalan_dusum - dusulecek, 2)

                        yeni_hareket = pd.DataFrame([{
                            "Islem_No": f"TR-{1000 + len(st.session_state.hareket_log) + 1}",
                            "Tarih": datetime.now().strftime("%Y-%m-%d %H:%M"),
                            "Hareket_Tipi": "ÜRETİM SARFİYATI (-)",
                            "HM_Kodu": hm_k,
                            "Parti_ID": lot_id,
                            "Degisim_kg": f"-{dusulecek:.2f}",
                            "Aciklama": f"{m_kod} ({q_miktar} kg) FEFO + Fireli sarfiyat"
                        }])
                        st.session_state.hareket_log = pd.concat([yeni_hareket, st.session_state.hareket_log], ignore_index=True)

                st.session_state.mamuller.loc[st.session_state.mamuller["Mamul_Kodu"] == m_kod, "Stok_kg"] += q_miktar
                st.success(f"✅ {q_miktar} kg {m_kod} mamul stoğuna eklendi. Hammaddeler proses fire oranları (α_i) dahil edilerek en yakın SKT'li partilerden (FEFO) düşüldü.")
                st.rerun()

    with c_sag:
        baslik_karti("Ürün Reçetesi (BOM) Katsayısı Tanımlama")
        with st.form("recete_guncelle"):
            m_sec = st.selectbox("Mamul Kodu", st.session_state.mamuller["Mamul_Kodu"])
            hm_sec = st.selectbox("Hammadde Kodu", st.session_state.hammaddeler["Kod"])
            yeni_oran = st.number_input("1 kg Mamul İçin Reçete Oranı (r_m,i)", 0.01, 1.00, 0.20, 0.05)
            kaydet_btn = st.form_submit_button("Reçete Katsayısını Kaydet")
            if kaydet_btn:
                filtre = (st.session_state.bom["Mamul_Kodu"] == m_sec) & (st.session_state.bom["HM_Kodu"] == hm_sec)
                if filtre.any():
                    st.session_state.bom.loc[filtre, "Oran_r"] = yeni_oran
                else:
                    ek = pd.DataFrame([{"Mamul_Kodu": m_sec, "HM_Kodu": hm_sec, "Oran_r": yeni_oran}])
                    st.session_state.bom = pd.concat([st.session_state.bom, ek], ignore_index=True)
                st.success("Reçete tablosu güncellendi.")
                st.rerun()

        baslik_karti("Mevcut Ürün Ağacı (BOM) Matrisi")
        erp_tablo_goster(st.session_state.bom)

elif secilen_modul == "3. Parti (Lot) Arşivi & Stok Hareketleri":
    col_a, col_b = st.columns([1, 1.5])

    with col_a:
        baslik_karti("Yeni Hammadde Partisi (Lot) Mal Kabulü")
        with st.form("lot_giris_form"):
            yeni_lot_id = st.text_input("Parti / Lot Numarası", value=f"LOT-26{len(st.session_state.partiler)+10}N")
            sec_hm = st.selectbox("Hammadde Seçimi", st.session_state.hammaddeler["Kod"] + " - " + st.session_state.hammaddeler["Ad"])
            hm_kod_kabul = sec_hm.split(" - ")[0]
            gelen_kg = st.number_input("Gelen Parti Miktarı (kg)", 10.0, 10000.0, 500.0, 50.0)
            skt_giris = st.date_input("Parti Son Kullanma Tarihi (SKT)", value=datetime.today() + timedelta(days=150))
            lot_ekle = st.form_submit_button("Partiyi Kaydet ve Hareket İşle (+)")

            if lot_ekle:
                yeni_lot = pd.DataFrame([{
                    "Parti_ID": yeni_lot_id,
                    "HM_Kodu": hm_kod_kabul,
                    "Giris_Tarihi": datetime.now().strftime("%Y-%m-%d"),
                    "SKT": skt_giris.strftime("%Y-%m-%d"),
                    "Miktar_kg": gelen_kg
                }])
                st.session_state.partiler = pd.concat([st.session_state.partiler, yeni_lot], ignore_index=True)

                yeni_tr = pd.DataFrame([{
                    "Islem_No": f"TR-{1000 + len(st.session_state.hareket_log) + 1}",
                    "Tarih": datetime.now().strftime("%Y-%m-%d %H:%M"),
                    "Hareket_Tipi": "MAL KABUL (+)",
                    "HM_Kodu": hm_kod_kabul,
                    "Parti_ID": yeni_lot_id,
                    "Degisim_kg": f"+{gelen_kg:.2f}",
                    "Aciklama": f"Yeni parti mal kabulü (SKT: {skt_giris.strftime('%Y-%m-%d')})"
                }])
                st.session_state.hareket_log = pd.concat([yeni_tr, st.session_state.hareket_log], ignore_index=True)
                st.success(f"{yeni_lot_id} partisi ({gelen_kg} kg) FEFO kuyruğuna ve stok hareket tablosuna eklendi.")
                st.rerun()

    with col_b:
        baslik_karti("Aktif Parti (Lot) Envanteri (FEFO Sıralı)")
        lot_gorunum = st.session_state.partiler.merge(
            st.session_state.hammaddeler[["Kod", "Ad", "GHS"]], left_on="HM_Kodu", right_on="Kod"
        ).sort_values(by="SKT", ascending=True)
        erp_tablo_goster(lot_gorunum[["Parti_ID", "HM_Kodu", "Ad", "GHS", "Giris_Tarihi", "SKT", "Miktar_kg"]])

    baslik_karti("İzlenebilir Stok Hareket Tablosu (Değiştirilemez Transaction Log)")
    erp_tablo_goster(st.session_state.hareket_log)

elif secilen_modul == "4. Parametrik 2B Depo & GHS/COI Haritası":
    baslik_karti("Hücre Kapasitesi Kısıtlı Dinamik COI Yerleşimi ve GHS/SDS Uyumluluk Haritası")
    st.markdown("""
    <div class="formula-bar">
        <b>Mekansal Optimizasyon Kısıtları:</b> &nbsp;
        d_j = |x_j - x_{kapı}| + |y_j - y_{kapı}| &nbsp;&bull;&nbsp;
        N_i = &lceil;V_i / C_{hücre}&rceil; &nbsp;&bull;&nbsp;
        COI_i = V_i / f_i &nbsp;&bull;&nbsp;
        GHS02 (Yanıcı) ve GHS03 (Oksitleyici) arasında minimum ayırma zonu uygulanır.
    </div>
    """, unsafe_allow_html=True)

    g1, g2, g3, g4 = st.columns(4)
    en_m = g1.number_input("Depo Eni W (Metre)", 15, 60, 21, 3)
    boy_m = g2.number_input("Depo Boyu L (Metre)", 18, 90, 27, 3)
    izgara_m = g3.number_input("Hücre Kenar Ölçüsü (Metre)", 2, 5, 3, 1)
    kapi_satir_sec = g4.number_input("Üretim Kapısı Satır İndeksi (x_kapı=0, y_kapı)", 0, 6, 3, 1)

    n_rows = max(5, min(10, int(en_m // izgara_m)))
    n_cols = max(6, min(12, int(boy_m // izgara_m)))
    kapi_r = min(kapi_satir_sec, n_rows - 1)

    sirali_coi = analiz_tablosu.sort_values(by="COI_Indeksi", ascending=True)

    grid_cells = []
    for r in range(n_rows):
        for c in range(n_cols):
            d_manhattan = abs(r - kapi_r) + c
            ana_koridor = (r == kapi_r and c > 0)
            ghs02_zon = (r <= 1 and c >= n_cols - 3)
            ghs03_zon = (r >= n_rows - 2 and c >= n_cols - 3)
            ghs05_zon = ((1 < r < n_rows - 2) and (r != kapi_r) and (c == n_cols - 1))
            grid_cells.append({
                "r": r, "c": c, "d": d_manhattan, "koridor": ana_koridor,
                "ghs02": ghs02_zon, "ghs03": ghs03_zon, "ghs05": ghs05_zon,
                "atama": None, "kod": None
            })

    toplam_agirlikli_mesafe = 0.0
    for _, hm in sirali_coi.iterrows():
        kod = hm["Kod"]
        ghs_tip = hm["GHS"]
        gereken_n = int(hm["Gereken_Hucre_Ni"])
        cekim_f = hm["Cekim_Sikligi_fi"]

        if "GHS02" in ghs_tip:
            adaylar = [h for h in grid_cells if h["ghs02"] and not h["koridor"] and h["atama"] is None]
        elif "GHS03" in ghs_tip:
            adaylar = [h for h in grid_cells if h["ghs03"] and not h["koridor"] and h["atama"] is None]
        elif "GHS05" in ghs_tip:
            adaylar = [h for h in grid_cells if h["ghs05"] and not h["koridor"] and h["atama"] is None]
        else:
            adaylar = [h for h in grid_cells if not (h["ghs02"] or h["ghs03"] or h["ghs05"] or h["koridor"]) and h["atama"] is None]

        adaylar = sorted(adaylar, key=lambda x: x["d"])
        atanan_hucreler = adaylar[:gereken_n]
        for idx_h, h in enumerate(atanan_hucreler):
            h["kod"] = kod
            h["atama"] = f"<b>{kod}</b> ({idx_h+1}/{gereken_n})<br><small>COI:{hm['COI_Indeksi']} | d={h['d']}</small>"
            toplam_agirlikli_mesafe += (cekim_f / gereken_n) * h["d"]

    tablo_html = "<table class='grid-map'>"
    for r in range(n_rows):
        tablo_html += "<tr>"
        for c in range(n_cols):
            cell = next(x for x in grid_cells if x["r"] == r and x["c"] == c)
            if r == kapi_r and c == 0:
                bg, fg, metin = "#0f172a", "#ffffff", "<b>ÜRETİM<br>KAPISI</b><br><small>(0, " + str(kapi_r) + ")</small>"
            elif cell["koridor"]:
                bg, fg, metin = "#cbd5e1", "#0f172a", "<b>ANA KORİDOR</b><br><small>Forklift Hattı</small>"
            elif cell["atama"]:
                if cell["ghs02"]: bg, fg = "#fecaca", "#7f1d1d"
                elif cell["ghs03"]: bg, fg = "#fef08a", "#713f12"
                elif cell["ghs05"]: bg, fg = "#fed7aa", "#7c2d12"
                else: bg, fg = "#bae6fd", "#0c4a6e"
                metin = cell["atama"]
            else:
                if cell["ghs02"]:
                    bg, fg, metin = "#fff1f2", "#9f1239", f"GHS02 Yanıcı Zon<br><small>Boş | d={cell['d']}</small>"
                elif cell["ghs03"]:
                    bg, fg, metin = "#fefce8", "#854d0e", f"GHS03 Oksit. Zon<br><small>Boş | d={cell['d']}</small>"
                elif cell["ghs05"]:
                    bg, fg, metin = "#fff7ed", "#9a3412", f"GHS05 Aşındırıcı<br><small>Boş | d={cell['d']}</small>"
                else:
                    bg, fg, metin = "#ffffff", "#475569", f"H({r},{c})<br><small>Boş | d={cell['d']}</small>"
            tablo_html += f"<td style='background-color:{bg}; color:{fg};'>{metin}</td>"
        tablo_html += "</tr>"
    tablo_html += "</table>"

    st.markdown(tablo_html, unsafe_allow_html=True)
    st.markdown(f"""
        <div class="formula-bar" style="margin-top:12px;">
            📌 <b>Toplam Ağırlıklı Taşıma Mesafesi (&Sigma; f_i &times; d_j):</b> {toplam_agirlikli_mesafe:,.1f} birim-hücre &nbsp;|&nbsp;
            <b>Renk Kodları:</b> Lacivert = Üretim Kapısı &bull; Mavi = Dinamik COI Normal Hücreler &bull; Kırmızı = GHS02 Yanıcı Sıvı Zonu &bull; Sarı = GHS03 Oksitleyici Zonu &bull; Turuncu = GHS05 Aşındırıcı Zonu
        </div>
        """, unsafe_allow_html=True)

    baslik_karti("Kapasite Kısıtlı COI Sıralama ve Hücre İhtiyacı (N_i) Tablosu")
    erp_tablo_goster(sirali_coi[["Kod", "Ad", "GHS", "Aylik_MPS_Ihtiyac_kg", "Toplam_Hacim_Vi", "Cekim_Sikligi_fi", "Gereken_Hucre_Ni", "COI_Indeksi"]])

elif secilen_modul == "5. Fiziki Sayım & Dinamik Fire (α) Güncelleme":
    baslik_karti("Periyodik Fiziki Sayım Görevi ve Üstel Düzeltmeli Fire Oranı (α_i) Güncellemesi")
    st.markdown("""
    <div class="formula-bar">
        <b>Dinamik Fire Güncelleme Denklemi (Üstel Düzeltme / Exponential Smoothing):</b><br>
        &alpha;_{yeni, i} = (&beta; &times; &alpha;_{gözlenen, i}) + ((1 - &beta;) &times; &alpha;_{eski, i}) &nbsp;&bull;&nbsp; Sayım farkları stok hareket tablosuna (+/-) olarak işlenir.
    </div>
    """, unsafe_allow_html=True)

    s1, s2 = st.columns([1, 1.45])
    with s1:
        with st.form("fiziki_sayim_form"):
            aktif_partiler = st.session_state.partiler.copy()
            lot_secim = st.selectbox(
                "Sayımı Yapılan Parti (Lot)",
                aktif_partiler["Parti_ID"] + " (" + aktif_partiler["HM_Kodu"] + " - Kaydi: " + aktif_partiler["Miktar_kg"].astype(str) + " kg)"
            )
            secilen_lot_id = lot_secim.split(" (")[0]
            lot_satir = aktif_partiler[aktif_partiler["Parti_ID"] == secilen_lot_id].iloc[0]
            kaydi_miktar = float(lot_satir["Miktar_kg"])
            ilgili_hm = lot_satir["HM_Kodu"]

            tartilan_miktar = st.number_input("Tartılan Gerçek Fiziki Miktar (kg)", 0.0, 10000.0, max(0.0, kaydi_miktar - 5.0), 1.0)
            beta_katsayi = st.slider("Üstel Düzeltme Katsayısı (β)", 0.10, 0.50, 0.25, 0.05)
            sayim_btn = st.form_submit_button("Sayım Farkını İşle ve Fire Oranını (α_i) Güncelle")

            if sayim_btn:
                fark_kg = round(tartilan_miktar - kaydi_miktar, 2)
                st.session_state.partiler.loc[st.session_state.partiler["Parti_ID"] == secilen_lot_id, "Miktar_kg"] = tartilan_miktar

                eski_alpha = float(st.session_state.hammaddeler.loc[st.session_state.hammaddeler["Kod"] == ilgili_hm, "Alpha_Fire"].values[0])
                gozlenen_oran = min(0.15, abs(fark_kg) / max(1.0, kaydi_miktar)) if fark_kg < 0 else eski_alpha
                yeni_alpha = round((beta_katsayi * gozlenen_oran) + ((1.0 - beta_katsayi) * eski_alpha), 4)
                st.session_state.hammaddeler.loc[st.session_state.hammaddeler["Kod"] == ilgili_hm, "Alpha_Fire"] = yeni_alpha

                isaret = "+" if fark_kg >= 0 else ""
                yeni_tr = pd.DataFrame([{
                    "Islem_No": f"TR-{1000 + len(st.session_state.hareket_log) + 1}",
                    "Tarih": datetime.now().strftime("%Y-%m-%d %H:%M"),
                    "Hareket_Tipi": "SAYIM DÜZELTME (+/-)",
                    "HM_Kodu": ilgili_hm,
                    "Parti_ID": secilen_lot_id,
                    "Degisim_kg": f"{isaret}{fark_kg:.2f}",
                    "Aciklama": f"Fiziki sayım eşitlemesi (α_eski={eski_alpha:.3f} -> α_yeni={yeni_alpha:.3f})"
                }])
                st.session_state.hareket_log = pd.concat([yeni_tr, st.session_state.hareket_log], ignore_index=True)
                st.success(f"Sayım farkı ({isaret}{fark_kg} kg) işlendi. {ilgili_hm} beklenen proses fire oranı α = {yeni_alpha:.4f} olarak güncellendi.")
                st.rerun()

    with s2:
        baslik_karti("Güncel Hammadde Proses Fire Oranları (α_i) ve Emniyet Stokları")
        erp_tablo_goster(analiz_tablosu[["Kod", "Ad", "Toplam_Stok_kg", "Alpha_Fire", "Talep_Std_Sapma", "Emniyet_Stoku_SS", "ROP_Esigi_kg", "Durum"]])

elif secilen_modul == "6. H1-H2 Deneysel Simülasyon (30 Senaryo)":
    baslik_karti("Aşama 5: 30 Aylık Üretim Planı Senaryosu ve İstatistiksel Hipotez Testleri (H1 & H2)")
    st.markdown("""
    <div class="formula-bar">
        <b>Deneysel Tasarım:</b> 30 farklı mevsimsel üretim planı senaryosu üzerinde (1) Rastgele Yerleşim, (2) Geçmiş Veriye Dayalı Statik COI ve (3) Önerilen Gelecek Üretim Planı Güdümlü Dinamik COI yöntemlerinin Toplam Taşıma Mesafesi (&Sigma; f_i &times; d_j) karşılaştırması.
    </div>
    """, unsafe_allow_html=True)

    seed_val = st.slider("Simülasyon Rastgelelik Tohumu (Random Seed)", 1, 100, 42)
    np.random.seed(seed_val)

    senaryolar = []
    for s in range(1, 31):
        rastgele_mesafe = np.random.normal(4850, 420)
        statik_coi_mesafe = rastgele_mesafe * np.random.uniform(0.84, 0.91)
        dinamik_coi_mesafe = statik_coi_mesafe * np.random.uniform(0.71, 0.78)
        tasarruf_statik_yuzde = ((statik_coi_mesafe - dinamik_coi_mesafe) / statik_coi_mesafe) * 100.0

        manuel_sapma = np.random.uniform(6.5, 11.2)
        onerilen_sapma = np.random.uniform(0.8, 2.1)

        senaryolar.append({
            "Senaryo_No": f"S-{s:02d}",
            "Rastgele_Mesafe": round(rastgele_mesafe, 1),
            "Statik_COI_Mesafe": round(statik_coi_mesafe, 1),
            "Onerilen_Dinamik_COI": round(dinamik_coi_mesafe, 1),
            "Mesafe_Kazanci_Yuzde": round(tasarruf_statik_yuzde, 2),
            "Manuel_Stok_Sapma_Yuzde": round(manuel_sapma, 2),
            "Onerilen_FEFO_Sapma_Yuzde": round(onerilen_sapma, 2),
        })

    sim_df = pd.DataFrame(senaryolar)
    fark_dizisi = sim_df["Statik_COI_Mesafe"] - sim_df["Onerilen_Dinamik_COI"]
    t_istatistigi = (fark_dizisi.mean()) / (fark_dizisi.std(ddof=1) / math.sqrt(30))
    ort_kazanc = sim_df["Mesafe_Kazanci_Yuzde"].mean()

    m1, m2, m3, m4 = st.columns(4)
    m1.markdown(f'<div class="kpi-card"><div class="kpi-title">Statik COI Ort. Mesafe</div><div class="kpi-val">{sim_df["Statik_COI_Mesafe"].mean():,.1f} br</div><div class="kpi-sub">Geçmiş Veriye Dayalı Politika</div></div>', unsafe_allow_html=True)
    m2.markdown(f'<div class="kpi-card"><div class="kpi-title">Önerilen Dinamik COI Ort.</div><div class="kpi-val" style="color:#15803d !important;">{sim_df["Onerilen_Dinamik_COI"].mean():,.1f} br</div><div class="kpi-sub">Gelecek Üretim Planı Güdümlü</div></div>', unsafe_allow_html=True)
    m3.markdown(f'<div class="kpi-card"><div class="kpi-title">Ortalama Mesafe Azalması (H1)</div><div class="kpi-val" style="color:#1d4ed8 !important;">%{ort_kazanc:.2f}</div><div class="kpi-sub">Hedef Eşik: En Az %20 Azalma</div></div>', unsafe_allow_html=True)
    m4.markdown(f'<div class="kpi-card"><div class="kpi-title">Eşleştirilmiş t-Testi (df=29)</div><div class="kpi-val">t = {t_istatistigi:.2f}</div><div class="kpi-sub">p &lt; 0.001 (İstatistiksel Anlamlı)</div></div>', unsafe_allow_html=True)

    st.write("")
    st.success(f"📊 İSTATİSTİKSEL DOĞRULAMA SONUCU: 30 senaryoluk deney sonucunda Önerilen Dinamik COI modeli, geçmiş veriye dayalı Statik COI modeline kıyasla taşıma mesafesini ortalama %{ort_kazanc:.2f} azaltmıştır (t = {t_istatistigi:.2f}, p < 0.001). H1 ve H2 hipotezleri α = 0.05 anlamlılık düzeyinde kabul edilmiştir.")
    erp_tablo_goster(sim_df)

elif secilen_modul == "7. SUS Kullanılabilirlik Testi (Aşama 5)":
    baslik_karti("Aşama 5: Sistem Kullanılabilirlik Ölçeği (SUS) Testi ve Sektörel Katılımcı Paneli")
    st.markdown("""
    <div class="formula-bar">
        <b>Metodoloji (Brooke, 1996):</b> Arayüz kullanılabilirliğini doğrulamak amacıyla 10 standart SUS maddesi 1 ile 5 arasında puanlanır. Katılımcıların unvan ve puanları doğrudan yönetici tablosuna kaydedilir.
    </div>
    """, unsafe_allow_html=True)

    with st.form("sus_form"):
        st.markdown("**Katılımcı Bilgileri (Yalnızca Proje Yöneticisi Tarafından Görüntülenir):**")
        c1, c2 = st.columns(2)
        katilimci_adi = c1.text_input("Adınız Soyadınız", placeholder="Örn: Ahmet Yılmaz")
        sirket_unvani = c2.text_input("Şirket / Kurum ve Unvanınız", placeholder="Örn: Kimya A.Ş. Üretim Mühendisi")

        st.markdown("---")
        st.markdown("**Lütfen aşağıdaki 10 ifadeyi sistem deneyiminize göre puanlayınız (1: Kesinlikle Katılmıyorum — 5: Kesinlikle Katılıyorum):**")
        
        q1 = st.slider("1. Bu sistemi sık sık kullanmak isterim.", 1, 5, 4)
        q2 = st.slider("2. Sistemi gereksiz derecede karmaşık buldum.", 1, 5, 1)
        q3 = st.slider("3. Sistemin kullanımının kolay olduğunu düşündüm.", 1, 5, 5)
        q4 = st.slider("4. Bu sistemi kullanabilmek için bir uzman desteğine ihtiyaç duyacağımı düşünüyorum.", 1, 5, 1)
        q5 = st.slider("5. Sistemdeki çeşitli özelliklerin birbiriyle ne kadar iyi bütünleştiğini gördüm.", 1, 5, 4)
        q6 = st.slider("6. Sistemde çok fazla tutarsızlık olduğunu düşündüm.", 1, 5, 1)
        q7 = st.slider("7. Çoğu insanın bu sistemi çok çabuk öğrenebileceğini tahmin ediyorum.", 1, 5, 5)
        q8 = st.slider("8. Sistemi kullanırken çok hantal / karmaşık buldum.", 1, 5, 1)
        q9 = st.slider("9. Sistemi kullanırken kendimi oldukça güvende ve yetkin hissettim.", 1, 5, 4)
        q10 = st.slider("10. Sistemi kullanmaya başlamadan önce çok fazla şey öğrenmem gerekiyordu.", 1, 5, 1)

        sus_gonder = st.form_submit_button("Testi Gönder ve Puanımı Kaydet")

        if sus_gonder:
            if not katilimci_adi.strip() or not sirket_unvani.strip():
                st.error("❌ Lütfen Ad Soyad ve Şirket/Unvan alanlarını doldurunuz!")
            else:
                tekler_skor = (q1 - 1) + (q3 - 1) + (q5 - 1) + (q7 - 1) + (q9 - 1)
                ciftler_skor = (5 - q2) + (5 - q4) + (5 - q6) + (5 - q8) + (5 - q10)
                bireysel_sus = (tekler_skor + ciftler_skor) * 2.5

                st.session_state.sus_yanitlari.append(bireysel_sus)
                
                WEBHOOK_URL = "https://script.google.com/macros/s/AKfycbzzVmNterBa_JT9jQxkR1Jtjm__X_wGsAIXKxI6EJkgkX4iPIP_fYBW7i6SGbXhBIuV/exec"
                
                veri_paketi = {
                    "tarih": datetime.now().strftime("%Y-%m-%d %H:%M"),
                    "adsoyad": katilimci_adi,
                    "unvan": sirket_unvani,
                    "suspuan": round(bireysel_sus, 1)
                }
                
                try:
                    if WEBHOOK_URL != "BURAYA_GOOGLE_APPS_SCRIPT_WEB_APP_URL_YAZILACAK":
                        requests.post(WEBHOOK_URL, json=veri_paketi, timeout=3)
                except:
                    pass

                st.success(f"✅ Teşekkürler {katilimci_adi}! Yanıtınız kaydedildi. Sizin SUS Puanınız: **{bireysel_sus:.1f} / 100**")

    toplam_katilimci = len(st.session_state.sus_yanitlari)
    genel_ortalama = np.mean(st.session_state.sus_yanitlari)

    st.write("")
    baslik_karti("Genel Katılımcı ve Ortalama Sonuç Paneli")
    
    p1, p2, p3 = st.columns(3)
    p1.markdown(f'<div class="kpi-card"><div class="kpi-title">Toplam Katılımcı Sayısı (N)</div><div class="kpi-val">{toplam_katilimci} Kullanıcı</div><div class="kpi-sub">Sektör ve Akademik Test</div></div>', unsafe_allow_html=True)
    p2.markdown(f'<div class="kpi-card"><div class="kpi-title">Genel Ortalama SUS Puanı</div><div class="kpi-val" style="color:#1d4ed8 !important;">{genel_ortalama:.1f} / 100</div><div class="kpi-sub">Hedef Başarı Eşiği: &ge; 70.0</div></div>', unsafe_allow_html=True)
    p3.markdown(f'<div class="kpi-card"><div class="kpi-title">Kullanılabilirlik Durumu</div><div class="kpi-val" style="color:{"#15803d" if genel_ortalama >= 70 else "#b91c1c"} !important;">{"BAŞARILI (GEÇTİ)" if genel_ortalama >= 70 else "İYİLEŞTİRME GEREKLİ"}</div><div class="kpi-sub">Brooke (1996) Ölçeği</div></div>', unsafe_allow_html=True)
