import streamlit as st
import math

CAMERA_DB = {
    "DJI Mavic 3 Enterprise (M3E)": {
        "focal_length": 24.0,       
        "sensor_width": 17.3,       
        "sensor_height": 13.0,      
        "pixel_width": 5280,        
        "pixel_height": 3956        
    },
    "DJI Phantom 4 RTK": {
        "focal_length": 8.8,        
        "sensor_width": 13.2,       
        "sensor_height": 8.8,       
        "pixel_width": 5472,        
        "pixel_height": 3648        
    },
    "DJI Zenmuse P1 (Matrice 350)": {
        "focal_length": 35.0,       
        "sensor_width": 35.9,       
        "sensor_height": 24.0,      
        "pixel_width": 8192,        
        "pixel_height": 5460        
    }
}

st.title("🛸 AI Flight Planner (Beta v2.0)")
st.write("تخطيط الطيران الجوي الذكي وحساب معايير السلامة")

st.header("⚙️ إعدادات المشروع والكاميرا")


camera_choice = st.selectbox("اختر نوع كاميرا الدرون:", list(CAMERA_DB.keys()))
cam = CAMERA_DB[camera_choice]

gsd = st.number_input("الدقة المطلوبة على الأرض GSD (سم/بكسل):", min_value=0.5, max_value=20.0, value=3.0)
p_overlap = st.slider("الـ Overlap الطولي (Sidelap) %:", 50, 90, 70)
q_overlap = st.slider("الـ Overlap العرضي (Frontlap) %:", 50, 90, 80)
wind_speed = st.number_input("سرعة الرياح الحالية في الموقع (كم/ساعة):", min_value=0.0, max_value=60.0, value=15.0)

st.subheader("🗺️ أبعاد المنطقة المراد رفعها")
area_width = st.number_input("عرض المنطقة (متر):", min_value=100, value=1000)
area_length = st.number_input("طول المنطقة (متر):", min_value=100, value=1000)

pixel_size_mm = cam["sensor_width"] / cam["pixel_width"]
gsd_m = gsd / 100.0
flight_altitude = (cam["focal_length"] * gsd_m) / pixel_size_mm

ground_w = (cam["sensor_width"] * flight_altitude) / cam["focal_length"]
ground_h = (cam["sensor_height"] * flight_altitude) / cam["focal_length"]

line_spacing = ground_w * (1 - (p_overlap / 100.0))

ai_safety_factor = 1.0
if wind_speed > 25.0:
    ai_safety_factor = 0.85  
    st.warning("⚠️ الرياح شديدة! الـ AI قام بتقليص المسافة بين اللقطات لضمان التغطية ومنع الفجوات.")

photo_spacing = ground_h * (1 - (q_overlap / 100.0)) * ai_safety_factor

num_lines = math.ceil(area_width / line_spacing)
photos_per_line = math.ceil(area_length / photo_spacing)
total_photos = num_lines * photos_per_line
camera_interval = 2.0  
max_safe_speed_ms = photo_spacing / camera_interval
max_safe_speed_kmh = max_safe_speed_ms * 3.6
st.header("📊 مخرجات خطة الطيران")
col1, col2 = st.columns(2)

with col1:
    st.metric("ارتفاع الطيران المناسب (H)", f"{flight_altitude:.2f} متر")
    st.metric("أبعاد الصورة على الأرض", f"{ground_w:.1f}م × {ground_h:.1f}م")
    st.metric("المسافة بين خطوط الطيران", f"{line_spacing:.2f} متر")

with col2:
    st.metric("إجمالي عدد خطوط الطيران", f"{num_lines} خطوط")
    st.metric("عدد الصور في الخط الواحد", f"{photos_per_line} صورة")
    st.metric("إجمالي الصور المطلوبة", f"{total_photos} صورة") 
    st.metric("السرعة القصوى الآمنة", f"{max_safe_speed_kmh:.2f} كم/ساعة")
st.header("💾 تصدير خطة الطيران")
def generate_kml(lines, spacing, length):
   
    kml_content = """<?xml version="1.0" encoding="UTF-8"?>
<kml xmlns="http://www.opengis.net/kml/2.2">
  <Document>
    <name>AI Flight Lines</name>
    <Style id="yellowLineGreenPoly">
      <LineStyle>
        <color>7f00ffff</color>
        <width>4</width>
      </LineStyle>
    </Style>
"""
 st.markdown("### 🌍 تحديد موقع منطقة الدراسة جغرافياً")
 user_lat = st.number_input("دائرة العرض (Latitude) - كمثال: 31.04", value=31.04, format="%.6f")
 user_lon = st.number_input("خط الطول (Longitude) - كمثال: 31.38", value=31.38, format="%.6f")

for i in range(lines):
    x_coord = i * spacing
    

    lon1 = user_lon + (x_coord / 111000)
    lat1 = user_lat
    
    lon2 = user_lon + (x_coord / 111000)
    lat2 = user_lat + (area_length / 111000)
    
    kml_content += f"""<Placemark>
<name>Line {i+1}</name>
<styleUrl>#yellowLineGreenPoly</styleUrl>
<LineString>
<coordinates>
{lon1},{lat1},0
{lon2},{lat2},0
</coordinates>
</LineString>
</Placemark>
"""
