import os

import plotly.express as px
import streamlit as st
from configs.visuals import VisualsConfig as Config
from constants import Constants as C
from visuals import menu

###################### Functions  ########################


###################### Content page ##########################

# Sidebarmenu
menu()

# Text
st.title("Feature Selection Saturation")