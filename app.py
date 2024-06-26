import streamlit as st
import streamlit.components.v1 as components

from datetime import datetime, timedelta
from services.searchNews import SearchNews
from services.articlesToTranscript import TranscriptWriter
from services.textToSpeech import TextToSpeech
import time

# Define the user inputs as Streamlit widgets
st.title("yoursDaily\nYour daily AI generated podcast.")

# Options for topics of interest
topics = ["Artificial Intelligence", "Tennis", "Politics", "Economics"]
USER_PREFERENCES = st.multiselect("Select your topics of interest", topics, default=[])

# Toggle for custom topic input
custom_topic = None
with st.expander("Interested in something else ? Add a custom topic"):
    custom_topic = st.text_input("Enter a custom topic")
    if st.button("Add Custom Topic"):
        if custom_topic:
            USER_PREFERENCES.append(custom_topic)
            topics.append(custom_topic)
            st.success(f"Topics are now: {USER_PREFERENCES}")
        else:
            st.error("Please enter a valid topic.")

# Mapping options to days
time_options = {
    "Last 24 hours": 1,
    "Last week": 7,
    "Last month": 30
}
time_range = st.selectbox("Select the time range for news articles", list(time_options.keys()))
DAYS_AGO = time_options[time_range]

date_cutoff = (datetime.now() - timedelta(days=DAYS_AGO)).strftime("%Y-%m-%d")

if st.button("Generate Podcast"):
    # Update the preferences string
    preferences = USER_PREFERENCES + [custom_topic]
    rephrased_preferences = " or ".join([f"Recent news about {topic}" for topic in preferences])
    st.success(rephrased_preferences)

    with st.status("Searching for news...") as status:
        search_client = SearchNews()
        news = search_client.run(
            query=rephrased_preferences,
            date_cutoff=date_cutoff,
            num_results=10
        )
        time.sleep(1)  # Simulate time taken to search news
        st.write(f"Number of articles retrieved: {len(news)}")
        sources = set(article['source'] for article in news if article['source'] is not None)
        sources_list = ', '.join(source for source in sources)
        st.write(f"Found related news from the following sources: {sources_list}")
        status.update(label="News search complete!", state="complete")
    
    with st.status("Creating transcript from news articles...") as status:
        writer = TranscriptWriter()
        transcript = writer.run(
            articles=news,
            user_preferences=rephrased_preferences,
            length=4096
        )
        time.sleep(1)  # Simulate time taken to create transcript
        status.update(label="Transcript creation complete!", state="complete")

    with st.status("Generating podcast from transcript...") as status:
        podcast = TextToSpeech(voice_id="Xb7hH8MSUJpSbSDYk0k2")
        podcast_path = podcast.run(
            text=transcript,
            transcript_name=f"{date_cutoff}-123"
        )
        time.sleep(1)  # Simulate time taken to generate podcast
        status.update(label="Podcast generation complete!", state="complete")

    # Display the audio file to play
    st.write("Podcast generated:")
    st.audio(podcast_path)

    st.write("Like it ? Download your podcast and share it on Twitter/X:")
    components.html(
    f"""
        <a href="https://twitter.com/share?ref_src=twsrc%5Etfw" class="twitter-share-button" 
        data-text="Check out my AI generated podcast on {rephrased_preferences}🎈" 
        data-url="https://github.com/IronJayx/yoursDaily"
        data-show-count="false">
        data-size="Large" 
        data-hashtags="streamlit,python"
        Tweet
        </a>
        <script async src="https://platform.twitter.com/widgets.js" charset="utf-8"></script>
    """
    )   

    # Display URLs of the retrieved news
    st.write("Want to dive deeper? Here is the list of articles used to generate the audio:")
    for article in news:
        st.write(f"- [{article['title']}]({article['url']})")

