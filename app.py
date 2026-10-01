import streamlit as st
import json

st.set_page_config(page_title="Chatbot Darija - Khadija", page_icon="🇲🇦", layout="centered")

# --- زواق مغربي حمر وخضر ---
st.markdown("""
<style>
    /* الخلفية */
   .stApp {
        background: linear-gradient(180deg, #ffffff 0%, #fff5f5 100%);
    }
    /* العنوان */
    h1 {
        color: #C1272D!important;
        text-align: center;
        font-weight: bold;
        text-shadow: 1px 1px 2px #006233;
    }
    /* رسائل البوت - بالخضر */
    div[data-testid="stChatMessage"]:nth-child(even) {
        background-color: #E8F5E9!important;
        border-left: 5px solid #006233!important;
        border-radius: 15px!important;
    }
    /* رسائل المستخدم - بالحمر */
    div[data-testid="stChatMessage"]:nth-child(odd) {
        background-color: #FFEBEE!important;
        border-right: 5px solid #C1272D!important;
        border-radius: 15px!important;
    }
    /* زر الإرسال */
    button[kind="primary"] {
        background-color: #C1272D!important;
        border-color: #006233!important;
    }
    /* شريط الكتابة */
   .stChatInput {
        border: 2px solid #006233!important;
        border-radius: 20px!important;
    }
</style>
""", unsafe_allow_html=True)

st.title("🇲🇦 شات بوت خديجة بالدارجة")
st.markdown("<h3 style='text-align:center; color:#006233;'>مرحبا بيك! أنا كنهضر غير بالدارجة المغربية ❤️💚</h3>", unsafe_allow_html=True)
st.markdown("<p style='text-align:center;'>سولني أي حاجة...</p>", unsafe_allow_html=True)

# قراءة البيانات
try:
    with open('data.json', 'r', encoding='utf-8') as f:
        data = json.load(f)
except:
    data = []

def get_answer(question):
    question = question.lower().strip()
    for item in data:
        for p in item.get("patterns", []):
            if p.lower() in question or question in p.lower():
                return item.get("responses", ["ما فهمتش"])[0]
    return "سمح ليا، ما فهمتش سؤالك مزيان، عاود صيغو بطريقة أخرى؟ 😅"

if "messages" not in st.session_state:
    st.session_state.messages = []

for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.write(msg["content"])

if prompt := st.chat_input("كتب سؤالك هنا بالدارجة... 🇲🇦"):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.write(prompt)

    answer = get_answer(prompt)
    st.session_state.messages.append({"role": "assistant", "content": answer})
    with st.chat_message("assistant"):
        st.write(answer)
