import streamlit as st
import math

st.title("🛸 نظام تخطيط الطيران الذكي (AI Flight Planner)")
st.subheader("تطوير م/ أحمد حسين - أتمتة حسابات المساحة الجوية")

st.markdown("---")
col1, col2 = st.columns(2)

with col1:
    st.header("⚙️ مدخلات المشروع")
    project_width = st.number_input("عرض منطقة المشروع (متر)", value=1000)
    project_length = st.number_input("طول منطقة المشروع (متر)", value=2000)
    image_width = st.number_input("عرض الصورة على الأرض W (متر)", value=150)
    image_height = st.number_input("طول الصورة على الأرض H (متر)", value=100)

with col2:
    st.header("💨 ظروف الطيران والطقس")
    sidelap = st.slider("نسبة التداخل الجانبي (%)", min_value=10, max_value=90, value=60)
    overlap = st.slider("نسبة التداخل الطولي (%)", min_value=10, max_value=90, value=70)
    aircraft_speed = st.number_input("سرعة الطائرة (متر/ثانية)", value=12)
    wind_speed = st.slider("سرعة الرياح الحالية (عقدة)", min_value=0, max_value=40, value=18)

st.markdown("---")
if wind_speed > 15:
    safety_margin_photos = 6
    st.error(f"⚠️ تحذير: سرعة الرياح ({wind_speed} عقدة) مرتفعة! تم رفع هامش الأمان تلقائياً لـ {safety_margin_photos} صور لضمان التغطية ومنع الفجوات.")
else:
    safety_margin_photos = 4
    st.success(f"✅ الطقس مستقر: سرعة الرياح ({wind_speed} عقدة) آمنة. تم استخدام هامش الأمان القياسي ({safety_margin_photos} صور).")
SP = image_width * (100 - sidelap) / 100
NFL = math.ceil((project_width / SP) + 1)
B = image_height * (100 - overlap) / 100
NIM = math.ceil((project_length / B) + 1 + safety_margin_photos)
total_images = NFL * NIM
time_interval = B / aircraft_speed
st.header("📌 مخرجات خطة الطيران الفعالة")

res_col1, res_col2 = st.columns(2)
with res_col1:
    st.metric("التباعد بين خطوط الطيران (SP)", f"{SP} متر")
    st.metric("عدد خطوط الطيران الفعلي (NFL)", f"{NFL} خطوط")
    st.metric("القاعدة الجوية (B)", f"{B} متر")

with res_col2:
    st.metric("عدد الصور في الخط الواحد (NIM)", f"{NIM} صور")
    st.metric("إجمالي صور المشروع بالكامل", f"{total_images} صورة")
    st.metric("تظبيط تايمر الكاميرا تلقائياً", f"كل {time_interval} ثانية")