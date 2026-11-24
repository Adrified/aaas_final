import streamlit as st
import pandas as pd

# colle ici le lien CSV publie de ton Google Sheet
# si c'est vide, on utilise examples.csv
SHEET_URL = ""

st.set_page_config(page_title="Who Tells Africa's Story?", layout="wide")


@st.cache_data(ttl=300)
def load_data():
    if SHEET_URL == "":
        df = pd.read_csv("examples.csv")
    else:
        df = pd.read_csv(SHEET_URL)
    # cellules vides -> texte vide
    df = df.fillna("").astype(str)
    return df


def make_options(df, column):
    options = ["All"]
    for value in sorted(df[column].unique()):
        if value != "":
            options.append(value)
    return options


def show_card(row):
    with st.container(border=True):
        st.markdown("**" + row["title"] + "**")
        st.caption(row["type"] + " | " + row["country"] + " | " + row["platform"])

        if row["creator_or_outlet"] != "":
            st.write("By: " + row["creator_or_outlet"])
        if row["theme"] != "":
            st.write("Theme: " + row["theme"])

        # l'analyse avec le scholar
        if row["analysis"] != "":
            st.markdown("**What it shows** (" + row["scholar"] + ")")
            st.write(row["analysis"])
        if row["limits"] != "":
            st.markdown("**Limits**")
            st.write(row["limits"])

        if row["link"] != "":
            st.markdown("[Open the original](" + row["link"] + ")")


def show_cards(df):
    if len(df) == 0:
        st.info("No examples match these filters.")
    else:
        for index, row in df.iterrows():
            show_card(row)


df = load_data()

st.title("Who Tells Africa's Story?")

tab_about, tab_framework, tab_explore, tab_compare, tab_sources = st.tabs(["About", "Framework", "Explore", "Compare", "Sources"])


# page d'intro, change le texte si tu veux
with tab_about:
    st.header("The argument")
    st.write(
        "Western media keeps telling one story about Africa: a place of poverty, "
        "conflict, and need. That story continues the colonial erasure Nkrumah and "
        "Woodson wrote about. Online, African creators are telling their own stories "
        "and pushing back. But digital platforms have their own gatekeepers, so they "
        "do not remove the power behind the old story."
    )
    st.header("How to use this site")
    st.write(
        "Framework explains the scholars behind the project. "
        "Explore lets you filter examples by country, theme, and type. "
        "Compare puts Western coverage next to African-made work on the same theme. "
        "Each card says what the example shows, and for African-made work, where it fell short."
    )
    st.header("How I picked the examples")
    st.write(
        "Each example links to the original. My note on each one says what it shows. "
        "These are my choices, so they shape the story too."
    )


# les scholars, en mots simples
with tab_framework:
    st.header("Where the single story comes from")

    st.subheader("Woodson and Nkrumah")
    st.write(
        "Woodson argued that schooling taught Black people to see themselves through the eyes "
        "of those who oppressed them. Nkrumah argued that African history was erased and retold "
        "through a European lens. Western media carries that same habit outside the classroom."
    )

    st.subheader("Terence Ranger: invented tradition")
    st.write(
        "Ranger shows that colonial officials did not just describe Africa, they rewrote it. "
        "They wrote down African custom and turned flexible practice into fixed rules. "
        "They also believed every African belonged to a tribe, even though most Africans moved "
        "between many identities. As Ranger puts it, quoting John Iliffe: Europeans believed "
        "Africans belonged to tribes; Africans built tribes to belong to. "
        "Treating Africa as one simple, unchanging place is an old colonial move, not just a media mistake."
    )

    st.subheader("Chimamanda Ngozi Adichie: the single story")
    st.write(
        "Adichie says a single story is made by showing a people as one thing over and over. "
        "The problem with stereotypes is not that they are untrue but that they are incomplete. "
        "She ties this to power: who tells the story, and whose version becomes the definitive one."
    )

    st.header("What digital space changes, and what it doesn't")

    st.subheader("Nanjala Nyabola: Kenyans on Twitter")
    st.write(
        "Nyabola shows how #KOT used Twitter to talk back to CNN and to their own government. "
        "She calls this a networked public sphere where locals can build their own counternarrative."
    )
    st.write(
        "But she also shows the limits. People online are a subset of a subset: those with electricity, "
        "internet, and accounts. Governments pay for bots and bloggers to push their side. "
        "And in 2016 Uganda shut down social media during its election, and people had to use VPNs to get around it."
    )


with tab_explore:
    col1, col2, col3 = st.columns(3)
    with col1:
        country = st.selectbox("Country", make_options(df, "country"))
    with col2:
        theme = st.selectbox("Theme", make_options(df, "theme"))
    with col3:
        kind = st.selectbox("Type", make_options(df, "type"))

    filtered = df
    if country != "All":
        filtered = filtered[filtered["country"] == country]
    if theme != "All":
        filtered = filtered[filtered["theme"] == theme]
    if kind != "All":
        filtered = filtered[filtered["type"] == kind]

    st.write(str(len(filtered)) + " examples")
    show_cards(filtered)


# cote a cote: western vs african-made
with tab_compare:
    compare_theme = st.selectbox("Pick a theme", make_options(df, "theme"), key="compare_theme")

    picked = df
    if compare_theme != "All":
        picked = picked[picked["theme"] == compare_theme]

    left, right = st.columns(2)
    with left:
        st.subheader("Western coverage")
        show_cards(picked[picked["type"] == "Western coverage"])
    with right:
        st.subheader("African-made")
        show_cards(picked[picked["type"] == "African-made"])


with tab_sources:
    st.header("Scholarly sources")
    st.markdown(
        "- Adichie, Chimamanda Ngozi. \"The Danger of a Single Story.\" TED Talk, 2009.\n"
        "- Nkrumah, Kwame. \"The African Genius.\" Speech, 1963.\n"
        "- Nyabola, Nanjala. *Digital Democracy, Analogue Politics: How the Internet Era Is Transforming "
        "Politics in Kenya.* London: Bloomsbury Academic & Professional, 2018.\n"
        "- Ranger, Terence. \"The Invention of Tradition in Colonial Africa.\" In *The Invention of Tradition*, "
        "edited by Eric Hobsbawm and Terence Ranger, 211-262. Cambridge: Cambridge University Press, 1983.\n"
        "- Woodson, Carter G. *The Mis-Education of the Negro.* 1933."
    )

    # les exemples viennent du sheet
    st.header("Examples (primary sources)")
    for index, row in df.iterrows():
        line = "- " + row["title"] + ", " + row["creator_or_outlet"]
        if row["link"] != "":
            line = line + ". [Link](" + row["link"] + ")"
        st.markdown(line)
