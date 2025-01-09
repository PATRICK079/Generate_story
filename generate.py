import random
import ollama
import streamlit as st
import logging 
from llama_index.core.llms import ChatMessage
from llama_index.llms.ollama import Ollama

logging.basicConfig(level=logging.INFO)

def chat_short_story(length, genre, theme, tone, writing_style):
    # Set the system message for the assistant
    system_message = "You are a highly creative short story writer capable of writing across any genre."
    system_message += " and generate title for all the story created."
    
    # Construct the prompt with all the details
    prompt = (
        f"Write a creative short story of {length} words in the {genre} genre. "
        f"Use a {writing_style} writing style with a {tone} tone. "
        f"The story should revolve around the theme of {theme}. "
        f"and create a compelling narrative to captivate the audience."
    )

    # Interact with the model using ollama.chat
    result = ollama.chat(
        model="llama2",  # Replace with the correct model identifier you want to use
        messages=[
            {"role": "system", "content": system_message},
            {"role": "user", "content": prompt},
        ]
    )

    # Assuming the result contains a key "content" for the story output
    return result["message"]["content"]

# Predefined options
Length = [100, 250, 750]
Length = [l for l in Length if l >= 100]
r_length = random.choice(Length)

Genre = [
    "Fiction", "Nonfiction", "Drama", "Poetry", "Fantasy", "Horror", "Mystery",
    "Science Fiction", "Suspense", "Women's fiction", "Supernatural/Paranormal", "Young adult"
]
r_genre = random.choice(Genre)

Themes = [
    "Love", "Redemption", "Forgiveness", "Coming of age", "Revenge", "Good vs evil",
    "Bravery and hardship", "The power of social status", "The destructive nature of love",
    "The fallibility of the human condition"
]
r_themes = random.choice(Themes)

Writing_Styles = ["Expository", "Narrative", "Descriptive", "Persuasive", "Creative"]
r_Style = random.choice(Writing_Styles)

Tones = ["Formal", "Optimistic", "Worried", "Friendly", "Curious", "Assertive", "Encouraging"]
r_tones = random.choice(Tones)

# Streamlit Interface setup
st.title("Welcome to the Patrick's Story Generator")

story_length = st.slider("Story Length", min_value=100, max_value=2500, value=100)
story_genre = st.selectbox("Story Genre", options=Genre)
story_theme = st.selectbox("Story Theme", options=Themes)
writing_style = st.selectbox("Writing Style", options=Writing_Styles)
story_tone = st.selectbox("Story Tone", options=Tones)

if st.button("Generate Story"):
    story = chat_short_story(story_length, story_genre, story_theme, story_tone, writing_style)
    st.write(story)
