import streamlit as st

# --- إعدادات الصفحة الاحترافية ---
st.set_page_config(
    page_title="AL-POSTAN AI | Pro Marketing Suite",
    page_icon="🚀",
    layout="wide"
)

# --- نظام التحقق من الدخول (كلمة المرور) ---
def check_password():
    if "authenticated" not in st.session_state:
        st.session_state.authenticated = False

    if not st.session_state.authenticated:
        st.title("🔐 منطقة العملاء - AL-POSTAN AI")
        password = st.text_input("من فضلك أدخل كود التفعيل الخاص بك:", type="password")
        if st.button("دخول"):
            if password == "1234":  # يمكنك تغيير كلمة المرور هنا
                st.session_state.authenticated = True
                st.rerun()
            else:
                st.error("❌ كود التفعيل غير صحيح. تواصل مع الدعم لشرائه.")
        return False
    return True

if check_password():
    # --- واجهة البرنامج الرئيسية ---
    with st.sidebar:
        st.title("⚙️ الإعدادات")
        st.info("مرحباً بك في النسخة الاحترافية من مستشار البستان الذكي.")
        st.markdown("---")
        if st.button("تسجيل الخروج"):
            st.session_state.authenticated = False
            st.rerun()

    st.title("🚀 AL-POSTAN AI Marketing Pro")
    st.write("الأداة المتكاملة لتوليد الخطط التسويقية والمحتوى الإعلاني بضغطة زر.")
    st.markdown("---")

    # --- منطقة المدخلات ---
    col1, col2 = st.columns([1, 1], gap="large")

    with col1:
        st.markdown("### 📋 بيانات المنتج")
        product_name = st.text_input("اسم المنتج/الخدمة", placeholder="مثال: متجر البستان للعطور")
        pain_point = st.text_area("المشكلة التي تعالجها", placeholder="مثال: صعوبة العثور على عطور ثابتة وفخمة")
        value_prop = st.text_area("القيمة التي تقدمها", placeholder="مثال: ثبات يدوم 48 ساعة بزيوت أصلية")

    with col2:
        st.markdown("### 🎯 الجمهور والهدف")
        target_audience = st.text_input("الجمهور المستهدف", placeholder="مثال: العرسان، محبي الأناقة")
        competitor_analysis = st.text_area("لماذا يختارك العميل؟", placeholder="مثال: نستخدم زيوت فرنسية خام بأسعار تنافسية")
        desired_action = st.text_input("الإجراء المطلوب", placeholder="مثال: اطلب الآن عبر الواتساب")

    st.markdown("---")

    # --- معالجة النتائج ---
    if st.button("توليد الخطة التسويقية النهائية ✨", type="primary", use_container_width=True):
        if not all([product_name, pain_point, value_prop, target_audience, desired_action]):
            st.warning("⚠️ يرجى تعبئة كافة الحقول لضمان جودة الخطة.")
        else:
            # محاكاة التفكير والتحليل لإعطاء قيمة للمنتج
            progress_bar = st.progress(0)
            status_text = st.empty()
            
            for percent in range(0, 101, 20):
                status_text.text(f"جاري تحليل البيانات... {percent}%")
                progress_bar.progress(percent)
                import time
                time.sleep(0.3)
            
            st.balloons()
            st.success("🎉 تمت المهمة بنجاح! إليك مخرجاتك التسويقية:")

            # عرض النتائج في بطاقات (Containers)
            res_col1, res_col2 = st.columns(2)

            with res_col1:
                with st.expander("📈 الاستراتيجية المقترحة", expanded=True):
                    st.write(f"**خطة {product_name}**")
                    st.write(f"سنركز على استهداف {target_audience} من خلال إبراز {value_prop} كحل جذري لـ {pain_point}.")

            with res_col2:
                with st.expander("✉️ نص الإيميل التسويقي", expanded=True):
                    email_body = f"مرحباً، هل تعاني من {pain_point}؟\nنقدم لك {product_name} الذي يتميز بـ {competitor_analysis}.\n{desired_action} الآن!"
                    st.code(email_body, language="markdown")

            # قسم الأكواد الإعلانية (Copywriting)
            st.markdown("### ✍️ المحتوى الإعلاني (Social Media Copy)")
            tab1, tab2 = st.tabs(["نموذج P.A.S", "نموذج AIDA"])
            
            with tab1:
                content_pas = f"المشكلة: {pain_point}\nالحل: {product_name}\nالنتيجة: {value_prop}\nالأكشن: {desired_action}"
                st.code(content_pas)
            
            with tab2:
                content_aida = f"انتباه: للـ {target_audience} فقط!\nاهتمام: هل سمعت عن {product_name}؟\nرغبة: تمتع بـ {competitor_analysis}.\nفعل: {desired_action}"
                st.code(content_aida)

            # --- ميزة التحميل كملف ---
            full_plan = f"خطة تسويق: {product_name}\n\nالجمهور: {target_audience}\nالميزة: {value_prop}\nالإيميل المقترح:\n{email_body}"
            st.download_button(
                label="📥 تحميل الخطة كملف نصي (TXT)",
                data=full_plan,
                file_name=f"Marketing_Plan_{product_name}.txt",
                mime="text/plain"
            )

    # --- التذييل ---
    st.markdown("---")
    st.markdown("<center>جميع الحقوق محفوظة © 2024 لبرنامج AL-POSTAN AI</center>", unsafe_allow_html=True)