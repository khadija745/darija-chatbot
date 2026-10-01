import json
import random
 
import streamlit as st
 
st.set_page_config(page_title="Khadija · Darija Bot", page_icon="🫖", layout="centered")
 
# ---------- Design: Majorelle blue + saffron, inspired by Marrakech ----------
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Reem+Kufi:wght@500;700&family=Tajawal:wght@400;500;700&display=swap');
 
:root {
    --blue: #2B3A9E;      /* Majorelle blue */
    --blue-deep: #17205E;
    --saffron: #F2B632;
    --paper: #F7F9FF;
    --ink: #1B1F3B;
}
 
html, body, .stApp, [data-testid="stAppViewContainer"] {
    font-family: 'Tajawal', sans-serif;
    direction: rtl;
    color: var(--ink);
}
 
/* Background: soft blue with a faint zellige-like diamond grid */
.stApp {
    background-color: var(--paper);
    background-image:
        linear-gradient(45deg, rgba(43,58,158,.05) 25%, transparent 25%, transparent 75%, rgba(43,58,158,.05) 75%),
        linear-gradient(45deg, rgba(43,58,158,.05) 25%, transparent 25%, transparent 75%, rgba(43,58,158,.05) 75%);
    background-size: 44px 44px;
    background-position: 0 0, 22px 22px;
}
 
header[data-testid="stHeader"] { background: transparent; }
#MainMenu, footer { visibility: hidden; }
 
/* Hero banner shaped like a Moroccan arch */
.hero {
    background: var(--blue);
    color: #fff;
    text-align: center;
    padding: 2.2rem 1.5rem 1.6rem;
    margin: 0 auto 1.8rem;
    max-width: 420px;
    border-radius: 200px 200px 18px 18px;
    border-bottom: 6px solid var(--saffron);
    box-shadow: 0 14px 30px rgba(23,32,94,.25);
}
.hero h1 {
    font-family: 'Reem Kufi', sans-serif;
    font-size: 2.1rem;
    margin: .4rem 0 .2rem;
    color: #fff;
}
.hero p { margin: 0; color: #D9DEFF; font-size: 1rem; }
.hero .lamp { font-size: 2rem; }
 
/* Chat bubbles */
[data-testid="stChatMessage"] {
    border-radius: 18px;
    padding: .9rem 1.1rem;
    margin-bottom: .7rem;
    border: 1px solid rgba(43,58,158,.15);
    box-shadow: 0 4px 12px rgba(23,32,94,.06);
}
/* user = saffron */
[data-testid="stChatMessage"]:has([data-testid="stChatMessageAvatarUser"]) {
    background: #FFF4D6;
    border-right: 6px solid var(--saffron);
}
/* bot = blue */
[data-testid="stChatMessage"]:has([data-testid="stChatMessageAvatarAssistant"]) {
    background: #fff;
    border-right: 6px solid var(--blue);
}
[data-testid="stChatMessage"] p { font-size: 1.05rem; line-height: 1.8; }
 
/* Input */
[data-testid="stChatInput"] {
    border: 2px solid var(--blue);
    border-radius: 999px;
    background: #fff;
}
[data-testid="stChatInput"]:focus-within {
    border-color: var(--saffron);
    box-shadow: 0 0 0 3px rgba(242,182,50,.35);
}
[data-testid="stChatInput"] textarea { direction: rtl; font-family: 'Tajawal', sans-serif; }
 
/* Sidebar */
[data-testid="stSidebar"] { background: var(--blue-deep); direction: rtl; }
[data-testid="stSidebar"] * { color: #fff; }
[data-testid="stSidebar"] .stButton button {
    background: var(--saffron);
    color: var(--blue-deep);
    border: none;
    font-weight: 700;
    border-radius: 999px;
}
 
@media (prefers-reduced-motion: reduce) { * { transition: none !important; } }
</style>
""", unsafe_allow_html=True)
 
# ---------- Header ----------
st.markdown("""
<div class="hero">
    <div class="lamp">🪔</div>
    <h1>خديجة</h1>
    <p>مرحبا بيك! هضر معايا بالدارجة وسولني اللي بغيتي.</p>
</div>
""", unsafe_allow_html=True)
 
# ---------- Data ----------
try:
    with open("data.json", "r", encoding="utf-8") as f:
        data = json.load(f)
except Exception:
    data = []
 
FALLBACK = "سمح ليا، ما فهمتش سؤالك مزيان. عاود صيغو بطريقة أخرى."
 
 
def get_answer(question: str) -> str:
    q = question.lower().strip()
    for item in data:
        for p in item.get("patterns", []):
            p = p.lower()
            if p in q or q in p:
                return random.choice(item.get("responses", [FALLBACK]))
    return FALLBACK
 
 
# ---------- Sidebar ----------
with st.sidebar:
    st.markdown("### خديجة")
    st.caption("بوت كيجاوب بالدارجة المغربية")
    if st.button("مسح المحادثة"):
        st.session_state.messages = []
        st.rerun()
 
# ---------- Chat ----------
if "messages" not in st.session_state:
    st.session_state.messages = []
 
AVATARS = {"user": "🧑", "assistant": "🫖"}
 
for msg in st.session_state.messages:
    with st.chat_message(msg["role"], avatar=AVATARS[msg["role"]]):
        st.write(msg["content"])
 
if prompt := st.chat_input("كتب سؤالك هنا بالدارجة..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user", avatar=AVATARS["user"]):
        st.write(prompt)
 
    answer = get_answer(prompt)
    st.session_state.messages.append({"role": "assistant", "content": answer})
    with st.chat_message("assistant", avatar=AVATARS["assistant"]):
        st.write(answer)
 
