import streamlit as st
from engine.inference import InferenceEngine

st.set_page_config(page_title="SaeeD LogiC", page_icon="🧠")
st.title("🧠 SaeeD LogiC")
st.write("ذكاء اصطناعي محلي 100% — بدون API، بدون مفاتيح، بدون إنترنت")

if "engine" not in st.session_state:
    st.session_state.engine = InferenceEngine()

if "history" not in st.session_state:
    st.session_state.history = []

user_input = st.text_input("اطرح سؤالك هنا:")

if user_input:
    answer = st.session_state.engine.answer(user_input)
    st.session_state.history.append((user_input, answer))

for q, a in reversed(st.session_state.history):
    st.markdown(f"**أنت:** {q}")
    st.markdown(f"**الرد:** {a}")
    st.markdown("---")

st.divider()
st.caption("هذا النظام يتعلم بس من قاعدة المعرفة (data/knowledge.json). "
           "كل ما أضفت أسئلة وأجوبة أكثر، صار أذكى وأدق — بدون أي اتصال خارجي.")
