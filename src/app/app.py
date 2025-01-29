import os
import json
import pandas as pd
import matplotlib.pyplot as plt
import shutil

import streamlit as st
from streamlit_javascript import st_javascript

from get_data import get_sentences
from classify import classify_sentences

from config import Config

##################################################
#
# Configurable Settings (those affecting the UI)
#

histogram_horizontal = Config["histogram_horizontal"]  # Horizontal or vertical histogram
default_granularity =  Config["default_granularity"]  # Default granularity for intent classification

st.set_page_config(
    page_title="Intentify",  # Title that appears in the browser tab
    page_icon="🌟",  # Favicon that appears in the browser tab
    # layout="wide"  # Optional: Use "wide" or "centered" layout
)


##################################################
#
# App Settings (those not affecting the UI)
#

data_dir = Config["data_dir"]
data_file_name = Config["data_file_name"]
data_file = f"{data_dir}/{data_file_name}"
if not os.path.exists(data_dir):
    os.makedirs(data_dir)

cache_dir = Config["cache_dir"]
if not os.path.exists(cache_dir):
    os.makedirs(cache_dir)

# Default Intent Data
intent_data = {
    "metadata": {
        "granularity": default_granularity,
        "lines": 0,
        "sentences": 0,
        "intents": 0,
    },
    "intents": {},
}


##################################################
#
# UI CSS Styling
#
# st.write("<a name='top'></a>", unsafe_allow_html=True)


##################################################
#
# UI App starts here
#
st.write("<div style='text-align: center; font-weight: bold; font-size: 30px;'>Welcome to Intentify</div>", unsafe_allow_html=True)
st.write("<div style='text-align: center; font-weight: bold; font-size: 20px;'>Your Intent Analysis Dashboard</div>", unsafe_allow_html=True)
st.write(
    """
    <div style='text-align: center; font-weight: bold; font-size: 16px;'>
    <a href="#granularity-setting">Metadata</a>
    &nbsp; | &nbsp;
    <a href="#intent-counts">Intent Counts</a>
    &nbsp; | &nbsp;
    <a href="#intents">Intents</a>
    &nbsp; | &nbsp;
    <a href="#data-files">Data Files</a>
    </div>
    """,
    unsafe_allow_html=True
)
st.write("<div style='text-align: center; font-size: 16px;'>You may press R to refresh.</div>", unsafe_allow_html=True)

url = st_javascript("await fetch('').then(r => window.parent.location.href)")

st.markdown(
    """
    <style>
    .slider-labels {
        display: flex;
        justify-content: space-between;
        margin-top: -10px; /* Adjust vertical spacing */
        font-size: 0.9rem; /* Adjust font size */
    }
    </style>
    """,
    unsafe_allow_html=True
)


##################################################
#
# Show Metadata
#

col1, col2, col3 = st.columns([5, 1, 3])


##################################################
# Granularity Slider

with col1:
    st.subheader("Granularity Setting")

    granularity = st.slider(
        " ",
        min_value=0,
        max_value=100,
        value=intent_data["metadata"]["granularity"], # default_granularity,
        step=1
    )
    # st.write(f"DEBUG: Granularity: {granularity}")
    st.markdown(
        """
        <div class="slider-labels">
            <span>Less Intents</span>
            <span>More Intents</span>
        </div>
        """,
        unsafe_allow_html=True
    )


##################################################
# Load or generate Intent Data
# This block needs to come after the Granularity Slider block to get the latest granularity value

intent_data_dir = f"{cache_dir}"
intent_data_file_name = f"intent_data_t{granularity}.json"
intent_data_file = f"{intent_data_dir}/{intent_data_file_name}"
# st.write(f"DEBUG: Reading intent data from file: {intent_data_file}")
if os.access(intent_data_file, os.R_OK):
    # Load the intent data from the JSON file
    with open(intent_data_file, "r") as file:
        intent_data = json.load(file)
else:
    with st.spinner(f"Generating intent data with a granularity of {granularity}... Please wait"):
        # Generate intent data using classify_sentences function
        sentences, lines = get_sentences(data_file)
        intents = classify_sentences(sentences, granularity)
        intent_data = {
            "metadata": {
                "granularity": granularity,
                "lines": len(lines),
                "sentences": len(sentences),
                "intents": len(intents),
            },
            "intents": intents,
        }
        # Save the intent data to the JSON file
        with open(intent_data_file, "w") as file:
            json.dump(intent_data, file, indent=2)


