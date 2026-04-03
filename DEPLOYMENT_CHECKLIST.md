# Deployment Checklist for Ad Optimization Platform

Use this checklist to ensure your project is ready for production deployment on Netlify (or alternative platforms).

## Pre-Deployment Verification

### Code Quality
- [ ] All Python files pass linting (check `flake8_output.txt`)
- [ ] No hardcoded passwords or API keys
- [ ] No debug code or print statements left in production code
- [ ] All imports are used (no unused imports)
- [ ] Code follows PEP 8 style guide

### Dependencies
- [ ] All required packages are in `requirements.txt`
- [ ] `requirements.txt` versions are pinned (e.g., `Flask==3.0.0`)
- [ ] No conflicting package versions
- [ ] Tested locally with fresh virtual environment:
  ```bash
  python -m venv test_venv
  source test_venv/bin/activate  # On Windows: test_venv\Scripts\activate
  pip install -r requirements.txt
  ```

### Configuration
- [ ] `config.py` updated with environment variable support
- [ ] `.env.example` created with all required variables
- [ ] `SECRET_KEY` environment variable configured (not hardcoded)
- [ ] Database configuration supports both SQLite (dev) and PostgreSQL (prod)
- [ ] Upload and report directories are configurable via environment variables

### Database
- [ ] Database migrations are handled automatically
- [ ] SQLAlchemy models are properly defined
- [ ] Database can be reset safely in production:
  ```bash
  with app.app_context():
      db.create_all()
  ```
- [ ] For cloud deployment: PostgreSQL connection string ready
- [ ] Database backup plan in place

### Authentication & Security
- [ ] Flask-Login is properly configured
- [ ] Password hashing implemented (password_hash, verify_password)
- [ ] Session management is secure
- [ ] CORS headers are configured if needed
- [ ] HTTPS enforced (Netlify provides this by default)
- [ ] Cookie security settings appropriate for production

### Static Files
- [ ] All CSS/JS files in `static/` folder
- [ ] Static files have unique names (cache busting if needed)
- [ ] Images and assets are optimized
- [ ] No large binary files in source code

### Templates
- [ ] All HTML templates render without errors
- [ ] Email templates have fallback text versions
- [ ] No hardcoded URLs, use `url_for()` function
- [ ] Templates use proper escaping to prevent XSS attacks

### Analytics & Features
- [ ] Machine learning models train correctly
- [ ] Feature engineering produces valid outputs
- [ ] EDA functions handle edge cases
- [ ] Prediction endpoints return proper JSON
- [ ] CSV file uploads validate file format and size

### Testing
- [ ] Manual testing of login flow
- [ ] Manual testing of data upload
- [ ] Manual testing of analytics/reports
- [ ] Manual testing of prediction features
- [ ] Test with sample data from `datasets/`

## Netlify-Specific Checklist

### Build Configuration
- [ ] `netlify.toml` present and configured
- [ ] Build command: `pip install -r requirements.txt && npm install`
- [ ] Functions directory: `netlify/functions`
- [ ] Publish directory: `static`
- [ ] `package.json` created
- [ ] `runtime.txt` specifies Python 3.11

### Serverless Function
- [ ] `netlify/functions/app.py` created and tested
- [ ] Function properly handles WSGI requests
- [ ] Error handling returns proper HTTP status codes
- [ ] Logs are properly formatted for debugging

### Environment Variables (in Netlify Dashboard)
- [ ] `FLASK_ENV=production`
- [ ] `FLASK_APP=app.py`
- [ ] `SECRET_KEY=<cryptographically-random-value>`
- [ ] `DATABASE_URL=postgresql://...` (if using cloud database)
- [ ] `ENVIRONMENT=production`
- [ ] `PYTHON_VERSION=3.11`

### .gitignore
- [ ] `.env` file excluded (should not be in git)
- [ ] Virtual environment excluded (`venv/`)
- [ ] `__pycache__/` and `.pyc` files excluded
- [ ] `instance/` and `database.db` excluded for local dev
- [ ] `.netlify/` folder excluded

### Repository
- [ ] Code committed and pushed to GitHub
- [ ] Latest changes are in the `main` branch
- [ ] No merge conflicts
- [ ] Meaningful commit messages

