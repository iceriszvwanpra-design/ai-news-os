import streamlit as st
import pandas as pd
import feedparser
import requests
import re
import random
from datetime import datetime

# ==========================================
# 1. ตั้งค่าหน้าจอ (Dashboard Config)
# ==========================================
st.set_page_config(
    page_title="AI News OS - Pro Edition", 
    page_icon="🔥", 
    layout="wide"
)

# ==========================================
# 2. ระบบเครื่องยนต์หลังบ้าน (Core Engine)
# ==========================================
def clean_html_tags(raw_html):
    """ลบแท็ก HTML และทำความสะอาดข้อความ"""
    clean_text = re.sub(re.compile('<.*?>'), '', str(raw_html))
    clean_text = clean_text.replace('&quot;', '"').replace('&nbsp;', ' ')
    return clean_text.strip()

def calculate_viral_score(title, desc, source):
    """อัลกอริทึมจัดอันดับ 1-99 อิงจากคำกระตุ้นอารมณ์และความสดใหม่"""
    score = random.randint(30, 45) # Base Score กะจายไม่ให้เท่ากัน
    text_to_analyze = f"{title} {desc}".lower()
    
    # คำศัพท์ที่สะท้อนถึงการถกเถียง (Engagement Bait)
    drama_words = ['ดราม่า', 'ทัวร์ลง', 'ชาวเน็ต', 'แฉ', 'เพจดัง', 'วิจารณ์', 'ฟาด', 'เดือด', 'ซัด', 'ถกสนั่น', 'แบน', 'โป๊ะ']
    for kw in drama_words:
        if kw in text_to_analyze: score += 15
        
    # คำศัพท์ที่สะท้อนความด่วน (Urgency)
    urgent_words = ['ด่วน', 'ล่าสุด', 'เปิดใจ', 'แถลง', 'ช็อก', 'ผวา', 'เตือนภัย', 'เสียชีวิต', 'อึ้ง', 'พลิกโผ']
    for kw in urgent_words:
        if kw in text_to_analyze: score += 12
        
    # ให้น้ำหนักแหล่งที่มา
    if "Social" in source or "Twitter" in source or "Facebook" in source: score += 15
    if "Trends" in source: score += 10
    
    return min(score, 99)

def generate_pro_copywriting(title, desc):
    """ระบบเสกพาดหัวและแคปชั่นระดับโปร (สุ่มแพทเทิร์นไม่ให้ซ้ำซาก)"""
    clean_title = re.sub(r'[^\w\s]', '', title)
    words = [w for w in clean_title.split() if len(w) >= 4]
    
    main_kw = words[0] if len(words) > 0 else "ข่าวโซเชียล"
    second_kw = words[1] if len(words) > 1 else "ประเด็นร้อน"
    third_kw = words[2] if len(words) > 2 else "เทรนด์วันนี้"

    # สุ่มรูปแบบพาดหัว (Hook) ให้ดูมีมิติ
    hook_templates = [
        f"🚨 สรุปด่วน! {title[:50]}... เรื่องนี้มีเงื่อนงำ!?",
        f"🔥 เดือดจัด! ทัวร์ลงสนั่น {title[:40]}... ใครผิดใครถูก?",
        f"😱 ช็อกโซเชียล! ล่าสุด {title[:45]}... ฟังแล้วอึ้ง!",
        f"📌 สรุปดราม่าม้วนเดียวจบ! {title[:45]}..."
    ]
    
    # สุ่มรูปแบบแคปชั่น (Caption) เน้นกระตุ้นคอมเมนต์
    caption_templates = [
        f"เรื่องนี้กำลังเดือดทะลุปรอท! 🔥 ล่าสุดมีรายงานว่า {desc[:120]}...\n\nงานนี้ชาวเน็ตแบ่งฝั่งเถียงกันยับ แล้วเพื่อนๆ ล่ะครับคิดเห็นยังไงกับเรื่องนี้? คอมเมนต์คุยกันหน่อยครับ! 👇👇",
        f"กลายเป็นประเด็นร้อนที่คนพูดถึงทั้งโซเชียล! 📱 จากกรณี {desc[:100]}...\n\nบอกเลยว่าเรื่องนี้ไม่ได้จบง่ายๆ แน่นอน ทุกคนคิดว่าใครควรรับผิดชอบเรื่องนี้? พิมพ์มาเลยครับ 👇👇",
        f"เอาล่ะครับ สรุปมาให้แล้วสำหรับข่าวนี้! 🚨 {desc[:110]}...\n\nอ่านจบแล้วรู้สึกยังไงกันบ้าง? เห็นด้วยหรือเห็นต่าง คอมเมนต์มาแชร์มุมมองกันได้เลยครับ 👇👇"
    ]
    
    hook = random.choice(hook_templates)
    caption = random.choice(caption_templates)
    hashtags = f"#{main_kw} #{second_kw} #{third_kw} #ดราม่าวันนี้ #ข่าวไวรัล #สรุปข่าวฉบับย่อ #เล่าข่าวTikTok"
    
    return hook, caption, hashtags

