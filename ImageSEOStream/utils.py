import zipfile
import shutil
from pathlib import Path
import os
import re
import json
from datetime import datetime
import hashlib

def validate_folder(folder_path):
    """
    Validate if the folder contains supported image files
    
    Args:
        folder_path (Path): Path to the folder to validate
        
    Returns:
        bool: True if folder contains valid images, False otherwise
    """
    if not folder_path.exists() or not folder_path.is_dir():
        return False
    
    supported_extensions = {'.jpg', '.jpeg', '.png', '.webp'}
    
    for file_path in folder_path.iterdir():
        if file_path.is_file() and file_path.suffix.lower() in supported_extensions:
            return True
    
    return False

def create_zip_file(folder_path, zip_name=None):
    """
    Create a ZIP file containing all files in the specified folder
    
    Args:
        folder_path (str or Path): Path to the folder to zip
        zip_name (str): Optional name for the ZIP file
        
    Returns:
        Path: Path to the created ZIP file, or None if failed
    """
    try:
        folder_path = Path(folder_path)
        
        if not folder_path.exists() or not folder_path.is_dir():
            return None
        
        if zip_name is None:
            zip_name = f"{folder_path.name}.zip"
        
        zip_path = folder_path.parent / zip_name
        
        with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
            for file_path in folder_path.rglob('*'):
                if file_path.is_file():
                    # Add file to zip with relative path
                    arcname = file_path.relative_to(folder_path)
                    zipf.write(file_path, arcname)
        
        return zip_path
        
    except Exception as e:
        print(f"Error creating ZIP file: {str(e)}")
        return None

def get_file_size_mb(file_path):
    """
    Get file size in megabytes
    
    Args:
        file_path (Path): Path to the file
        
    Returns:
        float: File size in MB
    """
    try:
        size_bytes = file_path.stat().st_size
        return size_bytes / (1024 * 1024)
    except Exception:
        return 0.0

def clean_filename(filename):
    """
    Clean a filename to make it safe for file systems
    
    Args:
        filename (str): Original filename
        
    Returns:
        str: Cleaned filename
    """
    # Remove or replace problematic characters
    filename = re.sub(r'[<>:"/\\|?*]', '', filename)
    filename = re.sub(r'\s+', '_', filename)  # Replace spaces with underscores
    filename = filename.strip('.')  # Remove leading/trailing dots
    
    # Ensure filename isn't empty or just an extension
    if not filename or filename.startswith('.'):
        filename = 'file' + filename
    
    return filename

def ensure_unique_filename(directory, filename):
    """
    Ensure filename is unique in the specified directory
    
    Args:
        directory (Path): Target directory
        filename (str): Proposed filename
        
    Returns:
        str: Unique filename
    """
    directory = Path(directory)
    original_filename = filename
    name_part = Path(filename).stem
    extension = Path(filename).suffix
    
    counter = 1
    while (directory / filename).exists():
        filename = f"{name_part}_{counter}{extension}"
        counter += 1
    
    return filename

def get_supported_image_files(folder_path):
    """
    Get list of supported image files in a folder
    
    Args:
        folder_path (Path): Path to the folder
        
    Returns:
        list: List of supported image file paths
    """
    folder_path = Path(folder_path)
    supported_extensions = {'.jpg', '.jpeg', '.png', '.webp'}
    
    image_files = []
    for file_path in folder_path.iterdir():
        if (file_path.is_file() and 
            file_path.suffix.lower() in supported_extensions):
            image_files.append(file_path)
    
    return sorted(image_files)

def format_file_size(size_bytes):
    """
    Format file size in human-readable format
    
    Args:
        size_bytes (int): Size in bytes
        
    Returns:
        str: Formatted size string
    """
    for unit in ['B', 'KB', 'MB', 'GB']:
        if size_bytes < 1024.0:
            return f"{size_bytes:.1f} {unit}"
        size_bytes /= 1024.0
    return f"{size_bytes:.1f} TB"

def validate_api_key(api_key):
    """
    Enhanced validation for API key format
    
    Args:
        api_key (str): API key to validate
        
    Returns:
        dict: Validation result with status and message
    """
    if not api_key:
        return {
            'valid': False,
            'message': 'API key is required'
        }
    
    # Check if it's empty or just whitespace
    if not api_key.strip():
        return {
            'valid': False,
            'message': 'API key cannot be empty'
        }
    
    # OpenAI API keys typically start with 'sk-' and are around 51 characters
    if api_key.startswith('sk-') and len(api_key) >= 20:
        return {
            'valid': True,
            'message': 'API key format looks valid'
        }
    
    return {
        'valid': False,
        'message': 'Invalid API key format. Should start with "sk-"'
    }

