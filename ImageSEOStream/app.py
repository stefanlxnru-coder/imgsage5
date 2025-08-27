"""
ImageSEO Pro - Advanced AI Image Analyzer & SEO Optimizer

A sophisticated Streamlit application that leverages OpenAI's GPT-4o vision model
to analyze images and generate SEO-optimized descriptions with advanced local SEO features.
"""

import streamlit as st
import os
import zipfile
from pathlib import Path
import shutil
import base64
import tempfile
from datetime import datetime
from image_processor import ImageProcessor
from utils import create_zip_file, validate_folder, calculate_processing_stats

# Load configuration
try:
    from config import (
        DEFAULT_API_KEY, DEFAULT_SETTINGS, UI_SETTINGS, 
        PROCESSING_SETTINGS, ADVANCED_SETTINGS, SERVICE_CATEGORIES
    )
except ImportError:
    # Default configuration if config.py doesn't exist
    DEFAULT_API_KEY = ""
    DEFAULT_SETTINGS = {
        "description_style": "SEO Optimized",
        "length_range": (15, 25),
        "company_name": "",
        "location": "",
        "service_type": "",
        "output_format": "WebP Optimized",
        "quality": 85,
        "crop_dimensions": None
    }
    UI_SETTINGS = {
        "theme": "modern",
        "sidebar_expanded": True,
        "auto_open_browser": True,
        "port": 8501
    }
    PROCESSING_SETTINGS = {
        "max_images_per_batch": 10,
        "max_file_size_mb": 20,
        "supported_formats": [".jpg", ".jpeg", ".png", ".webp"]
    }
    ADVANCED_SETTINGS = {
        "retry_attempts": 3,
        "enable_image_enhancement": True,
        "enable_compression_analytics": True,
        "auto_cleanup_temp_files": True,
        "enable_detailed_logging": False
    }

# Get API key from environment variable first, then config
def get_api_key():
    """Get API key from environment variable or config"""
    return os.getenv("OPENAI_API_KEY", DEFAULT_API_KEY)

# Page configuration
st.set_page_config(
    page_title="ImageSEO Pro - AI Image Analyzer",
    page_icon="🎯",
    layout="wide",
    initial_sidebar_state="expanded" if UI_SETTINGS.get("sidebar_expanded", True) else "collapsed"
)

