import streamlit as st
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import PromptTemplate       # Corrected import for prompts
from langchain_core.output_parsers import StrOutputParser # New import for output
import os

# --- 1. PAGE CONFIGURATION ---
st.set_page_config(layout="wide")
# --- 2. SET UP GEMINI API KEY ---
# The temporary variable to hold your key (REPLACE 'YOUR_KEY_HERE' with your actual key)
GEMINI_KEY = "AIzaSyD_UolN7Hjl5RglEu4NbXF4lB-Rd5x_pVI" # <--- PASTE YOUR KEY HERE
# os.environ["GEMINI_API_KEY"] = GEMINI_KEY # <-- Keep this line commented or delete it

# --- 3. STREAMLIT UI ---
st.title("Tweet Generator 🎯")
st.markdown("### Generate tweets on any topic")

# Input Fields
topic = st.text_input("Topic", placeholder="e.g., India, space travel, AI")
number_of_tweets = st.slider("Number of tweets", min_value=1, max_value=10, value=5)

# --- 4. LLM & PROMPT SETUP ---

# Initialize the model 
try:
    llm = ChatGoogleGenerativeAI(model="gemini-2.5-flash", google_api_key=GEMINI_KEY) 
except Exception as e:
    st.error(f"Failed to initialize the Gemini model. Check your API key. Error: {e}")
    llm = None    
# Define the Prompt Template
template = """
You are a creative social media expert. Your task is to generate {num_tweets} unique, engaging, and professional tweets about the given topic.
Each tweet must include relevant hashtags.
Present the tweets as a numbered list.

Topic: {topic}
Number of tweets to generate: {num_tweets}
"""

prompt = PromptTemplate(
    input_variables=["num_tweets", "topic"],
    template=template,
)

# --- 4b. LCEL Chain Construction (The new way) ---
if llm:
    # Use the modern Runnable Sequence (LCEL) instead of LLMChain
    # This construction replaces the need for the LLMChain import!
    chain = prompt | llm | StrOutputParser()
    
# --- 5. GENERATION LOGIC ---
if st.button("Generate"):
    # Input Validation
    if not topic:
        st.warning("Please enter a topic to generate tweets.")
    elif llm is None:
        pass
    else:
        with st.spinner(f"Generating {number_of_tweets} tweets on '{topic}'..."):
            try:
                # Run the LCEL chain using .invoke()
                response = chain.invoke(
                    {"num_tweets": number_of_tweets, "topic": topic}
                )
                
                # Display the result
                st.markdown(response)

            except Exception as e:
                st.error(f"An error occurred during generation: {e}")