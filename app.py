# -*- coding: utf-8 -*-
# TÜBİTAK 2209-A Araştırma Projesi Prototipi
# Konu: Kimya Sektöründe Reçete Tabanlı Otomatik Stok Düşümü ve Parametrik Depo Yerleşimi KDS

from datetime import datetime, timedelta
import math
import numpy as np
import pandas as pd
import streamlit as st

st.set_page_config(
    page_title="KİM-KDS | Envanter ve Parametrik Depo Optimizasyon Sistemi",
    layout="wide",
    initial_sidebar_state="expanded",
)

st.markdown(
    """
<style>
    .main { background-color: #f4f6f9; }
    .stApp header { background-color: #0f2c59; }
    div[data-testid="stMetricValue"] { font-size: 1.5rem; font-weight: 700; color: #0f2c59; }
    div[data-testid="stMetricLabel"] { font-size: 0.85rem; color: #475569; font-weight: 600; }
    .erp-header {
        background-color: #0f2c59;
        color: #ffffff;
        padding: 14px 20px;
        border-radius: 4px;
        margin-bottom: 18px;
        border-left: 5px solid #3b82f6;
    }
    .erp-header h2 { margin: 0; font-size: 1.35rem; color: #ffffff; font-weight: 600; }
    .erp-header p { margin: 4px 0 0 0; font-size: 0.85rem; color: #cbd5e1; }
    .section-box {
        background: #ffffff;
        padding: 16px;
        border-radius: 4px;
        border: 1px solid #cbd5e1;
        margin-bottom: 14px;
    }
    .grid-table { border-collapse: collapse; width: 100%; font-family: monospace; font-size: 12px; }
    .grid-table td {
        border: 1px solid #94a3b8;
        text-align: center;
        padding: 8px 4px;
        height: 48px;
        width: 70px;
    }
</style>
""",
    unsafe_allow_html=True,
)


