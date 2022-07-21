import spacy
from streamlit_lottie import st_lottie

from apps import url_analysis, serp_analysis
from multipage import MultiApp
from utils import *

st.set_page_config(
    layout="wide",
    page_title="The Entities Swissknife",
    page_icon="https://cdn.shortpixel.ai/spai/q_lossy+ret_img+to_auto/https://studiomakoto.it/wp-content/uploads/2021/08/cropped-favicon-16x16-1-192x192.png",
    menu_items={
        "Get help": None,
        "Report a bug": None,
        "About": None
    }
)
local_css("assets/search.css")
lotti_path = load_lotti_file('data/tes.json')
if "en_nlp" not in st.session_state:
    st.session_state.en_nlp = spacy.load("en_core_web_sm")

if "it_nlp" not in st.session_state:
    st.session_state.it_nlp = spacy.load("it_core_news_sm")


hide_st_style = """
            <style>
            footer {visibility: hidden;}
            [title^='streamlit_lottie.streamlit_lottie'] {
                margin-bottom: -35px;
                margin-top: -90px;
            }
            </style>
            """
st.markdown(hide_st_style, unsafe_allow_html=True)
st.markdown(
    "###### [![this is an image link](https://studiomakoto.it/wp-content/uploads/2021/08/header-logo.webp)](https://studiomakoto.it/?utm_source=streamlit&utm_medium=app&utm_campaign=Entities-swissknife)")
st.markdown(
    "###### Made in [![this is an image link](https://i.imgur.com/iIOA6kU.png)](https://www.streamlit.io/) , with ❤️ by [@max_geraci](https://studiomakoto.it/makoto_member/massimiliano-geraci/)   |   [![Twitter Follow](https://img.shields.io/twitter/follow/max_geraci?style=social)](https://twitter.com/max_geraci)   |   [![this is an image link](https://i.imgur.com/thJhzOO.png)](https://www.buymeacoffee.com/MaxG.SEO)")

with st.sidebar:
    st_lottie(lotti_path, width=280, height=180, loop=False)

# I have to used multiple apps to handle the searching criteria. One for custom search and second for keyword search.
app = MultiApp()
app.add_app("URL Analysis", url_analysis.app)
app.add_app("SERP Analysis", serp_analysis.app)
app.run()
