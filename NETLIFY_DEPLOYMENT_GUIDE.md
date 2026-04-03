# Netlify Deployment Guide - Ad Optimization Platform

## Overview
This project has been configured for deployment on Netlify. This guide provides step-by-step instructions to deploy your Flask application successfully.

## Important Notes

⚠️ **Database Considerations:**
- The default SQLite database cannot be persisted on Netlify (ephemeral filesystem)
- For production, use a cloud database service:
  - **PostgreSQL** (recommended): Heroku Postgres, Railway, Neon
  - **MongoDB**: Atlas (free tier available)
  - **MySQL**: PlanetScale, Railway

## Pre-Deployment Checklist

- [ ] Fork/Clone the repository to GitHub
- [ ] Create a Netlify account at https://netlify.com
- [ ] Set up a cloud database (PostgreSQL recommended)
- [ ] Update environment variables in Netlify console
- [ ] Install dependencies locally and test

## Step 1: Prepare Your GitHub Repository

```bash
# Navigate to your project
cd ad-optimization-main

# Ensure all files are committed
git add .
git commit -m "Prepare for Netlify deployment"
git push origin main
```

## Step 2: Set Up a Cloud Database

### Option A: PostgreSQL on Railway (Recommended)

1. Visit https://railway.app
2. Create new Project → Provision PostgreSQL
3. Copy the database URL from Railway dashboard
4. Database URL format: `postgresql://user:password@host:port/dbname`

### Option B: PostgreSQL on Neon

1. Visit https://console.neon.tech
2. Create a new project
3. Copy the full connection string

### Option C: MongoDB Atlas

1. Visit https://www.mongodb.com/cloud/atlas
2. Create a free cluster
3. Get your MongoDB connection string
4. Install PyMongo: `pip install pymongo`

## Step 3: Configure Netlify

### 3.1 Connect Your Repository

1. Log in to Netlify
2. Click "New site from Git"
3. Select your GitHub repository
4. Build settings:
   - **Build command**: `pip install -r requirements.txt && npm install`
   - **Publish directory**: `static`
   - **Functions directory**: `netlify/functions`

### 3.2 Set Environment Variables

In Netlify Dashboard → Site Settings → Build & Deploy → Environment:

```env
FLASK_ENV=production
FLASK_APP=app.py
SECRET_KEY=your-very-secure-random-key-change-this
DATABASE_URL=postgresql://user:password@host:port/dbname
ENVIRONMENT=production
PYTHON_VERSION=3.11
```

### 3.3 Generate a Secure Secret Key

```python
import secrets
print(secrets.token_hex(32))
```

Use this output for the `SECRET_KEY` in Netlify environment variables.

## Step 4: Deploy

### Automatic Deployment
1. Push code to GitHub → Netlify automatically deploys
2. Monitor deployment in Netlify Dashboard

### Manual Deployment
```bash
# Install Netlify CLI
npm install -g netlify-cli

# Authenticate
netlify login

# Deploy
netlify deploy --prod
```

## Step 5: Verify Deployment

1. Check Netlify Dashboard for deployment status
2. Visit your site URL
3. Test login and basic functionality
4. Check Functions logs in Netlify Dashboard

## Troubleshooting

### Issue: "Module not found" errors
**Solution**: Ensure all Python packages are in `requirements.txt`
```bash
pip freeze > requirements.txt
```

### Issue: Database not persisting
**Solution**: Verify you're using a cloud database (not SQLite):
```python
# Check in config.py
DATABASE_URL=postgresql://...  # Must be set in Netlify
```

### Issue: Large static files not loading
**Solution**: Check file size limits
- Max file size upload: 16MB (configured in app)
- Netlify free plan: ~100MB total

### Issue: Authentication not working
**Solution**: 
1. Verify SECRET_KEY is set in Netlify environment
2. Check cookie settings for HTTPS (production)
3. Test in deployment preview first

### Issue: Long deployment times
**Solution**:
- scikit-learn and pandas can take time to build
- Netlify builds are optimized; allow 5-10 minutes first time

## Build Output Location

Your site will be built as:
```
https://your-site-name.netlify.app
```

Update any hardcoded URLs in your application to use this domain.

## Security Best Practices

1. **Never commit `.env` file** - use Netlify environment variables only
2. **Change `SECRET_KEY`** - use a cryptographically random string
3. **Use HTTPS** - Netlify provides SSL by default
4. **Protect database credentials** - never push to GitHub
5. **Enable two-factor authentication** on GitHub and Netlify

## Production Optimization Tips

1. **Reduce file sizes** - Compress dataset CSV files
2. **Cache static assets** - Configure cache headers
3. **Monitor performance** - Use Netlify Analytics
4. **Set up error monitoring** - Consider Sentry integration
5. **Database optimization** - Add indexes to frequently queried columns

## Monitor and Logs

Access deployment logs in Netlify Dashboard:
- **Deploy logs** - Build output and errors
- **Function logs** - Runtime errors and debugging
- **Netlify Analytics** - Page views and performance

## Rollback Deployment

To rollback to a previous version:
1. Netlify Dashboard → Deploys
2. Find desired previous deployment
3. Click the three dots → "Publish deploy"

## Additional Resources

- [Netlify Documentation](https://docs.netlify.com)
- [Python on Netlify Functions](https://docs.netlify.com/functions/overview/)
- [Environment Variables Guide](https://docs.netlify.com/configure-builds/environment-variables/)
- [Flask Documentation](https://flask.palletsprojects.com/)

## Support and Issues

If deployment fails:
1. Check Netlify build logs for specific errors
2. Verify all environment variables are set
3. Test locally: `flask run`
4. Ensure database connection string is correct
5. Check that all Python packages are in `requirements.txt`

## Alternative Deployment Platforms

If Netlify doesn't meet your needs:

- **Render.com** - Native Flask support, free tier available
- **Railway.app** - Container-based, supports databases
- **Heroku** (paid) - Good for Python apps
- **AWS Elastic Beanstalk** - Scalable, complex setup
- **Google Cloud Run** - Serverless, pay-per-use

---

**Good luck with your deployment! 🚀**