def init_db():
    if "hammaddeler" not in st.session_state:
        st.session_state.hammaddeler = pd.DataFrame(
            [
                {
                    "Kod": "HM-01",
                    "Ad": "Titanyum Dioksit (TiO2)",
                    "Teorik_Stok_kg": 1450.0,
                    "Fiziki_Stok_kg": 1435.0,
                    "Birim_Hacim_m2": 1.2,
                    "Tedarik_Suresi_Gun": 7,
                    "Gunluk_Tuketim_kg": 45.0,
                    "Fire_Std_Sapma": 4.2,
                    "Sinif": "Normal",
                    "SKT": "2027-04-15",
                },
                {
                    "Kod": "HM-02",
                    "Ad": "Stiren Akrilik Emülsiyon",
                    "Teorik_Stok_kg": 2100.0,
                    "Fiziki_Stok_kg": 2080.0,
                    "Birim_Hacim_m2": 1.5,
                    "Tedarik_Suresi_Gun": 5,
                    "Gunluk_Tuketim_kg": 80.0,
                    "Fire_Std_Sapma": 6.5,
                    "Sinif": "Normal",
                    "SKT": "2027-01-20",
                },
                {
                    "Kod": "HM-03",
                    "Ad": "Mikronize Kalsit (CaCO3)",
                    "Teorik_Stok_kg": 3800.0,
                    "Fiziki_Stok_kg": 3790.0,
                    "Birim_Hacim_m2": 2.4,
                    "Tedarik_Suresi_Gun": 3,
                    "Gunluk_Tuketim_kg": 110.0,
                    "Fire_Std_Sapma": 8.0,
                    "Sinif": "Normal",
                    "SKT": "2028-06-01",
                },
                {
                    "Kod": "HM-04",
                    "Ad": "Ksilen (Aromatik Solvent)",
                    "Teorik_Stok_kg": 310.0,
                    "Fiziki_Stok_kg": 295.0,
                    "Birim_Hacim_m2": 1.0,
                    "Tedarik_Suresi_Gun": 6,
                    "Gunluk_Tuketim_kg": 55.0,
                    "Fire_Std_Sapma": 5.8,
                    "Sinif": "Yanici",
                    "SKT": "2026-12-10",
                },
                {
                    "Kod": "HM-05",
                    "Ad": "Poliüretan Reçine Bazı",
                    "Teorik_Stok_kg": 890.0,
                    "Fiziki_Stok_kg": 885.0,
                    "Birim_Hacim_m2": 1.4,
                    "Tedarik_Suresi_Gun": 8,
                    "Gunluk_Tuketim_kg": 40.0,
                    "Fire_Std_Sapma": 3.5,
                    "Sinif": "Yanici",
                    "SKT": "2027-02-28",
                },
                {
                    "Kod": "HM-06",
                    "Ad": "Hidrojen Peroksit (%50)",
                    "Teorik_Stok_kg": 420.0,
                    "Fiziki_Stok_kg": 412.0,
                    "Birim_Hacim_m2": 1.0,
                    "Tedarik_Suresi_Gun": 5,
                    "Gunluk_Tuketim_kg": 30.0,
                    "Fire_Std_Sapma": 2.9,
                    "Sinif": "Oksitleyici",
                    "SKT": "2026-11-25",
                },
                {
                    "Kod": "HM-07",
                    "Ad": "Mono Etilen Glikol (MEG)",
                    "Teorik_Stok_kg": 640.0,
                    "Fiziki_Stok_kg": 638.0,
                    "Birim_Hacim_m2": 0.8,
                    "Tedarik_Suresi_Gun": 4,
                    "Gunluk_Tuketim_kg": 22.0,
                    "Fire_Std_Sapma": 1.8,
                    "Sinif": "Normal",
                    "SKT": "2027-08-12",
                },
            ]
        )

    if "mamuller" not in st.session_state:
        st.session_state.mamuller = pd.DataFrame(
            [
                {
                    "Mamul_Kodu": "M-101",
                    "Mamul_Adi": "Akrilik Dış Cephe Boyası",
                    "Mevcut_Stok_kg": 1200.0,
                    "Aylik_MPS_Hedef_kg": 8500.0,
                },
                {
                    "Mamul_Kodu": "M-102",
                    "Mamul_Adi": "Endüstriyel Poliüretan Kaplama",
                    "Mevcut_Stok_kg": 650.0,
                    "Aylik_MPS_Hedef_kg": 4200.0,
                },
                {
                    "Mamul_Kodu": "M-103",
                    "Mamul_Adi": "Aktif Oksijenli Yüzey Kimyasalı",
                    "Mevcut_Stok_kg": 400.0,
                    "Aylik_MPS_Hedef_kg": 3000.0,
                },
            ]
        )

    if "bom" not in st.session_state:
        st.session_state.bom = pd.DataFrame(
            [
                {"Mamul_Kodu": "M-101", "HM_Kodu": "HM-01", "Oran_kg": 0.25},
                {"Mamul_Kodu": "M-101", "HM_Kodu": "HM-02", "Oran_kg": 0.35},
                {"Mamul_Kodu": "M-101", "HM_Kodu": "HM-03", "Oran_kg": 0.35},
                {"Mamul_Kodu": "M-101", "HM_Kodu": "HM-07", "Oran_kg": 0.05},
                {"Mamul_Kodu": "M-102", "HM_Kodu": "HM-04", "Oran_kg": 0.35},
                {"Mamul_Kodu": "M-102", "HM_Kodu": "HM-05", "Oran_kg": 0.50},
                {"Mamul_Kodu": "M-102", "HM_Kodu": "HM-01", "Oran_kg": 0.15},
                {"Mamul_Kodu": "M-103", "HM_Kodu": "HM-06", "Oran_kg": 0.40},
                {"Mamul_Kodu": "M-103", "HM_Kodu": "HM-07", "Oran_kg": 0.20},
                {"Mamul_Kodu": "M-103", "HM_Kodu": "HM-03", "Oran_kg": 0.40},
            ]
        )

    if "giris_arsivi" not in st.session_state:
        st.session_state.giris_arsivi = pd.DataFrame(
            [
                {
                    "Islem_No": "IRS-2026-081",
                    "Tarih": "2026-10-18",
                    "HM_Kodu": "HM-01",
                    "Miktar_kg": 1000.0,
                    "Parti_No": "LOT-884A",
                    "SKT": "2027-04-15",
                    "Atanan_Hucre": "H(1,2)",
                },
                {
                    "Islem_No": "IRS-2026-084",
                    "Tarih": "2026-10-22",
                    "HM_Kodu": "HM-04",
                    "Miktar_kg": 500.0,
                    "Parti_No": "LOT-901X",
                    "SKT": "2026-12-10",
                    "Atanan_Hucre": "H(0,4) [Yanıcı Zonu]",
                },
                {
                    "Islem_No": "IRS-2026-089",
                    "Tarih": "2026-10-29",
                    "HM_Kodu": "HM-02",
                    "Miktar_kg": 1500.0,
                    "Parti_No": "LOT-912B",
                    "SKT": "2027-01-20",
                    "Atanan_Hucre": "H(1,1)",
                },
            ]
        )

    if "uretim_log" not in st.session_state:
        st.session_state.uretim_log = pd.DataFrame(
            [
                {
                    "Tarih_Saat": "2026-11-02 14:20",
                    "Mamul_Kodu": "M-101",
                    "Uretilen_kg": 400.0,
                    "Durum": "Backflushing Tamamlandı",
                },
                {
                    "Tarih_Saat": "2026-11-03 09:45",
                    "Mamul_Kodu": "M-102",
                    "Uretilen_kg": 250.0,
                    "Durum": "Backflushing Tamamlandı",
                },
            ]
        )


