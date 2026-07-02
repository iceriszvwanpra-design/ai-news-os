import streamlit as st
import pandas as pd
import feedparser
import requests
import re
from datetime import datetime

# ==========================================
# 1. ตั้งค่าหน้าจอ (Dashboard Config)
# ==========================================
st.set_page_config(
    page_title="AI News OS - Master Edition", 
    page_icon="👑", 
    layout="wide"
)

# ==========================================
# 2. ระบบเครื่องยนต์หลังบ้าน (Core Engine)
# ==========================================
def clean_html_tags(raw_html):
    clean_text = re.sub(re.compile('<.*?>'), '', str(raw_html))
    return clean_text.strip()

def calculate_algorithm_score(title, desc, source):
    score = 40 
    text_to_analyze = f"{title} {desc}".lower()
    
    drama_keywords = ['ดราม่า', 'ทัวร์ลง', 'ชาวเน็ต', 'แฉ', 'เพจดัง', 'วิจารณ์', 'ฟาด', 'เดือด', 'ซัด', 'ถกสนั่น']
    for kw in drama_keywords:
        if kw in text_to_analyze: score += 12
        
    urgent_keywords = ['ด่วน', 'ล่าสุด', 'เปิดใจ', 'แถลง', 'ช็อก', 'ผวา', 'เตือนภัย', 'เสียชีวิต', 'อึ้ง']
    for kw in urgent_keywords:
        if kw in text_to_analyze: score += 10
        
    if "X (Twitter)" in source or "Facebook" in source: score += 15
    if "Google Trends" in source: score += 10
    
    return min(score, 99)

def generate_action_plan(title, desc):
    clean_title = re.sub(r'[^\w\s]', '', title)
    words = [w for w in clean_title.split() if len(w) >= 4] 
    main_kw = words[0] if words else "กระแสวันนี้"
    second_kw = words[1] if len(words) > 1 else "เรื่องเด่น"
    
    hook = f"🚨 สรุปดราม่าด่วน! {title[:45]}... ใครผิดใครถูก!?"
    
    caption = (
        f"เรื่องนี้กำลังเดือดทะลุปรอท! 🔥 ล่าสุดมีรายงานว่า {desc[:100]}...\n\n"
        f"งานนี้ชาวเน็ตแบ่งฝั่งเถียงกันยับ แล้วเพื่อนๆ ล่ะครับคิดเห็นยังไงกับเรื่องนี้? "
        f"คอมเมนต์คุยกันหน่อยครับ! 👇👇"
    )
    
    hashtags = f"#{main_kw} #{second_kw} #ดราม่าวันนี้ #สรุปข่าว #เล่าข่าวTikTok #เทรนด์วันนี้"
    
    return hook, caption, hashtags

# ==========================================
# 3. หน้าจอแสดงผล (User Interface)
# ==========================================
st.title("👑 AI News OS: The Ultimate Viral Aggregator")
st.markdown("ระบบศูนย์กลางสแกนกระแสข่าวไวรัลจาก **Google, X (Twitter) และ Facebook** จัดอันดับ Top 50 แบบเรียลไทม์")

if "master_news_data" not in st.session_state:
    st.session_state.master_news_data = []

if st.button("🚀 สแกนกระแสไวรัล 50 อันดับแบบเรียลไทม์ (Scan Now)", type="primary", use_container_width=True):
    with st.spinner("กำลังเจาะระบบดึงข้อมูลและประมวลผลอัลกอริทึม..."):
        raw_data = []
        headers = {'User-Agent': 'Mozilla/5.0'}
        
        feed_sources = {
            "🔴 Google Trends (เทรนด์ค้นหาด่วน)": "https://trends.google.com/trending/rss?geo=TH",
            "🐦 กระแสโซเชียล X (Twitter)": "https://rssfeeds.sanook.com/rss/feeds/sanook/news.social.xml",
            "🔵 ดราม่าเพจดัง Facebook": "https://www.thairath.co.th/rss/news/society",
            "🎭 วงการบันเทิง/ดารา": "https://www.thairath.co.th/rss/ent"
        }
        
        for source_name, url in feed_sources.items():
            try:
                res = requests.get(url, timeout=10, headers=headers)
                feed = feedparser.parse(res.content)
                for entry in feed.entries[:25]:
                    desc = clean_html_tags(entry.get("summary", entry.get("description", "")))
                    score = calculate_algorithm_score(entry.title, desc, source_name)
                    
                    raw_data.append({
                        "Viral Score": score,
                        "แพลตฟอร์ม": source_name,
                        "พาดหัวข่าว": entry.title,
                        "เนื้อหาโดยย่อ": desc,
                        "ลิงก์ต้นทาง": entry.link
                    })
            except:
                pass
                    
        sorted_data = sorted(raw_data, key=lambda x: x['Viral Score'], reverse=True)
        unique_data = []
        seen_titles = set()
        
        for item in sorted_data:
            if item['พาดหัวข่าว'] not in seen_titles:
                unique_data.append(item)
                seen_titles.add(item['พาดหัวข่าว'])
                
        st.session_state.master_news_data = unique_data[:50]
        st.success("✅ ดึงข้อมูลและจัดอันดับสำเร็จ!")

if st.session_state.master_news_data:
    df = pd.DataFrame(st.session_state.master_news_data)
    
    st.markdown("---")
    st.subheader("📊 ตารางคัดกรอง 50 อันดับความปัง (Top 50 Viral Ranking)")
    
    st.dataframe(
        df[["Viral Score", "แพลตฟอร์ม", "พาดหัวข่าว", "ลิงก์ต้นทาง"]],
        column_config={
            "Viral Score": st.column_config.ProgressColumn(
                "โอกาสดันฟีด (%)",
                format="%d",
                min_value=0,
                max_value=99,
            ),
            "ลิงก์ต้นทาง": st.column_config.LinkColumn("🔗 เปิดดูข่าวเต็ม")
        },
        use_container_width=True,
        height=450,
        hide_index=True
    )
    
    st.markdown("---")
    st.subheader("🎯 สตูดิโอสั่งการ (Content Blueprint)")
    
    news_options = [f"อันดับ {idx+1} | [Score: {item['Viral Score']}] {item['พาดหัวข่าว'][:60]}..." for idx, item in enumerate(st.session_state.master_news_data)]
    selected_idx = st.selectbox("📌 เลือกประเด็นไวรัลที่ต้องการให้ทีมงานนำไปผลิตคลิป:", range(len(news_options)), format_func=lambda x: news_options[x])
    selected_news = st.session_state.master_news_data[selected_idx]
    
    hook, caption, tags = generate_action_plan(selected_news['พาดหัวข่าว'], selected_news['เนื้อหาโดยย่อ'])
    
    col1, col2 = st.columns(2)
    with col1:
        st.error("🚨 1. พาดหัวหน้าคลิป (Hook)")
        st.code(hook, language="text")
        
        st.info("🖼️ 2. แหล่งข้อมูลประกอบคลิป")
        st.markdown(f"**ลิงก์หลักฐาน:** [ข่าวต้นฉบับ]({selected_news['ลิงก์ต้นทาง']})")
        
    with col2:
        st.success("💬 3. แคปชั่นเรียกยอดคอมเมนต์ (Caption)")
        st.code(caption, language="text")
        
        st.warning("🏷️ 4. ชุดแฮชแท็กดันฟีด (Hashtags)")
        st.code(tags, language="text")
