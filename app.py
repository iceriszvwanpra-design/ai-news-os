import streamlit as st
import pandas as pd
import feedparser
import requests
import re

st.set_page_config(page_title="AI News OS v4.0 Ultra Viral", page_icon="🚀", layout="wide")

# ระบบแบ่งเมนูสำหรับบริษัทสเกลใหญ่
menu = st.sidebar.radio("🏢 ศูนย์ควบคุมความไวรัล", ["🔥 กวาดเทรนด์เดือด Google Trends", "🎨 คัมภีร์ลับ & เทมเพลต 1,000,000 วิ"])

if "viral_trends" not in st.session_state:
    st.session_state.viral_trends = []

if menu == "🔥 กวาดเทรนด์เดือด Google Trends":
    st.title("🚀 AI News OS v4.0 - เครื่องจักรกวาดเทรนด์ระเบิดวิว")
    st.write("ระบบดักจับคีย์เวิร์ดที่คนไทยกำลังคลั่งสูงสุด เพื่อทำคลิปดักหน้าอัลกอริทึม")
    
    if st.button("📡 เจาะระบบ Google Trends ประเทศไทยด่วนที่สุด"):
        with st.spinner("กำลังเจาะข้อมูลคีย์เวิร์ดไวรัล..."):
            # ดึงข้อมูลเทรนด์สดของประเทศไทย
            url = "https://trends.google.com/trending/rss?geo=TH"
            try:
                response = requests.get(url, timeout=10, headers={'User-Agent': 'Mozilla/5.0'})
                feed = feedparser.parse(response.content)
                
                all_trends = []
                if feed.entries:
                    for idx, entry in enumerate(feed.entries):
                        # ดึงจำนวนการค้นหาจาก tag พิเศษของ google trends
                        search_count = entry.get("ht_approx_pvalues", "5,000+ การค้นหา")
                        # ล้างคำอธิบาย
                        desc = entry.get("summary", entry.get("description", ""))
                        clean_desc = re.sub(re.compile('<.*?>'), '', desc).strip()
                        
                        all_trends.append({
                            "อันดับเทรนด์": idx + 1,
                            "คีย์เวิร์ด/ประเด็นร้อน": entry.title,
                            "ความแรง (จำนวนค้นหา)": search_count,
                            "สรุปเนื้อหาเบื้องต้น": clean_desc if clean_desc else "กระแสกำลังพุ่งแรง รีบหยิบไปทำคอนเทนต์",
                            "ลิงก์เจาะลึก": entry.link
                        })
                st.session_state.viral_trends = all_trends
                st.success(f"💥 กวาดเทรนด์สำเร็จ! พบคีย์เวิร์ดระดับไวรัล {len(st.session_state.viral_trends)} ประเด็น")
            except Exception as e:
                st.error(f"เกิดข้อผิดพลาดในการเชื่อมต่อ: {str(e)}")

    if st.session_state.viral_trends:
        df = pd.DataFrame(st.session_state.viral_trends)
        
        st.subheader("📰 เลือกคีย์เวิร์ดเด่น เพื่อเสกสคริปต์สะกดจิตคนดู")
        
        # กล่องเลือกคีย์เวิร์ด
        trend_titles = [f"อันดับ {item['อันดับเทรนด์']} | {item['คีย์เวิร์ด/ประเด็นร้อน']} ({item['ความแรง (จำนวนค้นหา)']})" for item in st.session_state.viral_trends]
        selected_index = st.selectbox("🎯 เลือกประเด็นที่คิดว่าแซ่บที่สุด:", range(len(trend_titles)), format_func=lambda x: trend_titles[x])
        selected_item = st.session_state.viral_trends[selected_index]
        
        # แผงโครงสร้างบริษัท จ่ายงานพนักงาน
        st.markdown("### 👥 แผงสั่งการทีมงานหลังบ้าน")
        col1, col2, col3 = st.columns(3)
        with col1:
            st.selectbox("👤 มอบหมายทีม Creative:", ["ทีมค้นหา 1", "ทีมค้นหา 2", "ตัวพี่เอง"])
        with col2:
            st.selectbox("🎬 ส่งต่อทีม Editor ตัดต่อ:", ["มือตัด TikTok 1", "มือตัด TikTok 2", "ทีมตัดขยี้ดราม่า"])
        with col3:
            st.selectbox("📊 เป้าหมายยอดวิวคลิปนี้:", ["🔥 100,000+ (ไวรัลกลาง)", "🚀 1,000,000+ (ทลายฟีด)"])
            
        # สูตรลับสคริปต์ไวรัลเวอร์ชันจิตวิทยา
        st.subheader("🎬 สคริปต์จิตวิทยาขยี้ใจ (สำหรับโยนใส่ CapCut พากย์เสียง AI)")
        
        keyword = selected_item['คีย์เวิร์ด/ประเด็นร้อน']
        st.warning(f"💡 **คีย์เวิร์ดต้องห้ามถอดออก:** คำว่า **'{keyword}'** ต้องขึ้นเป็นตัวหนังสือตัวใหญ่ ๆ ตั้งแต่วินาทีแรก ห้ามพิมพ์ผิดเด็ดขาด!")
        
        hook_text = f"\"อย่าเพิ่งเลื่อนผ่าน! ถ้าคุณยังไม่รู้เรื่อง {keyword} ที่ตอนนี้กำลังเดือดทะลุปรอท! คนไทยค้นหากันเป็นแสนครั้งในไม่กี่ชั่วโมง!\""
        body_text = f"\"ชนวนเหตุมาจากเรื่องนี้เลย... เพราะ {selected_item['สรุปเนื้อหาเบื้องต้น'][:100]}... ซึ่งเรื่องนี้มีเงื่อนงำที่หลายคนยังไม่รู้ และกำลังทัวร์ลงยับ\""
        cta_text = f"\"คิดว่าเรื่อง {keyword} นี้ ใครผิดใครถูก? คอมเมนต์ถกกันด้านล่างด่วน ๆ และกดติดตามช่องนี้ไว้เลย!\""
        
        st.markdown(f"""
        | ส่วนของคลิป | บทพูดสำหรับ AI พากย์เสียง | อารมณ์ซาวด์ / เอฟเฟกต์ | เทคนิคการตัดต่อระดับองค์กรใหญ่ |
        | :--- | :--- | :--- | :--- |
        | **1. Stop Scroller (0-3 วิ)** | {hook_text} | เสียงเอฟเฟกต์เบสกระแทก (**Sub Bass Drop**) + เสียงซาวด์กระซิบ | ขึ้นภาพเบลอ ๆ แซ่บ ๆ และกระแทกตัวหนังสือสีแดง/เหลือง ขยับตามเสียงพูด |
        | **2. ขยี้ประเด็น (4-20 วิ)** | {body_text} | เพลงแนวลึกลับ สืบสวน (**Aggressive Phonk / Cyberpunk**) | ตัดสลับหน้าจอแชต หน้าคอมเมนต์ หรือรูปคนในข่าวทุก ๆ 1.2 วินาที (ห้ามแช่ภาพเด็ดขาด) |
        | **3. ล่อคอมเมนต์ (21-30 วิ)** | {cta_text} | เสียงเอฟเฟกต์แผ่นเสียงสะดุด (**Vinyl Scratch**) แล้วตัดเงียบ | ขึ้นลูกศรกะพริบชี้ไปที่ปุ่มคอมเมนต์ บีบให้คนดูพิมพ์เปิดสงครามคีย์บอร์ดเพื่อดันฟีด |
        """)
        
        st.subheader("📊 ตารางอันดับความแรงเทรนด์ทั้งหมดในประเทศไทย")
        st.dataframe(df.set_index("อันดับเทรนด์"), use_container_width=True, height=400)

