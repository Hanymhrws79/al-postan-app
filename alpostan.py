import streamlit as st
import google.generativeai as genai

# 1. إعدادات الصفحة
st.set_page_config(page_title="البستان AI", layout="wide")

# 2. تصميم الواجهة
st.markdown("""
<style>
.main-title {text-align: center; background-color: #1b5e20; padding: 20px; border-radius: 15px; margin-bottom: 25px;}
.main-title h1 {color: white; font-family: 'Cairo', sans-serif; margin: 0;}
</style>
<div class="main-title"><h1>🌳 منصة البستان AI</h1></div>
""", unsafe_allow_html=True)

# 3. جلب البيانات من Secrets
try:
    # إعداد مكتبة جوجل
    genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
    
    # --- التعديل الجذري هنا لحل خطأ 404 ---
    # نستخدم gemini-1.5-flash كنموذج افتراضي مستقر
    model = genai.GenerativeModel(model_name="gemini-1.5-flash")
    
    # كلمة السر
    MASTER_PASSWORD = str(st.secrets["APP_PASSWORD"])
except Exception as e:
    st.error("⚠️ تأكد من إعداد Secrets بشكل صحيح.")
    st.stop()

# 4. نظام تسجيل الدخول
if "auth" not in st.session_state:
    st.session_state["auth"] = False

if not st.session_state["auth"]:
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.subheader("🔐 دخول النظام")
        pwd = st.text_input("أدخل كود التفعيل:", type="password")
        if st.button("دخول"):
            if pwd == MASTER_PASSWORD:
                st.session_state["auth"] = True
                st.rerun()
            else:
                st.error("❌ الكود غير صحيح")
else:
    # 5. واجهة البرنامج الأساسية
    with st.sidebar:
        st.header("📊 بيانات المشروع")
        name = st.text_input("اسم النشاط التجاري:")
        niche = st.text_input("المجال:")
        comp = st.text_area("المنافسين (اكتب كل منافس في سطر):")
        submit_btn = st.button("🚀 تحليل الآن")
        
        if st.button("تسجيل الخروج"):
            st.session_state["auth"] = False
            st.rerun()

    if submit_btn:
        if name and niche and comp:
            with st.spinner("⏳ جاري التحليل..."):
                try:
                    prompt = f"حلل منافسين لـ {name} في مجال {niche}. المنافسين: {comp}. اعرض النتائج في جداول Markdown بالعربية."
                    
                    # طلب التوليد مع تحديد الإصدار المستقر داخلياً
                    response = model.generate_content(prompt)
                    
                    st.success(f"✅ تم التحليل بنجاح لـ {name}")
                    st.markdown(response.text)
                except Exception as e:
                    # إذا استمر الخطأ، سنعرض رسالة تفصيلية للمساعدة
                    st.error(f"خطأ في الاتصال: {e}")
                    st.info("نصيحة: تأكد من تحديث ملف requirements.txt إلى google-generativeai>=0.8.0")
        else:
            st.warning("⚠️ فضلاً أكمل جميع البيانات.")

st.markdown("---")
st.caption("برمجة وتطوير البستان AI © 2026")
