import streamlit as st
from googleapiclient.discovery import build
import google.generativeai as genai
import time

# CSS مخصص لإخفاء الروابط عند تمرير الفأرة
hide_links_style = """
    <style>
    a {
        text-decoration: none;
        color: inherit;
        pointer-events: none;
    }
    a:hover {
        text-decoration: none;
        color: inherit;
        cursor: default.
    }
    </style>
    """
st.markdown(hide_links_style, unsafe_allow_html=True)

# Set the title of the application
st.title('YouTube Content Creator')

# Input field for the keyword
keyword = st.text_input('Enter Topic To Create Content')

# YouTube API Key (replace 'YOUR_API_KEY' with your actual API key)
YOUTUBE_API_KEY = 'AIzaSyDCvbnrh3_ynhBqozI6dRFCKtrf_GHyrNU'
youtube = build('youtube', 'v3', developerKey=YOUTUBE_API_KEY)

# Generative AI API Key
GOOGLE_API_KEY = 'AIzaSyDbMa95_4sF1AtHpDOxKDRov7mRh0ldcqY'
genai.configure(api_key=GOOGLE_API_KEY)

# Create an instance of the GenerativeModel
model = genai.GenerativeModel('gemini-pro')

def search_videos(youtube, keyword, order='relevance'):
    try:
        search_response = youtube.search().list(
            q=keyword,
            part='id,snippet',
            maxResults=15,
            type='video',
            order=order
        ).execute()
    except Exception as e:
        st.error(f"Error in YouTube Data API, Try Again Later")
        raise

    titles = [item['snippet']['title'] for item in search_response['items']]
    return titles

# Prompt styles
prompt_styles = {
    "Concise Summary Style": f"Read all titles and analysis them as a concise summary, including the main points and key information. Then, create one succinct title from these summarized titles. Finally, generate a summary transcript in 100 lines for the concise title you've created only. only print title and script that you generated in output , nothing else,remeber your replay in same entring keyword language , Here are the video titles related to the keyword {keyword}:\n\n",
    "Educational Style": f"Read all titles and analysis them in an educational style, clearly explaining the information in a simple and systematic manner. Then, create one informative title from these educational titles. Finally, generate a  transcript in 100 lines for the educational title you've created only.only print title and script that you generated in output , nothing else, remeber your replay in same entring keyword language,Here are the video titles related to the keyword {keyword}:\n\n",
    "Factual News Style": f"Read all titles and analysis them in a factual news style, presenting the facts and information directly and clearly. Then, create one factual news title from these informative titles. Finally, generate a  transcript in 100 lines for the news title you've composed only. only print title and script that you generated in output , nothing else,remeber your replay in same entring keyword language,Here are the video titles related to the keyword {keyword}:\n\n",
    "Comedic Style": f"Read all titles and give them a comedic twist, filled with jokes and humor. Then, craft one hilarious title from these reimagined titles. Finally, generate a  transcript in 100 lines for the funny title you've created only.only print title and script that you generated in output , nothing else,remeber your replay in same entring keyword language, Here are the video titles related to the keyword {keyword}:\n\n",
    "Scary Style": f"Read all titles and infuse them with a sense of fear and tension, adding frightening elements and scary stories. Then, create one terrifying title from these spooky titles. Finally, generate a  transcript in 100 lines for the scary title you've written only. only print title and script that you generated in output , nothing else,remeber your replay in same entring keyword language,Here are the video titles related to the keyword {keyword}:\n\n",
    "Tragic Style": f"Read all titles and analysis them in a tragic style, highlighting sad emotions and tragic events. Then, create one sorrowful title from these tragic titles. Finally, generate a  transcript in 100 lines for the melancholic title you've composed only. only print title and script that you generated in output , nothing else,remeber your replay in same entring keyword language,Here are the video titles related to the keyword {keyword}:\n\n",
    "Mysterious Style": f"Read all titles and analysis them to be intriguing and full of mystery, keeping readers in suspense. Then, create one suspenseful title from these mysterious titles. Finally, generate a  transcript in 100 lines for the mysterious title you've crafted only.only print title and script that you generated in output , nothing else,remeber your replay in same entring keyword language, Here are the video titles related to the keyword {keyword}:\n\n",
    "Commentary and Impressionistic Style": f"Read all titles and analysis them in a commentary and impressionistic style, including personal opinions and interpretations. Then, create one impressionistic title from these subjective titles. Finally, generate a  transcript in 100 lines for the title you've written only, expressing your feelings and impressions towards it.only print title and script that you generated in output , nothing else, remeber your replay in same entring keyword language,Here are the video titles related to the keyword {keyword}:\n\n",
    "Promotional Style": f"Read all titles and analysis them in a promotional manner, focusing on the benefits and advantages with persuasive language. Then, create one compelling title from these promotional titles. Finally, generate a  transcript in 100 lines for the promotional title you've crafted only.only print title and script that you generated in output , nothing else,remeber your replay in same entring keyword language, Here are the video titles related to the keyword {keyword}:\n\n"
}

# Dropdown menu for selecting the style
style = st.selectbox('Choose the Style of the Content', list(prompt_styles.keys()))

# Button to start extracting the titles
if st.button('Start Creating'):
    if keyword:
        try:
            # Display a loading message
            with st.spinner('Creating Content...'):
                # Search for videos using the keyword with default order
                titles_default = search_videos(youtube, keyword, order='relevance')

                # Adding a small delay to avoid rate limiting
                time.sleep(5)

                # Search for videos using the keyword with 'viewCount' order
                titles_view_count = search_videos(youtube, keyword, order='viewCount')

                # Combine both lists of titles
                all_titles = titles_default + titles_view_count

                # Generate summary of the titles based on selected style
                prompt = prompt_styles[style].replace("{{keyword}}", keyword) + "\n".join(all_titles)
                response = model.generate_content(prompt)
                summary = response.text

                # Display the summary
                st.text_area('Summary', summary, height=300)

        except Exception as e:
            st.error(f"General Error, Try Again Later")
