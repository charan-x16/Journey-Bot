from Travel_agents import Guide_expert, location_expert, planner_expert
from Travel_tasks import guide_task, location_task, planner_task
from crewai import Crew, Process
import streamlit as st 

st.title("Journey-Bot")
st.markdown("""
# 🧳 Plan Your Next Adventure with AI!

Welcome to your **smart travel assistant** 🤖✈️  
Tell us where you're going, and we’ll craft a **personalized itinerary** just for you!

### 🌍 What You’ll Get:
- 🎡 **Top attractions** tailored to your interests  
- 💰 **Accommodation suggestions** & budget planning  
- 🍲 **Local food gems** you shouldn't miss  
- 🚆 **Transportation tips** and **visa info**  

Just enter your travel details below —  
Your perfect trip starts now! 🌟
""")

# User Inputs
from_city = st.text_input("🏠 **Starting From**", placeholder="e.g., Bangalore, India")
destination_city = st.text_input("📍 **Destination**", placeholder="e.g., Rome, Italy")

st.markdown("---")

st.markdown("### 📅 Choose your travel dates")
date_from = st.date_input("🚀 **Departure Date**")
date_to = st.date_input("🛬 **Return Date**")

st.markdown("---")

interests = st.text_area(
    "💡 **Tell us what you love**",
    placeholder="e.g., art museums, wine tasting, beach activities, mountain hiking...",
    height=100
)

# Button for the CrewAI
if st.button("✨Generate Tavel Plan"):
    if not from_city or not destination_city or not date_from or not date_to or not interests:
        st.error("⚠️ Please fill in all fields before generating your travel plan.")
    else:
        st.markdown("⏳AI is preparing your personalized travel itinerary... Please wait.")

        # Intialize Tasks 
        loc_task = location_task(location_expert, from_city, destination_city, date_from, date_to)
        guide_task = guide_task(Guide_expert, destination_city, interests, date_from, date_to)
        plan_task = planner_task([loc_task, guide_task], planner_expert, destination_city, interests, date_from, date_to)

        # Define Crew
        crew = Crew(
            agents = [location_expert, Guide_expert, planner_expert],
            tasks = [loc_task, guide_task, plan_task],
            process = Process.sequential,
            full_output = True,
            verbose=True
        )

        result = crew.kickoff()

        # Display Results 
        st.subheader("✅ Your AI-Powered Travel Plan")
        st.markdown(result)

        # Ensure result is a string
        travel_plan_text = str(result)  # ✅ Convert CrewOutput to string

        st.download_button(
            label="📥 Download Travel Plan",
            data=travel_plan_text,  # ✅ Now passing a valid string
            file_name=f"Travel_Plan_{destination_city}.txt",
            mime="text/plain"
        )