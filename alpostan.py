import streamlit as st
import google.generativeai as genai

# 1. إعداد الاتصال بمفتاحك المجاني
try:
    genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
    # نستخدم Flash لأنه النسخة المجانية الأقوى حالياً
    model = genai.GenerativeModel('gemini-1.5-flash')
except Exception as e:
    st.error("تأكد من وضع المفتاح في Secrets")

# 2. واجهة التطبيق
st.set_page_config(page_title="البستان AI", page_icon="🌳")
st.title("🌳 منصة البستان AI")
st.subheader("مساعدك الذكي في التحليل التسويقي")

# 3. نظام الدخول
if "authenticated" not in st.session_state:
    st.session_state["authenticated"] = False

if not st.session_state["authenticated"]:
    user_pwd = st.text_input("أدخل كود التفعيل الخاص بك:", type="password")
    if st.button("دخول"):
        if user_pwd == str(st.secrets["APP_PASSWORD"]):
            st.session_state["authenticated"] = True
            st.rerun()
        else:
            st.error("الكود غير صحيح")
else:
    # 4. محرك التحليل
    with st.form("marketing_form"):
        name = st.text_input("اسم النشاط التجاري:")
        niche = st.text_input("مجال العمل:")
        submit = st.form_submit_button("🚀 ابدأ التحليل الذكي")

    if submit:
        if name and niche:
            with st.spinner("جاري التفكير وبناء الخطة..."):
                try:
                    prompt = f"أنت خبير تسويق. قدم 5 نصائح استراتيجية لـ {name} في مجال {niche} وجدول محتوى بسيط."
                    response = model.generate_content(prompt)
                    st.success("تم التحليل بنجاح!")
                    st.markdown(response.text)
                except Exception as e:
                    st.error(f"حدث خطأ: {e}")
        else:
            st.warning("يرجى كتابة الاسم والمجال")

    if st.sidebar.button("تسجيل الخروج"):
        st.session_state["authenticated"] = False
        st.rerun()

