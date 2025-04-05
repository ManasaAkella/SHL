import streamlit as st
import requests

st.set_page_config(page_title="SHL Assessment Recommender 💼", layout="centered")

st.title("🔍 SHL Assessment Recommendation System")
st.markdown("Type a **skill** or **keyword** to get relevant SHL assessments.")

# Input
skill = st.text_input("🧠 Enter skill or keyword", "")

if st.button("🚀 Recommend"):
    if skill.strip() == "":
        st.warning("Please enter a skill, buddy! ")
    else:
        with st.spinner("Finding the perfect assessments for you... 🧭"):
            try:
                response = requests.get(f"http://127.0.0.1:8000/recommend_assessments?skill={skill}")
                data = response.json()
                
                if "error" in data or "message" in data:
                    st.error(data.get("error", data.get("message", "Something went wrong 😢")))
                else:
                    st.success(f"🎉 Found {len(data)} recommendation(s)!")
                    for item in data:
                        st.markdown(f"""
                        **📝 Name:** [{item['Name']}]({item['URL']})  
                        **📌 Skills:** {item['Skills']}  
                        ---  
                        """)
            except Exception as e:
                st.error(f"💥 Error fetching recommendations: {e}")
