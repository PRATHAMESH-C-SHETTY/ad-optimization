# Quick Start: Deploy to Netlify in 10 Minutes

This is the fastest path to getting your Ad Optimization Platform live on Netlify.

## Prerequisites
- GitHub account (free)
- Netlify account (free)
- Railway account for PostgreSQL (free)

## Step 1: Set Up PostgreSQL Database (2 min)

1. Visit https://railway.app (created account if needed)
2. Click "Start a New Project" → Click "Provision PostgreSQL"
3. In Railway dashboard:
   - Click the PostgreSQL plugin
   - Go to "Connect" tab
   - Copy the "Postgres Connection URL"
   - Save it - you'll need this in Step 3

## Step 2: Push Code to GitHub (2 min)

```bash
cd "d:\internship projects\ad-optimization-main 1"

# Verify everything is ready
git status

# Add and commit everything
git add .
git commit -m "Ready for Netlify deployment"

# Push to GitHub
git push origin main
```

## Step 3: Deploy to Netlify (4 min)

1. Go to https://app.netlify.com
2. Click "Add new site" → "Import an existing project"
3. Select GitHub → Select your repository name
4. **Build settings:**
   - Build command: `pip install -r requirements.txt && npm install`
   - Publish directory: `static`
   - Functions directory: `netlify/functions`
5. Click "Advanced" → "New variable"
   - Add these variables:
   ```
   FLASK_ENV = production
   FLASK_APP = app.py
   DATABASE_URL = [paste from Railway Step 1]
   SECRET_KEY = [generate secure key - see below]
   ENVIRONMENT = production
   PYTHON_VERSION = 3.11
   ```

### Generate Secure Secret Key

Run in terminal:
```bash
python -c "import secrets; print(secrets.token_hex(32))"
```
Copy the output and use it for `SECRET_KEY` in Netlify.

6. Click "Deploy site"
7. **Wait 5-10 minutes** for first build (takes time for Python packages)

## Step 4: Verify It Works (1 min)

1. Once deployed, go to your Netlify dashboard
2. Your site URL will be shown (like `https://your-site-name.netlify.app`)
3. Click the link to visit your site
4. Try:
   - ✅ Login page loads
   - ✅ Sign up works
   - ✅ Upload a CSV file
   - ✅ View dashboard

## Troubleshooting

**Build failed?**
- Check build logs in Netlify dashboard
- Most common: Wrong DATABASE_URL format

**Site shows errors?**
- Check deployed logs in Netlify Functions
- Verify DATABASE_URL is set correctly
- Make sure SECRET_KEY is not empty

**Login not working?**
- Clear browser cookies
- Check if SECRET_KEY is set in Netlify
- Verify database connection in logs

## Your Site is Live! 🎉

Share your URL: `https://your-site-name.netlify.app`

## Next Steps

- **Custom Domain**: Netlify dashboard → Domain settings → Add custom domain
- **HTTPS**: Automatic! Netlify handles SSL
- **Monitoring**: Check Netlify Analytics dashboard
- **Updates**: Push to GitHub → Netlify auto-deploys

## Important Reminders

⚠️ **Never commit `.env` file** - Only use Netlify dashboard for secrets

✅ **Always use cloud database** - SQLite won't work on Netlify

📊 **Monitor your deployments** - Check Netlify dashboard regularly

---

## FAQ

**Q: How much does this cost?**  
A: Netlify (free), Railway PostgreSQL (free tier available)

**Q: Can I use a custom domain?**  
A: Yes, in Netlify dashboard add your domain

**Q: How do I update my site?**  
A: Push to main branch on GitHub → Netlify auto-deploys

**Q: Where are my files stored?**  
A: Database in Railway, Code in GitHub, Static files in Netlify

**Q: How long does first deployment take?**  
A: First build: 5-10 minutes. Updates: 1-2 minutes

---

**All set! Your platform is now live on Netlify! 🚀**

For detailed setup, see [NETLIFY_DEPLOYMENT_GUIDE.md](NETLIFY_DEPLOYMENT_GUIDE.md)  
For alternatives, see [ALTERNATIVE_DEPLOYMENT.md](ALTERNATIVE_DEPLOYMENT.md)