def apply_modern_css():
    """Apply modern, clean CSS styling"""
    st.markdown("""
    <style>
    /* Global styles */
    .main {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        min-height: 100vh;
    }
    
/* Force all text to be white */
* {
    color: white !important;
    /* Header styling */
    .header-container {
        background: rgba(255, 255, 255, 0.95);
        backdrop-filter: blur(10px);
        border-radius: 15px;
        padding: 1rem;
        margin-bottom: 1rem;
        box-shadow: 0 8px 32px rgba(0, 0, 0, 0.1);
        border: 1px solid rgba(255, 255, 255, 0.2);
    }
    
    .app-title {
        background: linear-gradient(45deg, #667eea, #764ba2);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        font-size: 2.5rem;
        font-weight: 800;
        margin: 0;
        text-align: center;
    }
    
    .app-subtitle {
        color: #6c757d;
        font-size: 1.1rem;
        text-align: center;
        margin: 0.5rem 0 0 0;
        font-weight: 400;
    }
    
    /* Card styling */
    .stCard {
        background: rgba(255, 255, 255, 0.95);
        backdrop-filter: blur(10px);
        border-radius: 12px;
        padding: 0.75rem;
        margin: 0.25rem 0;
        box-shadow: 0 4px 20px rgba(0, 0, 0, 0.08);
        border: 1px solid rgba(255, 255, 255, 0.2);
    }
    
    /* File uploader styling */
    .stFileUploader > div {
        background: rgba(255, 255, 255, 0.9);
        border: 3px dashed #667eea;
        border-radius: 15px;
        padding: 2rem;
        text-align: center;
        transition: all 0.3s ease;
    }
    
    .stFileUploader > div:hover {
        border-color: #764ba2;
        background: rgba(255, 255, 255, 0.95);
        transform: translateY(-2px);
    }
    
    /* Button styling */
    .stButton > button {
        background: linear-gradient(45deg, #667eea, #764ba2);
        color: white;
        border: none;
        border-radius: 12px;
        padding: 0.75rem 1.5rem;
        font-weight: 600;
        font-size: 1rem;
        transition: all 0.3s ease;
        box-shadow: 0 4px 15px rgba(102, 126, 234, 0.3);
    }
    
    .stButton > button:hover {
        background: linear-gradient(45deg, #764ba2, #667eea);
        transform: translateY(-2px);
        box-shadow: 0 8px 25px rgba(102, 126, 234, 0.4);
    }
    
    /* Sidebar styling */
    .css-1d391kg {
        background: rgba(255, 255, 255, 0.95) !important;
        backdrop-filter: blur(10px);
        border-right: 1px solid rgba(255, 255, 255, 0.2);
    }
    
    /* Progress bar styling */
    .stProgress > div > div {
        background: linear-gradient(90deg, #667eea, #764ba2);
        border-radius: 10px;
    }
    
    /* Success/Error messages */
    .stSuccess {
        background: rgba(40, 167, 69, 0.1);
        border: 1px solid #28a745;
        color: #155724;
        border-radius: 10px;
        padding: 0.75rem;
        margin: 0.5rem 0;
    }
    
    .stError {
        background: rgba(220, 53, 69, 0.1);
        border: 1px solid #dc3545;
        color: #721c24;
        border-radius: 10px;
        padding: 0.75rem;
        margin: 0.5rem 0;
    }
    
    /* Fix white text on white background */
    .stMarkdown, .stText {
        color: #333 !important;
    }
    
    /* Ensure proper contrast for all text elements */
    .stMarkdown p, .stMarkdown div, .stMarkdown span {
        color: #333 !important;
    }
    
    /* Fix info boxes */
    .stAlert {
        background: rgba(255, 255, 255, 0.95) !important;
        color: #333 !important;
        border: 1px solid #ddd !important;
    }
    
    /* Fix expander headers */
    .streamlit-expanderHeader {
        color: #333 !important;
        background: rgba(255, 255, 255, 0.9) !important;
    }
    
    /* Fix sidebar text */
    .css-1d391kg {
        color: #333 !important;
    }
    
    /* Modern dark theme with white text */
    * {
        color: white !important;
    }
    
    /* Streamlit components styling */
    .stMarkdown, .stText, .stAlert, .stSuccess, .stError, .stWarning, .stInfo, 
    .stFileUploader, .stExpander, .stSelectbox, .stTextInput, .stSlider,
    .stButton, .stDownloadButton, .stProgress, .stEmpty {
        color: white !important;
    }
    
    /* Sidebar styling */
    .css-1d391kg, .css-1d391kg * {
        color: white !important;
    }
    
    /* Expander styling */
    .streamlit-expanderHeader {
        background: rgba(25, 50, 100, 0.98) !important;
        color: white !important;
        border: 1px solid #4a90e2 !important;
        border-radius: 8px !important;
    }
    
    .streamlit-expanderContent {
        background: rgba(25, 50, 100, 0.95) !important;
        color: white !important;
    }
    
    .streamlit-expanderContent * {
        color: white !important;
    }
    
    /* Alert boxes */
    .stAlert {
        background: rgba(25, 50, 100, 0.98) !important;
        color: white !important;
        border: 1px solid #1e3a8a !important;
        font-weight: 500 !important;
    }
    
    .stSuccess {
        background: rgba(20, 80, 40, 0.95) !important;
        color: white !important;
        border: 1px solid #16a34a !important;
        font-weight: 500 !important;
    }
    
    .stError {
        background: rgba(80, 20, 20, 0.95) !important;
        color: white !important;
        border: 1px solid #dc2626 !important;
        font-weight: 500 !important;
    }
    
    .stWarning {
        background: rgba(80, 60, 20, 0.95) !important;
        color: white !important;
        border: 1px solid #d97706 !important;
        font-weight: 500 !important;
    }
    
    .stInfo {
        background: rgba(20, 60, 80, 0.95) !important;
        color: white !important;
        border: 1px solid #0891b2 !important;
        font-weight: 500 !important;
    }
    
    /* Card and component backgrounds */
    .stCard {
        background: rgba(25, 50, 100, 0.95) !important;
        color: white !important;
    }
    
    .compact-upload-area, .file-list, .result-item {
        background: rgba(25, 50, 100, 0.95) !important;
        color: white !important;
    }
    
    /* File uploader styling */
    .stFileUploader > div {
        background: rgba(25, 50, 100, 0.95) !important;
        color: white !important;
        border: 2px dashed #4a90e2 !important;
    }
    
    /* Hide file uploader pagination and preview */
    div[data-testid="stFileUploader"] [data-testid="stExpander"],
    div[data-testid="stFileUploader"] button[aria-label*="page"],
    div[data-testid="stFileUploader"] .row-widget,
    div[data-testid="stFileUploader"] [role="navigation"] {
        display: none !important;
    }
    
    /* Stats cards */
    .stats-card {
        background: linear-gradient(135deg, #667eea, #764ba2);
        color: white;
        padding: 1rem;
        border-radius: 12px;
        text-align: center;
        margin: 0.5rem 0;
    }
    
    .stats-number {
        font-size: 2rem;
        font-weight: 800;
        margin: 0;
    }
    
    .stats-label {
        font-size: 0.9rem;
        opacity: 0.9;
        margin: 0.25rem 0 0 0;
    }
    
    /* Feature badges */
    .feature-badge {
        display: inline-block;
        background: linear-gradient(45deg, #667eea, #764ba2);
        color: white;
        padding: 0.4rem 0.8rem;
        border-radius: 15px;
        font-size: 0.8rem;
        font-weight: 600;
        margin: 0.2rem;
    }
    
                    /* Compact upload area */
                .compact-upload-area {
                    background: rgba(255, 255, 255, 0.95);
                    border: 2px dashed #667eea;
                    border-radius: 12px;
                    padding: 1rem;
                    text-align: center;
                    margin: 0.5rem 0;
                    transition: all 0.3s ease;
                }
    
    .compact-upload-area:hover {
        border-color: #764ba2;
        transform: translateY(-1px);
    }
    
                    /* Results styling */
                .result-item {
                    background: rgba(255, 255, 255, 0.9);
                    border-radius: 8px;
                    padding: 0.75rem;
                    margin: 0.25rem 0;
                    border-left: 3px solid #667eea;
                }
    
                    /* Compact file list */
                .file-list {
                    background: rgba(255, 255, 255, 0.9);
                    border-radius: 8px;
                    padding: 0.75rem;
                    margin: 0.25rem 0;
                    max-height: 150px;
                    overflow-y: auto;
                }
    
    .file-item {
        padding: 0.5rem;
        border-bottom: 1px solid #eee;
        display: flex;
        justify-content: space-between;
        align-items: center;
    }
    
    .file-item:last-child {
        border-bottom: none;
    }
    
    /* Responsive design */
    @media (max-width: 768px) {
        .app-title {
            font-size: 2rem;
        }
        
        .header-container {
            padding: 1rem;
        }
    }
    </style>
    """, unsafe_allow_html=True)