def calculate_processing_stats(processed_images):
    """
    Calculate comprehensive statistics for processed images
    
    Args:
        processed_images (list): List of processed image dictionaries
        
    Returns:
        dict: Statistics dictionary
    """
    if not processed_images:
        return {
            'total_count': 0,
            'avg_description_length': 0,
            'unique_descriptions': 0,
            'common_words': [],
            'total_original_size': 0,
            'total_processed_size': 0,
            'avg_compression_ratio': 0,
            'processing_time': 0
        }
    
    total_count = len(processed_images)
    
    # Calculate average description length
    total_words = sum(len(img['description'].split()) for img in processed_images)
    avg_description_length = total_words / total_count
    
    # Count unique descriptions
    unique_descriptions = len(set(img['description'] for img in processed_images))
    
    # Find common words
    all_words = []
    for img in processed_images:
        words = img['description'].lower().split()
        all_words.extend(words)
    
    word_freq = {}
    for word in all_words:
        if len(word) > 2:  # Only count words longer than 2 characters
            word_freq[word] = word_freq.get(word, 0) + 1
    
    # Get top 5 most common words
    common_words = sorted(word_freq.items(), key=lambda x: x[1], reverse=True)[:5]
    
    # Calculate size statistics
    total_original_size = sum(img.get('original_size', 0) for img in processed_images)
    total_processed_size = sum(img.get('processed_size', 0) for img in processed_images)
    
    avg_compression_ratio = 0
    if total_original_size > 0:
        avg_compression_ratio = ((total_original_size - total_processed_size) / total_original_size) * 100
    
    return {
        'total_count': total_count,
        'avg_description_length': round(avg_description_length, 1),
        'unique_descriptions': unique_descriptions,
        'common_words': [word for word, count in common_words],
        'total_original_size': total_original_size,
        'total_processed_size': total_processed_size,
        'avg_compression_ratio': round(avg_compression_ratio, 1)
    }

def generate_processing_report(processed_images, processing_time=None):
    """
    Generate a detailed processing report
    
    Args:
        processed_images (list): List of processed image dictionaries
        processing_time (float): Processing time in seconds
        
    Returns:
        dict: Detailed report
    """
    stats = calculate_processing_stats(processed_images)
    
    report = {
        'timestamp': datetime.now().isoformat(),
        'summary': {
            'total_images': stats['total_count'],
            'processing_time': processing_time,
            'avg_compression': f"{stats['avg_compression_ratio']}%",
            'total_size_saved': format_file_size(stats['total_original_size'] - stats['total_processed_size'])
        },
        'statistics': stats,
        'images': []
    }
    
    # Add individual image details
    for img in processed_images:
        original_mb = img.get('original_size', 0) / (1024 * 1024)
        processed_mb = img.get('processed_size', 0) / (1024 * 1024)
        compression = ((original_mb - processed_mb) / original_mb * 100) if original_mb > 0 else 0
        
        report['images'].append({
            'original_name': img['original'],
            'processed_name': img['processed'],
            'description': img['description'],
            'original_size_mb': round(original_mb, 2),
            'processed_size_mb': round(processed_mb, 2),
            'compression_percent': round(compression, 1)
        })
    
    return report

def save_processing_report(report, output_folder):
    """
    Save processing report to JSON file
    
    Args:
        report (dict): Processing report
        output_folder (Path): Output folder path
        
    Returns:
        Path: Path to saved report file
    """
    try:
        output_folder = Path(output_folder)
        output_folder.mkdir(exist_ok=True)
        
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        report_filename = f"processing_report_{timestamp}.json"
        report_path = output_folder / report_filename
        
        with open(report_path, 'w', encoding='utf-8') as f:
            json.dump(report, f, indent=2, ensure_ascii=False)
        
        return report_path
    except Exception as e:
        print(f"Error saving report: {str(e)}")
        return None