init_db()


def hesapla_rop_ve_coi(hm_df, mamul_df, bom_df, tasiyici_kapasite=250.0):
    df = hm_df.copy()
    z_degeri = 1.65

    mps_ihtiyac = {}
    for _, hm in df.iterrows():
        kod = hm["Kod"]
        ilgili_receteler = bom_df[bom_df["HM_Kodu"] == kod]
        toplam_m = 0.0
        for _, r in ilgili_receteler.iterrows():
            m_hedef = mamul_df.loc[
                mamul_df["Mamul_Kodu"] == r["Mamul_Kodu"], "Aylik_MPS_Hedef_kg"
            ].values[0]
            toplam_m += m_hedef * r["Oran_kg"]
        mps_ihtiyac[kod] = toplam_m

    df["Gelecek_Ay_MPS_Ihtiyac_kg"] = df["Kod"].map(mps_ihtiyac)
    df["Cekim_Sikligi_fi"] = df["Gelecek_Ay_MPS_Ihtiyac_kg"].apply(
        lambda m: max(1, math.ceil(m / tasiyici_kapasite))
    )
    df["Toplam_Hacim_Vi"] = (
        df["Fiziki_Stok_kg"] / 500.0
    ) * df["Birim_Hacim_m2"]
    df["Toplam_Hacim_Vi"] = df["Toplam_Hacim_Vi"].round(2).clip(lower=1.0)
    df["COI_Indeksi"] = (df["Toplam_Hacim_Vi"] / df["Cekim_Sikligi_fi"]).round(
        4
    )

    df["Emniyet_Stoku_SS"] = (
        z_degeri * df["Fire_Std_Sapma"] * np.sqrt(df["Tedarik_Suresi_Gun"])
    ).round(1)
    df["ROP_Seviyesi_kg"] = (
        (df["Gelecek_Ay_MPS_Ihtiyac_kg"] / 30.0) * df["Tedarik_Suresi_Gun"]
        + df["Emniyet_Stoku_SS"]
    ).round(1)
    df["Fire_Farki_kg"] = (df["Teorik_Stok_kg"] - df["Fiziki_Stok_kg"]).round(1)
    df["Siparis_Durumu"] = np.where(
        df["Fiziki_Stok_kg"] <= df["ROP_Seviyesi_kg"],
        "KRİTİK - SİPARİŞ VER",
        "YETERLİ",
    )

    return df


st.sidebar.markdown("### KİM-KDS v2.4")
st.sidebar.caption(
    "Üretim Planı Güdümlü Parametrik Depo ve Stok Kontrol Sistemi"
)
st.sidebar.markdown("---")

