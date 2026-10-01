import streamlit as st
import json
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

with open('data.json', encoding='utf-8') as f:
    data = json.load(f)

questions = [item['q'] for item in data]
answers = [item['a'] for item in data]

vectorizer = TfidfVectorizer()
X = vectorizer.fit_transform(questions)

st.title("Chatbot Darija - Projet S5")
st.write("سولني أي حاجة بالدارجة")

user_q = st.text_input("كتب سؤالك هنا:")

if user_q:
    user_vec = vectorizer.transform([user_q])
    sim = cosine_similarity(user_vec, X)
    idx = sim.argmax()
    st.success(answers[idx])
import streamlit as st
import json

st.set_page_config(page_title="Chatbot Darija", page_icon="🇲🇦", layout="centered")

# --- الزواق ---
st.markdown("""
<style>
   .stApp { background-color: #FFF8F0; }
    h1 { color: #C1272D; text-align: center; }
   .stChatMessage { border-radius: 15px; }
</style>
""", unsafe_allow_html=True)

st.title("🇲🇦 شات بوت بالدارجة المغربية")
st.markdown("<p style='text-align:center'>سولني أي حاجة بالدارجة و نجاوبك!</p>", unsafe_allow_html=True)

# قراءة البيانات
try:
    with open('data.json', 'r', encoding='utf-8') as f:
        data = json.load(f)
except:
    data = []

def get_answer(question):
    question = question.lower()
    for item in data:
        # كاين نوعين ديال data.json
        q = item.get('q') or item.get('patterns',[''])[0] if isinstance(item.get('patterns'), list) else item.get('patterns','')
        if isinstance(q, list): q = q[0]

        if q.lower() in question or question in q.lower():
            a = item.get('a') or item.get('responses',[''])[0] if isinstance(item.get('responses'), list) else item.get('responses','')
            if isinstance(a, list): a = a[0]
            return a
    return "سمح ليا، ما فهمتش سؤالك، عاود صيغو بطريقة أخرى؟ 😅"

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
