import streamlit as st
import instaloader
import plotly.graph_objects as go
from fake_score import calculate_fake_score
import time

def show_gauge(score):
    fig = go.Figure(go.Indicator(
        mode = "gauge+number",
        value = score,
        title = {'text': "Fake Skoru"},
        gauge = {
            'axis': {'range': [0, 100]},
            'bar': {'color': "white"},
            'steps': [
                {'range': [0, 40], 'color': "green"},
                {'range': [40, 70], 'color': "yellow"},
                {'range': [70, 100], 'color': "red"}],
            'threshold': {
                'line': {'color': "black", 'width': 4},
                'thickness': 0.75,
                'value': score}
        }
    ))
    st.plotly_chart(fig, use_container_width=True)

st.set_page_config(page_title="Instagram Fake Catcher", page_icon="🔍")
st.title("🔍 Instagram Fake Catcher")
username = st.text_input("Bir kullanıcı adı gir", placeholder="örnek: akiifdora")

if st.button("Analiz Et") and username:
    L = instaloader.Instaloader()

    with st.spinner("Veriler çekiliyor..."):
        try:
            info_placeholder = st.info("⏳ Çok fazla sorgu atmamak için yavaşlatma uygulanıyor. Lütfen bekle...")
            time.sleep(3)
            profile = instaloader.Profile.from_username(L.context, username)
            score = calculate_fake_score(profile)
            info_placeholder.empty()

            if score >= 70:
                st.error("⚠️ Bu hesap büyük ihtimalle fake haberin olsun.")
            elif score >= 40:
                st.warning("🤔 Bu hesap şüpheli görünüyor aman dikkat et.")
            else:
                st.success("✅ Bu hesap büyük ihtimalle gerçek rahat olabilirsin.")

            st.subheader("📊 Detaylar")
            col1, col2 = st.columns([1, 3])

            with col1:
                st.markdown("🔐 **Gizli Hesap:**")
                st.markdown("📝 **Biyografi:**")
                st.markdown("📸 **Gönderi Sayısı:**")
                st.markdown("🟠 **Biyografi Durumu:**")
                st.markdown("📷 **Profil Fotoğrafı:**")
                st.markdown("👥 **Takipçi Sayısı:**")
                st.markdown("➡️ **Takip Edilen Sayısı:**")
                st.markdown("📊 **Takipçi/Takip Oranı:**")
                st.markdown("⚠️ **Oran Durumu:**")

            with col2:
                st.markdown(f"{'🔐 Bu hesap gizli' if profile.is_private else '🌐 Bu hesap herkese açık'}")
                st.markdown(f"{profile.biography if profile.biography else 'Yok'}")
                st.markdown(f"{profile.mediacount}")

                # Biyografi uzunluğu durumu
                bio_len = len(profile.biography.strip()) if profile.biography else 0
                if bio_len == 0:
                    st.markdown("🟠 Biyografisi yok şüphe kokusunu aldın mı?")
                elif bio_len < 20:
                    st.markdown("🟡 Biyografi kısa belki de yazı yazmayı sevmiyordur.")
                else:
                    st.markdown("🟢 Biyografi uzunluğu normal görünüyor.")

                # Profil fotoğrafı
                if profile.profile_pic_url:
                    st.markdown(f"[Açmak için tıkla!]({profile.profile_pic_url})")
                else:
                    st.markdown("Yok")

                # Takipçi ve takip edilen sayısı ile oran
                followers = profile.followers
                followees = profile.followees
                ratio = followers / followees if followees != 0 else 0

                st.markdown(f"{followers}")
                st.markdown(f"{followees}")
                st.markdown(f"{ratio:.2f}")

                if ratio < 0.3:
                    st.markdown("🟠 Takipçi/Takip oranı çok düşük, dikkatli ol.")
                elif ratio > 6:
                    st.markdown("🟢 Takipçi/Takip oranı yüksek, genelde gerçek hesap.")
                else:
                    st.markdown("🟡 Takipçi/Takip oranı ortalama, şüpheli olabilir.")

            show_gauge(score)

            with st.expander("ℹ️ Fake Score nedir? Neye göre belirleniyor?"):
                st.markdown("""
            **Fake Score**, aşağıdaki kriterlere göre hesaplanır:

            - 📸 Profil fotoğrafı olup olmaması  
            - 📝 Biyografi varlığı ve uzunluğu  
            - 🔐 Hesap gizli mi?  
            - 👥 Takipçi ve takip edilen sayısı  
            - ⚖️ Takipçi/Takip oranı (çok dengesizse şüphelidir)  
            - 📤 Gönderi sayısı

            Bu veriler istatistiksel olarak sahte hesapların davranış örüntülerine göre değerlendirilir. Sonuç 0-100 arası bir skor olarak gösterilir.
                """)

        except Exception as e:
            error_msg = str(e).lower()
            info_placeholder.empty()

            if "please wait a few minutes" in error_msg or "429" in error_msg:
                st.error("⚠️ Instagram seni geçici olarak engellemiş gibi görünüyor. Lütfen birkaç dakika sonra tekrar dene.")
            elif "username" in error_msg and "not found" in error_msg:
                st.warning("❌ Girdiğin kullanıcı adı bulunamadı.")
            elif "login" in error_msg or "session" in error_msg:
                st.error("🔒 Bu işlem için giriş yapılması gerekiyor olabilir.")
            elif "403" in error_msg or "401" in error_msg:
                st.error("🚫 Yetkisiz işlem. Instagram'dan veri alınamıyor.")
            else:
                st.error("💥 Beklenmeyen bir hata oluştu. Lütfen tekrar dene ya da farklı bir kullanıcı adı gir.")