menu = st.sidebar.radio(
    "Sistem Modülleri",
    [
        "1. Genel Envanter ve ROP Paneli",
        "2. Ürün Ağacı (BOM) ve Üretim Düşümü",
        "3. Mal Kabul Arşivi ve FEFO Takibi",
        "4. Parametrik 2B Depo Haritası (COI)",
        "5. Döngüsel Sayım ve Fire Denetimi",
    ],
)

st.sidebar.markdown("---")
tasiyici_kap = st.sidebar.number_input(
    "Forklift Tek Sefer Taşıma Kapasitesi (kg)",
    min_value=50.0,
    max_value=2000.0,
    value=250.0,
    step=50.0,
)
analiz_df = hesapla_rop_ve_coi(
    st.session_state.hammaddeler,
    st.session_state.mamuller,
    st.session_state.bom,
    tasiyici_kap,
)

st.markdown(
    """
<div class="erp-header">
    <h2>KİM-KDS | Kimya Sektörü Karar Destek ve Depo Optimizasyon Sistemi</h2>
    <p>Modül: Reçete Tabanlı Otomatik Düşüm (Backflushing) &bull; MPS/BOM Çözümleme &bull; COI &amp; Manhattan 2B Grid Yerleşimi &bull; GHS/ADR Kısıtları</p>
</div>
""",
    unsafe_allow_html=True,
)

if menu == "1. Genel Envanter ve ROP Paneli":
    kritik_sayisi = int(
        (analiz_df["Siparis_Durumu"] == "KRİTİK - SİPARİŞ VER").sum()
    )
    toplam_stok = analiz_df["Fiziki_Stok_kg"].sum()
    toplam_fire = analiz_df["Fire_Farki_kg"].sum()

    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Toplam Hammadde Kalemi (SKU)", f"{len(analiz_df)} Kalem")
    c2.metric("Toplam Fiziki Hammadde Stoğu", f"{toplam_stok:,.1f} kg")
    c3.metric("ROP Altına Düşen Kritik Kalem", f"{kritik_sayisi} Hammadde")
    c4.metric("Kümülatif Proses Fire Sapması (ΔS)", f"{toplam_fire:,.1f} kg")

    if kritik_sayisi > 0:
        kritik_kodlar = ", ".join(
            analiz_df[analiz_df["Siparis_Durumu"] == "KRİTİK - SİPARİŞ VER"][
                "Ad"
            ].tolist()
        )
        st.error(
            f"DİNAMİK ROP UYARISI: Gelecek 1 aylık üretim planı (MPS) ve tedarik süreleri (L) dikkate alındığında şu hammaddeler Yeniden Sipariş Noktasının altına düşmüştür: {kritik_kodlar}"
        )

    st.subheader(
        "Hammadde Envanter, COI Öncelik ve Dinamik Sipariş (ROP) Tablosu"
    )
    gosterim_kolonlari = [
        "Kod",
        "Ad",
        "Sinif",
        "Teorik_Stok_kg",
        "Fiziki_Stok_kg",
        "Gelecek_Ay_MPS_Ihtiyac_kg",
        "ROP_Seviyesi_kg",
        "COI_Indeksi",
        "SKT",
        "Siparis_Durumu",
    ]
    st.dataframe(analiz_df[gosterim_kolonlari], use_container_width=True)

    st.subheader("Mamul Stokları ve Gelecek 1 Aylık Ana Üretim Planı (MPS)")
    st.dataframe(st.session_state.mamuller, use_container_width=True)

