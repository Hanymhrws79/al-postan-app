import streamlit as st
import google.generativeai as genai

st.set_page_config(page_title="البستان AI")

# محاولة الاتصال بمفتاح الـ API
try:
    genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
    
    # هنا التعديل الذكي: سنحاول تجربة كل الأسماء الممكنة حتى يعمل واحد منها
    model_names = ['gemini-1.5-flash-latest', 'gemini-1.5-flash', 'gemini-pro']
    model = None
    
    for name in model_names:
        try:
            model = genai.GenerativeModel(name)
            # تجربة وهمية للتأكد أن النموذج شغال
            test_res = model.generate_content("hi")
            break # إذا نجح، توقف عن البحث
        except:
            continue
            
    if model is None:
        st.error("عذراً، جميع نماذج جوجل غير متاحة حالياً في هذه النسخة.")
except Exception as e:
    st.error(f"خطأ في الإعدادات: {e}")

st.title("🌳 البستان AI")

# نظام الدخول البسيط
if "authenticated" not in st.session_state:
    st.session_state["authenticated"] = False

if not st.session_state["authenticated"]:
    pwd = st.text_input("كود التفعيل:", type="password")
    if st.button("دخول"):
        if pwd == str(st.secrets["APP_PASSWORD"]):
            st.session_state["authenticated"] = True
            st.rerun()
else:
    bus_name = st.text_input("اسم مشروعك:")
    if st.button("حلل الآن"):
        try:
            # استخدام أسلوب توليد يتماشى مع النسخ القديمة والجديدة
            response = model.generate_content(f"حلل تسويق {bus_name} باختصار")
            st.write(response.text)
        except Exception as e:
            st.error(f"حدث خطأ: {e}")