def calculate_file_hash(file_path):
    """
    Calculate SHA-256 hash of a file
    
    Args:
        file_path (Path): Path to the file
        
    Returns:
        str: SHA-256 hash of the file
    """
    try:
        hash_sha256 = hashlib.sha256()
        with open(file_path, "rb") as f:
            for chunk in iter(lambda: f.read(4096), b""):
                hash_sha256.update(chunk)
        return hash_sha256.hexdigest()
    except Exception:
        return None

def validate_image_file(file_path):
    """
    Comprehensive image file validation
    
    Args:
        file_path (Path): Path to the image file
        
    Returns:
        dict: Validation result
    """
    try:
        file_path = Path(file_path)
        
        # Check if file exists
        if not file_path.exists():
            return {
                'valid': False,
                'message': 'File does not exist'
            }
        
        # Check if it's a file
        if not file_path.is_file():
            return {
                'valid': False,
                'message': 'Path is not a file'
            }
        
        # Check file size
        file_size = file_path.stat().st_size
        if file_size == 0:
            return {
                'valid': False,
                'message': 'File is empty'
            }
        
        # Check file size limit (20MB)
        if file_size > 20 * 1024 * 1024:
            return {
                'valid': False,
                'message': 'File size exceeds 20MB limit'
            }
        
        # Check file extension
        supported_extensions = {'.jpg', '.jpeg', '.png', '.webp'}
        if file_path.suffix.lower() not in supported_extensions:
            return {
                'valid': False,
                'message': f'Unsupported file format: {file_path.suffix}'
            }
        
        # Try to open with PIL to validate image
        try:
            from PIL import Image
            with Image.open(file_path) as img:
                img.verify()
        except Exception as e:
            return {
                'valid': False,
                'message': f'Invalid image file: {str(e)}'
            }
        
        return {
            'valid': True,
            'message': 'File is valid',
            'size_mb': file_size / (1024 * 1024),
            'format': file_path.suffix.lower()
        }
        
    except Exception as e:
        return {
            'valid': False,
            'message': f'Validation error: {str(e)}'
        }

def cleanup_temp_files(temp_folder):
    """
    Clean up temporary files and folders
    
    Args:
        temp_folder (Path): Path to temporary folder
        
    Returns:
        bool: True if cleanup successful
    """
    try:
        temp_folder = Path(temp_folder)
        if temp_folder.exists():
            shutil.rmtree(temp_folder)
        return True
    except Exception as e:
        print(f"Error cleaning up temp files: {str(e)}")
        return False

def get_image_metadata(file_path):
    """
    Extract basic metadata from image file
    
    Args:
        file_path (Path): Path to the image file
        
    Returns:
        dict: Image metadata
    """
    try:
        from PIL import Image
        from PIL.ExifTags import TAGS
        
        with Image.open(file_path) as img:
            metadata = {
                'format': img.format,
                'mode': img.mode,
                'size': img.size,
                'width': img.size[0],
                'height': img.size[1],
                'aspect_ratio': round(img.size[0] / img.size[1], 2),
                'file_size': file_path.stat().st_size
            }
            
            # Try to extract EXIF data
            try:
                exif_data = img._getexif()
                if exif_data:
                    exif_info = {}
                    for tag_id, value in exif_data.items():
                        tag = TAGS.get(tag_id, tag_id)
                        exif_info[tag] = value
                    metadata['exif'] = exif_info
            except Exception:
                pass  # EXIF data not available
            
            return metadata
            
    except Exception as e:
        return {
            'error': str(e),
            'file_size': file_path.stat().st_size if file_path.exists() else 0
        }

def estimate_processing_time(num_images, avg_file_size_mb):
    """
    Estimate processing time based on number of images and file sizes
    
    Args:
        num_images (int): Number of images to process
        avg_file_size_mb (float): Average file size in MB
        
    Returns:
        dict: Time estimates
    """
    # Rough estimates based on typical processing times
    base_time_per_image = 5  # seconds for small images
    size_factor = avg_file_size_mb / 2  # Additional time for larger files
    
    estimated_seconds = num_images * (base_time_per_image + size_factor)
    
    minutes = int(estimated_seconds // 60)
    seconds = int(estimated_seconds % 60)
    
    return {
        'total_seconds': estimated_seconds,
        'formatted_time': f"{minutes}m {seconds}s",
        'per_image_seconds': estimated_seconds / num_images if num_images > 0 else 0
    }
