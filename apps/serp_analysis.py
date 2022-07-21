from collections import Counter
from st_aggrid import GridUpdateMode, AgGrid, GridOptionsBuilder, DataReturnMode
from utils import *
import utils

langs, locs, data = load_lang_loc_file('data/ll.json')


def app():
    with st.expander("ℹ️ - About this app "):
        st.markdown(
            """  
    This app, devoted to ✍️[Semantic Publishing](https://en.wikipedia.org/wiki/Semantic_publishing)✍️, relies on:
    -   [Text Razor API](https://www.textrazor.com/) for Named-Entity Recognition ([NER](https://en.wikipedia.org/wiki/Named-entity_recognition)) and Linking ([NEL](https://en.wikipedia.org/wiki/Entity_linking));
    -   [Google NLP API](https://cloud.google.com/natural-language) for NER and NEL;
    -   Wikipedia API for scraping entities description;
    -   For everything else, the beauty and power of 🐍Python🐍 and Streamlit.
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
    -   Discover how NLU (Natural Language Understanding) algorithms “understand” your text to optimize it until the topics which are more relevant to you have the best relevance/salience score;
    -   Analyze your SERP competitor’s main topics to discover possible topical gaps in your content;
    -   Generate the JSON-LD markup (and inject it into your page schema) to explicit which topics your page is about to search engines. Declare your main topic with the 'about' property. Use the 'mentions' property to declare your secondary topics. This is helpful for disambiguation purposes too;
    -   Analyze short texts such as a copy for an ad or a bio/description for an About-page (i.e., the [Entity Home](https://kalicube.com/faq/brand-serps/entity-home-in-seo-explainer/)).
           """
        )
    st.sidebar.info(
        '##### Read this article to [learn more about how to use The Entities Swissknife](https://studiomakoto.it/digital-marketing/entity-seo-semantic-publishing/).')

    if not author_serp_token:
        serp_key = st.text_input('Please enter a valid SERP API Key (Required)')
    else:
        serp_key = author_serp_token
    st.session_state.serp_key = serp_key

    # Search form starts here.
    col1, col2, col3, col4 = st.columns([1.8, 1.25, 1.25, 1.25])

    with col1:
        keywords = st.text_input("Search keywords", "", placeholder="Search keywords")

    with col2:
        location = st.selectbox(
            "location",
            locs,
        )
    with col3:
        language = st.selectbox(
            "language",
            data[location],
        )
    with col4:
        bsearch_clicked = st.button(label="Search")

    if bsearch_clicked:
        if not st.session_state.serp_key:
            st.warning("Please enter a valid SERP API Key")
            st.stop()
        if keywords == "":
            if "df" in st.session_state:
                del st.session_state.df
                st.session_state.extract_entities = False
            else:
                st.warning("Please enter a valid search keyword")
        else:
            st.session_state.keywords = keywords
            st.session_state.location = location
            st.session_state.language = language
            st.session_state.extract_entities = False
            # use dataforseo or serp scale api to get the search results
            with st.spinner(text="Fetching results"):
                st.session_state.df = get_serp_search_results(st.session_state.keywords, st.session_state.language,
                                                              st.session_state.location, st.session_state.serp_key)
    if "df" in st.session_state and "keywords" in st.session_state and keywords != "":
        df = st.session_state.df
        gb = GridOptionsBuilder.from_dataframe(df)
        gb.configure_default_column(value=True, enableRowGroup=True, aggFunc=None, editable=True)
        gb.configure_selection(selection_mode="multiple", use_checkbox=True)
        AgGrid(
            df,
            key="#" + st.session_state.keywords,
            gridOptions=gb.build(),
            enable_enterprise_modules=False,
            update_mode=GridUpdateMode.SELECTION_CHANGED,
            data_return_mode=DataReturnMode.AS_INPUT,
            height=400,
            reload_data=False,
            fit_columns_on_grid_load=True,
            configure_side_bar=False,
        )

        cl1, cl2 = st.columns([1.8, 0.4])
        with cl1:
            st.write("Select the dropdown option to exclude entities in analysis.")
        with cl2:
            selection = st.selectbox("", ["URL", "Text"])
        if selection == "Text":
            placeholder = "Albert Einstein was born at Ulm, in Württemberg, Germany, on March 14, 1879."
        else:
            placeholder = "https://en.wikipedia.org/wiki/Albert_Einstein"

        # add dropdown for url or text
        with cl1:
            st.session_state.selection = st.text_area("", placeholder=placeholder)
        with cl2:
            options = 30
            if st.session_state["#{}".format(st.session_state.keywords)]:
                options = len(st.session_state["#{}".format(st.session_state.keywords)]["selectedRows"]) + 1
                if options == 2:
                    options = 30
            no_of_pages = st.selectbox(label="min no. pages", options=list(range(1, options)), index=1)
        with cl1:
            submitted = st.button("Extract Entities")
        # use min number of pages to extract the entities
        st.session_state.extract_entities = True

        if submitted:
            with st.spinner(text="Getting entities"):
                # find entities in selected rows from st.session_state
                if "#{}".format(st.session_state.keywords) in st.session_state and st.session_state[
                    "#{}".format(st.session_state.keywords)] is not None:
                    # use textrazor for to get entities for different languages.
                    entities, total, con = get_entities(
                        st.session_state["#{}".format(st.session_state.keywords)]["selectedRows"],
                        st.session_state.language, author_textrazor_token)
                    e = entities[con.keys()].values.ravel().tolist()
                    e = [i for i in e if pd.isnull(i) == False]
                    c = Counter(e)
                    rows = len(st.session_state["#{}".format(st.session_state.keywords)]["selectedRows"])
                    max_count = max(rows, no_of_pages)
                    min_count = min(rows, no_of_pages)
                    c = {k: v for (k, v) in c.items() if min_count <= v <= max_count}
                    pages = pd.DataFrame({"Entities": c.keys(), "no of pages": c.values()})
                    for i, v in con.items():
                        c = entities.loc[entities[i].isin(pages["Entities"].values.tolist()), v].values.tolist()
                        pages = pd.concat([pages, pd.DataFrame({v: c}).reset_index(drop=True)], axis=1)
                    # df = pd.merge(df, pages, on='Entities', how='inner')
                    urls = list(total.keys()) + ["no of pages"]
                    df = pd.concat([pages, pd.DataFrame(columns=urls)])
                    for k, v in total.items():
                        for i, ent in df.iterrows():
                            if ent[0] in v.keys():
                                df.at[i, k] = v[ent[0]]
                    df.fillna(0, inplace=True)
                    df[urls] = df[urls].astype(int)
                    df["no of pages"] = df["no of pages"].astype(str)

                    if st.session_state.selection != "":
                        is_url = utils.is_url(st.session_state.selection)
                        not_present_entities, _ = get_entities_razor(author_textrazor_token,
                                                                     st.session_state.selection,
                                                                     st.session_state.language, is_url)
                        df = df[~df["Entities"].isin(not_present_entities["Entities"].values.tolist())]
                    utils.multi_conf(df, list(con.values()))
                    cols = ["Entities", "no of pages"]
                    for (k, v), (k2, v2) in zip(total.items(), con.items()):
                        cols.append(k)
                        cols.append(v2)
                    df = df[cols]
                    if len(df) > 0:
                        df.sort_values("Entities", inplace=True)
                        dfd = df
                        df = set_min_max(df)
                        st.write("### Entities")
                        st.table(df)

                        download_buttons = ""
                        download_buttons += utils.download_button(pd.DataFrame(dfd), "entities.csv",
                                                                  "Download Entities CSV ✨",
                                                                  pickle_it=False)
                        st.markdown(download_buttons, unsafe_allow_html=True)
                    else:
                        st.write("No entities found in selected pages.")
                else:
                    st.warning("Please select some rows")