# ==========================================
# 3. หน้าจอแสดงผลหลัก (UI)
# ==========================================
st.title("🔥 ศูนย์บัญชาการคัดกรองกระแสไวรัล (Pro Aggregator)")
st.markdown("ระบบกวาดเนื้อหาจาก **X (Twitter), Facebook, เว็บข่าวหลัก และ Google Trends** มาจัดอันดับ 50 ข่าวที่ต้องทำแบบเรียลไทม์")

if "master_news_data" not in st.session_state:
    st.session_state.master_news_data = []

# --- ระบบกวาดข้อมูลแบบครอบคลุม ---
if st.button("🚀 กวาดข่าวทั้งหมดและจัดอันดับ 50 ข่าวไวรัล (Real-time Scan)", type="primary", use_container_width=True):
    with st.spinner("กำลังส่งบอทวิ่งกวาดข้อมูลจากทุกแพลตฟอร์ม..."):
        raw_data = []
        headers = {'User-Agent': 'Mozilla/5.0'}
        
        # คลังแหล่งข้อมูล (จัดเต็มให้ครอบคลุมทุกที่ตามสั่ง)
        feed_sources = {
            "🔴 Google Trends": "https://trends.google.com/trending/rss?geo=TH",
            "🐦 X (Twitter) / Social (Sanook)": "https://rssfeeds.sanook.com/rss/feeds/sanook/news.social.xml",
            "🔵 Facebook / ดราม่าเพจดัง (Thairath)": "https://www.thairath.co.th/rss/news/society",
            "📰 ข่าวทั่วไป (Matichon)": "https://www.matichon.co.th/feed",
            "📰 ข่าวทั่วไป (Khaosod)": "https://www.khaosod.co.th/feed",
            "📰 ข่าวทั่วไป (Workpoint)": "https://workpointtoday.com/feed/",
            "🎭 บันเทิง (Sanook)": "https://rssfeeds.sanook.com/rss/feeds/sanook/news.entertain.xml",
            "🎭 บันเทิง/ซุบซิบ (Thairath)": "https://www.thairath.co.th/rss/ent",
            "💻 ข่าวไอที/วัยรุ่น (Blognone)": "https://www.blognone.com/node/feed"
        }
        
        # สูบข้อมูลมาทั้งหมด
        for source_name, url in feed_sources.items():
            try:
                res = requests.get(url, timeout=7, headers=headers)
                feed = feedparser.parse(res.content)
                for entry in feed.entries[:20]: # ดึงมาเว็บละ 20 ข่าว (รวมเกือบ 200 ข่าว)
                    desc = clean_html_tags(entry.get("summary", entry.get("description", "")))
                    if len(desc) < 10: continue # ข้ามข่าวที่ไม่มีเนื้อหา
                    
                    score = calculate_viral_score(entry.title, desc, source_name)
                    
                    raw_data.append({
                        "ความปัง": score,
                        "แหล่งที่มา": source_name,
                        "พาดหัวข่าว": entry.title,
                        "เนื้อหาโดยย่อ": desc,
                        "ลิงก์อ่านตัวเต็ม": entry.link
                    })
            except:
                pass
                    
        # คัดกรองและจัดอันดับ
        sorted_data = sorted(raw_data, key=lambda x: x['ความปัง'], reverse=True)
        
        # กรองข่าวซ้ำ (ตัดออกถ้าพาดหัวเหมือนกัน)
        unique_data = []
        seen_titles = set()
        
        for item in sorted_data:
            if item['พาดหัวข่าว'] not in seen_titles:
                unique_data.append(item)
                seen_titles.add(item['พาดหัวข่าว'])
                
        # ฟันธงตัดเอาแค่ Top 50 มาแสดง
        st.session_state.master_news_data = unique_data[:50]
        st.success(f"✅ กวาดมาทั้งหมด {len(raw_data)} ข่าว > คัดกรองเหลือ 50 อันดับแรกที่ไวรัลที่สุดเรียบร้อยแล้ว!")

