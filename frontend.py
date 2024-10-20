import streamlit as st
import pandas as pd
import requests
from io import BytesIO
import random

# Set the page configuration with a title and star emoji
st.set_page_config(
    page_title="Star Size Predictor 🌠",
    page_icon="🌟"
)

st.markdown("""
    <style>
        .footer {
            position: fixed;
            left: 0;
            bottom: 0;
            width: 100%;
            background-color: rgba(255, 255, 255, 1);
            color: rgba(0, 0, 0, 1);
            text-align: center;
            padding: 10px;
            font-size: 14px;
            font-weight: bold;
            z-index: 1000;
        }

        .stApp {
            padding-bottom: 50px;
        }
    </style>
    <div class="footer">
        <p>This is project is created as part of Curriculum of Machine Learning for Astronomy Training Program at Spartificial</p>
    </div>
""", unsafe_allow_html=True)

# Custom CSS for background images
background_image_urls = [
    "https://i.ytimg.com/vi/tU4aKTz9Ky0/maxresdefault.jpg",
    "https://i.ytimg.com/vi/HMSRTEnV_Hw/maxresdefault.jpg?sqp=-oaymwEmCIAKENAF8quKqQMa8AEB-AH-CYAC0AWKAgwIABABGEsgRihyMA8=&amp;rs=AOn4CLBVO1pirlKMXbkO0WqSMXa0OOOssQ.jpg",  
    "https://i.pinimg.com/originals/04/5f/10/045f10b4643df21923387b777f56bcbb.jpg",
    "https://image.winudf.com/v2/image/Y29tLkx3cE1hc3Rlci5TcGExNDdfc2NyZWVuXzBfazg2aXh1ZG0/screen-0.jpg?fakeurl=1&type=.jpg",
    "https://steamuserimages-a.akamaihd.net/ugc/80344884637849543/48DFCE86803381928F8315C96FCF1FDD94118859/?imw=512&amp;imh=320&amp;ima=fit&amp;impolicy=Letterbox&amp;imcolor=%23000000&amp;letterbox=true.jpg",
    "https://media.wired.com/photos/5b7f64cbbe2f8d3a624b77b2/4:3/w_2000,h_1500,c_limit/SPoW_82318_01.jpg",
    "https://images-wixmp-ed30a86b8c4ca887773594c2.wixmp.com/f/5eae36e3-278f-4731-be00-1440d36eca76/d30idy4-9a4a96ed-33be-4941-99c1-8b77adb23288.jpg?token=eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpc3MiOiJ1cm46YXBwOjdlMGQxODg5ODIyNjQzNzNhNWYwZDQxNWVhMGQyNmUwIiwic3ViIjoidXJuOmFwcDo3ZTBkMTg4OTgyMjY0MzczYTVmMGQ0MTVlYTBkMjZlMCIsImF1ZCI6WyJ1cm46c2VydmljZTpmaWxlLmRvd25sb2FkIl0sIm9iaiI6W1t7InBhdGgiOiIvZi81ZWFlMzZlMy0yNzhmLTQ3MzEtYmUwMC0xNDQwZDM2ZWNhNzYvZDMwaWR5NC05YTRhOTZlZC0zM2JlLTQ5NDEtOTljMS04Yjc3YWRiMjMyODguanBnIn1dXX0.urB7x7zyDCCRhro0z1HDVMWXZ9HJi9NgdXurlCon43Q"
]

# Randomly select a background image URL
background_image_url = random.choice(background_image_urls)

page_bg_img = f"""
<style>
[data-testid="stAppViewContainer"] {{
    background-image: url("{background_image_url}");
    background-size: cover;
    background-position: center;
    background-repeat: no-repeat;
    background-attachment: fixed;
}}

[data-testid="stSidebar"] {{
    background-color: rgba(255, 255, 255, 0.7);
}}


.gray-container {{
    background-color: rgba(255, 255, 255, 0.8); 
    color: black;
    padding: 10px;
    border-radius: 10px;
    font-size: 18px;
    line-height: 1.6;
}}

</style>
"""

