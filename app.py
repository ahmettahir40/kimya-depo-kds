elif secilen_modul == "7. SUS Kullanılabilirlik Testi (Aşama 5)":
    baslik_karti(
        "Aşama 5: Sistem Kullanılabilirlik Ölçeği (SUS) Testi ve Sektörel Katılımcı Paneli"
    )
    st.markdown(
        """
    <div class="formula-bar">
        <b>Metodoloji (Brooke, 1996):</b> Arayüz kullanılabilirliğini doğrulamak amacıyla 10 standart SUS maddesi 1 ile 5 arasında puanlanır. Katılımcıların unvan ve puanları doğrudan yönetici tablosuna kaydedilir.
    </div>
    """,
        unsafe_allow_html=True,
    )

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
                
                # Google Sheets Webhook Bağlantısı (URL başarıyla entegre edildi)
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

    # Canlı Katılımcı ve Ortalama Paneli
    toplam_katilimci = len(st.session_state.sus_yanitlari)
    genel_ortalama = np.mean(st.session_state.sus_yanitlari)

    st.write("")
    baslik_karti("Genel Katılımcı ve Ortalama Sonuç Paneli")
    
    p1, p2, p3 = st.columns(3)
    p1.markdown(f'<div class="kpi-card"><div class="kpi-title">Toplam Katılımcı Sayısı (N)</div><div class="kpi-val">{toplam_katilimci} Kullanıcı</div><div class="kpi-sub">Sektör ve Akademik Test</div></div>', unsafe_allow_html=True)
    p2.markdown(f'<div class="kpi-card"><div class="kpi-title">Genel Ortalama SUS Puanı</div><div class="kpi-val" style="color:#1d4ed8 !important;">{genel_ortalama:.1f} / 100</div><div class="kpi-sub">Hedef Başarı Eşiği: &ge; 70.0</div></div>', unsafe_allow_html=True)
    p3.markdown(f'<div class="kpi-card"><div class="kpi-title">Kullanılabilirlik Durumu</div><div class="kpi-val" style="color:{"#15803d" if genel_ortalama >= 70 else "#b91c1c"} !important;">{"BAŞARILI (GEÇTİ)" if genel_ortalama >= 70 else "İYİLEŞTİRME GEREKLİ"}</div><div class="kpi-sub">Brooke (1996) Ölçeği</div></div>', unsafe_allow_html=True)
