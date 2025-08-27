# 🎯 ImgSage Configuration
# Edit these settings to customize your experience

# Default API Key (leave empty to prompt user)
# You can set your OpenAI API key here for convenience
# For production, use environment variables instead
DEFAULT_API_KEY = ""

# Default Settings for Image Processing
DEFAULT_SETTINGS = {
    "description_style": "SEO Optimized",  # Options: "SEO Optimized", "Local SEO Optimized", "Detailed", "Concise", "Creative"
    "length_range": (15, 30),  # Min and max words for descriptions (Medium)
    "company_name": "",  # Your business name - will be included if provided
    "location": "",  # Your location - will be included if provided
    "service_type": "",  # Your service type - will be included if provided
    "output_format": "WebP Optimized",  # Options: "WebP Optimized", "JPG Optimized", "Keep Original"
    "quality": 85,  # Image quality (60-95)
    "crop_dimensions": None  # Options: None, (1200, 630), (1200, 500), (600, 725), (800, 800)
}

# UI Settings
UI_SETTINGS = {
    "theme": "modern",  # Theme for the interface
    "sidebar_expanded": True,  # Start with sidebar expanded
    "auto_open_browser": True,  # Automatically open browser
    "port": 8501  # Port for the web interface
}

# Processing Settings
PROCESSING_SETTINGS = {
    "max_images_per_batch": 10,  # Maximum images to process at once
    "max_file_size_mb": 20,  # Maximum file size per image
    "supported_formats": [".jpg", ".jpeg", ".png", ".webp"]  # Supported image formats
}

# Service Categories and Sub-Services
SERVICE_CATEGORIES = {
    "🏡 Home Construction & Remodeling": [
        "Home construction",
        "Home remodeling", 
        "Kitchen remodeling",
        "Bathroom remodeling",
        "Basement finishing",
        "Attic conversions",
        "Home additions"
    ],
    "🪟 Exterior & Structural Work": [
        "Roofing",
        "Siding", 
        "Window installation",
        "Door installation",
        "Gutter installation",
        "Foundation repair",
        "Masonry & concrete work"
    ],
    "🌳 Outdoor Living & Landscaping": [
        "Deck building",
        "Patio installation",
        "Pergola & gazebo building", 
        "Outdoor kitchens & fireplaces",
        "Fence installation",
        "Pool & spa installation",
        "Landscaping & hardscaping"
    ],
    "🛠️ Interior Finishes & Carpentry": [
        "Flooring installation",
        "Drywall installation",
        "Painting",
        "Trim & carpentry",
        "Cabinet installation",
        "Stair & railing construction"
    ],
    "⚡ Mechanical, Electrical & Plumbing (MEP)": [
        "Electrical work",
        "Plumbing",
        "HVAC",
        "Smart home systems"
    ],
    "🧱 Specialty Services": [
        "Insulation",
        "Solar panel installation",
        "Soundproofing",
        "Accessibility modifications",
        "Storm shelters & safe rooms"
    ],
    "🏢 Commercial Contracting": [
        "Commercial build-outs",
        "Retail remodeling",
        "Restaurant & hospitality construction",
        "Industrial facilities"
    ]
}

# Advanced Settings
ADVANCED_SETTINGS = {
    "retry_attempts": 3,  # Number of retry attempts for API calls
    "enable_image_enhancement": True,  # Enable automatic image enhancement
    "enable_compression_analytics": True,  # Show compression statistics
    "auto_cleanup_temp_files": True,  # Automatically clean up temporary files
    "enable_detailed_logging": False  # Enable detailed logging for debugging
}
