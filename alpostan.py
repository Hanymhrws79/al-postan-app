import streamlit as st
import google.generativeai as genai

# 1. إعداد واجهة الصفحة
st.set_page_config(page_title="البستان AI - المساعد الذكي", layout="wide")

# تصميم اللوجو والهوية البصرية
st.markdown("""
    <style>
    .main-title {
        text-align: center; 
        background-color: #1b5e20; 
        padding: 20px; 
        border-radius: 15px;
        margin-bottom: 25px;
    }
    .main-title h1 { color: white; font-family: 'Cairo', sans-serif; margin: 0; }
    .main-title p { color: #c8e6c9; font-size: 1.1em; }
    </style>
    <div class="main-title">
        <h1>🌳 البستان AI</h1>
        <p>المنصة الذكية لتحليل المنافسين وبناء استراتيجيات التسويق</p>
    </div>
    """, unsafe_allow_html=True)

# 2. جلب المفاتيح السرية من الخزنة (Secrets)
try:
    genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
    # السطر 32 المعدل والمنضبط المسافات:
    model = genai.GenerativeModel('gemini-1.5-flash')
    MASTER_PASSWORD = st.secrets["APP_PASSWORD"]
except KeyError:
    st.error("⚠️ خطأ: لم يتم العثور على المفاتيح في إعدادات Secrets.")
    st.stop()

# 3. نظام التحقق من الهوية
if "authenticated" not in st.session_state:
    st.session_state["authenticated"] = False

if not st.session_state["authenticated"]:
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.subheader("🔐 تسجيل الدخول")
        user_pass = st.text_input("أدخل كود التفعيل الخاص بك:", type="password")
        if st.button("دخول النظام"):
            if user_pass == str(MASTER_PASSWORD):
                st.session_state["authenticated"] = True
                st.rerun()
            else:
                st.error("❌ الكود غير صحيح.")
else:
    # 4. القائمة الجانبية للمدخلات
    with st.sidebar:
        st.header("⚙️ بيانات الحملة")
        name = st.text_input("اسم النشاط التجاري:")
        niche = st.text_input("مجال العمل:")
        audience = st.text_input("الجمهور المستهدف:")
        competitors = st.text_area("المنافسون:")
        budget = st.number_input("الميزانية الشهرية ($):", min_value=0, value=500)
        tone = st.selectbox("نبرة الصوت:", ["احترافية", "مرحة", "حماسية", "تعليمية"])
        submit = st.button("🚀 تحليل وبناء الخطة")

    # 5. عرض النتائج
    if submit:
        if name and niche and competitors:
            with st.spinner('⏳ جاري التحليل...'):
                prompt = f"صمم تقرير تسويقي لـ {name} في مجال {niche}. الجمهور: {audience}. المنافسون: {competitors}. الميزانية: {budget}. النبرة: {tone}. اعرض النتائج في جداول Markdown."
                try:
                    response = model.generate_content(prompt)
                    st.success(f"✅ تم تجهيز استراتيجية {name}")
                    st.markdown(response.text)
                except Exception as e:
                    st.error(f"حدث خطأ: {e}")

    if st.sidebar.button("تسجيل الخروج"):
        st.session_state["authenticated"] = False
        st.rerun()