elif menu == "🎨 คัมภีร์ลับ & เทมเพลต 1,000,000 วิ":
    st.title("🎨 ระบบโรงงานคอนเทนต์: มาตรฐานสากลเพื่อยอดวิวหลักล้าน")
    st.write("ให้พนักงานทุกคนอ่านและทำตามหน้านี้อย่างเคร่งครัด หากคลิปไหนยอดวิวต่ำกว่าหมื่น ให้กลับมาเช็กที่นี่")
    
    st.markdown("""
    ### ⚡ สูตรลับในการดักจับอัลกอริทึม (TikTok/Reels Engine Optimization)
    1. **กฎ 2 วินาทีแรก (The Hook):** ต้องเปิดด้วยประโยคคำถาม หรือคำเตือนที่ทำให้คนรู้สึกว่า 'ถ้าเลื่อนผ่านจะคุยกับเขาไม่รู้เรื่อง'
    2. **สร้างสงครามคอมเมนต์ (Engagement Bait):** อัลกอริทึมจะดันคลิปที่มีคนคอมเมนต์เถียงกันยาวที่สุด ยิ่งพนักงานเขียนบทชวนให้คนคิดต่างได้ ยอดวิวจะพุ่งเป็นล้านในข้ามคืน
    3. **ความถี่ในการอัปโหลด:** แนะนำให้ปล่อยเป็นรอบ ทุก ๆ 2 ชั่วโมง (เช่น 10:00, 12:00, 14:00) เพื่อให้อัลกอริทึมกินพื้นที่ฟีดตลอดทั้งวัน
    
    ### 📂 คลังเครื่องมือที่พนักงานต้องดึงไปใช้ (Brand Assets)
    * 🎨 **สไตล์ฟอนต์บริษัท:** ฟอนต์ตัวหนาขอบดำ พื้นหลังสติกเกอร์สีเหลือง (สะดุดตาคนสายตาสั้น)
    * 🔊 **คลังเสียง Sound Effect:** เสียงเตือนเฟซบุ๊ก, เสียงเอฟเฟกต์ตบมุก, เสียงซาวด์ระทึกขวัญ
    * 🤖 **การตั้งค่าเสียงพากย์ AI:** ใช้ความเร็วระดับ `1.1x` เสมอ ห้ามใช้ความเร็วปกติ เพราะคนยุคนี้ชอบฟังอะไรสปีดเร็ว ๆ
    """)
    import streamlit as st
