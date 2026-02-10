import streamlit as st
import pandas as pd
import random
import urllib.parse

# --- إعدادات الصفحة ---
st.set_page_config(
    page_title="AL-POSTAN AI Marketing Suite",
    page_icon="🚀",
    layout="wide"
)

# --- تنسيق التصميم (CSS) ---
st.markdown("""
    <style>
    .main { background-color: #f8f9fa; }
    .stButton>button { width: 100%; border-radius: 8px; height: 3em; background-color: #27ae60; color: white; font-weight: bold; }
    .whatsapp-btn {
        display: inline-block;
        padding: 0.75em 1.25em;
        background-color: #25D366;
        color: white;
        text-align: center;
        text-decoration: none;
        border-radius: 8px;
        font-weight: bold;
        width: 100%;
    }
    </style>
    """, unsafe_allow_html=True)

# --- العنوان الرئيسي ---
st.title("💡 منظومة AL-POSTAN للتسويق الذكي")
st.markdown("🛠️ *الإصدار المطور v2.0 - معالجة ذكية للبيانات*")
st.divider()

# --- القائمة الجانبية (Sidebar) ---
with st.sidebar:
    st.image("https://cdn-icons-png.flaticon.com/512/1998/1998087.png", width=100)
    st.header("📲 بيانات العميل")
    client_phone = st.text_input("رقم واتساب العميل", placeholder="2010XXXXXXXX")
    st.caption("أدخل الرقم بالصيغة الدولية بدون (+) أو أصفار إضافية")
    st.divider()
    st.info("هذا الإصدار يدعم الإرسال من المتصفح مباشرة (Cloud Friendly)")

# --- التبويبات ---
tab1, tab2, tab3, tab4 = st.tabs([
    "📊 تحليل السوق", "✍️ توليد المحتوى", "🎨 التصميم المرئي", "📅 جدول الـ 30 يوماً"
])

with tab1:
    col1, col2 = st.columns(2)
    with col1:
        prod_name = st.text_input("اسم المنتج أو الخدمة", value="برنامج كاشير البستان")
        pain_point = st.text_area("ألم العميل", value="صعوبة حساب الأرباح وضياع الفواتير")
    with col2:
        target_group = st.text_input("الجمهور المستهدف", value="أصحاب السوبر ماركت")
        competitor_flaw = st.text_area("نقاط ضعف المنافسين", value="دعم فني بطيء وأسعار مرتفعة")

with tab2:
    col3, col4 = st.columns(2)
    with col3:
        advantage = st.text_input("ميزتك الكبرى", value="دعم فني 24 ساعة وربط بالموبايل")
    with col4:
        offer = st.text_input("العرض الخاص", value="خصم 25% وتركيب مجاني")

with tab3:
    visual_style = st.selectbox("نمط الصور", ["Photorealistic", "3D Render", "Flat Design", "Cinematic"])

with tab4:
    generate_calendar = st.checkbox("توليد جدول 30 يوماً", value=True)

# --- معالجة البيانات ---
if st.button("توليد المنظومة التسويقية الكاملة ✨"):
    if not prod_name or not pain_point:
        st.error("⚠️ يرجى تعبئة البيانات الأساسية أولاً.")
    else:
        # 1. بناء التقرير
        report_text = f"""🚀 خطة تسويق: {prod_name}
----------------------------------
🎯 الجمهور: {target_group}
❌ المشكلة: {pain_point}
⚔️ ميزتنا: {advantage}
🔥 العرض: {offer}

📢 إعلان مقترح:
هل تعبت من {pain_point}؟ مع {prod_name} وفرنا لك {advantage}. اطلب الآن واحصل على {offer}!
----------------------------------
🎨 وصف الـ AI:
Digital art of {target_group} using {prod_name}, solving {pain_point}, style: {visual_style}, 8k resolution.
"""
        
        # 2. توليد الجدول كبيانات منظمة
        content_types = [
            "💡 تعليمي: كيف تتغلب على {pain}؟",
            "🎯 بيعي: لماذا {prod} هو الأفضل لـ {target}؟",
            "❓ تفاعلي: ما هي أكبر عقبة تواجهك؟",
            "🌟 نجاح: قصة عميل مع {prod}",
            "🎁 عرض: {offer} لفترة محدودة"
        ]
        
        calendar_data = []
        full_calendar_text = "\n📅 جدول المحتوى:\n"
        for i in range(1, 31):
            idea = random.choice(content_types).format(pain=pain_point, prod=prod_name, offer=offer, target=target_group)
            calendar_data.append({"اليوم": f"يوم {i}", "الفكرة المقترحة": idea})
            full_calendar_text += f"{i}. {idea}\n"

        # تخزين في session_state
        st.session_state['report'] = report_text + full_calendar_text
        st.session_state['df'] = pd.DataFrame(calendar_data)

        # عرض النتائج
        st.success("✅ تم التجهيز بنجاح")
        st.markdown(f"```\n{report_text}\n```")
        
        if generate_calendar:
            with st.expander("📅 عرض جدول الـ 30 يوماً"):
                st.table(st.session_state['df'])

# --- أدوات التصدير ---
if 'report' in st.session_state:
    st.divider()
    c1, c2 = st.columns(2)
    
    with c1:
        # تحميل الملف
        st.download_button(
            label="📥 تحميل الخطة (Text)",
            data=st.session_state['report'],
            file_name="marketing_plan.txt",
            mime="text/plain"
        )
    
    with c2:
        # إرسال واتساب عبر رابط مباشر (يعمل في كل مكان)
        if client_phone:
            encoded_text = urllib.parse.quote(st.session_state['report'])
            whatsapp_url = f"https://wa.me/{client_phone}?text={encoded_text}"
            st.markdown(f'<a href="{whatsapp_url}" target="_blank" class="whatsapp-btn">📲 إرسال للعميل عبر واتساب</a>', unsafe_allow_html=True)
        else:
            st.warning("أدخل رقم الهاتف لتفعيل زر الواتساب")
