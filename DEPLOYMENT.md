# 🚀 Deployment Guide

This guide covers deploying ImgSage to various platforms.

## 📋 Prerequisites

- Python 3.11 or higher
- OpenAI API key with GPT-4o access
- Git repository access

## 🌐 Render Deployment (Recommended)

### Step 1: Prepare Your Repository

1. **Fork or clone the repository**
   ```bash
   git clone https://github.com/yourusername/imagesage.git
   cd imagesage
   ```

2. **Verify the deployment files exist:**
   - `requirements.txt` - Python dependencies
   - `Procfile` - Render service configuration
   - `runtime.txt` - Python version specification
   - `render.yaml` - Render service definition

### Step 2: Deploy to Render

1. **Sign up for Render** at [render.com](https://render.com)

2. **Create a new Web Service**
   - Click "New +" → "Web Service"
   - Connect your GitHub repository
   - Select the repository you want to deploy

3. **Configure the service:**
   - **Name**: `imagesage` (or your preferred name)
   - **Environment**: `Python`
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `streamlit run ImageSEOStream/app.py --server.port=$PORT --server.address=0.0.0.0`

4. **Set Environment Variables:**
   - Click "Environment" tab
   - Add `OPENAI_API_KEY` with your OpenAI API key
   - Add `PYTHON_VERSION` = `3.11.18`

5. **Deploy:**
   - Click "Create Web Service"
   - Render will automatically build and deploy your app

### Step 3: Access Your App

- Your app will be available at: `https://your-app-name.onrender.com`
- The first deployment may take 5-10 minutes

## 🐳 Docker Deployment

### Local Docker

1. **Build the image:**
   ```bash
   docker build -t imagesage .
   ```

2. **Run the container:**
   ```bash
   docker run -p 8501:8501 -e OPENAI_API_KEY="your-api-key" imagesage
   ```

3. **Access the app:**
   - Open `http://localhost:8501` in your browser

### Docker Compose

1. **Create `docker-compose.yml`:**
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
         - ./data:/app/data
   ```

2. **Run with Docker Compose:**
   ```bash
   docker-compose up -d
   ```

## ☁️ Other Cloud Platforms

### Heroku

1. **Install Heroku CLI**
2. **Create `Procfile` for Heroku:**
   ```
   web: streamlit run ImageSEOStream/app.py --server.port=$PORT --server.address=0.0.0.0
   ```

3. **Deploy:**
   ```bash
   heroku create your-app-name
   heroku config:set OPENAI_API_KEY="your-api-key"
   git push heroku main
   ```

### Google Cloud Run

1. **Build and push to Google Container Registry:**
   ```bash
   gcloud builds submit --tag gcr.io/PROJECT-ID/imagesage
   ```

2. **Deploy to Cloud Run:**
   ```bash
   gcloud run deploy imagesage \
     --image gcr.io/PROJECT-ID/imagesage \
     --platform managed \
     --allow-unauthenticated \
     --set-env-vars OPENAI_API_KEY="your-api-key"
   ```

### AWS Elastic Beanstalk

1. **Create `Procfile` for AWS:**
   ```
   web: streamlit run ImageSEOStream/app.py --server.port=$PORT --server.address=0.0.0.0
   ```

2. **Deploy using AWS CLI or console**

## 🔧 Environment Variables

| Variable | Description | Required | Default |
|----------|-------------|----------|---------|
| `OPENAI_API_KEY` | Your OpenAI API key | Yes | None |
| `PYTHON_VERSION` | Python version | No | 3.11.18 |
| `STREAMLIT_SERVER_PORT` | Port for Streamlit | No | 8501 |
| `STREAMLIT_SERVER_ADDRESS` | Server address | No | 0.0.0.0 |

## 🛠️ Troubleshooting

### Common Issues

1. **Build fails with OpenCV error:**
   - Ensure you're using Python 3.11+
   - Check that all dependencies are in `requirements.txt`

2. **App doesn't start:**
   - Verify the `Procfile` is correct
   - Check environment variables are set
   - Review build logs for errors

3. **API key not working:**
   - Ensure `OPENAI_API_KEY` is set correctly
   - Verify the API key has GPT-4o access
   - Check API key format (should start with `sk-`)

4. **Memory issues:**
   - Reduce batch size in settings
   - Optimize image sizes before upload
   - Consider upgrading to a larger instance

### Performance Optimization

1. **For Render Free Tier:**
   - Limit batch processing to 5 images
   - Use lower quality settings
   - Enable auto-cleanup

2. **For Production:**
   - Use paid tiers for better performance
   - Enable caching where possible
   - Monitor resource usage

## 📊 Monitoring

### Health Checks

The app includes health check endpoints:
- `/_stcore/health` - Streamlit health check
- `/` - Main application

### Logs

- **Render**: View logs in the Render dashboard
- **Docker**: `docker logs <container-id>`
- **Local**: Check console output

## 🔒 Security Considerations

1. **API Key Security:**
   - Never commit API keys to version control
   - Use environment variables
   - Rotate keys regularly

2. **File Upload Security:**
   - Validate file types and sizes
   - Clean up temporary files
   - Limit upload sizes

3. **Network Security:**
   - Use HTTPS in production
   - Configure CORS if needed
   - Monitor for abuse

## 📈 Scaling

### Horizontal Scaling

- Use load balancers for multiple instances
- Implement session management
- Consider database for persistent storage

### Vertical Scaling

- Upgrade instance sizes
- Optimize code performance
- Use CDN for static assets

## 🆘 Support

If you encounter issues:

1. Check the [GitHub Issues](https://github.com/yourusername/imagesage/issues)
2. Review the [README.md](README.md) for setup instructions
3. Check platform-specific documentation
4. Create a new issue with detailed error information

---

**Happy Deploying! 🚀**