import pandas as pd
import feedparser
import requests
import re
import random

st.set_page_config(page_title="AI Viral Predictor v6.0", page_icon="🧠", layout="wide")

st.title("🧠 AI Algorithm Predictor v6.0 - ระบบจำลองสมองกลดันฟีด")
st.write("วิเคราะห์และให้ 'คะแนนความไวรัล' ตามเกณฑ์ที่ TikTok และ Reels ชอบดันขึ้นฟีด")

# --- เครื่องยนต์ประเมินความไวรัลจำลอง ---
def calculate_viral_score(title, description):
    score = 40 # คะแนนพื้นฐาน
    
    # 1. Trigger Words (คำกระตุ้นอารมณ์) - ยิ่งมีเยอะ อัลกอริทึมยิ่งชอบ
    high_impact_words = ['ดราม่า', 'แฉ', 'เดือด', 'ทัวร์ลง', 'ช็อก', 'ผวา', 'ด่วน', 'ล่าสุด', 'เตือนภัย', 'เลิก', 'เสียชีวิต']
    medium_impact_words = ['เปิดใจ', 'ชาวเน็ต', 'วิจารณ์', 'แห่', 'หลุด', 'อึ้ง', 'ไวรัล', 'ซัด']
    
    text_to_check = str(title) + " " + str(description)
    
    for word in high_impact_words:
        if word in text_to_check: score += 15
    for word in medium_impact_words:
        if word in text_to_check: score += 8
        
    # สุ่มเพิ่มความผันผวนเล็กน้อยให้ดูเป็นธรรมชาติ
    score += random.randint(-5, 10)
    
    # ล็อกเพดานคะแนน
    if score > 99: score = 99
    if score < 20: score = random.randint(20, 35)
    
    return score

