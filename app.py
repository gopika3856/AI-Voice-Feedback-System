import streamlit as st
import whisper
from gtts import gTTS
import os

st.set_page_config(page_title="AI Voice Feedback System")

st.title("Customer Feedback System")

uploaded_file = st.file_uploader(
    "Upload Customer Voice Feedback",
    type=["mp3", "wav", "m4a"]
)

if uploaded_file is not None:

    st.audio(uploaded_file)

    # Save uploaded audio
    with open("temp_audio.wav", "wb") as f:
        f.write(uploaded_file.getbuffer())

    st.success("Audio uploaded successfully!")

    if st.button("Convert Voice to Text"):

        with st.spinner("Converting voice to text..."):

            model = whisper.load_model("base")

            result = model.transcribe("temp_audio.wav")

            feedback_text = result["text"]

        st.subheader("Customer Feedback")
        st.write(feedback_text)

        # Sentiment Analysis
        feedback_lower = feedback_text.lower()

        positive_words = [
            "good", "great", "excellent", "super",
            "nice", "best", "awesome", "perfect"
        ]

        negative_words = [
            "bad", "poor", "worst", "problem",
            "not good", "damage", "issue"
        ]

        if any(word in feedback_lower for word in positive_words):

            sentiment = "Positive"

            reply_text = (
                "Thank you very much for your valuable feedback. "
                "We are delighted that you liked our marble work. "
                "Please feel free to contact us again for future orders."
            )

        elif any(word in feedback_lower for word in negative_words):

            sentiment = "Negative"

            reply_text = (
                "Thank you for your feedback. "
                "We sincerely apologize for the inconvenience caused. "
                "We will definitely work on improving our service. "
                "Your comments are very valuable to us."
            )

        else:

            sentiment = "Neutral"

            reply_text = (
                "Thank you for your feedback. "
                "Your comments are important to us. "
                "We appreciate your support."
            )

        # Display Sentiment
        st.subheader("Customer Satisfaction")
        st.write(sentiment)

        # Display AI Reply
        st.subheader("Response")
        st.write(reply_text)

        # Convert Reply to Voice
        tts = gTTS(text=reply_text, lang='en')
        tts.save("reply.mp3")

        # Play Voice Reply
        st.subheader("Response")
        st.audio("reply.mp3")