## Cloud Database Setup (Required for Netlify)

Choose one and complete:

### PostgreSQL on Railway
- [ ] Account created at https://railway.app
- [ ] PostgreSQL project created
- [ ] Database URL copied (format: `postgresql://...`)
- [ ] Host, port, username, password verified
- [ ] Database accessible from Netlify function

### PostgreSQL on Neon
- [ ] Account created at https://console.neon.tech
- [ ] Project created
- [ ] Connection string copied
- [ ] Added to Netlify environment variables

### MongoDB Atlas
- [ ] Account created at https://www.mongodb.com/cloud/atlas
- [ ] Cluster created
- [ ] Network access configured for Netlify IP (0.0.0.0/0)
- [ ] Connection string copied

## Deployment Steps

### Step 1: Prepare for Deployment
```bash
# Update requirements.txt
pip freeze > requirements.txt

# Add all files
git add .

# Commit with meaningful message
git commit -m "Prepare for Netlify deployment with cloud database"

# Push to GitHub
git push origin main
```

### Step 2: Create Netlify Site
- [ ] Account created at https://netlify.com
- [ ] GitHub repository connected
- [ ] Build settings configured (see netlify.toml)
- [ ] Environment variables set in Netlify dashboard
- [ ] Initial deployment triggered

### Step 3: Verify Deployment
- [ ] Check deployment status in Netlify dashboard
- [ ] No build errors in logs
- [ ] No function errors in logs
- [ ] Site loads without errors
- [ ] Can access login page
- [ ] Can view dashboard

## Post-Deployment Testing

### Basic Functionality
- [ ] Website loads at `https://your-site.netlify.app`
- [ ] Login page displays correctly
- [ ] Can create new account
- [ ] Can login with account
- [ ] Can upload CSV file
- [ ] Can view analytics dashboard
- [ ] Can run predictions

### Performance
- [ ] Pages load in < 3 seconds
- [ ] No console errors (check browser DevTools)
- [ ] Images load correctly
- [ ] Charts and graphs render properly
- [ ] Database queries are reasonably fast

### Data Integrity
- [ ] Uploaded data is stored correctly
- [ ] Analytics calculations are accurate
- [ ] Predictions are generated properly
- [ ] Reports can be downloaded
- [ ] User sessions persist across page refreshes

### Error Handling
- [ ] Invalid login shows error message
- [ ] File upload errors handled gracefully
- [ ] Missing data handled without crashing
- [ ] Large files rejected with proper message
- [ ] Network errors don't break the app

## Monitoring & Maintenance

### Setup Monitoring
- [ ] Enable Netlify Analytics (optional paid feature)
- [ ] Set up error notifications (Sentry recommended)
- [ ] Monitor function execution logs
- [ ] Monitor database size and performance

### Regular Maintenance
- [ ] Check for security updates monthly
- [ ] Review error logs weekly
- [ ] Monitor function execution times
- [ ] Backup database regularly
- [ ] Clean up old uploaded files

### Security Audit
- [ ] No sensitive data in logs
- [ ] No API keys exposed in error messages
- [ ] HTTPS enforced across all pages
- [ ] User passwords stored securely (hashed)
- [ ] CSRF tokens present in forms

## Rollback Plan

If deployment has critical issues:
- [ ] Previous working deployment identified
- [ ] Netlify rollback procedure documented
- [ ] Git rollback process tested
- [ ] Communication plan for users

## Troubleshooting Reference

Common issues and solutions documented in:
- `NETLIFY_DEPLOYMENT_GUIDE.md` - Detailed troubleshooting
- `ALTERNATIVE_DEPLOYMENT.md` - If Netlify doesn't work
- Function logs in Netlify dashboard
- Build logs in Netlify dashboard

## Sign-Off

- **Deployment Date**: _______________
- **Deployed By**: _______________
- **Environment**: Production
- **Status**: ☐ Ready ☐ In Progress ☐ Deployed ☐ Issues Found

## Notes

```
[Use this space to document any specific configuration or issues]




```

---

**Checklist Version**: 1.0  
**Last Updated**: April 2026  
**Next Review**: [Specify date]