# Inject the CSS to the app
st.markdown(page_bg_img, unsafe_allow_html=True)

# Title and description of the app
st.markdown('<h1 style="color: magenta;">Star Size Predictor ✨</h1>', unsafe_allow_html=True)

# Instructions on how to use the app
st.markdown("""
<div class="gray-container">
    <h4 style="color: maroon;"><u>How to use this app:</u></h4>
    <ol>
        <li><b>Enter the number of Stars to generate the dataset with its Brightness and Size Values.</b></li>
        <li><b>Click on Create Dataset and  Generate Predictions Button.</b></li>
        <li><b>It will generate the dataset and also predict the star sizes using Linear Regression.</b></li>
        <li><b>Plot the True Sizes and Predicted Sizes by Linear Regression based on the Brightness values.</b></li>
        <li><b>You can now download the generated data, predicted data and the plot if needed.</b></li>
    </ol>
</div>
""", unsafe_allow_html=True)


# Define the FastAPI endpoints for local development
PREDICT_ENDPOINT = "https://star-size-predictor.onrender.com/predict/"
PLOT_ENDPOINT = "https://star-size-predictor.onrender.com/plot/"
CREATE_DATA_ENDPOINT = "https://star-size-predictor.onrender.com/create_data/"

# Initialize session state to track the last uploaded file
if 'last_uploaded_file' not in st.session_state:
    st.session_state.last_uploaded_file = None

# Initialize session state for predictions
if 'predicted_df' not in st.session_state:
    st.session_state.predicted_df = None

# Initialize session state for generated dataset
if 'generated_df' not in st.session_state:
    st.session_state.generated_df = None

# Dataset creation section
st.text("")
st.markdown("""
<div style='background-color: rgba(230, 230, 250, 0.7); padding: 0px 1px 1px 10px; border-radius: 10px;'>
    <h4 style='color: #000000;'>👇 Generate the Star Dataset with its Brightness and Size Values</h4>
</div>
""", unsafe_allow_html=True)
st.text("")
n_samples = st.number_input("Enter the number of Stars:-", min_value=10, value=500)
if st.button("Create Dataset and Generate Predictions"):
    with st.spinner("Generating dataset... (it may take a while if the app was idle for more than 15 minutes)"):
        response = requests.post(CREATE_DATA_ENDPOINT, params={"n_samples": n_samples})
        if response.status_code == 200:
            st.session_state.generated_df = pd.read_csv(BytesIO(response.content))
            
            # Send the generated dataset for predictions
            with st.spinner("Generating predictions..."):
                prediction_response = requests.post(PREDICT_ENDPOINT, files={"file": BytesIO(response.content)})
                if prediction_response.status_code == 200:
                    st.session_state.predicted_df = pd.read_csv(BytesIO(prediction_response.content))
                else:
                    st.error("Failed to generate predictions. Please try again.")
        else:
            st.error("Failed to create dataset. Please try again.")

# Display the generated dataset and predicted CSV side by side
if 'generated_df' in st.session_state and st.session_state.predicted_df is not None:
    col1, col2 = st.columns(2)
    
    with col1:
        st.write("#### Generated Dataset")
        st.dataframe(st.session_state.generated_df)
    
    with col2:
        st.write("#### Predicted CSV")
        st.dataframe(st.session_state.predicted_df)

# Show the button to trigger plot generation only if predictions are done
if st.session_state.predicted_df is not None:
    if st.button("Plot the Linear Regression"):
        with st.spinner("Generating plot..."):
            predicted_csv_bytes = st.session_state.predicted_df.to_csv(index=False).encode('utf-8')
            plot_response = requests.post(PLOT_ENDPOINT, files={"file": predicted_csv_bytes})
        
        if plot_response.status_code == 200:
            st.image(BytesIO(plot_response.content))
        else:
            st.error("Failed to generate the plot. Please try again.")
