import openai
import streamlit as st

# Set up your OpenAI API key here (replace with your key)
openai.api_key = "your-openai-api-key"

# Dropdown to select summary length
summary_length = st.selectbox("Select Summary Length:", ["Short", "Medium", "Long"])

# Map selected summary length to max_tokens
def get_max_tokens(length):
    if length == "Short":
        return 100
    elif length == "Medium":
        return 200
    else:
        return 300


# Function to summarize text using GPT-4
def summarize_text(input_text):
    try:
        # Request GPT-4 to summarize the text
        max_tokens = get_max_tokens(summary_length)  # corrected variable name
        response = openai.Completion.create(
            engine="text-davinci-003",  # Choose GPT-4 if available, or use a relevant model
            prompt=f"Summarize the following text in a concise way:\n\n{input_text}",
            max_tokens=max_tokens,  # Limit tokens to control summary length
            temperature=0.5,  # Controls creativity
        )
        summary = response.choices[0].text.strip()
        return summary
    except Exception as e:
        return f"Error: {e}"

# Streamlit App Layout
st.title("Automated Content Summarization Tool")
st.write("Enter your text below, and we'll summarize it for you.")

# Text input from the user
user_input = st.text_area("Input text to summarize", height=250)

# Initialize the summary variable to None
summary = None

# Button to trigger summarization
if st.button("Summarize"):
    if user_input:
        with st.spinner("Generating summary..."):
            summary = summarize_text(user_input)
            st.subheader("Summary:")
            st.write(summary)
    else:
        st.error("Please input some text to summarize!")

# Button to clear input
if st.button("Clear"):
    st.session_state['user_input'] = ''

# Display download button if summary is generated
if summary:
    st.download_button(
        label="Download Summary as Text File",
        data=summary,
        file_name="summary.txt",
        mime="text/plain"
    )
