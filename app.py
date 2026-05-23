import streamlit as st
from groq import Groq
ACADEMY_INFO = """
اسم الأكاديمية: [code leader]
الكورسات: [python,app inventor,scratch,graphics,ict,unity,godot  ]
المواعيد: [السبت من 9ص الي 9 مو الاحد من 9ص الي 9 م ,الاثنين من 9ص الي 9 م , الثلاثاء من 9ص الي 9 م , الاربعاء من 9ص الي 9 م , الخميس من 9ص الي 9 م]
التواصل: [واتس:01030115464]
"""

GROQ_MODEL = "llama-3.3-70b-versatile"

st.set_page_config(page_title="مساعد الأكاديمية", page_icon="🎓")
st.title(" مساعد الأكاديمية")

api_key = st.secrets["GROQ_API_KEY"]

if st.sidebar.button(" مسح المحادثة"):
    st.session_state.messages = []

if "messages" not in st.session_state:
    st.session_state.messages = []

for msg in st.session_state.messages:
    with st.chat_message("user" if msg["role"] == "user" else "assistant"):
        st.write(msg["content"])

user_input = st.chat_input("اكتب سؤالك هنا...")

if user_input:
    st.session_state.messages.append({"role": "user", "content": user_input})

    with st.chat_message("assistant"):
        with st.spinner("جاري الرد..."):
            client = Groq(api_key=api_key)

            system = f"""أنت مساعد ودود لأكاديمية أطفال. أجب باللغة العربية بشكل مختصر وواضح.
أجب فقط بناءً على هذه المعلومات:
{ACADEMY_INFO}
إذا السؤال خارج المعلومات، قل: تواصل معنا مباشرة."""

            response = client.chat.completions.create(
                model=GROQ_MODEL,
                messages=[{"role": "system", "content": system}] + st.session_state.messages,
                max_tokens=512,
            )

            reply = response.choices[0].message.content
            st.write(reply)
            st.session_state.messages.append({"role": "assistant", "content": reply})
