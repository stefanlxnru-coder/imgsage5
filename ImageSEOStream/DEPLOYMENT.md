# 🚀 Deployment Guide

This guide covers deploying ImgSage to various cloud platforms.

## 📋 Prerequisites

Before deploying, ensure you have:

1. **OpenAI API Key**: Get one from [OpenAI Platform](https://platform.openai.com/api-keys)
2. **GitHub Account**: For repository hosting
3. **Cloud Platform Account**: Render, Heroku, or similar

## 🌐 Render Deployment (Recommended)

Render is the recommended platform for deploying ImgSage due to its simplicity and free tier.

### Step 1: Prepare Your Repository

1. **Fork or clone** this repository to your GitHub account
2. **Ensure** all files are in the `ImageSEOStream` directory
3. **Verify** the following files exist:
   - `app.py`
   - `requirements.txt`
   - `render.yaml`
   - `Dockerfile`

### Step 2: Create Render Account

1. Go to [render.com](https://render.com)
2. Sign up with your GitHub account
3. Verify your email address

### Step 3: Deploy the Application

1. **Create New Web Service**
   - Click "New +" → "Web Service"
   - Connect your GitHub repository
   - Select the repository containing ImgSage

2. **Configure the Service**
   - **Name**: `imagesage` (or your preferred name)
   - **Environment**: `Python 3`
   - **Region**: Choose closest to your users
   - **Branch**: `main` (or your default branch)
   - **Root Directory**: `ImageSEOStream`
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `streamlit run app.py --server.port=$PORT --server.address=0.0.0.0`

3. **Add Environment Variables**
   - Click "Environment" tab
   - Add the following variable:
     - **Key**: `OPENAI_API_KEY`
     - **Value**: Your OpenAI API key
     - **Sync**: Leave unchecked

4. **Deploy**
   - Click "Create Web Service"
   - Wait for the build to complete (5-10 minutes)
   - Your app will be available at the provided URL

### Step 4: Verify Deployment

1. **Check the logs** for any errors
2. **Test the application** by uploading an image
3. **Verify** API key functionality

## 🐳 Docker Deployment

### Local Docker

```bash
# Build the image
docker build -t imagesage .

# Run the container
docker run -p 8501:8501 -e OPENAI_API_KEY="your-api-key" imagesage
```

### Docker Compose

Create a `docker-compose.yml` file:

```yaml
version: '3.8'
services:
  imagesage:
    build: .
    ports:
      - "8501:8501"
    environment:
      - OPENAI_API_KEY=${OPENAI_API_KEY}
    volumes:
      - ./temp_input:/app/temp_input
      - ./processed_images:/app/processed_images
```

Run with:
```bash
docker-compose up --build
```

## ☁️ Heroku Deployment

### Step 1: Install Heroku CLI

```bash
# macOS
brew install heroku/brew/heroku

# Windows
# Download from https://devcenter.heroku.com/articles/heroku-cli
```

### Step 2: Login and Create App

```bash
# Login to Heroku
heroku login

# Create new app
heroku create your-app-name

# Set environment variables
heroku config:set OPENAI_API_KEY="your-api-key-here"
```

### Step 3: Deploy

```bash
# Add Heroku remote
heroku git:remote -a your-app-name

# Deploy
git push heroku main
```

## 🔧 Environment Variables

### Required Variables

| Variable | Description | Example |
|----------|-------------|---------|
| `OPENAI_API_KEY` | Your OpenAI API key | `sk-...` |

### Optional Variables

| Variable | Description | Default |
|----------|-------------|---------|
| `PORT` | Server port | `8501` |
| `STREAMLIT_SERVER_ADDRESS` | Server address | `0.0.0.0` |
| `PYTHON_VERSION` | Python version | `3.11.18` |

## 🛠️ Troubleshooting

### Common Issues

1. **Build Fails**
   - Check `requirements.txt` for correct dependencies
   - Verify Python version compatibility
   - Check build logs for specific errors

2. **App Won't Start**
   - Verify `OPENAI_API_KEY` is set correctly
   - Check start command in platform settings
   - Review application logs

3. **API Errors**
   - Ensure OpenAI API key is valid
   - Check API key has sufficient credits
   - Verify GPT-4o access

4. **File Upload Issues**
   - Check file size limits (20MB max)
   - Verify supported formats (JPG, PNG, WebP)
   - Ensure proper file permissions

### Debug Commands

```bash
# Check application status
curl http://localhost:8501/_stcore/health

# View logs
heroku logs --tail  # Heroku
# Check platform-specific log viewer for other platforms

# Test API key
python -c "import openai; openai.api_key='your-key'; print('Valid')"
```

## 📊 Performance Optimization

### For Production

1. **Enable Caching**
   - Set up Redis or similar cache
   - Configure Streamlit caching

2. **Load Balancing**
   - Use multiple instances
   - Configure auto-scaling

3. **Monitoring**
   - Set up health checks
   - Monitor API usage
   - Track error rates

### Resource Requirements

| Component | Minimum | Recommended |
|-----------|---------|-------------|
| RAM | 512MB | 1GB |
| CPU | 0.5 cores | 1 core |
| Storage | 1GB | 2GB |

## 🔒 Security Considerations

1. **API Key Security**
   - Never commit API keys to version control
   - Use environment variables
   - Rotate keys regularly

2. **File Upload Security**
   - Validate file types
   - Limit file sizes
   - Scan for malware

3. **Network Security**
   - Use HTTPS in production
   - Configure CORS properly
   - Set up rate limiting

## 📈 Scaling

### Horizontal Scaling

1. **Multiple Instances**
   - Deploy multiple app instances
   - Use load balancer
   - Configure session management

2. **Database Integration**
   - Add database for user data
   - Store processing history
   - Enable user accounts

### Vertical Scaling

1. **Resource Upgrades**
   - Increase RAM allocation
   - Add more CPU cores
   - Upgrade storage

## 🆘 Support

If you encounter issues:

1. **Check the logs** for error messages
2. **Review this guide** for common solutions
3. **Open an issue** on GitHub
4. **Contact support** for platform-specific issues

---

**Happy Deploying! 🚀**
