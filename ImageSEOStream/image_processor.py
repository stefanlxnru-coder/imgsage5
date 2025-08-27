import base64
import os
import re
from pathlib import Path
from PIL import Image, ImageOps, ImageEnhance
import io
try:
    import cv2
    import numpy as np
    OPENCV_AVAILABLE = True
except ImportError:
    OPENCV_AVAILABLE = False
    print("Warning: OpenCV not available. Some image processing features may be limited.")
from openai import OpenAI
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class ImageProcessor:
    def __init__(self, api_key):
        """Initialize the ImageProcessor with OpenAI API key"""
        self.client = OpenAI(api_key=api_key)
        # Use the latest GPT-4o model for best vision capabilities
        self.model = "gpt-4o"
        self.max_retries = 3
        self.retry_delay = 1
    
    def analyze_image(self, image_path, style="SEO Optimized", length_range=(10, 15), company_name="", location="", service_type=""):
        """
        Analyze an image and generate a description based on the specified style
        
        Args:
            image_path (Path): Path to the image file
            style (str): Style of description to generate
            length_range (tuple): Min/max word count for description
            company_name (str): Company name for local SEO
            location (str): Location for local SEO
            service_type (str): Service type for contractor businesses
            
        Returns:
            str: Generated description
        """
        for attempt in range(self.max_retries):
            try:
                # Load and validate image
                image = self._load_and_prepare_image(image_path)
                
                # Convert to base64
                image_base64 = self._image_to_base64(image)
                
                # Create enhanced prompt
                prompt = self._create_enhanced_prompt(style, length_range, company_name, location, service_type)
                
                # Call OpenAI Vision API with retry logic
                response = self._call_openai_api(prompt, image_base64)
                
                if response and response.choices and response.choices[0].message:
                    description = response.choices[0].message.content.strip()
                    if description:
                        # Clean and validate the description
                        description = self._clean_description(description, length_range, company_name, location, service_type)
                        return description
                
                # If we get here, try again
                if attempt < self.max_retries - 1:
                    logger.warning(f"Attempt {attempt + 1} failed, retrying...")
                    continue
                    
            except Exception as e:
                logger.error(f"Error in attempt {attempt + 1}: {str(e)}")
                if attempt < self.max_retries - 1:
                    continue
                else:
                    raise Exception(f"Failed to analyze image {image_path.name} after {self.max_retries} attempts: {str(e)}")
        
        # Fallback description
        return self._generate_fallback_description(image_path, company_name, location, service_type)
    
    def _load_and_prepare_image(self, image_path):
        """Load and prepare image for analysis"""
        try:
            image = Image.open(image_path)
            
            # Convert to RGB if necessary
            if image.mode in ('RGBA', 'LA', 'P'):
                image = image.convert('RGB')
            
            # Resize if too large (OpenAI has size limits)
            max_size = 1024
            if max(image.size) > max_size:
                image.thumbnail((max_size, max_size), Image.Resampling.LANCZOS)
            
            return image
            
        except Exception as e:
            raise Exception(f"Failed to load image: {str(e)}")
    
    def _image_to_base64(self, image):
        """Convert PIL image to base64 string"""
        try:
            buffered = io.BytesIO()
            image.save(buffered, format="JPEG", quality=85, optimize=True)
            return base64.b64encode(buffered.getvalue()).decode()
        except Exception as e:
            raise Exception(f"Failed to convert image to base64: {str(e)}")
    
    def _call_openai_api(self, prompt, image_base64):
        """Call OpenAI API with proper error handling"""
        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {
                        "role": "user",
                        "content": [
                            {
                                "type": "text",
                                "text": prompt
                            },
                            {
                                "type": "image_url",
                                "image_url": {
                                    "url": f"data:image/jpeg;base64,{image_base64}"
                                }
                            }
                        ]
                    }
                ],
                max_tokens=300,
                temperature=0.7
            )
            return response
        except Exception as e:
            raise Exception(f"OpenAI API call failed: {str(e)}")
    
    def _create_enhanced_prompt(self, style, length_range, company_name="", location="", service_type=""):
        """Create an enhanced prompt focused on actual image content for SEO alt text"""
        min_words, max_words = length_range
        
        # Business context for integration
        business_context = ""
        if company_name or location or service_type:
            business_parts = []
            if location:
                business_parts.append(location)
            if company_name:
                business_parts.append(company_name)
            if service_type:
                business_parts.append(service_type)
            
            business_context = f"""
BUSINESS CONTEXT (CLEAN INTEGRATION):
- Business info available: {', '.join(business_parts)}
- IMPORTANT: Create a natural description of the image first
- Use PROFESSIONAL language - avoid DIY, home improvement, or amateur terms
- Focus on PROFESSIONAL CONTRACTING and EXPERT WORKMANSHIP
- Use terms like: professional, expert, skilled, commercial-grade, contractor-quality
- DO NOT repeat business info multiple times in the description
- DO NOT use keyword stuffing - keep it natural and flowing
- Focus on describing what's actually in the image with professional terminology
- Business info will be added separately - focus on image content only"""

        # Enhanced base prompt with focus on actual image content
        base_prompt = f"""Analyze this image carefully and create a {min_words}-{max_words} word description that is:
- ACCURATE: Describe exactly what is visible in the image with precise details
- SEO-FRIENDLY: Use relevant, specific keywords that people actually search for
- PROFESSIONAL: Use expert contractor terminology, avoid DIY or amateur language
- NATURAL: Create a coherent, flowing description that makes logical sense
- DESCRIPTIVE: Include specific colors, materials, objects, and professional context
- FOCUSED: Prioritize the main subject and key visual elements that matter for SEO
- SENSIBLE: Ensure keywords flow naturally and make sense together
- NO REPETITION: Avoid repeating the same words, phrases, or concepts multiple times
- CONCISE: Use each important keyword only once, make every word count

PRIMARY GOAL: Create a professional, accurate alt text that describes the image content clearly and uses relevant SEO keywords that flow naturally together without repetition."""

        # Style-specific prompts with focus on image content
        style_prompts = {
            "SEO Optimized": f"""{base_prompt}
{business_context}

STYLE: SEO Optimized Alt Text
- Focus on what users would search for when looking for this type of image
- Include descriptive keywords naturally
- Describe the main subject, colors, and context
- Use terms that match search intent
- Prioritize accuracy over marketing language

Quality and accuracy are more important than exact word count.""",
            
            "Local SEO Optimized": f"""{base_prompt}
{business_context}

STYLE: Local SEO Optimized Alt Text
- Focus on the actual image content first
- If business info is provided and relevant, integrate naturally
- Use location-specific terms only if they make sense with the image
- Describe what's in the image accurately
- Include business context only when it enhances the description

Quality and accuracy are more important than exact word count.""",
            
            "Detailed": f"""{base_prompt}
{business_context}

STYLE: Detailed Alt Text Analysis
- Describe all visible elements comprehensively
- Include composition, lighting, colors, textures, objects
- Mention notable features and background details
- Provide thorough visual analysis
- Cover both main subjects and supporting elements

Quality and completeness are more important than exact word count.""",
            
            "Concise": f"""{base_prompt}
{business_context}

STYLE: Concise Alt Text
- Focus only on the most important elements
- Describe the main subject clearly and directly
- Keep it brief but informative
- Avoid unnecessary details
- Be direct and to the point

Quality and clarity are more important than exact word count.""",
            
            "Creative": f"""{base_prompt}
{business_context}

STYLE: Creative Alt Text
- Use vivid, engaging language
- Capture the mood and atmosphere
- Highlight artistic and aesthetic elements
- Create memorable descriptions
- Focus on visual appeal and emotional impact

Quality and creativity are more important than exact word count."""
        }
        
        return style_prompts.get(style, style_prompts["SEO Optimized"])
    
    def _clean_description(self, description, length_range, company_name="", location="", service_type=""):
        """Clean and format the description with intelligent business integration"""
        min_words, max_words = length_range
        
        # Remove quotes and extra whitespace
        description = description.strip('"').strip("'").strip()
        
        # Remove common unwanted phrases
        unwanted_phrases = [
            "this image shows", "this image depicts", "this image features",
            "the image shows", "the image depicts", "the image features",
            "in this image", "this picture shows", "this photograph shows",
            "this is an image of", "this is a picture of", "this is a photo of"
        ]
        
        for phrase in unwanted_phrases:
            description = re.sub(rf'\b{re.escape(phrase)}\b', '', description, flags=re.IGNORECASE)
        
        # Intelligent business integration
        if company_name or location or service_type:
            description = self._integrate_business_info(description, company_name, location, service_type)
        
        # Remove generic city names if no specific location is provided
        if not location or not location.strip():
            city_names = [
                'los angeles', 'new york', 'chicago', 'houston', 'phoenix', 'philadelphia',
                'san antonio', 'san diego', 'dallas', 'san jose', 'austin', 'jacksonville',
                'fort worth', 'columbus', 'charlotte', 'san francisco', 'indianapolis',
                'seattle', 'denver', 'washington', 'boston', 'nashville', 'baltimore',
                'oklahoma city', 'louisville', 'portland', 'las vegas', 'milwaukee',
                'albuquerque', 'tucson', 'fresno', 'sacramento', 'mesa', 'kansas city',
                'atlanta', 'long beach', 'colorado springs', 'raleigh', 'miami',
                'virginia beach', 'omaha', 'oakland', 'minneapolis', 'tulsa', 'tampa',
                'arlington', 'wichita', 'bakersfield', 'new orleans', 'cleveland',
                'anaheim', 'honolulu', 'henderson', 'stockton', 'chula vista',
                'buffalo', 'madison', 'reno', 'toledo', 'st. paul', 'chandler',
                'laredo', 'norfolk', 'corpus christi', 'cincinnati', 'riverside',
                'santa ana', 'lexington', 'pittsburgh', 'anchorage', 'saint paul',
                'lincoln', 'greensboro', 'plano', 'rochester', 'glendale', 'akron',
                'birmingham', 'fayetteville', 'san bernardino', 'spokane', 'des moines',
                'modesto', 'tacoma', 'shreveport', 'fontana', 'oxnard', 'aurora',
                'moreno valley', 'yonkers', 'huntington beach', 'montgomery',
                'amarillo', 'little rock', 'mobile', 'augusta', 'lubbock',
                'california', 'texas', 'florida', 'new york', 'pennsylvania',
                'illinois', 'ohio', 'georgia', 'north carolina', 'michigan'
            ]
            
            for city in city_names:
                pattern = r'\b' + re.escape(city) + r'\b'
                description = re.sub(pattern, '', description, flags=re.IGNORECASE)
        
        # Clean up extra spaces and punctuation
        description = ' '.join(description.split())
        description = description.rstrip('.,!?;:')
        
        # Apply flexible length control
        words = description.split()
        word_count = len(words)
        
        # Allow slight flexibility for quality
        if word_count > max_words + 3:
            words = words[:max_words + 2]
        elif word_count < min_words - 2:
            # If too short, don't truncate further
            pass
        
        # Join back and final cleanup
        description = ' '.join(words)
        
        # Remove repetitive words and phrases
        description = self._remove_repetition(description)
        
        # Ensure description isn't empty
        if not description or len(description.strip()) < 3:
            description = "professional-image-description"
        
        return description
    
    def _remove_repetition(self, description):
        """Remove repetitive words and phrases from description"""
        if not description:
            return description
        
        words = description.split()
        
        # Remove consecutive duplicate words
        cleaned_words = []
        for i, word in enumerate(words):
            if i == 0 or word.lower() != words[i-1].lower():
                cleaned_words.append(word)
        
        # Remove words that appear too frequently (more than 2 times)
        word_count = {}
        for word in cleaned_words:
            word_lower = word.lower()
            if len(word_lower) > 3:  # Only check words longer than 3 characters
                word_count[word_lower] = word_count.get(word_lower, 0) + 1
        
        # Filter out words that appear more than twice
        final_words = []
        word_usage = {}
        for word in cleaned_words:
            word_lower = word.lower()
            if len(word_lower) <= 3:  # Keep short words (articles, prepositions)
                final_words.append(word)
            else:
                current_usage = word_usage.get(word_lower, 0)
                if current_usage < 2:  # Allow each word maximum 2 times
                    final_words.append(word)
                    word_usage[word_lower] = current_usage + 1
        
        return ' '.join(final_words)
    
    def _integrate_business_info(self, description, company_name="", location="", service_type=""):
        """Intelligently integrate business information into the description naturally"""
        if not description:
            return description
        
        # Determine if business info should be integrated
        business_parts = []
        if location and location.strip():
            business_parts.append(location.strip())
        if company_name and company_name.strip():
            business_parts.append(company_name.strip())
        if service_type and service_type.strip():
            # Extract only the specific service, not the full category chain
            service_parts = service_type.strip().split(' → ')
            if len(service_parts) > 1:
                # Take the last part (specific service)
                specific_service = service_parts[-1].strip()
            else:
                # If no chain, use as is
                specific_service = service_type.strip()
            business_parts.append(specific_service)
        
        if not business_parts:
            return description
        
        # NEW APPROACH: Put business info at the beginning, avoid repetition
        # Check if business info is already in the description to avoid duplication
        description_lower = description.lower()
        company_in_desc = company_name and company_name.lower() in description_lower
        location_in_desc = location and location.lower() in description_lower
        service_in_desc = service_type and any(word.lower() in description_lower for word in service_type.split())
        
        # If business info is already integrated by AI, don't add it again
        if company_in_desc and (location_in_desc or service_in_desc):
            return description
        
        # PUT BUSINESS INFO AT THE BEGINNING - No repetition, clean format
        if len(business_parts) >= 3:
            # Company, Location, Service - put at beginning
            business_prefix = f"{business_parts[1]}-{business_parts[0]}-{business_parts[2].lower().replace(' ', '-')}"
            return f"{business_prefix}-{description}"
        elif len(business_parts) >= 2:
            # Company and Location/Service - put at beginning
            business_prefix = f"{business_parts[1]}-{business_parts[0].lower().replace(' ', '-')}"
            return f"{business_prefix}-{description}"
        else:
            # Single business element - put at beginning
            business_element = business_parts[0].lower().replace(' ', '-')
            return f"{business_element}-{description}"
    
    def _generate_fallback_description(self, image_path, company_name="", location="", service_type=""):
        """Generate a fallback description when AI analysis fails"""
        try:
            # Try to get basic image info
            with Image.open(image_path) as img:
                width, height = img.size
                format_name = img.format or "image"
            
            # Create basic description with business context
            parts = []
            
            if location:
                parts.append(location)
            
            if company_name:
                parts.append(company_name)
            
            if service_type:
                parts.append(service_type)
            
            parts.append(f"{format_name.lower()}")
            
            if width > height:
                parts.append("landscape")
            elif height > width:
                parts.append("portrait")
            else:
                parts.append("square")
            
            parts.append("image")
            
            return "-".join(parts)
            
        except Exception:
            return "professional-image-description"
    
    def create_seo_filename(self, description, original_extension):
        """
        Create an SEO-friendly filename from the description
        
        Args:
            description (str): The generated description
            original_extension (str): Original file extension
            
        Returns:
            str: SEO-friendly filename
        """
        # Convert to lowercase
        filename = description.lower()
        
        # Replace spaces with hyphens
        filename = re.sub(r'\s+', '-', filename)
        
        # Remove special characters, keep only alphanumeric and hyphens
        filename = re.sub(r'[^a-z0-9\-]', '', filename)
        
        # Remove multiple consecutive hyphens
        filename = re.sub(r'-+', '-', filename)
        
        # Remove leading/trailing hyphens
        filename = filename.strip('-')
        
        # Ensure filename isn't empty
        if not filename:
            filename = "processed-image"
        
        # Limit filename length - but don't cut words in half
        max_filename_length = 200  # Increased from 100
        if len(filename) > max_filename_length:
            # Find the last complete word before the limit
            truncated = filename[:max_filename_length]
            last_hyphen = truncated.rfind('-')
            if last_hyphen > max_filename_length * 0.8:  # If we can find a good break point
                filename = truncated[:last_hyphen]
            else:
                filename = truncated.rstrip('-')
        
        # Add extension
        filename += original_extension.lower()
        
        return filename
    
    def process_and_optimize_image(self, image_path, output_folder, description, output_format="WebP Optimized", quality=85, crop_dimensions=None):
        """
        Process, optimize, and save an image with enhanced features
        
        Args:
            image_path (Path): Original image path
            output_folder (Path): Output directory
            description (str): AI-generated description
            output_format (str): Output format choice
            quality (int): Compression quality
            crop_dimensions (tuple): Target dimensions for smart cropping
            
        Returns:
            Path: Path to the processed image
        """
        try:
            # Load image
            image = Image.open(image_path)
            
            # Convert to RGB if necessary
            if image.mode in ('RGBA', 'LA', 'P'):
                image = image.convert('RGB')
            
            # Apply smart cropping if requested
            if crop_dimensions and crop_dimensions != "No Cropping":
                image = self._smart_crop_image(image, crop_dimensions)
            
            # Apply image enhancements
            image = self._enhance_image(image)
            
            # Determine output format and extension
            file_extension, save_format = self._get_output_format(output_format, image_path)
            
            # Create SEO-friendly filename
            seo_filename = self.create_seo_filename(description, file_extension)
            seo_filename = self.handle_duplicate_filename(output_folder, seo_filename)
            
            # Output path
            output_path = output_folder / seo_filename
            
            # Optimize and save image
            self._optimize_and_save_image(image, output_path, save_format, quality)
            
            return output_path
            
        except Exception as e:
            raise Exception(f"Failed to process image {image_path.name}: {str(e)}")
    
    def _enhance_image(self, image):
        """Apply subtle image enhancements for better quality"""
        try:
            # Enhance sharpness slightly
            enhancer = ImageEnhance.Sharpness(image)
            image = enhancer.enhance(1.1)
            
            # Enhance contrast slightly
            enhancer = ImageEnhance.Contrast(image)
            image = enhancer.enhance(1.05)
            
            return image
        except Exception:
            # Return original if enhancement fails
            return image
    
    def _get_output_format(self, output_format, image_path):
        """Determine output format and extension"""
        if output_format == "WebP Optimized":
            return ".webp", "WEBP"
        elif output_format == "JPG Optimized":
            return ".jpg", "JPEG"
        else:  # Keep Original
            file_extension = image_path.suffix.lower()
            if file_extension in ['.jpg', '.jpeg']:
                return ".jpg", "JPEG"
            elif file_extension == '.png':
                return ".png", "PNG"
            elif file_extension == '.webp':
                return ".webp", "WEBP"
            else:
                return ".jpg", "JPEG"
    
    def _smart_crop_image(self, image, target_dimensions):
        """
        Apply enhanced smart resize and crop with PIL-based intelligent cropping
        
        Args:
            image (PIL.Image): Input image
            target_dimensions (tuple): (width, height) target dimensions
            
        Returns:
            PIL.Image: Resized and cropped image
        """
        try:
            target_width, target_height = target_dimensions
            original_width, original_height = image.size
            
            # Calculate aspect ratios
            target_ratio = target_width / target_height
            original_ratio = original_width / original_height
            
            # If already correct ratio, just resize
            if abs(target_ratio - original_ratio) < 0.01:
                return image.resize((target_width, target_height), Image.Resampling.LANCZOS)
            
            # Enhanced Stage 1: Smart resize with better scaling
            if target_ratio > original_ratio:
                # Target is wider - resize based on height, then crop width
                scale_factor = target_height / original_height
                new_width = int(original_width * scale_factor)
                new_height = target_height
            else:
                # Target is taller - resize based on width, then crop height  
                scale_factor = target_width / original_width
                new_width = target_width
                new_height = int(original_height * scale_factor)
            
            # Resize the image with high quality
            resized_image = image.resize((new_width, new_height), Image.Resampling.LANCZOS)
            
            # Enhanced Stage 2: Intelligent cropping based on image content
            return self._intelligent_crop_image(resized_image, target_dimensions)
            
        except Exception as e:
            logger.warning(f"Smart crop error: {e}")
            return self._center_crop_image(image, target_dimensions)
    
    def _intelligent_crop_image(self, image, target_dimensions):
        """
        Intelligent cropping that tries to preserve important content
        
        Args:
            image (PIL.Image): Input image
            target_dimensions (tuple): (width, height) target dimensions
            
        Returns:
            PIL.Image: Intelligently cropped image
        """
        try:
            target_width, target_height = target_dimensions
            original_width, original_height = image.size
            
            # Calculate aspect ratios
            target_ratio = target_width / target_height
            original_ratio = original_width / original_height
            
            # Strategy 1: Rule of thirds crop (more visually appealing)
            if target_ratio > original_ratio:
                # Target is wider - fit to width, crop height
                crop_width = original_width
                crop_height = int(original_width / target_ratio)
                
                # Use rule of thirds for vertical positioning
                # Focus on the middle third of the image (more interesting than center)
                top = (original_height - crop_height) // 3
                left = 0
            else:
                # Target is taller - fit to height, crop width
                crop_height = original_height
                crop_width = int(original_height * target_ratio)
                
                # Use rule of thirds for horizontal positioning
                # Focus on the middle third of the image
                left = (original_width - crop_width) // 3
                top = 0
            
            right = left + crop_width
            bottom = top + crop_height
            
            # Strategy 2: Try to find the most interesting area based on brightness
            try:
                # Convert to grayscale for brightness analysis
                gray_image = image.convert('L')
                
                # Analyze brightness in different crop areas
                best_crop = self._find_best_crop_area(gray_image, target_dimensions)
                if best_crop:
                    left, top, right, bottom = best_crop
                    cropped_image = image.crop((left, top, right, bottom))
                else:
                    # Fallback to rule of thirds
                    cropped_image = image.crop((left, top, right, bottom))
            except:
                # Fallback to rule of thirds if brightness analysis fails
                cropped_image = image.crop((left, top, right, bottom))
            
            return cropped_image.resize((target_width, target_height), Image.Resampling.LANCZOS)
            
        except Exception as e:
            logger.warning(f"Intelligent crop error: {e}")
            return self._center_crop_image(image, target_dimensions)
    
    def _find_best_crop_area(self, gray_image, target_dimensions):
        """
        Find the best crop area based on brightness analysis
        
        Args:
            gray_image (PIL.Image): Grayscale image
            target_dimensions (tuple): Target dimensions
            
        Returns:
            tuple: (left, top, right, bottom) or None
        """
        try:
            target_width, target_height = target_dimensions
            original_width, original_height = gray_image.size
            
            # Calculate crop dimensions
            target_ratio = target_width / target_height
            original_ratio = original_width / original_height
            
            if target_ratio > original_ratio:
                crop_width = original_width
                crop_height = int(original_width / target_ratio)
            else:
                crop_height = original_height
                crop_width = int(original_height * target_ratio)
            
            # Test different crop positions
            best_score = -1
            best_crop = None
            
            # Test 3 different positions for better results
            positions = [0.25, 0.5, 0.75]  # 25%, 50%, 75% positions
            
            for pos in positions:
                if target_ratio > original_ratio:
                    # Vertical crop
                    top = int((original_height - crop_height) * pos)
                    left = 0
                else:
                    # Horizontal crop
                    left = int((original_width - crop_width) * pos)
                    top = 0
                
                right = left + crop_width
                bottom = top + crop_height
                
                # Calculate average brightness in this area
                crop_area = gray_image.crop((left, top, right, bottom))
                brightness = sum(crop_area.getextrema()) / 2  # Average of min/max
                
                # Prefer areas with good contrast (not too bright, not too dark)
                if 50 <= brightness <= 200:  # Good brightness range
                    score = brightness
                    if score > best_score:
                        best_score = score
                        best_crop = (left, top, right, bottom)
            
            return best_crop
            
        except Exception as e:
            logger.warning(f"Brightness analysis error: {e}")
            return None
    
    def _center_crop_image(self, image, target_dimensions):
        """
        Enhanced center crop method
        
        Args:
            image (PIL.Image): Input image
            target_dimensions (tuple): (width, height) target dimensions
            
        Returns:
            PIL.Image: Cropped image
        """
        target_width, target_height = target_dimensions
        original_width, original_height = image.size
        
        # Calculate aspect ratios
        target_ratio = target_width / target_height
        original_ratio = original_width / original_height
        
        if target_ratio > original_ratio:
            # Target is wider - fit to width
            crop_width = original_width
            crop_height = int(original_width / target_ratio)
            left = 0
            top = (original_height - crop_height) // 2
        else:
            # Target is taller - fit to height
            crop_height = original_height
            crop_width = int(original_height * target_ratio)
            left = (original_width - crop_width) // 2
            top = 0
        
        right = left + crop_width
        bottom = top + crop_height
        
        # Crop and resize
        cropped_image = image.crop((left, top, right, bottom))
        return cropped_image.resize((target_width, target_height), Image.Resampling.LANCZOS)
    
    def _optimize_and_save_image(self, image, output_path, save_format, quality):
        """
        Optimize and save image with enhanced compression settings
        
        Args:
            image (PIL.Image): Image to save
            output_path (Path): Output file path
            save_format (str): Image format (JPEG, WEBP, etc.)
            quality (int): Compression quality
        """
        try:
            if save_format == "WEBP":
                # WebP specific optimizations
                image.save(
                    output_path,
                    format="WEBP",
                    quality=quality,
                    method=6,  # Best compression method
                    optimize=True,
                    lossless=False
                )
            elif save_format == "JPEG":
                # JPEG specific optimizations
                image.save(
                    output_path,
                    format="JPEG",
                    quality=quality,
                    optimize=True,
                    progressive=True,
                    subsampling=0  # Best quality subsampling
                )
            elif save_format == "PNG":
                # PNG optimization
                image.save(
                    output_path,
                    format="PNG",
                    optimize=True,
                    compress_level=9  # Maximum compression
                )
            else:
                # Fallback
                image.save(output_path, format=save_format, optimize=True)
                
        except Exception as e:
            raise Exception(f"Failed to save image: {str(e)}")
    
    def handle_duplicate_filename(self, output_folder, filename):
        """
        Handle duplicate filenames by adding a number suffix
        
        Args:
            output_folder (Path): Output directory path
            filename (str): Proposed filename
            
        Returns:
            str: Unique filename
        """
        output_path = Path(output_folder)
        original_filename = filename
        name_part = Path(filename).stem
        extension = Path(filename).suffix
        
        counter = 1
        while (output_path / filename).exists():
            filename = f"{name_part}-{counter}{extension}"
            counter += 1
        
        return filename
    
    def validate_image(self, image_path):
        """
        Validate if the file is a supported image format
        
        Args:
            image_path (Path): Path to the image file
            
        Returns:
            bool: True if valid image, False otherwise
        """
        try:
            with Image.open(image_path) as img:
                img.verify()
            return True
        except Exception:
            return False
    
    def get_image_info(self, image_path):
        """
        Get detailed information about the image
        
        Args:
            image_path (Path): Path to the image file
            
        Returns:
            dict: Image information
        """
        try:
            with Image.open(image_path) as img:
                return {
                    'format': img.format,
                    'mode': img.mode,
                    'size': img.size,
                    'file_size': image_path.stat().st_size,
                    'aspect_ratio': round(img.size[0] / img.size[1], 2)
                }
        except Exception as e:
            return {'error': str(e)}