def render_header():
    """Render the modern application header"""
    st.markdown("""
    <div class="header-container">
        <h1 class="app-title">🎯 ImgSage</h1>
        <p class="app-subtitle" style="color: #8B5CF6 !important; font-weight: 600;">Magic Image SEO Tool</p>
    </div>
    """, unsafe_allow_html=True)

def save_api_key_to_config(api_key):
    """Save API key to config file"""
    try:
        config_path = Path("config.py")
        if config_path.exists():
            # Read current config
            with open(config_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Update API key
            if 'DEFAULT_API_KEY = ' in content:
                # Replace existing API key
                import re
                content = re.sub(
                    r'DEFAULT_API_KEY = "[^"]*"',
                    f'DEFAULT_API_KEY = "{api_key}"',
                    content
                )
            else:
                # Add API key if not present
                content = content.replace(
                    '# Default API Key (leave empty to prompt user)',
                    f'# Default API Key (leave empty to prompt user)\nDEFAULT_API_KEY = "{api_key}"'
                )
            
            # Write updated config
            with open(config_path, 'w', encoding='utf-8') as f:
                f.write(content)
            
            return True
        else:
            # Create new config file
            config_content = f'''# 🎯 ImageSEO Pro Configuration
# Edit these settings to customize your experience

# Default API Key (leave empty to prompt user)
# You can set your OpenAI API key here for convenience
DEFAULT_API_KEY = "{api_key}"

# Default Settings for Image Processing
DEFAULT_SETTINGS = {{
    "description_style": "SEO Optimized",
    "length_range": (15, 25),
    "company_name": "",
    "location": "",
    "service_type": "",
    "output_format": "WebP Optimized",
    "quality": 85,
    "crop_dimensions": None
}}

# UI Settings
UI_SETTINGS = {{
    "theme": "modern",
    "sidebar_expanded": True,
    "auto_open_browser": True,
    "port": 8501
}}

# Processing Settings
PROCESSING_SETTINGS = {{
    "max_images_per_batch": 10,
    "max_file_size_mb": 20,
    "supported_formats": [".jpg", ".jpeg", ".png", ".webp"]
}}

# Advanced Settings
ADVANCED_SETTINGS = {{
    "retry_attempts": 3,
    "enable_image_enhancement": True,
    "enable_compression_analytics": True,
    "auto_cleanup_temp_files": True,
    "enable_detailed_logging": False
}}
'''
            with open(config_path, 'w', encoding='utf-8') as f:
                f.write(config_content)
            
            return True
    except Exception as e:
        st.error(f"Failed to save API key: {str(e)}")
        return False

def render_sidebar_config():
    """Render the sidebar configuration with full control options"""
    with st.sidebar:
        st.markdown("### ⚙️ Configuration")
        
        # API Key Section
        with st.expander("🔑 API Configuration", expanded=True):
            # Get saved API key
            saved_api_key = get_api_key()
            
            api_key = st.text_input(
                "OpenAI API Key",
                value=saved_api_key,
                type="password",
                help="Enter your OpenAI API key to enable AI analysis"
            )
            
            if api_key and api_key != saved_api_key:
                if st.button("💾 Save API Key"):
                    if save_api_key_to_config(api_key):
                        st.success("✅ API Key saved to config file")
                        st.rerun()
                    else:
                        st.error("❌ Failed to save API key")
            
            if api_key:
                st.success("✅ API Key configured")
            else:
                st.error("❌ API Key required")
        
        # Business Information Section
        with st.expander("🏢 Business Information", expanded=True):
            company_name = st.text_input(
                "🏢 Company Name (Optional)",
                value=st.session_state.get("company_name", DEFAULT_SETTINGS.get("company_name", "")),
                help="Your business name - will be included in descriptions if provided"
            )
            
            location = st.text_input(
                "🌍 Location (Optional)",
                value=st.session_state.get("location", DEFAULT_SETTINGS.get("location", "")),
                help="Your location - will be included in descriptions if provided"
            )
            
            # Service Category Selection
            service_category = st.selectbox(
                "🏗️ Service Category",
                ["Select a category..."] + list(SERVICE_CATEGORIES.keys()),
                index=0,
                help="Choose your primary service category"
            )
            
            # Service Type Selection (depends on category)
            service_type = ""
            if service_category and service_category != "Select a category...":
                sub_services = SERVICE_CATEGORIES[service_category]
                selected_service = st.selectbox(
                    "🔧 Specific Service",
                    ["Select a service..."] + sub_services,
                    index=0,
                    help="Choose your specific service type"
                )
                if selected_service and selected_service != "Select a service...":
                    service_type = selected_service
            else:
                # Fallback to text input if no category selected
                service_type = st.text_input(
                    "🔧 Service Type (Optional)",
                    value=st.session_state.get("service_type", DEFAULT_SETTINGS.get("service_type", "")),
                    help="Your service type - will be included in descriptions if provided"
                )
            
            # Show what will be included
            if company_name or location or service_type:
                st.info("📍 Business info will be integrated into descriptions")
                info_parts = []
                if location:
                    info_parts.append(f"Location: {location}")
                if company_name:
                    info_parts.append(f"Company: {company_name}")
                if service_type:
                    info_parts.append(f"Service: {service_type}")
                st.markdown(f"<div style='color: white; background: rgba(25, 50, 100, 0.98); padding: 0.75rem; border-radius: 8px; border: 2px solid #4a90e2; margin: 0.5rem 0;'><strong>Will include:</strong> {' | '.join(info_parts)}</div>", unsafe_allow_html=True)
        
        # Description Options
        with st.expander("📝 Description Options", expanded=True):
            # Always use SEO Optimized style for best results
            description_style = "SEO Optimized"
            
            # Calculate business info word count
            business_words = 0
            if company_name:
                business_words += len(company_name.split())
            if location:
                business_words += len(location.split())
            if service_type:
                business_words += len(service_type.split())
            
            # Smart word count filtering based on business info
            available_options = []
            if business_words <= 5:
                available_options = ["Low number of words", "Medium number of words", "High number of words"]
            elif business_words <= 10:
                available_options = ["Low number of words", "Medium number of words", "High number of words"]
            elif business_words <= 15:
                available_options = ["Medium number of words", "High number of words"]
            else:
                available_options = ["High number of words"]
            
            # Get current selection - default to Medium
            current_length = "Medium number of words"
            
            # If current selection is not available, use first available
            if current_length not in available_options:
                current_length = available_options[0]
            
            length_option = st.selectbox(
                "Length",
                available_options,
                index=available_options.index(current_length),
                help=f"Business info uses ~{business_words} words. Available options adjusted accordingly."
            )
            
            # Convert to min/max values
            length_ranges = {
                "Low number of words": (8, 15),
                "Medium number of words": (15, 30),
                "High number of words": (25, 60)
            }
            min_length, max_length = length_ranges[length_option]
        
        # Image Optimization
        with st.expander("🖼️ Image Optimization", expanded=True):
            output_format = st.selectbox(
                "Format",
                ["WebP Optimized", "JPG Optimized", "Keep Original"],
                index=["WebP Optimized", "JPG Optimized", "Keep Original"].index(
                    st.session_state.get("output_format", DEFAULT_SETTINGS.get("output_format", "WebP Optimized"))
                ),
                help="Choose output format for best performance"
            )
            
            quality = st.slider(
                "Quality",
                min_value=60,
                max_value=95,
                value=st.session_state.get("quality", DEFAULT_SETTINGS.get("quality", 85)),
                help="Higher quality = larger files"
            )
        
        # Smart Cropping
        with st.expander("✂️ Smart Cropping", expanded=False):
            # Enable/disable cropping
            enable_cropping = st.checkbox(
                "Enable Custom Cropping",
                value=False,
                help="Enable to set custom dimensions for smart resize and crop"
            )
            
            crop_dimensions = None
            if enable_cropping:
                st.markdown("**Custom Dimensions (Max: 8000x8000)**")
                
                col1, col2 = st.columns(2)
                with col1:
                    width = st.number_input(
                        "Width (px)",
                        min_value=100,
                        max_value=8000,
                        value=1200,
                        step=50,
                        help="Width in pixels (max 8000)"
                    )
                
                with col2:
                    height = st.number_input(
                        "Height (px)",
                        min_value=100,
                        max_value=8000,
                        value=630,
                        step=50,
                        help="Height in pixels (max 8000)"
                    )
                
                # Validate dimensions
                if width > 8000 or height > 8000:
                    st.error("⚠️ Maximum dimensions are 8000x8000 pixels")
                    crop_dimensions = None
                elif width < 100 or height < 100:
                    st.error("⚠️ Minimum dimensions are 100x100 pixels")
                    crop_dimensions = None
                else:
                    crop_dimensions = (width, height)
                    st.success(f"✅ Target dimensions: {width}x{height} pixels")
                
                st.markdown("""
                **Smart Cropping Features:**
                - Maintains aspect ratio to prevent distortion
                - Intelligently crops to focus on the main subject
                - Resizes images to fit within specified dimensions
                - Optimizes for best visual composition
                """)
        
        # Store values in session state
        st.session_state.company_name = company_name
        st.session_state.location = location
        st.session_state.service_type = service_type
        st.session_state.description_style = description_style
        st.session_state.output_format = output_format
        st.session_state.quality = quality
        st.session_state.crop_dimensions = crop_dimensions
        
        return api_key, description_style, (min_length, max_length), company_name, location, service_type, output_format, quality, crop_dimensions

def process_images(input_folder, api_key, description_style, length_range, company_name, location, service_type, output_format, quality, crop_dimensions):
    """Process all images with enhanced progress tracking and error handling"""
    try:
        # Get image files from the specific input folder - only process what's actually there
        image_files = []
        for ext in ['*.jpg', '*.jpeg', '*.png', '*.webp']:
            image_files.extend(input_folder.glob(ext))
            image_files.extend(input_folder.glob(ext.upper()))
        
        # Remove duplicates and sort files to ensure consistent processing order
        image_files = sorted(list(set(image_files)))
        
        if not image_files:
            st.error("❌ No valid image files found in the uploaded files.")
            return
        
        # Debug: Show what files were found
        st.info(f"🔍 Found {len(image_files)} image files to process")
        
        # Show the actual files being processed
        file_names = [f.name for f in image_files]
        st.info(f"📋 Files to process: {', '.join(file_names)}")
        
        # Process all uploaded images (no artificial limit)
        st.info(f"📊 Processing {len(image_files)} uploaded images")
        
        # Create processor
        processor = ImageProcessor(api_key)
        
        # Create output folder
        output_folder = Path("processed_images")
        output_folder.mkdir(exist_ok=True)
        st.session_state.output_folder = output_folder
        
        # Enhanced progress tracking
        progress_bar = st.progress(0)
        status_text = st.empty()
        
        # Create results container
        results_container = st.container()
        
        processed_count = 0
        st.session_state.processed_images = []
        
        with results_container:
            st.markdown("### 📊 Processing Results")
            
            for i, image_path in enumerate(image_files):
                try:
                    status_text.text(f"🔄 Processing {image_path.name}... ({i+1}/{len(image_files)})")
                    
                    # Analyze image
                    description = processor.analyze_image(
                        image_path,
                        description_style,
                        length_range,
                        company_name,
                        location,
                        service_type
                    )
                    
                    # Process and optimize
                    output_path = processor.process_and_optimize_image(
                        image_path,
                        output_folder,
                        description,
                        output_format,
                        quality,
                        crop_dimensions
                    )
                    
                    # Store results
                    st.session_state.processed_images.append({
                        'original': image_path.name,
                        'processed': output_path.name,
                        'description': description,
                        'original_size': image_path.stat().st_size,
                        'processed_size': output_path.stat().st_size
                    })
                    
                    processed_count += 1
                    progress_bar.progress((i + 1) / len(image_files))
                    
                    # Show individual result
                    with st.expander(f"✅ {image_path.name} → {output_path.name}", expanded=False):
                        col1, col2 = st.columns(2)
                        with col1:
                            st.markdown(f"<div style='color: white; background: rgba(25, 50, 100, 0.95); padding: 0.75rem; border-radius: 8px; border: 1px solid #4a90e2;'><strong>Description:</strong> {description}</div>", unsafe_allow_html=True)
                            # Debug: Show if business info was integrated
                            if company_name or location or service_type:
                                business_parts = []
                                if location:
                                    business_parts.append(location.lower())
                                if company_name:
                                    business_parts.append(company_name.lower())
                                if service_type:
                                    # Extract only the specific service
                                    service_parts = service_type.strip().split(' → ')
                                    if len(service_parts) > 1:
                                        specific_service = service_parts[-1].strip().lower()
                                    else:
                                        specific_service = service_type.strip().lower()
                                    business_parts.append(specific_service)
                                
                                # Check if business info is integrated (since we put it at the beginning with dashes)
                                description_lower = description.lower()
                                business_integrated = any(part.replace(' ', '-') in description_lower for part in business_parts)
                                
                                if business_integrated:
                                    business_display = " - ".join([company_name or '', location or '', service_type or '']).strip(' -')
                                    st.markdown(f"<div style='color: #90EE90; background: rgba(20, 80, 40, 0.95); padding: 0.5rem; border-radius: 6px; border: 1px solid #16a34a;'><strong>✅ Business info integrated:</strong> {business_display}</div>", unsafe_allow_html=True)
                                else:
                                    business_display = " - ".join([company_name or '', location or '', service_type or '']).strip(' -')
                                    st.markdown(f"<div style='color: #FFB6C1; background: rgba(80, 20, 20, 0.95); padding: 0.5rem; border-radius: 6px; border: 1px solid #dc2626;'><strong>❌ Business info missing:</strong> {business_display}</div>", unsafe_allow_html=True)
                        with col2:
                            original_mb = image_path.stat().st_size / (1024 * 1024)
                            processed_mb = output_path.stat().st_size / (1024 * 1024)
                            compression = ((original_mb - processed_mb) / original_mb) * 100
                            st.markdown(f"<div style='color: white; background: rgba(25, 50, 100, 0.95); padding: 0.75rem; border-radius: 8px; border: 1px solid #4a90e2;'><strong>Size:</strong> {original_mb:.1f}MB → {processed_mb:.1f}MB ({compression:.1f}% smaller)</div>", unsafe_allow_html=True)
                    
                except Exception as e:
                    st.error(f"❌ Error processing {image_path.name}: {str(e)}")
                    continue
        
        status_text.text(f"✅ Processing complete! Successfully processed {processed_count} images.")
        st.session_state.processing_complete = True
        
        # Show processing statistics
        if st.session_state.processed_images:
            stats = calculate_processing_stats(st.session_state.processed_images)
            show_processing_stats(stats)
        
    except Exception as e:
        st.error(f"❌ Processing failed: {str(e)}")
        st.error(f"Debug info: input_folder={input_folder}, files_found={len(image_files) if 'image_files' in locals() else 'N/A'}")

def show_processing_stats(stats):
    """Display processing statistics in a modern card layout"""
    st.markdown("### 📈 Processing Statistics")
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.markdown(f"""
        <div class="stats-card">
            <div class="stats-number">{stats['total_count']}</div>
            <div class="stats-label">Images Processed</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown(f"""
        <div class="stats-card">
            <div class="stats-number">{stats['avg_description_length']}</div>
            <div class="stats-label">Avg Words</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown(f"""
        <div class="stats-card">
            <div class="stats-number">{stats['unique_descriptions']}</div>
            <div class="stats-label">Unique Descriptions</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col4:
        if stats['common_words']:
            common_words_str = ", ".join(stats['common_words'][:3])
            st.markdown(f"""
            <div class="stats-card">
                <div class="stats-number">Top</div>
                <div class="stats-label">{common_words_str}</div>
            </div>
            """, unsafe_allow_html=True)

def render_compact_upload_section():
    """Render the compact upload section"""
    # Removed the upload section - only keep the drag & drop area
    pass

def main():
    """Main application function"""
    # Apply modern styling
    apply_modern_css()
    
    # Render header
    render_header()
    
    # Initialize session state
    if 'processed_images' not in st.session_state:
        st.session_state.processed_images = []
    if 'processing_complete' not in st.session_state:
        st.session_state.processing_complete = False
    if 'output_folder' not in st.session_state:
        st.session_state.output_folder = None
    
    # Get configuration from sidebar
    api_key, description_style, length_range, company_name, location, service_type, output_format, quality, crop_dimensions = render_sidebar_config()
    
    # Check API key
    if not api_key:
        st.error("❌ Please provide an OpenAI API key in the sidebar to continue.")
        st.stop()
    
    # Main content area - Clean drag & drop only
    # File uploader - direct drag & drop (max 10 images)
    uploaded_files = st.file_uploader(
        "Choose image files (max 10)",
        type=['jpg', 'jpeg', 'png', 'webp'],
        accept_multiple_files=True,
        help="Select up to 10 images for processing • Drag and drop or click to browse",
        label_visibility="collapsed"
    )
    
    # Limit to 10 images
    if uploaded_files and len(uploaded_files) > 10:
        st.warning(f"⚠️ Maximum 10 images allowed. Only the first 10 will be processed.")
        uploaded_files = uploaded_files[:10]
    
    if uploaded_files:
        # Show upload summary
        total_size = sum(file.size for file in uploaded_files)
        st.success(f"📁 {len(uploaded_files)} files uploaded ({total_size / (1024*1024):.1f} MB total)")
        
        # Files will be shown during the saving process with "Saved:" messages
        
        # Save uploaded files to temp directory
        input_folder = Path("temp_input")
        input_folder.mkdir(exist_ok=True)
        
        # Clear and populate folder - ensure clean state
        shutil.rmtree(input_folder, ignore_errors=True)
        input_folder.mkdir(exist_ok=True)
        
        # Also clear processed_images folder to avoid confusion
        processed_folder = Path("processed_images")
        if processed_folder.exists():
            shutil.rmtree(processed_folder, ignore_errors=True)
        
        # Debug: Show what we're saving
        st.info(f"💾 Saving {len(uploaded_files)} uploaded files to {input_folder}")
        
        for uploaded_file in uploaded_files:
            file_path = input_folder / uploaded_file.name
            with open(file_path, "wb") as f:
                f.write(uploaded_file.getbuffer())
            st.markdown(f"<div style='color: white;'>✅ Saved: {uploaded_file.name} ({uploaded_file.size / (1024*1024):.1f} MB)</div>", unsafe_allow_html=True)
        
        # Verify files were saved
        saved_files = list(input_folder.glob("*"))
        st.info(f"📁 Verified {len(saved_files)} files in temp directory")
        
        # Process button
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            if st.button("🚀 Start Processing", type="primary", use_container_width=True):
                # Clear previous results completely
                st.session_state.processed_images = []
                st.session_state.processing_complete = False
                
                # Clear output folder completely
                output_folder = Path("processed_images")
                if output_folder.exists():
                    shutil.rmtree(output_folder, ignore_errors=True)
                output_folder.mkdir(exist_ok=True)
                st.session_state.output_folder = output_folder
                
                if validate_folder(input_folder):
                    # Debug: Show business info being passed
                    st.info(f"🏢 Business Info: Company='{company_name}', Location='{location}', Service='{service_type}'")
                    
                    # Debug: Show what will be integrated
                    if company_name or location or service_type:
                        business_parts = []
                        if location:
                            business_parts.append(location)
                        if company_name:
                            business_parts.append(company_name)
                        if service_type:
                            # Extract only the specific service, not the full category chain
                            service_parts = service_type.strip().split(' → ')
                            if len(service_parts) > 1:
                                specific_service = service_parts[-1].strip()
                            else:
                                specific_service = service_type.strip()
                            business_parts.append(specific_service)
                        st.info(f"🔗 Will integrate: {' - '.join(business_parts)}")
                    
                    process_images(
                        input_folder,
                        api_key,
                        description_style,
                        length_range,
                        company_name,
                        location,
                        service_type,
                        output_format,
                        quality,
                        crop_dimensions
                    )
                else:
                    st.error("❌ No valid images found in the uploaded files.")
    
    # Show download section for completed processing
    if st.session_state.processing_complete and st.session_state.processed_images:
        st.markdown("---")
        st.markdown("### 📥 Download Results")
        
        if st.session_state.output_folder and Path(st.session_state.output_folder).exists():
            # Create ZIP with current batch files only
            current_batch_files = [Path(st.session_state.output_folder) / item['processed'] 
                                 for item in st.session_state.processed_images]
            
            if current_batch_files and all(f.exists() for f in current_batch_files):
                # Create temporary ZIP with proper cleanup
                try:
                    with tempfile.NamedTemporaryFile(delete=False, suffix='.zip') as tmp_zip:
                        zip_path = tmp_zip.name
                    
                    # Create the ZIP file with only the current batch
                    with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
                        for file_path in current_batch_files:
                            zipf.write(file_path, file_path.name)
                    
                    # Read ZIP data
                    with open(zip_path, "rb") as f:
                        zip_data = f.read()
                    
                    # Clean up temp file with retry logic
                    try:
                        os.unlink(zip_path)
                    except PermissionError:
                        # If file is still in use, schedule cleanup for later
                        import atexit
                        def cleanup_later():
                            try:
                                if os.path.exists(zip_path):
                                    os.unlink(zip_path)
                            except:
                                pass
                        atexit.register(cleanup_later)
                    
                    # Download button with cleanup
                    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                    
                    def clear_after_download():
                        # Clear all processed files and session state
                        if st.session_state.output_folder and Path(st.session_state.output_folder).exists():
                            shutil.rmtree(st.session_state.output_folder, ignore_errors=True)
                        st.session_state.processed_images = []
                        st.session_state.processing_complete = False
                        st.session_state.output_folder = None
                    
                    st.download_button(
                        label="📥 Download Processed Images",
                        data=zip_data,
                        file_name=f"imageseo_pro_batch_{timestamp}.zip",
                        mime="application/zip",
                        type="primary",
                        use_container_width=True,
                        on_click=clear_after_download
                    )
                    
                    st.info(f"📦 Package contains {len(current_batch_files)} optimized images")
                    
                    # Clear everything after successful download
                    st.success("✅ Download ready! Files will be cleared after download.")
                    
                except Exception as e:
                    st.error(f"❌ Error creating download package: {str(e)}")

if __name__ == "__main__":
    main()