##################################################
# Metadata
# This block needs to come after the Load or generate Intent Data block to get the latest intent_data

metadata = intent_data["metadata"]

with col3:
    st.markdown(
        f"""
        | Metadata | Value |
        | --- | --- |
        | Intents | {metadata["intents"]} |
        | Calls | {metadata["lines"]} |
        | Unique Sentences | {metadata["sentences"]} |
        | Granularity | {granularity} |
        """
    )

st.markdown("[[top]](#granularity-setting)")


##################################################
#
# Show Histogram of Intent Counts
#

intent_counts = {intent: len(sentences) for intent, sentences in intent_data["intents"].items()}
intent_counts = dict(sorted(intent_counts.items(), key=lambda item: item[1], reverse=True))
intent_df = pd.DataFrame(list(intent_counts.items()), columns=["Intent", "Count"]).sort_values(by="Count", ascending=histogram_horizontal)

st.subheader("Intent Counts")
if histogram_horizontal:
    plt.barh(intent_df["Intent"], intent_df["Count"], color="blue")
    plt.xlabel("Count")
    plt.ylabel("Intent")
    plt.title("Intent Counts")
    st.pyplot(plt)
else:
    # st.bar_chart(intent_df.set_index("Intent"))
    fig, ax = plt.subplots()
    ax.bar(intent_df["Intent"], intent_df["Count"], color="blue", edgecolor="black")
    ax.set_title("Intent Counts")
    ax.set_xlabel("Intent")
    ax.set_ylabel("Count")
    ax.set_xticklabels(intent_df["Intent"], rotation=90)
    st.pyplot(fig)

st.markdown("[[top]](#granularity-setting)")


##################################################
#
# Show An Expandable List of Intents
#

st.subheader("Intents")
for intent in intent_counts:
    with st.expander(f"{intent} ({intent_counts[intent]} sentences)"):
        for sentence in intent_data["intents"][intent]:
            st.write(f"- {sentence}")

st.markdown("[[top]](#granularity-setting)")



##################################################
#
# Data file download
#

st.subheader("Data Files")

if metadata["intents"] > 0:
    st.markdown(f"The result of this analysis is stored in a JSON file.")
    st.download_button(
        label="Download Intent Data (JSON)",
        data=open(intent_data_file, "rb").read(),
        file_name=intent_data_file_name,
        mime="text/plain",
    )

if metadata["sentences"] > 0:
    st.markdown(f"This analysis is based on contact data in text file with each line representing a call or message.")
    st.download_button(
        label="Download Contact Data (Text)",
        data=open(data_file, "rb").read(),
        file_name=data_file_name,
        mime="text/plain",
    )

st.markdown("---")
st.markdown("You may upload your own contact data file to analyze intents:")

# To avoid repeated uploads, we will keep track of whether a file has been uploaded
# file_uploaded is initialized to False
if "file_uploaded" not in st.session_state:
    st.session_state.file_uploaded = False

uploaded_file = st.file_uploader("Choose a file", type=["txt"])
if uploaded_file is not None and not st.session_state.file_uploaded:
    with open(data_file, "wb") as file:
        file.write(uploaded_file.read())
    st.success(f"File uploaded successfully: {data_file_name}")

    # Delete the cache
    try:
        shutil.rmtree(cache_dir)
        # st.success(f"Cached results have all been deleted")
    except Exception as e:
        st.error(f"Error deleting directory: {e}")

    # Recreate the cache directory
    try:
        os.makedirs(cache_dir, exist_ok=True)
        # st.success(f"A new cache has been created successfully.")
    except Exception as e:
        st.error(f"Error creating subdirectory: {e}")

    st.session_state.file_uploaded = True

    # st.rerun()
    # Reload the page from url
    st_javascript(f"window.location.href = '{url}'")

st.markdown("<div style='color: red'>Warning: Uploading a new file will overwrite the existing data file and all cached results.</div>", unsafe_allow_html=True)

st.markdown(f"[[top]](#granularity-setting)")

