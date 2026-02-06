import streamlit as st
import google.generativeai as genai

# إعداد الصفحة
st.set_page_config(page_title="البستان AI", layout="wide")

# دالة استدعاء الذكاء الاصطناعي بطريقة آمنة
def generate_ai_response(prompt):
    try:
        genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
        
        # محاولة استخدام 3 أسماء مختلفة للنموذج (لحل مشكلة 404)
        model_names = ['gemini-1.5-flash', 'gemini-1.5-flash-latest', 'gemini-pro']
        
        success = False
        for name in model_names:
            try:
                model = genai.GenerativeModel(name)
                response = model.generate_content(prompt)
                return response.text
            except:
                continue # إذا فشل هذا الاسم يجرب الذي يليه
        
        return "عذراً، لم أستطع الاتصال بالنماذج المتاحة حالياً. تأكد من صلاحية الـ API Key."
    except Exception as e:
        return f"حدث خطأ في النظام: {str(e)}"

# --- واجهة المستخدم ---
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
            st.error("الكود غير صحيح")
else:
    # التطبيق الأساسي
    with st.sidebar:
        st.header("إعدادات التحليل")
        biz_name = st.text_input("اسم النشاط:")
        biz_niche = st.text_input("المجال:")
        analyze = st.button("🚀 ابدأ التحليل")

    if analyze:
        if biz_name and biz_niche:
            with st.spinner("جاري التحليل باستخدام الذكاء الاصطناعي..."):
                full_prompt = f"أنت خبير تسويق، حلل مشروع {biz_name} في مجال {biz_niche} واعطني استراتيجية عمل وجدول محتوى."
                result = generate_ai_response(full_prompt)
                st.markdown("### 📊 نتائج التحليل:")
                st.write(result)
        else:
            st.warning("يرجى ملء البيانات")
