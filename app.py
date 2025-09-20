import streamlit as st

st.title("Cyberbullying & Harassment Detector")

text = st.text_area("Enter a message or comment to analyze:")

if st.button("Analyze"):
    bullying_words = ["stupid", "idiot", "hate", "kill", "loser"]
    if any(word in text.lower() for word in bullying_words):
        st.error("⚠ This looks like Cyberbullying/Harassment.")
    else:
        st.success("✅ This seems safe.")