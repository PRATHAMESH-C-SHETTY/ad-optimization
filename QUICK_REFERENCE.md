# ⚡ QUICK REFERENCE CARD - Netlify Deployment

## 🎯 START HERE
Read: `QUICK_DEPLOY.md` or `START_HERE.txt`

## 🚀 Deploy in 4 Steps

### Step 1: Database (2 min)
```
1. Go to https://railway.app
2. Create PostgreSQL database
3. Copy connection URL
```

### Step 2: Push Code (1 min)
```bash
git add .
git commit -m "Deploy to Netlify"
git push origin main
```

### Step 3: Netlify Setup (4 min)
```
1. https://netlify.com → Add new site
2. Connect GitHub repository
3. Environment variables:
   FLASK_ENV=production
   FLASK_APP=app.py
   DATABASE_URL=[from Railway]
   SECRET_KEY=[generate below]
   ENVIRONMENT=production
4. Deploy!
```

### Step 4: Generate Secret Key
```bash
python -c "import secrets; print(secrets.token_hex(32))"
```

## 📋 Files You Need

### Must Read
- `QUICK_DEPLOY.md` - Quick setup guide (⭐ START HERE)
- `START_HERE.txt` - This checklist
- `DEPLOYMENT_README.md` - Complete overview

### Reference
- `NETLIFY_DEPLOYMENT_GUIDE.md` - Detailed guide with troubleshooting
- `DEPLOYMENT_CHECKLIST.md` - Verification checklist
- `ALTERNATIVE_DEPLOYMENT.md` - Other platforms
- `FILES_INDEX.md` - Complete file reference

## 🔧 Verification
```bash
# Check if everything is ready
python verify_deployment.py

# Test locally
flask run --port=5001

# Test with Docker
docker-compose up
```

## 🔑 Environment Variables List

| Variable | Value | Required |
|----------|-------|----------|
| FLASK_ENV | production | ✅ Yes |
| FLASK_APP | app.py | ✅ Yes |
| SECRET_KEY | [random key] | ✅ Yes |
| DATABASE_URL | postgresql://... | ✅ Yes |
| ENVIRONMENT | production | Yes |
| PYTHON_VERSION | 3.11 | Yes |

## 📊 Key Files Created

```
Configuration:
  ✅ netlify.toml
  ✅ package.json
  ✅ runtime.txt
  ✅ .env.example

Application:
  ✅ netlify/functions/app.py
  ✅ config.py (updated)
  ✅ app.py (updated)
  ✅ requirements.txt (updated)

Docker:
  ✅ Dockerfile
  ✅ docker-compose.yml
  ✅ Procfile

CI/CD:
  ✅ .github/workflows/test-deploy.yml

Utilities:
  ✅ verify_deployment.py

Documentation:
  ✅ QUICK_DEPLOY.md
  ✅ NETLIFY_DEPLOYMENT_GUIDE.md
  ✅ DEPLOYMENT_CHECKLIST.md
  ✅ DEPLOYMENT_SUMMARY.md
  ✅ ALTERNATIVE_DEPLOYMENT.md
  ✅ DEPLOYMENT_README.md
  ✅ FILES_INDEX.md
  ✅ START_HERE.txt
```

## ✅ Pre-Deploy Checklist

- [ ] Code committed and pushed to GitHub
- [ ] PostgreSQL database created (Railway)
- [ ] Secret key generated
- [ ] DATABASE_URL copied
- [ ] Environment variables listed
- [ ] `verify_deployment.py` shows PASS
- [ ] Netlify account created

## 🚨 Common Issues

| Issue | Solution |
|-------|----------|
| Build fails | Check Netlify logs, verify DATABASE_URL |
| App won't start | Verify SECRET_KEY is set |
| Login doesn't work | Check DATABASE_URL, clear cookies |
| Data not saving | Verify PostgreSQL connection string |
| Pages load slowly | First deployment is slower, normal |

## 📞 Help Resources

- Netlify docs: https://docs.netlify.com
- Railway docs: https://docs.railway.app
- Check: NETLIFY_DEPLOYMENT_GUIDE.md troubleshooting section

## 🎉 Success Indicators

✅ Site loads at `https://your-site.netlify.app`
✅ Login page displays
✅ Can create account
✅ Can upload CSV
✅ Dashboard shows data
✅ No browser console errors

## 🔐 Security Reminders

- ❌ DO NOT commit `.env` file
- ✅ DO use environment variables only
- ✅ DO regenerate SECRET_KEY for production
- ✅ DO use HTTPS (automatic)
- ✅ DO backup database regularly

## ⏱️ Expected Times

| Task | Duration |
|------|----------|
| Set up database | 2-3 min |
| Push to Git | 1 min |
| Configure Netlify | 3-4 min |
| First build | 5-10 min |
| Total | ~15 min |

## 🎯 Next Steps

1. Read: `QUICK_DEPLOY.md`
2. Create: Railway PostgreSQL database
3. Configure: Environment variables
4. Deploy: Via Netlify dashboard
5. Verify: Visit your live site

---

**Everything is ready! Follow the 4 steps above and you're live! 🚀**

For detailed guide: Open `QUICK_DEPLOY.md`