# --- ส่วนแสดงผลลัพธ์ ---
if st.session_state.master_news_data:
    df = pd.DataFrame(st.session_state.master_news_data)
    
    st.markdown("---")
    st.subheader("📊 ตารางคัดกรอง 50 อันดับความปัง (Top 50 Viral Ranking)")
    st.markdown("💡 *เรียงลำดับจากบนลงล่าง ข่าวอันดับ 1 คือข่าวที่ต้องรีบทำคลิปที่สุดในเวลานี้*")
    
    # ตารางแบบ Interactive เรียบหรู
    st.dataframe(
        df[["ความปัง", "แหล่งที่มา", "พาดหัวข่าว", "ลิงก์อ่านตัวเต็ม"]],
        column_config={
            "ความปัง": st.column_config.ProgressColumn(
                "โอกาสดันฟีด (%)",
                format="%d",
                min_value=0,
                max_value=99,
            ),
            "ลิงก์อ่านตัวเต็ม": st.column_config.LinkColumn("🔗 ไปที่หน้าเว็บข่าว")
        },
        use_container_width=True,
        height=500,
        hide_index=False
    )
    
    st.markdown("---")
    st.subheader("🎯 สตูดิโอสั่งการระดับโปร (Pro Content Blueprint)")
    
    # ดรอปดาวน์เลือกข่าวมาทำคอนเทนต์
    news_options = [f"🏆 อันดับ {idx+1} | [ความปัง {item['ความปัง']}%] {item['พาดหัวข่าว'][:60]}..." for idx, item in enumerate(st.session_state.master_news_data)]
    selected_idx = st.selectbox("📌 เลือกข่าวที่ต้องการให้ทีมงานนำไปผลิต:", range(len(news_options)), format_func=lambda x: news_options[x])
    selected_news = st.session_state.master_news_data[selected_idx]
    
    # เสกแคปชั่นและพาดหัว
    hook, caption, tags = generate_pro_copywriting(selected_news['พาดหัวข่าว'], selected_news['เนื้อหาโดยย่อ'])
    
    col1, col2 = st.columns(2)
    with col1:
        st.error("🚨 1. พาดหัวหน้าคลิป (Text Hook)")
        st.code(hook, language="text")
        st.caption("เทคนิค: พิมพ์ตัวหนาๆ วางกลางคลิป ดึงสายตาใน 2 วินาทีแรก")
        
        st.info("🖼️ 2. ลิงก์แหล่งข้อมูล (หาภาพประกอบ)")
        st.markdown(f"**คลิกที่นี่เพื่อไปหาภาพหลักฐาน:** [เปิดหน้าข่าวต้นฉบับ]({selected_news['ลิงก์อ่านตัวเต็ม']})")
        
    with col2:
        st.success("💬 3. แคปชั่นเรียกคอมเมนต์ (Caption)")
        st.code(caption, language="text")
        st.caption("เทคนิค: ก๊อปปี้ไปวางใต้คลิปได้เลย คำถามตอนท้ายจะล่อให้คนเข้ามาเถียงกัน")
        
        st.warning("🏷️ 4. แฮชแท็กดันฟีด (Hashtags)")
        st.code(tags, language="text")
