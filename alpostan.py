import streamlit as st
import google.generativeai as genai

# 1. إعدادات الصفحة
st.set_page_config(page_title="البستان AI", layout="wide")

# 2. التأكد من المفاتيح
if "GEMINI_API_KEY" not in st.secrets:
    st.error("خطأ: مفتاح GEMINI_API_KEY غير موجود في Secrets")
    st.stop()

# 3. محاولة الاتصال (حل مشكلة الإصدارات)
genai.configure(api_key=st.secrets["GEMINI_API_KEY"])

# سنحاول تشغيل الموديل بأكثر من طريقة لضمان النجاح
try:
    # الطريقة الأولى: الاسم المباشر
    model = genai.GenerativeModel('gemini-1.5-flash')
except:
    try:
        # الطريقة الثانية: إضافة المسار
        model = genai.GenerativeModel('models/gemini-1.5-flash')
    except:
        # الطريقة الثالثة: الموديل القديم المستقر
        model = genai.GenerativeModel('gemini-pro')

# 4. واجهة المستخدم
st.title("🌳 منصة البستان AI")

if "auth" not in st.session_state:
    st.session_state["auth"] = False

if not st.session_state["auth"]:
    pwd = st.text_input("كود التفعيل:", type="password")
    if st.button("دخول"):
        if pwd == str(st.secrets["APP_PASSWORD"]):
            st.session_state["auth"] = True
            st.rerun()
else:
    name = st.text_input("اسم النشاط:")
    if st.button("تحليل الآن"):
        if name:
            with st.spinner("جاري التحليل..."):
                try:
                    # نستخدم توليد بسيط للتجربة
                    response = model.generate_content(f"اعطني نصيحة تسويقية لـ {name}")
                    st.write(response.text)
                except Exception as e:
                    st.error(f"خطأ في الـ API: {str(e)}")
        else:
            st.warning("ادخل الاسم")
