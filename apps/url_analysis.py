from spacy_streamlit import visualize_parser
import utils
from utils import *


def app():

    with st.expander("ℹ️ - About this app "):
        st.markdown(
            """
            This app, devoted to ✍️[Semantic Publishing](https://en.wikipedia.org/wiki/Semantic_publishing)✍️, relies on:
            -   [Text Razor API](https://www.textrazor.com/) for Named-Entity Recognition ([NER](https://en.wikipedia.org/wiki/Named-entity_recognition)) and Linking ([NEL](https://en.wikipedia.org/wiki/Entity_linking));
            -   Wikipedia API for scraping entities description;
            -   For everything else, the beauty and power of 🐍Python🐍 and Steamlit.
            """
        )

    with st.expander("✍️ - Semantic Publishing "):
        st.write(
            """
            The Entities Swissknife (TES) is a 100% 🐍Python🐍 app for Semantic publishing, i.e., publishing information on the web as documents accompanied by semantic markup (using the [schema.org](https://schema.org) vocabulary in JSON-LD format). Semantic publication provides a way for machines to understand the structure and meaning of the published information, making information search and data integration more efficient.
            Semantic publishing relies on Structured Data adoption and Entity Linking (Wikification). Named entities are then injected into the JSON-LD markup to make the Content Topics explicit and 🥰Search engines friendly🥰: declare the main topic with the '[about](https://schema.org/about)' property and the secondary topics with the '[mentions](https://schema.org/mentions)' property).
            The 'about' property should refer to 1-2 entities/topics at most, and these entities should be present in your H1 title. The 'mentions' properties should be no more than 3-5 depending on the article's length; as a general rule, an entities/topics should be explicitly mentioned in your schema markup if there is at least one paragraph dedicated to them (and they are possibly present in the relative headline).
            The table with the "Top Entities by Frequency" takes into account for the Frequency count also the normalized entities and not only the exact word with which the entities are present in the text.
            """
        )

    with st.expander("🔎 - How TES can support your Semantic SEO tasks "):
        st.write(
            """
            -   Know how NLU (Natural Language Understanding) algorithms “understand” your text to optimize it until the topics which are more relevant to you have the best relevance/salience score;
            -   Analyze your SERP competitor’s main topics to discover possible topical gaps in your content;
            -   Generate the JSON-LD markup (and inject it into your page schema) to explicit which topics your page is about to search engines. Declare your main topic with the 'about' property. Use the 'mentions' property to declare your secondary topics. This is helpful for disambiguation purposes too;
            -   Analyze short texts such as a copy for an ad or a bio/description for an About-page (i.e., the [Entity Home](https://kalicube.com/faq/brand-serps/entity-home-in-seo-explainer/)).
            """
        )
    df = None
    language_option = None
    with st.form("my_form"):
        input_type_selectbox = st.sidebar.selectbox(
            "Choose what you want to analyze",
            ("URL", "Text", "URL vs URL")
        )
        st.sidebar.info(
            '##### Read this article to [learn more about how to use The Entities Swissknife](https://studiomakoto.it/digital-marketing/entity-seo-semantic-publishing/).')

        if not author_textrazor_token:
            text_razor_key = st.text_input('Please enter a valid TextRazor API Key (Required)')
        else:
            text_razor_key = author_textrazor_token

        if input_type_selectbox == "URL":
            text_input = st.text_input('Please enter a URL',
                                       placeholder='https://gofishdigital.com/what-is-semantic-seo/')
            meta_tags_only = st.checkbox('Extract Entities only from meta tags (tag_title, meta_description & H1-4)')

            if "last_field_type" in st.session_state and st.session_state.last_field_type != input_type_selectbox:
                st.session_state.text_razor = False
            st.session_state.last_field_type = input_type_selectbox
        elif input_type_selectbox == "Text":
            if "last_field_type" not in st.session_state:
                st.session_state.last_field_type = input_type_selectbox
                st.session_state.text_razor = False
            if st.session_state.last_field_type != input_type_selectbox:
                st.session_state.text_razor = False
            st.session_state.last_field_type = input_type_selectbox
            meta_tags_only = False
            text_input = st.text_area('Please enter a text',
                                      placeholder='Posts involving Semantic SEO at Google include structured data, schema, and knowledge graphs, with SERPs that answer questions and rank entities - Bill Slawsky.')
        elif input_type_selectbox == "URL vs URL":
            if "last_field_type" in st.session_state and st.session_state.last_field_type != input_type_selectbox:
                st.session_state.text_razor = False
            meta_tags_only = False
            st.session_state.last_field_type = input_type_selectbox

            url1 = st.text_input(label='Enter first URL')
            url2 = st.text_input(label='Enter second URL')

            are_urls = utils.is_url(url1) and utils.is_url(url2)
            urls = [url1, url2]
            text_input = "None"

        is_url = utils.is_url(text_input)
        if input_type_selectbox != "URL vs URL":
            spacy_pos = st.checkbox('Process Part-of-Speech analysis with SpaCy')
            extract_categories_topics = st.checkbox('Extract Categories and Topics')
        scrape_all = st.checkbox(
            "Scrape ALL the Entities descriptions from Wikipedia. This is a time-consuming task, so grab a coffee if you need all the descriptions in your CSV file. The descriptions of the Entities you select for your 'about' and 'mentions' schema properties will be scraped and present in the corresponding JSON-LD files")
        submitted = st.form_submit_button("Submit")
        if submitted:
            if not text_razor_key:
                st.warning("Please fill out all the required fields")
            elif not text_input:
                st.warning("Please Enter a URL/Text in the required field")
            else:
                st.session_state.submit = True
                if input_type_selectbox == "URL vs URL":
                    output1, output2, entities1, entities2, language = utils.get_df_url2url_razor(text_razor_key, urls,
                                                                                                  are_urls)
                    st.session_state.text_razor = True
                    st.session_state.google_api = False
                    st.session_state.df_url1 = pd.DataFrame(output1)
                    st.session_state.df_url2 = pd.DataFrame(output2)
                    lang = language
                else:
                    output, response, topics_output, categories_output = utils.get_df_text_razor(text_razor_key,
                                                                                                 text_input,
                                                                                                 extract_categories_topics,
                                                                                                 is_url, scrape_all)
                    st.session_state.text = response.cleaned_text
                    st.session_state.text_razor = True
                    st.session_state.google_api = False
                    st.session_state.df_razor = pd.DataFrame(output)
                    if topics_output:
                        st.session_state.df_razor_topics = pd.DataFrame(topics_output)
                    if categories_output:
                        st.session_state.df_razor_categories = pd.DataFrame(categories_output)
                    lang = response.language
                st.session_state.lang = lang
                language_option = lang

    if 'submit' in st.session_state and ("text_razor" in st.session_state and st.session_state.text_razor == True):
        if st.session_state.last_field_type == "URL vs URL":
            df1 = st.session_state["df_url1"].drop(columns=["DBpedia Category", "Wikidata Id", "Wikipedia Link"])
            df2 = st.session_state["df_url2"].drop(columns=["DBpedia Category", "Wikidata Id", "Wikipedia Link"])
            ab = pd.merge(df1, df2, how='inner', on=["name"])
            ab.dropna(inplace=True)
            names = pd.DataFrame({"Entities": ab["name"].values.tolist()})
            amb = df1[~df1.name.isin(ab.name)]
            bma = df2[~df2.name.isin(ab.name)]
            st.write("### Entities")
            col1, col2, col3 = st.columns([1.25, .75, 3])
            col1.markdown("Entities in both URLs")
            col1.write(names)
            with col2:
                selection = st.radio(label='Select Entities', options=['Url1 only', 'Url2 only'])

            if "Url1 only" == selection:
                col3.markdown("Entities in Url1")
                col3.write(amb)
            elif "Url2 only" == selection:
                col3.markdown("Entities in Url2")
                col3.write(bma)

            download_buttons = ""
            download_buttons += utils.download_button(names, 'url_common.csv',
                                                      'Download common Entities CSV ✨', pickle_it=False)
            if not amb.empty:
                download_buttons += utils.download_button(amb, 'url1-url2.csv',
                                                          'Download url1 Entities CSV ✨', pickle_it=False)
            else:
                st.write("0 entities in url1 which are not present in url2")
            if not bma.empty:
                download_buttons += utils.download_button(bma, 'url2-url1.csv',
                                                          'Download url2 Entities CSV ✨', pickle_it=False)
            else:
                st.write("0 entities in url2 which are not present url1")
            st.markdown(download_buttons, unsafe_allow_html=True)

        else:
            text_input, is_url = utils.write_meta(text_input, meta_tags_only, is_url)
            if 'df_razor' in st.session_state:
                df = st.session_state["df_razor"]

            if len(df) > 0:
                df['temp'] = df['Relevance Score'].str.strip('%').astype(float)
                df = df.sort_values('temp', ascending=False)
                del df['temp']
                selected_about_names = st.multiselect('Select About Entities:', df.name)
                selected_mention_names = st.multiselect('Select Mentions Entities:', df.name)
                utils.word_frequency(df, text_input, language_option, st.session_state.text)
                st.write('### Entities', df)
                df = df.sort_values('Frequency', ascending=False)
                st.write('### Top 10 Entities by Frequency', df[['name', 'Frequency']].head(10))
            utils.conf(df, "Confidence Score")

            c, t = st.columns(2)
            if 'df_razor_categories' in st.session_state and extract_categories_topics:
                with c:
                    df_categories = st.session_state["df_razor_categories"]
                    st.write('### Categories', df_categories)
            if 'df_razor_topics' in st.session_state and extract_categories_topics:
                with t:
                    df_topics = st.session_state["df_razor_topics"]
                    st.write('### Topics', df_topics)

            if len(df) > 0:
                about_download_button = utils.download_button(
                    utils.convert_schema("about",
                                         df.loc[df['name'].isin(selected_about_names)].to_json(orient='records'),
                                         scrape_all, st.session_state.lang), 'about-entities.json',
                    'Download About Entities JSON-LD ✨', pickle_it=False)
                if len(df.loc[df['name'].isin(selected_about_names)]) > 0:
                    st.markdown(about_download_button, unsafe_allow_html=True)
                mention_download_button = utils.download_button(utils.convert_schema("mentions", df.loc[
                    df['name'].isin(selected_mention_names)].to_json(orient='records'), scrape_all,
                                                                                     st.session_state.lang),
                                                                'mentions-entities.json',
                                                                'Download Mentions Entities JSON-LD ✨', pickle_it=False)
                if len(df.loc[df['name'].isin(selected_mention_names)]) > 0:
                    st.markdown(mention_download_button, unsafe_allow_html=True)
            if "df_razor_topics" in st.session_state and extract_categories_topics:
                df_topics = st.session_state["df_razor_topics"]
                download_buttons = ""
                download_buttons += utils.download_button(df_topics, 'topics.csv', 'Download all Topics CSV ✨',
                                                          pickle_it=False)
                st.markdown(download_buttons, unsafe_allow_html=True)
            if "df_razor_categories" in st.session_state and extract_categories_topics:
                df_categories = st.session_state["df_razor_categories"]
                download_buttons = ""
                download_buttons += utils.download_button(df_categories, 'categories.csv',
                                                          'Download all Categories CSV ✨',
                                                          pickle_it=False)
                st.markdown(download_buttons, unsafe_allow_html=True)
            if len(df) > 0:
                download_buttons = ""
                download_buttons += utils.download_button(df, 'entities.csv', 'Download all Entities CSV ✨',
                                                          pickle_it=False)
                st.markdown(download_buttons, unsafe_allow_html=True)
            if spacy_pos:
                if st.session_state.lang in "eng":
                    doc = st.session_state.en_nlp(st.session_state.text)
                elif st.session_state.lang in "ita":
                    doc = st.session_state.it_nlp(st.session_state.text)
                visualize_parser(doc)