def get_viral_tier(score):
    if score >= 85: return "🔥 ระเบิดฟีด (ดันแน่นอน)"
    elif score >= 70: return "⚡ มีโอกาสแมสสูง"
    else: return "📉 ข่าวทั่วไป (ข้ามได้เลย)"

if "scored_trends" not in st.session_state:
    st.session_state.scored_trends = []

if st.button("🔮 สแกนกระแสโซเชียล และให้ระบบประเมินความไวรัล"):
    with st.spinner("ระบบกำลังจำลองอัลกอริทึม และคำนวณ Viral Score..."):
        all_data = []
        headers = {'User-Agent': 'Mozilla/5.0'}
        
        sources = {
            "🔴 กระแสสังคม/การค้นหา": "https://www.thairath.co.th/rss/news/society",
            "🐦 ดราม่าวงการบันเทิง": "https://www.thairath.co.th/rss/ent",
            "🌐 ไวรัลโซเชียล": "https://rssfeeds.sanook.com/rss/feeds/sanook/news.social.xml"
        }
        
        for source_name, url in sources.items():
            try:
                res = requests.get(url, timeout=10, headers=headers)
                feed = feedparser.parse(res.content)
                for entry in feed.entries[:12]:
                    desc = entry.get("summary", entry.get("description", ""))
                    clean_desc = re.sub(re.compile('<.*?>'), '', desc).strip()
                    
                    # ส่งเข้าเครื่องยนต์คิดคะแนน
                    v_score = calculate_viral_score(entry.title, clean_desc)
                    tier = get_viral_tier(v_score)
                    
                    all_data.append({
                        "Viral Score": v_score,
                        "สถานะดันฟีด": tier,
                        "หมวดหมู่": source_name,
                        "หัวข้อที่เป็นประเด็น": entry.title,
                        "เนื้อหาเบื้องต้น": clean_desc[:100] + "..."
                    })
            except: pass
            
        # จัดเรียงจากคะแนนมากไปน้อย (เอาตัวท็อปไว้บนสุด)
        sorted_data = sorted(all_data, key=lambda x: x['Viral Score'], reverse=True)
        st.session_state.scored_trends = sorted_data
        st.success("คำนวณเสร็จสิ้น! คัดกรองจากข่าวทั้งหมด เหลือเฉพาะตัวที่อัลกอริทึมน่าจะชอบที่สุด")

if st.session_state.scored_trends:
    df = pd.DataFrame(st.session_state.scored_trends)
    
    st.subheader("📊 ตารางคัดกรอง: เรียงลำดับตามโอกาสไวรัล (Viral Potential)")
    # แสดงตารางแบบเน้นคะแนน
    st.dataframe(
        df.style.background_gradient(subset=['Viral Score'], cmap='Reds'),
        use_container_width=True, 
        height=400
    )
    
    st.markdown("---")
    st.subheader("🎯 เลือกประเด็นระดับ 'ระเบิดฟีด' ไปสั่งงานทีม")
    
    # กรองมาเฉพาะตัวท็อปให้เลือก
    top_items = [item for item in st.session_state.scored_trends if item['Viral Score'] >= 70]
    if top_items:
        titles = [f"[{item['Viral Score']}%] {item['หัวข้อที่เป็นประเด็น']}" for item in top_items]
        selected_index = st.selectbox("เลือกประเด็นที่คะแนนสูงที่สุด:", range(len(titles)), format_func=lambda x: titles[x])
        selected_item = top_items[selected_index]
        
        st.info(f"**เหตุผลที่ระบบคิดว่าเรื่องนี้จะปัง:** เพราะมีคีย์เวิร์ดที่กระตุ้นให้เกิดคอมเมนต์ และเป็นกระแสสังคมที่คนอยากรู้ตอนจบ (คะแนนประเมิน: {selected_item['Viral Score']}%)")
    else:
        st.warning("ตอนนี้ไม่มีประเด็นไหนแรงพอที่จะเสี่ยงทำคลิปครับ แนะนำให้รอกวาดใหม่ในอีก 2 ชั่วโมง")
        import streamlit as st
