def get_custom_css():
    """Return custom CSS for the application"""
    return """
    <style>
    /* Sidebar configuration title */
    [data-testid="stSidebar"] > div:first-child h1 {
        font-size: 24px !important;
        font-weight: 600 !important;
    }
    
    /* Sidebar section headers */
    .css-1d391kg, [data-testid="stSidebar"] h2, [data-testid="stSidebar"] h3 {
        font-size: 24px !important;
        font-weight: 600 !important;
    }
    
    /* Sidebar labels */
    [data-testid="stSidebar"] label {
        font-size: 18px !important;
        font-weight: 500 !important;
    }
    
    /* Tab labels */
    .stTabs [data-baseweb="tab-list"] button [data-testid="stMarkdownContainer"] p {
        font-size: 24px !important;
        font-weight: 600 !important;
    }
    
    /* Main content headers */
    h1 { font-size: 42px !important; }
    h2 { font-size: 32px !important; }
    h3 { font-size: 24px !important; }
    
    /* Main title styling */
    .main-title {
        font-size: 48px !important;
        font-weight: 700 !important;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        text-align: center;
        margin-bottom: 30px !important;
        padding: 20px 0;
    }
    </style>
    """
