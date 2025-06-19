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
        padding: 0 1rem;
    }
    
    /* Responsive container */
    .container {
        max-width: 1200px;
        margin: 0 auto;
        padding: 0 1rem;
    }
    
    .main-header {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 2rem 1rem;
        border-radius: 20px;
        margin-bottom: 2rem;
        box-shadow: 0 10px 30px rgba(0,0,0,0.15);
        position: relative;
        overflow: hidden;
    }
    
    .main-header::before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        bottom: 0;
        background: url('data:image/svg+xml,<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 100 100"><defs><pattern id="grain" width="100" height="100" patternUnits="userSpaceOnUse"><circle cx="25" cy="25" r="1" fill="white" opacity="0.1"/><circle cx="75" cy="75" r="1" fill="white" opacity="0.1"/><circle cx="50" cy="10" r="0.5" fill="white" opacity="0.1"/><circle cx="10" cy="60" r="0.5" fill="white" opacity="0.1"/><circle cx="90" cy="40" r="0.5" fill="white" opacity="0.1"/></pattern></defs><rect width="100" height="100" fill="url(%23grain)"/></svg>');
        pointer-events: none;
    }
    
    .main-title {
        color: white;
        text-align: center;
        font-size: clamp(1.8rem, 5vw, 2.5rem);
        font-weight: 700;
        margin: 0;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.3);
        position: relative;
        z-index: 1;
    }
    
    .main-subtitle {
        color: rgba(255,255,255,0.9);
        text-align: center;
        font-size: clamp(0.9rem, 3vw, 1.1rem);
        font-weight: 400;
        margin-top: 0.5rem;
        margin-bottom: 0;
        position: relative;
        z-index: 1;
    }
    
    .css-1d391kg {
        background: linear-gradient(180deg, #f8fafc 0%, #e2e8f0 100%);
        min-height: 100vh;
    }
    
    .sidebar-header {
        background: linear-gradient(135deg, #4c51bf 0%, #6b46c1 100%);
        color: white;
        padding: 1rem;
        border-radius: 15px;
        margin-bottom: 1.5rem;
        text-align: center;
        font-weight: 600;
        box-shadow: 0 4px 15px rgba(0,0,0,0.1);
        font-size: clamp(0.9rem, 2.5vw, 1.1rem);
    }
    
    .stSelectbox > div > div {
        background: white;
        border: 2px solid #e2e8f0;
        border-radius: 12px;
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
        box-shadow: 0 2px 4px rgba(0,0,0,0.05);
    }
    
    .stSelectbox > div > div:hover {
        border-color: #667eea;
        box-shadow: 0 4px 20px rgba(102, 126, 234, 0.15);
        transform: translateY(-1px);
    }
    
    .stSelectbox > div > div:focus-within {
        border-color: #667eea;
        box-shadow: 0 0 0 4px rgba(102, 126, 234, 0.1);
    }
    
    .stSelectbox > div > div > select,
    .stSelectbox > div > div > div[role="combobox"],
    .stSelectbox > div > div > div[role="combobox"] > div {
        color: #2d3748 !important;
        background: white !important;
        font-weight: 500;
    }
    
    .stSelectbox [data-baseweb="select"] > div > div,
    .stSelectbox [data-baseweb="select"] > div > div > div {
        color: #2d3748 !important;
        background: white !important;
    }
    
    .stSelectbox [role="listbox"] {
        background: white !important;
        border: 1px solid #e2e8f0 !important;
        border-radius: 12px !important;
        box-shadow: 0 10px 40px rgba(0,0,0,0.15) !important;
        backdrop-filter: blur(10px);
    }
    
    .stSelectbox [role="option"] {
        color: #2d3748 !important;
        background: white !important;
        padding: 0.75rem 1rem !important;
        transition: all 0.2s ease;
    }
    
    .stSelectbox [role="option"]:hover,
    .stSelectbox [role="option"][aria-selected="true"] {
        background: linear-gradient(135deg, #f7fafc 0%, #edf2f7 100%) !important;
        color: #667eea !important;
        transform: translateX(4px);
    }
    
    .stTextInput > div > div > input {
        background: white;
        border: 2px solid #e2e8f0;
        border-radius: 12px;
        padding: 0.875rem 1rem;
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
        font-weight: 500;
        box-shadow: 0 2px 4px rgba(0,0,0,0.05);
        color:black;
    }
    
    .stTextInput > div > div > input:focus {
        border-color: #667eea;
        box-shadow: 0 0 0 4px rgba(102, 126, 234, 0.1);
        transform: translateY(-1px);
        color:black;
    }
    
    .stTextInput > div > div > input::placeholder {
        color: black;
        font-weight: 400;
    }
    
    .stButton > button {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        border: none;
        padding: 1rem 2rem;
        border-radius: 12px;
        font-weight: 600;
        font-size: clamp(0.9rem, 2.5vw, 1.1rem);
        cursor: pointer;
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
        width: 100%;
        margin-top: 1rem;
        box-shadow: 0 4px 15px rgba(102, 126, 234, 0.3);
        position: relative;
        overflow: hidden;
    }
    
    .stButton > button:hover {
        transform: translateY(-3px);
        box-shadow: 0 8px 25px rgba(102, 126, 234, 0.4);
    }
    
    .stButton > button:active {
        transform: translateY(-1px);
    }
    
    .download-section {
        background: linear-gradient(135deg, #f8fafc 0%, #e2e8f0 100%);
        padding: 2rem;
        border-radius: 20px;
        margin: 2rem 0;
        box-shadow: 0 10px 30px rgba(0, 0, 0, 0.1);
        border: 1px solid rgba(255, 255, 255, 0.2);
        backdrop-filter: blur(10px);
    }
    
    .download-title {
        color: #2d3748;
        font-size: clamp(1.2rem, 4vw, 1.5rem);
        font-weight: 600;
        text-align: center;
    }
    
    .stDownloadButton > button {
        background: linear-gradient(135deg, #48bb78 0%, #38a169 100%);
        color: white;
        border: none;
        padding: 1rem 1.5rem;
        border-radius: 12px;
        font-weight: 600;
        font-size: clamp(0.8rem, 2vw, 0.95rem);
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
        width: 100%;
        box-shadow: 0 4px 15px rgba(72, 187, 120, 0.3);
        margin-bottom: 1rem;
    }
    
    .stDownloadButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 8px 25px rgba(72, 187, 120, 0.4);
    }
    
    .dataframe {
        border-radius: 15px;
        overflow: hidden;
        box-shadow: 0 10px 30px rgba(0,0,0,0.1);
        margin: 2rem 0;
        background: white;
    }
    
    .status-success {
        background: linear-gradient(135deg, #48bb78 0%, #38a169 100%);
        color: white;
        padding: 1.5rem;
        border-radius: 15px;
        text-align: center;
        font-weight: 500;
        margin: 1.5rem 0;
        box-shadow: 0 4px 15px rgba(72, 187, 120, 0.3);
        font-size: clamp(0.9rem, 2.5vw, 1rem);
    }
    
    .status-error {
        background: linear-gradient(135deg, #f56565 0%, #e53e3e 100%);
        color: white;
        padding: 1.5rem;
        border-radius: 15px;
        text-align: center;
        font-weight: 500;
        margin: 1.5rem 0;
        box-shadow: 0 4px 15px rgba(245, 101, 101, 0.3);
        font-size: clamp(0.9rem, 2.5vw, 1rem);
    }
    
    .feature-card {
        background: white;
        padding: 2rem 1.5rem;
        border-radius: 20px;
        box-shadow: 0 10px 30px rgba(0,0,0,0.1);
        margin-bottom: 2rem;
        border-left: 5px solid #667eea;
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
        position: relative;
        overflow: hidden;
    }
    
    .feature-card::before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        bottom: 0;
        background: linear-gradient(135deg, rgba(102, 126, 234, 0.02) 0%, rgba(118, 75, 162, 0.02) 100%);
        pointer-events: none;
    }
    
    .feature-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 20px 40px rgba(0,0,0,0.15);
        border-left-color: #764ba2;
    }
    
    .feature-title {
        color: #2d3748;
        font-weight: 700;
        margin-bottom: 1rem;
        font-size: clamp(1rem, 3vw, 1.2rem);
        position: relative;
        z-index: 1;
    }
    
    .feature-description {
        color: #718096;
        font-size: clamp(0.85rem, 2.5vw, 0.95rem);
        line-height: 1.6;
        position: relative;
        z-index: 1;
    }
    
    .metric-container {
        background: white;
        padding: 1.5rem;
        border-radius: 15px;
        box-shadow: 0 4px 15px rgba(0,0,0,0.08);
        text-align: center;
        margin-bottom: 1rem;
        transition: all 0.3s ease;
    }
    
    .metric-container:hover {
        transform: translateY(-3px);
        box-shadow: 0 8px 25px rgba(0,0,0,0.12);
    }
    
    .stSpinner {
        text-align: center;
        padding: 3rem;
    }
    
    .stSpinner > div {
        border-radius: 50%;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    }
    
    @media (max-width: 768px) {
        .main {
            padding: 0 0.5rem;
        }
        
        .main-header {
            padding: 1.5rem 1rem;
            margin-bottom: 1.5rem;
        }
        
        .feature-card {
            padding: 1.5rem 1rem;
            margin-bottom: 1.5rem;
        }
        
        .download-section {
            padding: 1.5rem 1rem;
            margin: 1.5rem 0;
        }
        
        .sidebar-header {
            padding: 0.75rem;
            margin-bottom: 1rem;
        }
        
        .stButton > button {
            padding: 0.875rem 1.5rem;
        }
        
        .stDownloadButton > button {
            padding: 0.875rem 1rem;
            margin-bottom: 0.75rem;
        }
    }
    
    @media (max-width: 480px) {
        .main-header {
            padding: 1rem 0.75rem;
            border-radius: 15px;
        }
        
        .feature-card {
            padding: 1.25rem 0.875rem;
            border-radius: 15px;
        }
        
        .download-section {
            padding: 1.25rem 0.875rem;
            border-radius: 15px;
        }
        
        .stSelectbox > div > div,
        .stTextInput > div > div > input {
            border-radius: 10px;
            color:black;
        }
        
        .stButton > button,
        .stDownloadButton > button {
            border-radius: 10px;
            font-size: 0.9rem;
        }
    }
    
    .stProgress .css-1cpxqw2 {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        border-radius: 10px;
    }
    
    /* Loading animation */
    @keyframes pulse {
        0%, 100% { opacity: 1; }
        50% { opacity: 0.5; }
    }
    
    .loading-pulse {
        animation: pulse 2s infinite;
    }
    
    /* Tags styling */
    .streamlit-tags {
        background: white;
        border-radius: 12px;
        padding: 0.5rem;
        box-shadow: 0 2px 4px rgba(0,0,0,0.05);
    }
    
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    
    @media (prefers-color-scheme: dark) {
        .feature-card {
            background: #2d3748;
            color: #e2e8f0;
        }
        
        .feature-title {
            color: #f7fafc;
        }
        
        .feature-description {
            color: #cbd5e0;
        }
        
        .download-section {
            background: linear-gradient(135deg, #2d3748 0%, #4a5568 100%);
        }
        
        .download-title {
            color: #f7fafc;
        }
    }
    
    /* Accessibility improvements */
    .stButton > button:focus,
    .stDownloadButton > button:focus {
        outline: 3px solid #667eea;
        outline-offset: 2px;
    }
    
    .stSelectbox > div > div:focus-within,
    .stTextInput > div > div > input:focus {
        outline: 2px solid #667eea;
        outline-offset: 2px;
        color:black;
    }
    
    /* Smooth scrolling */
    html {
        scroll-behavior: smooth;
    }
    
    /* Enhanced transitions */
    * {
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
    }
</style>
""", unsafe_allow_html=True)

st.markdown("""
<div class="main-header">
    <h1 class="main-title">🔍 Universal Web Scraper</h1>
    <p class="main-subtitle">Extract required data from any website with AI-powered precision</p>
</div>
""", unsafe_allow_html=True)

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
    suggestions=["title", "price", "description", "image", "link", "rating", "author", "date", "category", "brand"],
    maxtags=10,
    key="extraction_fields"
)


scrape_button = st.sidebar.button(
    "🚀 Start Scraping",
    key="scrape_btn",
    help="Click to begin the scraping process"
)

if not url and not scrape_button:
    st.markdown("""
    <div style="text-align: center; margin: 2rem 0;">
        <h2 style="color: #2d3748; font-weight: 600; margin-bottom: 1rem;">Welcome to the most advanced web scraper</h2>
        <p style="color: #718096; font-size: 1.1rem; margin-bottom: 2rem;">Get started by entering a URL and selecting the fields you want to extract</p>
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
            progress_bar = st.progress(0)
            status_text = st.empty()
            
            status_text.text("🔍 Initializing scraper...")
            progress_bar.progress(10)
            
            status_text.text("🌐 Connecting to website...")
            progress_bar.progress(30)
            
            status_text.text("🤖 AI analyzing page structure...")
            progress_bar.progress(50)
            
            with st.spinner("🔄 Extracting data... This may take a moment."):
                result = scrape_and_clean(url, keyword)
                progress_bar.progress(80)
                
                if isinstance(result, str):
                    try:
                        result_dict = json.loads(result)
                    except:
                        last_occurrence_index = result.rfind("}")
                        result = result[: last_occurrence_index + 1] + "]}"
                        result_dict = json.loads(result)
            
            status_text.text("📊 Processing and cleaning data...")
            progress_bar.progress(90)
            
            st.session_state.df = pd.DataFrame(result_dict["listings"])
            st.session_state.csv = st.session_state.df.to_csv(index=False).encode("utf-8")
            st.session_state.json = st.session_state.df.to_json(orient="records").encode("utf-8")
            
            excel_buffer = BytesIO()
            with pd.ExcelWriter(excel_buffer, engine="openpyxl") as writer:
                st.session_state.df.to_excel(writer, index=False, sheet_name="ScrapedData")
            excel_buffer.seek(0)
            st.session_state.excel_buffer = excel_buffer
            
            progress_bar.progress(100)
            status_text.text("✅ Scraping completed successfully!")
            
            import time
            time.sleep(1)
            progress_bar.empty()
            status_text.empty()
            
            st.markdown("""
            <div class="status-success">
                ✅ Data extraction completed successfully! Your data is ready for download.
            </div>
            """, unsafe_allow_html=True)
            
        except Exception as e:
            progress_bar.empty()
            status_text.empty()
            st.markdown(f"""
            <div class="status-error">
                ❌ Error during scraping: {str(e)}
                <br><small>Please check the URL and try again, or contact support if the issue persists.</small>
            </div>
            """, unsafe_allow_html=True)

if "df" in st.session_state and not st.session_state.df.empty:
    st.markdown("### 📊 Extraction Results")
    
    col1, col2, col3 = st.columns([1, 1, 1])
    with col1:
        st.markdown("""
        <div class="metric-container">
            <h3 style="color: #667eea; margin: 0; font-size: 2rem;">{}</h3>
            <p style="color: #718096; margin: 0; font-weight: 500;">Total Records</p>
        </div>
        """.format(len(st.session_state.df)), unsafe_allow_html=True)
    with col2:
        st.markdown("""
        <div class="metric-container">
            <h3 style="color: #667eea; margin: 0; font-size: 2rem;">{}</h3>
            <p style="color: #718096; margin: 0; font-weight: 500;">Data Fields</p>
        </div>
        """.format(len(st.session_state.df.columns)), unsafe_allow_html=True)
    with col3:
        st.markdown("""
        <div class="metric-container">
            <h3 style="color: #48bb78; margin: 0; font-size: 2rem;">100%</h3>
            <p style="color: #718096; margin: 0; font-weight: 500;">Success Rate</p>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("### 👀 Data Preview")
    st.dataframe(
        st.session_state.df,
        use_container_width=True,
        hide_index=True,
        height=400
    )
    
    st.markdown("""
    <div class="download-section">
        <h3 class="download-title">📥 Download Your Data</h3>
        <p style="text-align: center; color: #718096; ">Choose your preferred format and download your scraped data</p>
    </div>
    """, unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns([1, 1, 1])
    
    with col1:
        st.download_button(
            label="📄 Download CSV",
            data=st.session_state.csv,
            file_name=f"scraped_data_{pd.Timestamp.now().strftime('%Y%m%d_%H%M%S')}.csv",
            mime="text/csv",
            help="Download data as comma-separated values file",
            use_container_width=True
        )
    
    with col2:
        st.download_button(
            label="📋 Download JSON",
            data=st.session_state.json,
            file_name=f"scraped_data_{pd.Timestamp.now().strftime('%Y%m%d_%H%M%S')}.json",
            mime="application/json",
            help="Download data as JSON file",
            use_container_width=True
        )
    
    with col3:
        st.download_button(
            label="📊 Download Excel",
            data=st.session_state.excel_buffer,
            file_name=f"scraped_data_{pd.Timestamp.now().strftime('%Y%m%d_%H%M%S')}.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
            help="Download data as Excel spreadsheet",
            use_container_width=True
        )
    
    st.markdown("---")
    st.markdown("### 📈 Data Insights")
    
    insights_col1, insights_col2 = st.columns([1, 1])
    
    with insights_col1:
        total_cells = len(st.session_state.df) * len(st.session_state.df.columns)
        non_null_cells = st.session_state.df.count().sum()
        completeness = round((non_null_cells / total_cells) * 100, 1)
        
        st.markdown(f"""
        <div class="feature-card">
            <div class="feature-title">🔍 Data Quality</div>
            <div class="feature-description">
                <strong>Completeness:</strong> {completeness}%<br>
                <strong>Total Fields:</strong> {len(st.session_state.df.columns)}<br>
                <strong>Non-empty Values:</strong> {non_null_cells:,}
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    with insights_col2:
        columns_info = ", ".join(st.session_state.df.columns[:5])
        if len(st.session_state.df.columns) > 5:
            columns_info += f" and {len(st.session_state.df.columns) - 5} more..."
            
        st.markdown(f"""
        <div class="feature-card">
            <div class="feature-title">📋 Extracted Fields</div>
            <div class="feature-description">
                <strong>Fields:</strong> {columns_info}<br>
                <strong>Data Types:</strong> Mixed content detected<br>
                <strong>Structure:</strong> Tabular format ready
            </div>
        </div>
        """, unsafe_allow_html=True)

elif "df" in st.session_state and st.session_state.df.empty:
    st.markdown("""
    <div class="status-error">
        ⚠️ No data was extracted from the specified URL.
        <br><br>
        <strong>Possible reasons:</strong>
        <ul style="text-align: left; margin-top: 1rem;">
            <li>The website might be blocking automated requests</li>
            <li>The specified fields don't exist on the page</li>
            <li>The page content is dynamically loaded with JavaScript</li>
            <li>The website structure has changed recently</li>
        </ul>
        <br>
        <strong>Try:</strong> Different field names, checking if the website is accessible, or using more generic terms like 'text', 'link', or 'image'.
    </div>
    """, unsafe_allow_html=True)

