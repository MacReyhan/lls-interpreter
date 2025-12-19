import streamlit as st
import google.generativeai as genai
import os

# --- 1. SETUP & CONFIG ---
st.set_page_config(page_title="LLS Interpretty", page_icon="💎", layout="centered")

# REPLACE THIS WITH YOUR ACTUAL API KEY
# Or set it in your secrets.toml file
API_KEY = "NANANANA" 

try:
    genai.configure(api_key=API_KEY)
except Exception as e:
    st.error("⚠️ Hey bro, you forgot to paste your API Key in the code!")

# --- 2. THE BRAIN (Your System Prompt) ---
# I pasted your exact instructions here
system_instruction = """
Act as a specialized English-Bengali interpreter under the persona 'LLS INTERPRETTY '. Your primary function is to provide accurate and complete translations between English and Bengali, adhering strictly to the following rules:

Purpose and Goals:
* Provide high-quality, immediate, and culturally nuanced translations between English and Native Bengali.
* Ensure translations are presented in both the target language's script (Bengali or English) and a romanized version (Benglish for Bengali, or standard English romanization for English).
* Maintain a concise output, focusing solely on the translation results.
* If there are any short forms like MRI or ICU, etc., make them full form and include the Bengali translation for the full form as well.

Behaviors and Rules:
1) Input Handling:
    a) If the user's input is in English, the output must be in complete Bengali (using the Bengali script) with no English words interspersed.
    b) If the user's input is in Bengali (either script or romanized), the output must be in complete English.
    c) Do not engage in conversation, greetings, explanations, or any text beyond the required translation output and its romanized form.

2) Output Format (Strict Adherence):
    a) For English input:
        i. Line 1: The complete translation in Bengali script.
        ii. Line 2: The romanized version of the Bengali translation.
    b) For Bengali input:
        i. Line 1: The complete translation in English.
        ii. Line 2: The standard English pronunciation/romanization.

3) Handling Acronyms and Abbreviations:
    a) If an acronym or abbreviation is present (e.g., MRI, ICU), first expand it to its full form in the source language.
    b) Provide the translation of the full form in the target language following the strict output format rules.
"""

model = genai.GenerativeModel(
    model_name="gemini-1.5-flash-001",
    system_instruction=system_instruction
)

# --- 3. THE UI (Matching your Opal Screenshots & HTML) ---

# This CSS hides the default Streamlit header and makes the background match your screenshot (Dark Purple)
st.markdown("""
    <style>
        .stApp {
            background-color: #2e2b5e; /* Matching that dark purple Opal background */
            color: white;
        }
        /* Hide Streamlit elements */
        #MainMenu {visibility: hidden;}
        footer {visibility: hidden;}
        header {visibility: hidden;}
        
        /* Custom Input styling to look like Opal */
        .stTextInput > div > div > input {
            background-color: #1e1b4b;
            color: white;
            border: 1px solid #4c1d95;
            border-radius: 20px;
            padding: 10px;
        }
    </style>
""", unsafe_allow_html=True)

# Title (The "Input" Screen vibe)
st.markdown("<h1 style='text-align: center; color: #a0aaff; font-family: sans-serif;'>LLS INTERPRETTY</h1>", unsafe_allow_html=True)
st.markdown("<h3 style='text-align: center; color: #c7c7c7; font-weight: 300;'>Enter text in English or Bengali</h3>", unsafe_allow_html=True)

# The Input Box
user_input = st.text_input("", placeholder="Type here...", label_visibility="collapsed")

# --- 4. THE LOGIC & DYNAMIC DISPLAY ---
if user_input:
    with st.spinner("Translating..."):
        try:
            # Get response from Gemini
            response = model.generate_content(user_input)
            text_response = response.text.strip()
            
            # Split the lines based on your prompt rules (Line 1 = Script, Line 2 = Romanized)
            parts = text_response.split('\n')
            main_text = parts[0] if len(parts) > 0 else "Error"
            sub_text = parts[1] if len(parts) > 1 else ""

            # --- 5. THE OUTPUT (Injecting your HTML File) ---
            # I am using the exact HTML structure you sent, but inserting the python variables
            html_code = f"""
            <!DOCTYPE html>
            <html lang="en">
            <head>
                <script src="https://cdn.tailwindcss.com"></script>
                <style>
                    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;700&family=Outfit:wght@700&display=swap');
                    .font-display {{ font-family: 'Outfit', sans-serif; }}
                    .font-body {{ font-family: 'Inter', sans-serif; }}
                    .animate-float {{ animation: float 3s ease-in-out infinite; }}
                    @keyframes float {{
                        0% {{ transform: translateY(0px); }}
                        50% {{ transform: translateY(-10px); }}
                        100% {{ transform: translateY(0px); }}
                    }}
                </style>
            </head>
            <body class="bg-transparent p-4">
                <div class="bg-[#172a45] bg-opacity-90 backdrop-blur-lg shadow-2xl rounded-xl p-8 max-w-xl mx-auto text-center border border-gray-700">
                    <h1 class="text-4xl font-display font-bold text-[#64ffda] mb-6 animate-float">
                        অনুবাদ
                    </h1>
                    <div class="mb-8">
                        <p class="text-4xl font-bold text-[#ccd6f6] leading-tight mb-4 drop-shadow-lg">
                            {main_text}
                        </p>
                        <p class="text-xl font-body text-[#a0aaff] font-semibold italic">
                            {sub_text}
                        </p>
                    </div>
                    <div class="border-t border-gray-700 pt-6">
                        <p class="text-sm font-body text-gray-400">
                            Original: {user_input}
                        </p>
                    </div>
                </div>
            </body>
            </html>
            """
            
            # Render the HTML card
            st.components.v1.html(html_code, height=450, scrolling=False)

        except Exception as e:
            st.error(f"Something went wrong: {e}")
