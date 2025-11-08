# Render.com Setup Guide

Complete step-by-step guide to deploy this project on Render.com.

## Prerequisites

1. **Render.com Account**
   - Sign up at [https://render.com](https://render.com)
   - Free tier is sufficient for this project

2. **Git Repository**
   - Your code should be in a Git repository (GitHub, GitLab, or Bitbucket)
   - Repository should be accessible to Render.com

## Method 1: Using render.yaml (Recommended - Automated)

This is the easiest method as Render.com will automatically detect and configure services.

### Step 1: Push Code to Git Repository

If your code is already in a Git repository, ensure it's pushed:

```bash
cd /home/sylaw/jenkins_fullstack
git add .
git commit -m "Ready for Render.com deployment"
git push origin main
```

**Note**: If using the local Git repository, you'll need to push to a remote repository (GitHub, GitLab, or Bitbucket) that Render.com can access.

### Step 2: Connect Repository to Render.com

1. **Login to Render.com**
   - Go to [https://dashboard.render.com](https://dashboard.render.com)
   - Sign in or create an account

2. **Create New Blueprint**
   - Click the **"New +"** button in the top right
   - Select **"Blueprint"** from the dropdown

3. **Connect Repository**
   - Click **"Connect account"** if not already connected
   - Authorize Render.com to access your Git provider (GitHub/GitLab/Bitbucket)
   - Select your repository: `jenkins_fullstack` (or your repo name)
   - Click **"Connect"**

4. **Configure Blueprint**
   - Render will automatically detect `render.yaml` in your repository
   - Review the services that will be created:
     - `jenkins-fullstack-backend` (Web Service)
     - `jenkins-fullstack-frontend` (Static Site)
   - Click **"Apply"** or **"Create Blueprint"**

### Step 3: Review and Deploy

1. **Review Services**
   - Render will show you both services that will be created
   - Verify the configuration matches `render.yaml`

2. **Deploy Services**
   - Click **"Apply"** to create both services
   - Render will start building and deploying

3. **Monitor Deployment**
   - Watch the build logs in real-time
   - Backend will build first, then frontend
   - Both services will be deployed automatically

### Step 4: Get Your URLs

After deployment completes, you'll get:

- **Backend URL**: `https://jenkins-fullstack-backend.onrender.com`
- **Frontend URL**: `https://jenkins-fullstack-frontend.onrender.com`

### Step 5: Verify Deployment

1. **Test Backend**
   ```bash
   curl https://jenkins-fullstack-backend.onrender.com/api/health
   ```
   Should return: `{"status":"ok","message":"Backend API is running",...}`

2. **Test Frontend**
   - Open `https://jenkins-fullstack-frontend.onrender.com` in browser
   - Should see the React app
   - API health status should show "ok"

## Method 2: Manual Setup (Alternative)

If you prefer to set up services manually or need more control:

### Backend Service Setup

1. **Create Web Service**
   - In Render dashboard, click **"New +"** → **"Web Service"**
   - Connect your repository

2. **Configure Service**
   - **Name**: `jenkins-fullstack-backend`
   - **Environment**: `Node`
   - **Build Command**: `cd backend && npm install`
   - **Start Command**: `cd backend && npm start`
   - **Plan**: `Free` (or choose paid for always-on)

3. **Environment Variables**
   - Click **"Environment"** tab
   - Add variables:
     - `NODE_ENV` = `production`
     - `PORT` = `5000`

4. **Health Check**
   - **Health Check Path**: `/api/health`

5. **Deploy**
   - Click **"Create Web Service"**
   - Wait for deployment to complete
   - Note the URL: `https://jenkins-fullstack-backend.onrender.com`

### Frontend Service Setup

1. **Create Static Site**
   - In Render dashboard, click **"New +"** → **"Static Site"**
   - Connect your repository

2. **Configure Service**
   - **Name**: `jenkins-fullstack-frontend`
   - **Build Command**: `cd frontend && npm install && npm run build`
   - **Publish Directory**: `frontend/build`
   - **Plan**: `Free`

3. **Environment Variables**
   - Click **"Environment"** tab
   - Add variable:
     - `REACT_APP_API_URL` = `https://jenkins-fullstack-backend.onrender.com`
     - **Important**: Use the actual backend URL from step above

4. **Routes (Optional)**
   - For React Router support, add rewrite rule:
     - **Source**: `/*`
     - **Destination**: `/index.html`

5. **Deploy**
   - Click **"Create Static Site"**
   - Wait for deployment to complete
   - Note the URL: `https://jenkins-fullstack-frontend.onrender.com`

## Post-Deployment Configuration

### Update Frontend API URL

If you used manual setup, ensure the frontend environment variable is set:

1. Go to Frontend service in Render dashboard
2. Click **"Environment"** tab
3. Verify `REACT_APP_API_URL` is set to your backend URL
4. If changed, click **"Save Changes"** and redeploy

### Update Postman Production Environment

Update the production environment file:

```json
{
  "key": "base_url",
  "value": "https://jenkins-fullstack-backend.onrender.com"
}
```

Or update it in Postman directly.

## Troubleshooting

### Backend Issues

**Problem**: Backend service won't start
- **Solution**: Check build logs for errors
- Verify `PORT` environment variable is set
- Ensure `npm start` command works locally

**Problem**: Backend spins down (free tier)
- **Solution**: This is normal for free tier after 15 min inactivity
- First request after spin-down will be slow (cold start)
- Consider upgrading to paid plan for always-on

**Problem**: Health check failing
- **Solution**: Verify `/api/health` endpoint exists and returns 200
- Check service logs for errors

### Frontend Issues

**Problem**: Frontend shows API errors
- **Solution**: Verify `REACT_APP_API_URL` environment variable is set correctly
- Check that backend URL is accessible
- Ensure CORS is enabled in backend (already configured)

**Problem**: React Router routes not working
- **Solution**: Ensure rewrite rule is configured:
  - Source: `/*`
  - Destination: `/index.html`

**Problem**: Build fails
- **Solution**: Check build logs
- Verify all dependencies are in `package.json`
- Ensure Node.js version is compatible

### Common Issues

**Problem**: Services can't find each other
- **Solution**: Use full URLs in environment variables
- Backend URL should be: `https://jenkins-fullstack-backend.onrender.com`
- Frontend URL should be: `https://jenkins-fullstack-frontend.onrender.com`

**Problem**: Environment variables not updating
- **Solution**: After changing environment variables, redeploy the service
- Changes take effect on next deployment

## Testing Deployment

### 1. Test Backend API

```bash
# Health check
curl https://jenkins-fullstack-backend.onrender.com/api/health

# Get message
curl https://jenkins-fullstack-backend.onrender.com/api/message

# Submit data
curl -X POST https://jenkins-fullstack-backend.onrender.com/api/data \
  -H "Content-Type: application/json" \
  -d '{"name":"Test","message":"Hello from Render"}'
```

### 2. Test Frontend

1. Open `https://jenkins-fullstack-frontend.onrender.com` in browser
2. Verify:
   - Page loads correctly
   - API Health Status shows "ok"
   - Backend Message displays
   - Form submission works

### 3. Test with Postman

1. Import `postman/Production.postman_environment.json`
2. Select "Production" environment
3. Run all API tests
4. All tests should pass

## Continuous Deployment

Render.com automatically deploys when you push to your repository:

1. **Push to Git**
   ```bash
   git push origin main
   ```

2. **Render Detects Changes**
   - Render monitors your repository
   - Detects new commits

3. **Automatic Deployment**
   - Builds and deploys both services
   - Updates production URLs

4. **Monitor Deployments**
   - Check Render dashboard for deployment status
   - View build logs for any issues

## Free Tier Limitations

- **Backend**: Spins down after 15 minutes of inactivity
- **Cold Start**: First request after spin-down takes ~30 seconds
- **Build Time**: Limited build minutes per month
- **Bandwidth**: Limited bandwidth per month

## Upgrading to Paid Plans

For production use, consider upgrading:

1. **Backend Service**
   - Upgrade to "Starter" plan ($7/month)
   - Keeps service always-on
   - Faster response times

2. **Frontend Service**
   - Static sites are free and always available
   - No upgrade needed

## Security Considerations

1. **Environment Variables**
   - Never commit sensitive data
   - Use Render's environment variable management
   - Keep secrets secure

2. **CORS Configuration**
   - Backend already configured for CORS
   - Allows frontend to make API calls

3. **HTTPS**
   - Render provides free SSL certificates
   - All traffic is encrypted

## Next Steps

After successful deployment:

1. ✅ Test all endpoints
2. ✅ Verify frontend-backend communication
3. ✅ Update documentation with production URLs
4. ✅ Set up monitoring (optional)
5. ✅ Configure custom domain (optional)

## Support

- **Render.com Docs**: [https://render.com/docs](https://render.com/docs)
- **Render.com Support**: [https://render.com/support](https://render.com/support)
- **Project Issues**: Check project README.md

---

**Your project is now live on Render.com! 🚀**

