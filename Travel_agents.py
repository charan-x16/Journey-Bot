from crewai import Agent, LLM
from Travel_tools import search_web_tool
from langchain_groq import ChatGroq
import os 
from dotenv import load_dotenv



llm = LLM(
    model="groq/meta-llama/llama-4-scout-17b-16e-instruct",
    api_key=os.getenv("GROQ_API_KEY"),
)

# Agents 

Guide_expert = Agent(
        role = "City Local Guide expert",
        goal = "Provides information on things to do in the city based on user interests.",
        backstory="A local expert passionate about sharing city experiences.",
        tools=[search_web_tool],
        verbose=True,
        max_iter=2,
        llm=llm,
        )


location_expert = Agent(
        role="Travel Trip Expert",
        goal="Provides travel logistics and essential information.",
        backstory="A seasoned traveler who knows everything about different cities.",
        tools=[search_web_tool],  
        verbose=True,
        max_iter=2,
        llm=llm,
        allow_delegation=False,
        )


planner_expert = Agent(
        role="Travel Planning Expert",
        goal="Compiles all gathered information to create a travel plan.",
        backstory="An expert in planning seamless travel itineraries.",
        tools=[search_web_tool],
        verbose=True,
        max_iter=2,
       llm=llm,
        allow_delegation=False,
        )  