import pandas as pd
import feedparser
import requests
import re
from datetime import datetime

st.set_page_config(page_title="AI News OS v7.0 Ultimate", page_icon="👑", layout="wide")

st.title("👑 ศูนย์บัญชาการคัดกรองกระแสไวรัล (Top 50 Real-Time)")
st.markdown("ระบบดูดข้อมูลจากทุกแหล่ง (โซเชียล, ข่าวหลัก, เทรนด์) แล้วจัดอันดับความสำคัญในการทำคลิป พร้อมสูตรพาดหัวและแคปชั่น")

def calculate_priority_score(title, desc, source_name):
    score = 50 # Base score
    text = str(title).lower() + " " + str(desc).lower()
    
    # คำศัพท์ที่สะท้อนว่ามาจากดราม่าโซเชียล (X, Facebook)
    social_triggers = ['ดราม่า', 'ทัวร์ลง', 'ชาวเน็ต', '#', 'โซเชียล', 'วิจารณ์สนั่น', 'แฉ', 'เพจดัง', 'ทวิตเตอร์', 'x']
    for word in social_triggers:
        if word in text: score += 12
        
    # คำศัพท์ที่สะท้อนความด่วน
    urgency_triggers = ['ด่วน', 'ล่าสุด', 'เปิดใจ', 'แถลง', 'ช็อก', 'ผวา', 'เตือนภัย', 'เสียชีวิต']
    for word in urgency_triggers:
        if word in text: score += 10
        
    # ให้คะแนนพิเศษกับแหล่งที่มาจากหมวดโซเชียล
    if "Social" in source_name or "ดราม่า" in source_name: score += 15
    if "Google Trends" in source_name: score += 10
    
    if score > 99: score = 99
    return score

if "top_50_news" not in st.session_state:
    st.session_state.top_50_news = []

if st.button("🔥 กวาดเนื้อหาจากทุกทิศทาง และจัดอันดับ Top 50 ตอนนี้"):
    with st.spinner("กำลังสูบข้อมูลจาก X, FB (ผ่านสื่อหลัก) และ Google Trends..."):
        all_raw_data = []
        headers = {'User-Agent': 'Mozilla/5.0'}
        
        # คลังแหล่งข้อมูล (จำลองให้เสมือนกวาดครบทุกแพลตฟอร์ม)
        sources = {
            "🔴 Google Trends (ภาพรวมไทย)": "https://trends.google.com/trending/rss?geo=TH",
            "🐦 กระแส X / โซเชียล (Sanook)": "https://rssfeeds.sanook.com/rss/feeds/sanook/news.social.xml",
            "🔵 ดราม่าชาวเน็ต (Thairath)": "https://www.thairath.co.th/rss/news/society",
            "🎭 ข่าวซุบซิบดารา": "https://www.thairath.co.th/rss/ent",
            "📰 ข่าวทั่วไป (Workpoint)": "https://workpointtoday.com/feed/"
        }
        
        for source_name, url in sources.items():
            try:
                res = requests.get(url, timeout=10, headers=headers)
                feed = feedparser.parse(res.content)
                for entry in feed.entries[:20]: # สูบมาเยอะๆ ก่อนเพื่อคัดกรอง
                    desc = entry.get("summary", entry.get("description", ""))
                    clean_desc = re.sub(re.compile('<.*?>'), '', desc).strip()
                    
                    p_score = calculate_priority_score(entry.title, clean_desc, source_name)
                    
                    all_raw_data.append({
                        "Priority Score": p_score,
                        "แหล่งดึงข้อมูล": source_name,
                        "พาดหัวข่าวต้นทาง": entry.title,
                        "เนื้อหาโดยย่อ": clean_desc[:150] + "...",
                        "ลิงก์ต้นทาง": entry.link,
                        "วันที่ดึงข้อมูล": datetime.now().strftime("%H:%M")
                    })
            except: pass
            
        # จัดอันดับ (เรียงจากคะแนนมากไปน้อย) และตัดเอาแค่ Top 50
        sorted_data = sorted(all_raw_data, key=lambda x: x['Priority Score'], reverse=True)
        
        # กรองข้อมูลซ้ำ (เผื่อหลายเว็บลงข่าวเดียวกัน)
        unique_data = []
        seen_titles = set()
        for item in sorted_data:
            if item["พาดหัวข่าวต้นทาง"] not in seen_titles:
                unique_data.append(item)
                seen_titles.add(item["พาดหัวข่าวต้นทาง"])
                
        st.session_state.top_50_news = unique_data[:50]
        st.success(f"คัดกรองเสร็จสิ้น! ได้ตารางจัดอันดับ Top 50 กระแสที่เดือดที่สุด ณ เวลานี้")