elif menu == "2. Ürün Ağacı (BOM) ve Üretim Düşümü":
    col_sol, col_sag = st.columns([1, 1])

    with col_sol:
        st.subheader("Günlük Üretim Bildirimi ve Otomatik Düşüm")
        st.caption(
            "Üretilen mamul miktarı girildiğinde, reçete (BOM) katsayılarına göre hammadde stokları otomatik düşülür."
        )

        with st.form("uretim_formu"):
            mamul_secim = st.selectbox(
                "Üretilen Mamul",
                st.session_state.mamuller["Mamul_Kodu"]
                + " - "
                + st.session_state.mamuller["Mamul_Adi"],
            )
            secilen_m_kod = mamul_secim.split(" - ")[0]
            uretim_miktari = st.number_input(
                "Üretilen Miktar (kg)",
                min_value=1.0,
                max_value=5000.0,
                value=100.0,
                step=10.0,
            )

            ilgili_bom = st.session_state.bom[
                st.session_state.bom["Mamul_Kodu"] == secilen_m_kod
            ].merge(
                st.session_state.hammaddeler[["Kod", "Ad", "Fiziki_Stok_kg"]],
                left_on="HM_Kodu",
                right_on="Kod",
            )
            ilgili_bom["Dusulecek_Miktar_kg"] = (
                ilgili_bom["Oran_kg"] * uretim_miktari
            )
            st.markdown("**Reçeteye Göre Otomatik Düşülecek Hammaddeler:**")
            st.dataframe(
                ilgili_bom[
                    ["HM_Kodu", "Ad", "Oran_kg", "Dusulecek_Miktar_kg", "Fiziki_Stok_kg"]
                ],
                use_container_width=True,
            )

            onay = st.form_submit_button("Üretimi Kaydet ve Stoktan Düş (Backflush)")
            if onay:
                yetersiz = ilgili_bom[
                    ilgili_bom["Fiziki_Stok_kg"]
                    < ilgili_bom["Dusulecek_Miktar_kg"]
                ]
                if not yetersiz.empty:
                    st.error(
                        "HATA: Depoda yeterli fiziki hammadde stoğu bulunmamaktadır!"
                    )
                else:
                    for _, satir in ilgili_bom.iterrows():
                        hm_k = satir["HM_Kodu"]
                        dusum = satir["Dusulecek_Miktar_kg"]
                        st.session_state.hammaddeler.loc[
                            st.session_state.hammaddeler["Kod"] == hm_k,
                            "Teorik_Stok_kg",
                        ] -= dusum
                        st.session_state.hammaddeler.loc[
                            st.session_state.hammaddeler["Kod"] == hm_k,
                            "Fiziki_Stok_kg",
                        ] -= dusum

                    st.session_state.mamuller.loc[
                        st.session_state.mamuller["Mamul_Kodu"] == secilen_m_kod,
                        "Mevcut_Stok_kg",
                    ] += uretim_miktari

                    yeni_log = pd.DataFrame(
                        [
                            {
                                "Tarih_Saat": (
                                    datetime.now().strftime("%Y-%m-%d %H:%M")
                                ),
                                "Mamul_Kodu": secilen_m_kod,
                                "Uretilen_kg": uretim_miktari,
                                "Durum": "Backflushing Tamamlandı",
                            }
                        ]
                    )
                    st.session_state.uretim_log = pd.concat(
                        [yeni_log, st.session_state.uretim_log],
                        ignore_index=True,
                    )
                    st.success(
                        f"{uretim_miktari} kg {secilen_m_kod} mamul stoğuna eklendi ve hammaddeler reçeteye göre stoktan düşüldü."
                    )
                    st.rerun()

    with col_sag:
        st.subheader("Yeni Ürün Reçetesi (BOM) Bileşeni Tanımla")
        with st.form("bom_ekle_form"):
            m_kodu_yeni = st.selectbox(
                "Mamul Kodu", st.session_state.mamuller["Mamul_Kodu"]
            )
            hm_kodu_yeni = st.selectbox(
                "Hammadde Kodu", st.session_state.hammaddeler["Kod"]
            )
            oran_yeni = st.number_input(
                "1 kg Mamul İçin Kullanım Oranı (kg)",
                min_value=0.01,
                max_value=1.00,
                value=0.10,
                step=0.05,
            )
            bom_kaydet = st.form_submit_button("Reçete Satırını Güncelle / Ekle")
            if bom_kaydet:
                mevcut_kayit = (
                    st.session_state.bom["Mamul_Kodu"] == m_kodu_yeni
                ) & (st.session_state.bom["HM_Kodu"] == hm_kodu_yeni)
                if mevcut_kayit.any():
                    st.session_state.bom.loc[mevcut_kayit, "Oran_kg"] = (
                        oran_yeni
                    )
                else:
                    yeni_b = pd.DataFrame(
                        [
                            {
                                "Mamul_Kodu": m_kodu_yeni,
                                "HM_Kodu": hm_kodu_yeni,
                                "Oran_kg": oran_yeni,
                            }
                        ]
                    )
                    st.session_state.bom = pd.concat(
                        [st.session_state.bom, yeni_b], ignore_index=True
                    )
                st.success("Ürün ağacı (BOM) güncellendi.")
                st.rerun()

        st.subheader("Gerçekleşen Üretim ve Stok Düşüm Kayıtları")
        st.dataframe(st.session_state.uretim_log, use_container_width=True)

