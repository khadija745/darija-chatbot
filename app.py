import streamlit as st
import json

st.set_page_config(page_title="Chatbot Darija", page_icon="🇲🇦", layout="centered")

# --- الزواق ---
st.markdown("""
<style>
   .stApp { background-color: #FFF8F0; }
    h1 { color: #C1272D; text-align: center; font-family: 'Arial'; }
   .stChatMessage { border-radius: 15px; padding: 10px; }
</style>
""", unsafe_allow_html=True)

st.title("🇲🇦 شات بوت خديجة بالدارجة")
st.markdown("<p style='text-align:center'>سولني أي حاجة بالدارجة و نجاوبك!</p>", unsafe_allow_html=True)

# قراءة البيانات
try:
    with open('data.json', 'r', encoding='utf-8') as f:
        data = json.load(f)
except:
    data = []

def get_answer(question):
    question = question.lower().strip()
    for item in data:
        patterns = item.get("patterns", [])
        for p in patterns:
            if p.lower() in question or question in p.lower():
                # كيرجع أول جواب
                return item.get("responses", ["ما فهمتش"])[0]
    return "سمح ليا، ما فهمتش سؤالك مزيان، عاود صيغو بطريقة أخرى؟ 😅"

# تاريخ المحادثة
if "messages" not in st.session_state:
    st.session_state.messages = []

for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.write(msg["content"])

if prompt := st.chat_input("كتب سؤالك هنا بالدارجة..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.write(prompt)

    answer = get_answer(prompt)
    st.session_state.messages.append({"role": "assistant", "content": answer})
    with st.chat_message("assistant"):
        st.write(answer)



 
