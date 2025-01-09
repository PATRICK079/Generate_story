import random
import streamlit as st
import ollama
import logging

# Ensure you have Llama 2 model pulled in Ollama
try:
    ollama.pull("llama2")  # Pulls the Llama 2 model if it's not already pulled
except Exception as e:
    logging.error(f"Error pulling Llama 2 model: {e}")

def chat_short_story(length, genre, theme, tone, writing_style):
    # Set the system message for the assistant
    system_message = "You are a highly creative short story writer capable of writing across any genre."
    system_message += " and generate title for all the stories created."
    
    # Construct the prompt with all the details
    prompt = (
        f"Write a creative short story of {length} words in the {genre} genre. "
        f"Use a {writing_style} writing style with a {tone} tone. "
        f"The story should revolve around the theme of {theme}. "
        f"and create a compelling narrative to captivate the audience."
    )

    # Interact with the model using ollama.chat with the correct URL
    url = "http://localhost:11434/api/chat"  # Update with the correct Ollama API endpoint URL
    try:
        result = ollama.chat(
            model="llama2",  # Use Llama 2 model
            messages=[
                {"role": "system", "content": system_message},
                {"role": "user", "content": prompt},
            ],
            url=url  # Specify the custom URL for Ollama API
        )

        # Assuming the result contains a key "content" for the story output
        return result["message"]["content"]
    
    except Exception as e:
        logging.error(f"Error generating the story: {e}")
        return "Error generating the story. Please try again later."

# Streamlit interface setup
st.title("Welcome to Patrick's Story Generator")

# Predefined options for story attributes
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

# Streamlit input components
length = st.slider("Story Length", min_value=100, max_value=2500, value=r_length, step=50)
genre = st.selectbox("Story Genre", Genre, index=Genre.index(r_genre))
theme = st.selectbox("Story Theme", Themes, index=Themes.index(r_themes))
writing_style = st.selectbox("Writing Style", Writing_Styles, index=Writing_Styles.index(r_Style))
tone = st.selectbox("Story Tone", Tones, index=Tones.index(r_tones))

# Generate story button
if st.button("Generate Story"):
    story = chat_short_story(length, genre, theme, tone, writing_style)
    st.subheader("Generated Story:")
    st.write(story)