elif menu == "3. Mal Kabul Arşivi ve FEFO Takibi":
    c_sol, c_sag = st.columns([1, 2])

    with c_sol:
        st.subheader("Yeni Hammadde Mal Kabul Girişi")
        with st.form("mal_kabul_form"):
            irs_no = st.text_input("İrsaliye / İşlem No", value="IRS-2026-095")
            hm_sec = st.selectbox(
                "Gelen Hammadde",
                st.session_state.hammaddeler["Kod"]
                + " - "
                + st.session_state.hammaddeler["Ad"],
            )
            gelen_kod = hm_sec.split(" - ")[0]
            gelen_miktar = st.number_input(
                "Gelen Miktar (kg)", min_value=10.0, value=500.0, step=50.0
            )
            lot_no = st.text_input("Parti / Lot Numarası", value="LOT-940C")
            skt_tarih = st.date_input(
                "Son Kullanma Tarihi (FEFO İçin)",
                value=datetime.today() + timedelta(days=180),
            )
            kabul_onay = st.form_submit_button("Mal Kabulü Tamamla ve Arşivle")

            if kabul_onay:
                st.session_state.hammaddeler.loc[
                    st.session_state.hammaddeler["Kod"] == gelen_kod,
                    "Teorik_Stok_kg",
                ] += gelen_miktar
                st.session_state.hammaddeler.loc[
                    st.session_state.hammaddeler["Kod"] == gelen_kod,
                    "Fiziki_Stok_kg",
                ] += gelen_miktar
                sinif_bilgi = st.session_state.hammaddeler.loc[
                    st.session_state.hammaddeler["Kod"] == gelen_kod, "Sinif"
                ].values[0]
                atanan_h = (
                    "H(0,4) [Yanıcı Zonu]"
                    if sinif_bilgi == "Yanici"
                    else "H(1,2) [Dinamik Put-Away]"
                )

                yeni_arsiv = pd.DataFrame(
                    [
                        {
                            "Islem_No": irs_no,
                            "Tarih": datetime.now().strftime("%Y-%m-%d"),
                            "HM_Kodu": gelen_kod,
                            "Miktar_kg": gelen_miktar,
                            "Parti_No": lot_no,
                            "SKT": skt_tarih.strftime("%Y-%m-%d"),
                            "Atanan_Hucre": atanan_h,
                        }
                    ]
                )
                st.session_state.giris_arsivi = pd.concat(
                    [yeni_arsiv, st.session_state.giris_arsivi],
                    ignore_index=True,
                )
                st.success(
                    f"{gelen_miktar} kg {gelen_kod} stoka eklendi, arşivlendi ve {atanan_h} hücresine yönlendirildi."
                )
                st.rerun()

    with c_sag:
        st.subheader("Hammadde Tedarik ve Mal Kabul Arşivi")
        st.dataframe(st.session_state.giris_arsivi, use_container_width=True)

        st.subheader(
            "FEFO (Son Kullanma Tarihi Yaklaşan İlk Çıkar) Sevk Öncelik Listesi"
        )
        fefo_df = analiz_df[
            ["Kod", "Ad", "Sinif", "Fiziki_Stok_kg", "SKT"]
        ].sort_values(by="SKT", ascending=True)
        st.dataframe(fefo_df, use_container_width=True)

