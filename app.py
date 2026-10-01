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
