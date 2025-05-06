# Career Guidance Form using Streamlit
import streamlit as st

# Page Configuration
st.set_page_config(page_title="แบบฟอร์มแนะแนวอาชีพ", page_icon="🎓", layout="centered")

# Title and description
st.title("แบบฟอร์มแนะแนวอาชีพ")
st.write("""
โปรแกรมนี้ช่วยให้คุณกรอกข้อมูลส่วนตัวเกี่ยวกับการศึกษา ทักษะ ความสนใจ บุคลิกภาพ และอาชีพในฝัน 
จากนั้นจะแสดงสรุปข้อมูลที่กรอกและให้คำแนะนำเส้นทางอาชีพโดย ChatGPT (จำลอง) 
""")

# OpenAI API Key Input
api_key_input = st.text_input(
    label="ใส่ OpenAI API Key (ถ้ามี)", 
    placeholder="กรอก API Key ของ OpenAI ที่นี่", 
    type="password",
    key="openai_api_key"
)

# Career Information Form
with st.form(key="career_form"):
    st.subheader("ข้อมูลส่วนตัวสำหรับแนะแนวอาชีพ")
    education_level = st.selectbox(
        "ระดับการศึกษา", 
        ("มัธยมศึกษาตอนต้น", "มัธยมศึกษาตอนปลาย", "ปริญญาตรี", "ปริญญาโท", "ปริญญาเอก", "อื่นๆ")
    )
    major = st.text_input("สาขาวิชาที่เรียนหรือสนใจ")
    skills = st.multiselect(
        "ทักษะที่มีอยู่แล้ว", 
        ("การเขียนโปรแกรม", "การสื่อสาร", "การวิเคราะห์ข้อมูล", "การออกแบบ", "ภาษาต่างประเทศ", "แก้ปัญหา", "อื่นๆ")
    )
    interests = st.multiselect(
        "ความสนใจหรือสิ่งที่ชอบทำ", 
        ("อ่านหนังสือ", "เล่นกีฬา", "วาดภาพ", "เล่นเกม", "ดนตรี/ร้องเพลง", "ท่องเที่ยว", "เขียนบล็อก", "ช่วยเหลือสังคม", "อื่นๆ")
    )
    personality = st.multiselect(
        "ลักษณะบุคลิกภาพคร่าว ๆ", 
        ("ร่าเริง", "ใจเย็น", "สร้างสรรค์", "ชอบวิเคราะห์", "กล้าแสดงออก", "อ่อนไหว", "ชอบเป็นผู้นำ", "เก็บตัว")
    )
    dream_career = st.text_input("อาชีพในฝัน (ถ้ามี)")
    
    submitted = st.form_submit_button("ส่งข้อมูลและรับคำแนะนำ")

if submitted:
    # Display entered information
    st.subheader("สรุปข้อมูลของคุณ")
    st.write(f"- ระดับการศึกษา: **{education_level}**")
    st.write(f"- สาขาวิชาที่เรียน/สนใจ: **{major or '-'}**")
    st.write(f"- ทักษะ: **{', '.join(skills) if skills else '-'}**")
    st.write(f"- ความสนใจ: **{', '.join(interests) if interests else '-'}**")
    st.write(f"- บุคลิกภาพ: **{', '.join(personality) if personality else '-'}**")
    st.write(f"- อาชีพในฝัน: **{dream_career or '-'}**")
    
    # Prepare prompt for ChatGPT
    prompt = (
        f"ข้อมูลนักเรียน: ระดับการศึกษา {education_level}, สาขา {major}, "
        f"ทักษะ {', '.join(skills)}, ความสนใจ {', '.join(interests)}, บุคลิกภาพ {', '.join(personality)}, "
        f"อาชีพในฝัน {dream_career}. "
        "กรุณาให้คำแนะนำเส้นทางอาชีพที่เหมาะสม"
    )
    api_key = st.session_state.get("openai_api_key", "")
    
    if api_key:
        try:
            import openai
            openai.api_key = api_key
            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "คุณเป็นผู้ช่วยแนะแนวอาชีพ ช่วยให้นักเรียนค้นพบเส้นทางอาชีพที่เหมาะสมจากข้อมูลที่ให้มา"},
                    {"role": "user", "content": prompt}
                ]
            )
            advice = response.choices[0].message.content
        except Exception as e:
            advice = f"เกิดข้อผิดพลาดในการเรียกใช้งาน OpenAI: {e}"
        st.subheader("คำแนะนำจาก ChatGPT")
        st.write(advice)
    else:
        # Simulated ChatGPT response for users without API key
        st.subheader("คำแนะนำจาก ChatGPT (ตัวอย่าง)")
        example_advice = (
            f"จากข้อมูลที่ได้รับ คุณกำลังศึกษาอยู่ระดับ{education_level} สาขา{major or '-'} "
            f"มีทักษะด้าน{', '.join(skills) if skills else '-'} และสนใจด้าน{', '.join(interests) if interests else '-'} "
            f"บุคลิกภาพโดยทั่วไปคือ{', '.join(personality) if personality else '-'}."
            f"{f' และคุณมีอาชีพในฝันเป็น {dream_career}.' if dream_career else ''} "
            "ChatGPT แนะนำว่า คุณอาจพิจารณาเส้นทางอาชีพที่เกี่ยวข้องกับความสนใจและทักษะของคุณ "
            "เช่น หากคุณสนใจด้านวิทยาการคอมพิวเตอร์และมีทักษะเขียนโปรแกรม อาจลองสำรวจอาชีพในสายวิทยาการคอมพิวเตอร์ "
            "นอกจากนี้ การทดลองทำกิจกรรมต่าง ๆ หรือเรียนคอร์สออนไลน์ สามารถช่วยให้คุณค้นพบอาชีพที่เหมาะสมได้มากขึ้น"
        )
        st.write(example_advice)