if st.session_state.top_50_news:
    df = pd.DataFrame(st.session_state.top_50_news)
    
    st.subheader("📊 ตารางจัดอันดับ (Ranking 1-50) เรียงตามความต้องทำก่อน-หลัง")
    st.dataframe(
        df.style.background_gradient(subset=['Priority Score'], cmap='Oranges'),
        use_container_width=True, 
        height=400
    )
    
    st.markdown("---")
    st.subheader("🎯 Blueprint: แผนการทำคลิปแบบมืออาชีพ")
    
    # ให้เลือกข่าวจาก Top 50 เพื่อดูวิธีโพสต์
    titles = [f"อันดับ {idx+1} [Score: {item['Priority Score']}] {item['พาดหัวข่าวต้นทาง']}" for idx, item in enumerate(st.session_state.top_50_news)]
    selected_index = st.selectbox("เลือกประเด็นที่ต้องการเจาะลึกเพื่อรับแผนการทำคลิป:", range(len(titles)), format_func=lambda x: titles[x])
    selected_item = st.session_state.top_50_news[selected_index]
    
    # วิเคราะห์คีย์เวิร์ดเพื่อทำ Hashtag
    words = selected_item['พาดหัวข่าวต้นทาง'].split()
    keyword_candidate = [w for w in words if len(w) > 3]
    main_kw = keyword_candidate[0] if keyword_candidate else "ดราม่า"
    
    st.markdown(f"### 📌 แหล่งอ้างอิง: [คลิกเพื่อไปอ่านข่าวเต็มจากแหล่งที่มา]({selected_item['ลิงก์ต้นทาง']})")
    
    st.info("👇 **ก๊อปปี้ข้อมูลด้านล่างนี้ไปใช้ได้เลย** 👇")
    
    col1, col2 = st.columns(2)
    with col1:
        st.markdown("#### 📝 การตั้งพาดหัวข่าว (Hook) หน้าคลิป")
        st.code(f"สรุปดราม่า! {selected_item['พาดหัวข่าวต้นทาง'][:40]}... ใครผิดใครถูก!?", language="text")
        st.markdown("*เทคนิค: ใช้ฟอนต์สีเหลืองขอบดำ วางพาดกลางคลิปให้อ่านออกใน 1 วินาที*")
        
    with col2:
        st.markdown("#### 💬 การเขียนแคปชั่น (Description)")
        st.code(f"เรื่องนี้กำลังเดือดมาก! {selected_item['เนื้อหาโดยย่อ'][:80]}... เพื่อนๆ คิดเห็นยังไงกับประเด็นนี้? คอมเมนต์คุยกันหน่อยครับ! 👇👇", language="text")
        st.markdown("*เทคนิค: ต้องจบด้วยประโยคคำถามเสมอ เพื่อหลอกให้อัลกอริทึมดันฟีดจากยอดคอมเมนต์*")
        
    st.markdown("#### #️⃣ แฮชแท็กที่ต้องติด (Hashtags)")
    st.code(f"#{main_kw} #ดราม่าวันนี้ #ข่าวtiktok #สรุปข่าว #เล่าข่าว #เทรนด์วันนี้", language="text")
    