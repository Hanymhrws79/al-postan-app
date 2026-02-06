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
    # جلب مفتاح Gemini
    genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
    model = genai.GenerativeModel('gemini-pro')
    # جلب كلمة سر التطبيق
    MASTER_PASSWORD = st.secrets["APP_PASSWORD"]
except KeyError:
    st.error("⚠️ خطأ: لم يتم العثور على المفاتيح في إعدادات Secrets. يرجى إضافتها أولاً.")
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
            if user_pass == MASTER_PASSWORD:
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

    # 5. عرض النتائج والجداول
    if submit:
        if name and niche and competitors:
            with st.spinner('⏳ جاري استخراج البيانات وبناء الجداول...'):
                prompt = f"""
                أنت خبير تسويق رقمي. صمم تقرير لـ {name} في مجال {niche}.
                الجمهور: {audience} | الميزانية: {budget} | النبرة: {tone} | المنافسون: {competitors}

                اعرض النتائج في جداول Markdown:
                1. جدول تحليل المنافسين (المنافس، نقطة القوة، نقطة الضعف، خطة التفوق).
                2. جدول توزيع الميزانية الذكي (القناة، المبلغ، الهدف).
                3. جدول تقويم محتوى (7 أيام): (اليوم، الفكرة، المنصة، الهدف).
                
                قدم نصيحة ذهبية أخيرة. تحدث بالعربية.
                """
                
                try:
                    response = model.generate_content(prompt)
                    st.success(f"✅ تم تجهيز استراتيجية {name} بنجاح!")
                    st.markdown(response.text)
                    st.download_button("تحميل التقرير", response.text, file_name="strategy.txt")
                except Exception as e:
                    st.error(f"حدث خطأ: {e}")
        else:
            st.warning("⚠️ يرجى ملء الخانات الأساسية.")

    if st.sidebar.button("تسجيل الخروج"):
        st.session_state["authenticated"] = False
        st.rerun()

st.markdown("---")
st.caption("تم التطوير بواسطة البستان AI © 2026")
