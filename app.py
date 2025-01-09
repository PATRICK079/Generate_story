import random
import httpx  # To make HTTP requests to the Ollama API
import streamlit as st
import logging
import ollama
logging.basicConfig(level=logging.INFO)

# Function to generate short story using Ollama API
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

    # Interact with the model using Ollama API
    url = "http://localhost:11434/api/generate"  # Local Ollama API URL
    payload = {
        "input": prompt
    }

    # Send the request to Ollama API and get the response
    try:
        with httpx.Client() as client:
            response = client.post(url, json=payload)
            response.raise_for_status()  # Will raise an error for non-200 status codes
            data = response.json()
            # Assuming 'content' holds the story output
            return data["content"]
    except httpx.RequestError as e:
        logging.error(f"Error while requesting Ollama API: {e}")
        return "Error generating the story. Please try again later."
    except KeyError:
        logging.error("Unexpected response structure from the API")
        return "Error: Invalid response from the API."


# Predefined options for random selection
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

# User inputs for the story parameters
story_length = st.slider("Story Length", min_value=100, max_value=2500, value=100)
story_genre = st.selectbox("Story Genre", options=Genre)
story_theme = st.selectbox("Story Theme", options=Themes)
writing_style = st.selectbox("Writing Style", options=Writing_Styles)
story_tone = st.selectbox("Story Tone", options=Tones)

# Generate the story when the button is pressed
if st.button("Generate Story"):
    story = chat_short_story(story_length, story_genre, story_theme, story_tone, writing_style)
    st.write(story)