elif menu == "4. Parametrik 2B Depo Haritası (COI)":
    st.subheader(
        "Parametrik 2 Boyutlu Izgara (2D Grid) ve COI Yerleşim Optimizasyonu"
    )
    st.caption(
        "Formül: d_j = |x_j - x_p| + |y_j - y_p| (Manhattan Mesafesi) ve COI_i = V_i / f_i (Çekim Başına Hacim İndeksi)"
    )

    p1, p2, p3, p4 = st.columns(4)
    depo_en = p1.number_input(
        "Depo Eni - W (Metre)", min_value=12, max_value=90, value=24, step=3
    )
    depo_boy = p2.number_input(
        "Depo Boyu - L (Metre)", min_value=15, max_value=120, value=30, step=3
    )
    hucre_boyut = p3.number_input(
        "Standart Hücre/Palet Modülü (Metre)",
        min_value=2,
        max_value=6,
        value=3,
        step=1,
    )
    kapi_y = p4.number_input(
        "Üretim Bandı Giriş Kapısı Satırı (x_p=0, y_p)",
        min_value=0,
        max_value=7,
        value=2,
        step=1,
    )

    satir_sayisi = max(4, min(10, int(depo_en // hucre_boyut)))
    sutun_sayisi = max(5, min(12, int(depo_boy // hucre_boyut)))
    kapi_satir = min(kapi_y, satir_sayisi - 1)

    sirali_hm = analiz_df.sort_values(by="COI_Indeksi", ascending=True)

    hucreler = []
    for r in range(satir_sayisi):
        for c in range(sutun_sayisi):
            dist = abs(r - kapi_satir) + abs(c - 0)
            koridor_mu = r == kapi_satir and c > 0
            yanici_zon = r <= 1 and c >= sutun_sayisi - 2
            oksit_zon = r >= satir_sayisi - 2 and c >= sutun_sayisi - 2
            hucreler.append(
                {
                    "r": r,
                    "c": c,
                    "dist": dist,
                    "koridor": koridor_mu,
                    "yanici_zon": yanici_zon,
                    "oksit_zon": oksit_zon,
                    "atanan": None,
                }
            )

    for _, hm in sirali_hm.iterrows():
        kod = hm["Kod"]
        sinif = hm["Sinif"]
        gereken_hucre = max(1, min(3, int(math.ceil(hm["Toplam_Hacim_Vi"]))))

        if sinif == "Yanici":
            uygun = [
                h
                for h in hucreler
                if h["yanici_zon"] and not h["koridor"] and h["atanan"] is None
            ]
        elif sinif == "Oksitleyici":
            uygun = [
                h
                for h in hucreler
                if h["oksit_zon"] and not h["koridor"] and h["atanan"] is None
            ]
        else:
            uygun = [
                h
                for h in hucreler
                if not h["yanici_zon"]
                and not h["oksit_zon"]
                and not h["koridor"]
                and h["atanan"] is None
            ]
            uygun = sorted(uygun, key=lambda x: x["dist"])

        for h in uygun[:gereken_hucre]:
            h["atanan"] = f"{kod}<br><small>d={h['dist']}</small>"

    html_grid = "<table class='grid-table'>"
    for r in range(satir_sayisi):
        html_grid += "<tr>"
        for c in range(sutun_sayisi):
            h = next(
                item for item in hucreler if item["r"] == r and item["c"] == c
            )
            if r == kapi_satir and c == 0:
                bg = "#1e3a8a"
                fg = "#ffffff"
                icerik = "<b>ÜRETİM<br>KAPISI</b>"
            elif h["koridor"]:
                bg = "#e2e8f0"
                fg = "#475569"
                icerik = "KORİDOR"
            elif h["atanan"]:
                if h["yanici_zon"]:
                    bg = "#fecaca"
                    fg = "#991b1b"
                elif h["oksit_zon"]:
                    bg = "#fef08a"
                    fg = "#854d0e"
                else:
                    bg = "#bfdbfe"
                    fg = "#1e3a8a"
                icerik = f"<b>{h['atanan']}</b>"
            else:
                if h["yanici_zon"]:
                    bg = "#fff1f2"
                    fg = "#be123c"
                    icerik = f"Yanıcı Zon<br><small>d={h['dist']}</small>"
                elif h["oksit_zon"]:
                    bg = "#fefce8"
                    fg = "#a16207"
                    icerik = f"Oksit. Zon<br><small>d={h['dist']}</small>"
                else:
                    bg = "#ffffff"
                    fg = "#94a3b8"
                    icerik = f"Boş ({r},{c})<br><small>d={h['dist']}</small>"
            html_grid += (
                f"<td style='background-color:{bg}; color:{fg};'>{icerik}</td>"
            )
        html_grid += "</tr>"
    html_grid += "</table>"

    st.markdown(html_grid, unsafe_allow_html=True)
    st.caption(
        "Renk Kodları: Koyu Mavi = Üretim Bandı Giriş Kapısı (x_p, y_p) | Açık Mavi = COI Öncelikli Normal Hammaddeler | Kırmızı = GHS/ADR Yanıcı Güvenlik Zonu | Sarı = GHS/ADR Oksitleyici İzole Zon | Gri = Forklift Ana Koridoru"
    )

    st.subheader(
        "Gelecek 1 Aylık MPS Çözümlemesi ve COI Yerleşim Öncelik Tablosu"
    )
    st.dataframe(
        sirali_hm[
            [
                "Kod",
                "Ad",
                "Sinif",
                "Gelecek_Ay_MPS_Ihtiyac_kg",
                "Cekim_Sikligi_fi",
                "Toplam_Hacim_Vi",
                "COI_Indeksi",
            ]
        ],
        use_container_width=True,
    )

elif menu == "5. Döngüsel Sayım ve Fire Denetimi":
    st.subheader(
        "Döngüsel Sayım (Cycle Counting) ve Proses Fire Sapması (ΔS) Yönetimi"
    )
    st.caption(
        "Kimyasal üretimde buharlaşma, tozuma ve kazan dibi kalıntısı kaynaklı fireleri yakalamak için fiziki sayım giriş ekranı."
    )

    c_sayim1, c_sayim2 = st.columns([1, 2])
    with c_sayim1:
        with st.form("sayim_form"):
            hm_sayim = st.selectbox(
                "Sayımı Yapılan Hammadde",
                st.session_state.hammaddeler["Kod"]
                + " - "
                + st.session_state.hammaddeler["Ad"],
            )
            sayim_kod = hm_sayim.split(" - ")[0]
            mevcut_teo = st.session_state.hammaddeler.loc[
                st.session_state.hammaddeler["Kod"] == sayim_kod,
                "Teorik_Stok_kg",
            ].values[0]
            st.info(f"Sistemdeki Teorik Stok: {mevcut_teo} kg")
            yeni_fiziki = st.number_input(
                "Tartılan Gerçek Fiziki Stok (kg)",
                min_value=0.0,
                value=float(mevcut_teo),
                step=1.0,
            )
            sayim_onay = st.form_submit_button(
                "Sayım Farkını Kaydet ve Stoğu Eşitle"
            )

            if sayim_onay:
                st.session_state.hammaddeler.loc[
                    st.session_state.hammaddeler["Kod"] == sayim_kod,
                    "Fiziki_Stok_kg",
                ] = yeni_fiziki
                fark = mevcut_teo - yeni_fiziki
                st.success(
                    f"{sayim_kod} fiziki stoğu {yeni_fiziki} kg olarak güncellendi. Tespit edilen proses firesi (ΔS): {fark:.1f} kg."
                )
                st.rerun()

    with c_sayim2:
        analiz_guncel = hesapla_rop_ve_coi(
            st.session_state.hammaddeler,
            st.session_state.mamuller,
            st.session_state.bom,
            tasiyici_kap,
        )
        st.dataframe(
            analiz_guncel[
                [
                    "Kod",
                    "Ad",
                    "Teorik_Stok_kg",
                    "Fiziki_Stok_kg",
                    "Fire_Farki_kg",
                    "Fire_Std_Sapma",
                    "Emniyet_Stoku_SS",
                ]
            ],
            use_container_width=True,
        )