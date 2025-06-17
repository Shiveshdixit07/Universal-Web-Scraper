import json
from io import BytesIO
import pandas as pd
import streamlit as st
from streamlit_tags import st_tags_sidebar
from scrapper import scrape_and_clean

st.set_page_config(
    page_title="Universal Web Scraper",
    page_icon="🔍",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.markdown("""
<style>
    /* Import Google Fonts */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');
    
    /* Global styles */
    .main {
        font-family: 'Inter', sans-serif;
    }
    
    /* Header styling */
    .main-header {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 2rem 0;
        border-radius: 15px;
        margin-bottom: 2rem;
        box-shadow: 0 10px 30px rgba(0,0,0,0.1);
    }
    
    .main-title {
        color: white;
        text-align: center;
        font-size: 2.5rem;
        font-weight: 700;
        margin: 0;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.3);
    }
    
    .main-subtitle {
        color: rgba(255,255,255,0.9);
        text-align: center;
        font-size: 1.1rem;
        font-weight: 400;
        margin-top: 0.5rem;
        margin-bottom: 0;
    }
    
    /* Sidebar styling */
    .css-1d391kg {
        background: linear-gradient(180deg, #f8fafc 0%, #e2e8f0 100%);
    }
    
    .sidebar-header {
        background: linear-gradient(135deg, #4c51bf 0%, #6b46c1 100%);
        color: white;
        padding: 1rem;
        border-radius: 10px;
        margin-bottom: 1.5rem;
        text-align: center;
        font-weight: 600;
        box-shadow: 0 4px 15px rgba(0,0,0,0.1);
    }
    
    /* Form elements styling */
    .stSelectbox > div > div {
        background: white;
        border: 2px solid #e2e8f0;
        border-radius: 8px;
        transition: all 0.3s ease;
    }
    
    .stSelectbox > div > div:hover {
        border-color: #667eea;
        box-shadow: 0 0 0 3px rgba(102, 126, 234, 0.1);
    }
    
    /* Fix selectbox text visibility */
    .stSelectbox > div > div > select,
    .stSelectbox > div > div > div[role="combobox"],
    .stSelectbox > div > div > div[role="combobox"] > div {
        color: #2d3748 !important;
        background: white !important;
    }
    
    /* Fix dropdown options visibility */
    .stSelectbox [data-baseweb="select"] > div > div,
    .stSelectbox [data-baseweb="select"] > div > div > div {
        color: #2d3748 !important;
        background: white !important;
    }
    
    /* Fix dropdown menu styling */
    .stSelectbox [role="listbox"] {
        background: white !important;
        border: 1px solid #e2e8f0 !important;
        border-radius: 8px !important;
        box-shadow: 0 4px 15px rgba(0,0,0,0.1) !important;
    }
    
    .stSelectbox [role="option"] {
        color: #2d3748 !important;
        background: white !important;
    }
    
    .stSelectbox [role="option"]:hover,
    .stSelectbox [role="option"][aria-selected="true"] {
        background: #f7fafc !important;
        color: #667eea !important;
    }
    
    .stTextInput > div > div > input {
        background: white;
        border: 2px solid #e2e8f0;
        border-radius: 8px;
        padding: 0.75rem;
        transition: all 0.3s ease;
    }
    
    .stTextInput > div > div > input:focus {
        border-color: #667eea;
        box-shadow: 0 0 0 3px rgba(102, 126, 234, 0.1);
    }
    
    /* Button styling */
    .scrape-button {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        border: none;
        padding: 1rem 2rem;
        border-radius: 10px;
        font-weight: 600;
        font-size: 1.1rem;
        cursor: pointer;
        transition: all 0.3s ease;
        width: 100%;
        margin-top: 1rem;
        box-shadow: 0 4px 15px rgba(102, 126, 234, 0.3);
    }
    
    .scrape-button:hover {
        transform: translateY(-2px);
        box-shadow: 0 8px 25px rgba(102, 126, 234, 0.4);
    }
    
    /* Download section styling */
    .download-section {
       background: linear-gradient(135deg, #f8fafc 0%, #e2e8f0 100%);
       padding: 1rem;
       border-radius: 15px;
       margin-top: 1rem;
       box-shadow: 0 5px 20px rgba(0, 0, 0, 0.1);
       margin-bottom: 1rem;
       margin-left: 2rem;
       margin-right: 2rem;
    }
    
    .download-title {
        color: #2d3748;
        font-size: 1.5rem;
        font-weight: 600;
        text-align: center;
    }
    
    /* Download button styling */
    .stDownloadButton > button {
        background: linear-gradient(135deg, #48bb78 0%, #38a169 100%);
        color: white;
        border: none;
        padding: 0.75rem 1.5rem;
        border-radius: 8px;
        font-weight: 500;
        transition: all 0.3s ease;
        width: 100%;
        box-shadow: 0 4px 15px rgba(72, 187, 120, 0.3);
    }
    
    .stDownloadButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 8px 25px rgba(72, 187, 120, 0.4);
    }
    
    /* Data frame styling */
    .dataframe {
        border-radius: 10px;
        overflow: hidden;
        box-shadow: 0 5px 20px rgba(0,0,0,0.1);
        margin: 2rem 0;
    }
    
    /* Status indicators */
    .status-success {
        background: linear-gradient(135deg, #48bb78 0%, #38a169 100%);
        color: white;
        padding: 1rem;
        border-radius: 10px;
        text-align: center;
        font-weight: 500;
        margin: 1rem 0;
    }
    
    .status-error {
        background: linear-gradient(135deg, #f56565 0%, #e53e3e 100%);
        color: white;
        padding: 1rem;
        border-radius: 10px;
        text-align: center;
        font-weight: 500;
        margin: 1rem 0;
    }
    
    /* Spinner customization */
    .stSpinner {
        text-align: center;
        padding: 2rem;
    }
    
    /* Feature cards */
    .feature-card {
        background: white;
        padding: 1.5rem;
        border-radius: 12px;
        box-shadow: 0 4px 15px rgba(0,0,0,0.1);
        margin-bottom: 1rem;
        border-left: 4px solid #667eea;
    }
    
    .feature-title {
        color: #2d3748;
        font-weight: 600;
        margin-bottom: 0.5rem;
    }
    
    .feature-description {
        color: #718096;
        font-size: 0.9rem;
    }
    
    /* Hide Streamlit branding */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
</style>
""", unsafe_allow_html=True)

# Main header
st.markdown("""
<div class="main-header">
    <h1 class="main-title">🔍 Universal Web Scraper</h1>
    <p class="main-subtitle">Extract required data from any website with AI-powered precision</p>
</div>
""", unsafe_allow_html=True)

# Sidebar configuration
st.sidebar.markdown("""
<div class="sidebar-header">
    <h2>⚙️ Scraper Configuration</h2>
</div>
""", unsafe_allow_html=True)

st.sidebar.markdown("### 🤖 AI Model")
model = st.sidebar.selectbox(
    "Select AI Model",
    ("Gemini 1.5 Flash",),
    help="Choose the AI model for intelligent data extraction"
)

st.sidebar.markdown("### 🌐 Target URL")
url = st.sidebar.text_input(
    "Website URL",
    placeholder="https://example.com",
    help="Enter the URL of the website you want to scrape"
)

st.sidebar.markdown("### 🏷️ Data Fields")
keyword = st_tags_sidebar(
    label="Fields to Extract:",
    text="Press enter to add field",
    value=[],
    suggestions=["title", "price", "description", "image", "link", "rating", "author", "date"],
    maxtags=8,
    key="extraction_fields"
)


scrape_button = st.sidebar.button(
    "🚀 Start Scraping",
    key="scrape_btn",
    help="Click to begin the scraping process"
)

# Main content area
if not url and not scrape_button:
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("""
        <div class="feature-card">
            <div class="feature-title">🤖 AI-Powered</div>
            <div class="feature-description">Uses advanced AI to intelligently identify and extract data from web pages</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class="feature-card">
            <div class="feature-title">📊 Multiple Formats</div>
            <div class="feature-description">Export your data in CSV, JSON, or Excel format for maximum compatibility</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown("""
        <div class="feature-card">
            <div class="feature-title">⚡ Fast & Reliable</div>
            <div class="feature-description">Quick processing with robust error handling and data validation</div>
        </div>
        """, unsafe_allow_html=True)
    
   
if scrape_button:
    if not url:
        st.markdown("""
        <div class="status-error">
            ⚠️ Please enter a valid URL before scraping
        </div>
        """, unsafe_allow_html=True)
    elif not keyword:
        st.markdown("""
        <div class="status-error">
            ⚠️ Please specify at least one field to extract
        </div>
        """, unsafe_allow_html=True)
    else:
        try:
            with st.spinner("🔍 Analyzing website and extracting data... This may take a moment."):
                result = scrape_and_clean(url, keyword)
                
                if isinstance(result, str):
                    try:
                        result_dict = json.loads(result)
                    except:
                        last_occurrence_index = result.rfind("}")
                        result = result[: last_occurrence_index + 1] + "]}"
                        result_dict = json.loads(result)
            
            st.session_state.df = pd.DataFrame(result_dict["listings"])
            st.session_state.csv = st.session_state.df.to_csv(index=False).encode("utf-8")
            st.session_state.json = st.session_state.df.to_json(orient="records").encode("utf-8")
            
            excel_buffer = BytesIO()
            with pd.ExcelWriter(excel_buffer, engine="openpyxl") as writer:
                st.session_state.df.to_excel(writer, index=False, sheet_name="ScrapedData")
            excel_buffer.seek(0)
            st.session_state.excel_buffer = excel_buffer
            
            st.markdown("""
            <div class="status-success">
                ✅ Data extraction completed successfully!
            </div>
            """, unsafe_allow_html=True)
            
        except Exception as e:
            st.markdown(f"""
            <div class="status-error">
                ❌ Error during scraping: {str(e)}
            </div>
            """, unsafe_allow_html=True)

if "df" in st.session_state and not st.session_state.df.empty:
    st.markdown("### 📊 Extraction Results")
    
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Total Records", len(st.session_state.df))
    with col2:
        st.metric("Data Fields", len(st.session_state.df.columns))
    with col3:
        st.metric("Success Rate", "100%")
    
    st.markdown("### 👀 Data Preview")
    st.dataframe(
        st.session_state.df,
        use_container_width=True,
        hide_index=True
    )
    
    # Download section
    st.markdown("""
    <div class="download-section">
        <h3 class="download-title">📥 Download Your Data</h3>
    </div>
    """, unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.download_button(
            label="📄 Download CSV",
            data=st.session_state.csv,
            file_name=f"scraped_data_{pd.Timestamp.now().strftime('%Y%m%d_%H%M%S')}.csv",
            mime="text/csv",
            help="Download data as comma-separated values file"
        )
    
    with col2:
        st.download_button(
            label="📋 Download JSON",
            data=st.session_state.json,
            file_name=f"scraped_data_{pd.Timestamp.now().strftime('%Y%m%d_%H%M%S')}.json",
            mime="application/json",
            help="Download data as JSON file"
        )
    
    with col3:
        st.download_button(
            label="📊 Download Excel",
            data=st.session_state.excel_buffer,
            file_name=f"scraped_data_{pd.Timestamp.now().strftime('%Y%m%d_%H%M%S')}.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
            help="Download data as Excel spreadsheet"
        )

elif "df" in st.session_state and st.session_state.df.empty:
    st.markdown("""
    <div class="status-error">
        ⚠️ No data was extracted. Please try different field names or check if the website is accessible.
    </div>
    """, unsafe_allow_html=True)