import base64
import json
import random
 
import streamlit as st
 
st.set_page_config(page_title="Khadija · Darija Bot", page_icon="🕌", layout="centered")
 
RED = "#C1272D"
GREEN = "#006233"
 
# ---------- Logo: red disc with the green Moroccan star (pentagram) ----------
LOGO_SVG = f"""
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 100 100">
  <circle cx="50" cy="50" r="47" fill="{RED}" stroke="#ffffff" stroke-width="4"/>
  <polygon points="50,22 66.46,72.65 23.37,41.35 76.63,41.35 33.54,72.65"
           fill="none" stroke="{GREEN}" stroke-width="4.5" stroke-linejoin="miter"/>
</svg>
"""
LOGO_URI = "data:image/svg+xml;base64," + base64.b64encode(LOGO_SVG.encode()).decode()
 
# ---------- Design ----------
st.markdown(f"""
<style>
@import url('https://fonts.googleapis.com/css2?family=Reem+Kufi:wght@500;700&family=Tajawal:wght@400;500;700&display=swap');
 
html, body, .stApp, [data-testid="stAppViewContainer"] {{
    font-family: 'Tajawal', sans-serif;
    direction: rtl;
}}
 
.stApp {{
    background-color: #FFFDF8;
    background-image:
        linear-gradient(45deg, rgba(0,98,51,.05) 25%, transparent 25%, transparent 75%, rgba(0,98,51,.05) 75%),
        linear-gradient(45deg, rgba(0,98,51,.05) 25%, transparent 25%, transparent 75%, rgba(0,98,51,.05) 75%);
    background-size: 44px 44px;
    background-position: 0 0, 22px 22px;
}}
header[data-testid="stHeader"] {{ background: transparent; }}
#MainMenu, footer {{ visibility: hidden; }}
 
/* Header: red band, green base */
.hero {{
    background: {RED};
    color: #fff;
    text-align: center;
    padding: 1.6rem 1rem 1.3rem;
    margin-bottom: 1.6rem;
    border-radius: 22px;
    border-bottom: 8px solid {GREEN};
    box-shadow: 0 12px 26px rgba(193,39,45,.25);
}}
.hero img {{ width: 92px; height: 92px; filter: drop-shadow(0 4px 6px rgba(0,0,0,.25)); }}
.hero h1 {{
    font-family: 'Reem Kufi', sans-serif;
    font-size: 2.1rem;
    margin: .3rem 0 .1rem;
    color: #fff;
}}
.hero p {{ margin: 0; font-size: 1.05rem; color: #FFE9E9; }}
 
/* Chat bubbles */
[data-testid="stChatMessage"] {{
    border-radius: 18px;
    padding: .9rem 1.1rem;
    margin-bottom: .7rem;
    box-shadow: 0 4px 12px rgba(0,0,0,.05);
}}
[data-testid="stChatMessage"]:has([data-testid="stChatMessageAvatarUser"]) {{
    background: #FDECEC;
    border-right: 6px solid {RED};
}}
[data-testid="stChatMessage"]:has([data-testid="stChatMessageAvatarAssistant"]) {{
    background: #E6F4EC;
    border-right: 6px solid {GREEN};
}}
[data-testid="stChatMessage"] p {{ font-size: 1.05rem; line-height: 1.8; }}
 
/* Suggested-question buttons */
.stButton > button {{
    font-family: 'Tajawal', sans-serif;
    background: #fff;
    color: {GREEN};
    border: 2px solid {GREEN};
    border-radius: 999px;
    font-weight: 500;
}}
.stButton > button:hover {{
    background: {GREEN};
    color: #fff;
    border-color: {GREEN};
}}
.stButton > button:focus-visible {{ outline: 3px solid {RED}; }}
 
/* Input */
[data-testid="stChatInput"] {{
    border: 2px solid {GREEN};
    border-radius: 999px;
    background: #fff;
}}
[data-testid="stChatInput"]:focus-within {{
    border-color: {RED};
    box-shadow: 0 0 0 3px rgba(193,39,45,.25);
}}
[data-testid="stChatInput"] textarea {{ direction: rtl; font-family: 'Tajawal', sans-serif; }}
 
/* Sidebar */
[data-testid="stSidebar"] {{ background: {GREEN}; direction: rtl; }}
[data-testid="stSidebar"] * {{ color: #fff; }}
[data-testid="stSidebar"] .stButton > button {{
    background: {RED}; color: #fff; border: 2px solid #fff;
}}
</style>
 
<div class="hero">
    <img src="{LOGO_URI}" alt="Morocco logo"/>
    <h1>شات بوت خديجة</h1>
    <p>مرحبا بيك! كنهضر غير بالدارجة المغربية، سولني اللي بغيتي.</p>
</div>
""", unsafe_allow_html=True)
 
# ---------- Data ----------
try:
    with open("data.json", "r", encoding="utf-8") as f:
        data = json.load(f)
except Exception:
    data = []
 
FALLBACK = "سمح ليا، ما فهمتش سؤالك مزيان. عاود صيغو بطريقة أخرى."
 
SUGGESTIONS = [
    "شنو هي عاصمة المغرب؟",
    "كيفاش نوجد الطاجين؟",
    "كيفاش نوجد أتاي بالنعناع؟",
    "فين نسافر فالمغرب؟",
    "شنو معنى علم المغرب؟",
    "شنو هي العملة المغربية؟",
]
 
 
def get_answer(question: str) -> str:
    q = question.lower().strip().rstrip("؟?!.")
    for item in data:
        for p in item.get("patterns", []):
            p = p.lower()
            if p in q or q in p:
                return random.choice(item.get("responses", [FALLBACK]))
    return FALLBACK
 
 
# ---------- State ----------
if "messages" not in st.session_state:
    st.session_state.messages = []
if "pending" not in st.session_state:
    st.session_state.pending = None
 
with st.sidebar:
    st.markdown("### خديجة")
    st.caption("بوت كيجاوب بالدارجة المغربية")
    if st.button("مسح المحادثة", use_container_width=True):
        st.session_state.messages = []
        st.rerun()
 
AVATARS = {"user": "🧑", "assistant": "🫖"}
 
# ---------- Handle input (typed or clicked suggestion) ----------
prompt = st.chat_input("كتب سؤالك هنا بالدارجة...")
if st.session_state.pending:
    prompt = st.session_state.pending
    st.session_state.pending = None
 
if prompt:
    st.session_state.messages.append({"role": "user", "content": prompt})
    st.session_state.messages.append({"role": "assistant", "content": get_answer(prompt)})
 
# ---------- Render ----------
if not st.session_state.messages:
    st.markdown("**جرب واحد من هاد الأسئلة:**")
    cols = st.columns(2)
    for i, q in enumerate(SUGGESTIONS):
        if cols[i % 2].button(q, key=f"s{i}", use_container_width=True):
            st.session_state.pending = q
            st.rerun()
 
for msg in st.session_state.messages:
    with st.chat_message(msg["role"], avatar=AVATARS[msg["role"]]):
        st.write(msg["content"])
 

