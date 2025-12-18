# 🔧 Post-Deployment Steps for Render

## ✅ Phase 4: PostgreSQL Setup - COMPLETED ✓

Your code is now configured to use PostgreSQL on Render!

---

## 📋 After First Deploy on Render - IMPORTANT STEPS

### Step 1: Create PostgreSQL Database on Render

1. Go to your Render Dashboard
2. Click **"New +"** → **"PostgreSQL"**
3. Configure:
   - **Name:** `ecodonate-db`
   - **Database:** `ecodonate` (optional, default is fine)
   - **User:** `ecodonate_user` (optional, default is fine)
   - **Plan:** `Free` (for testing) or `Starter` (recommended for production)
4. Click **"Create Database"**
5. **Copy the "Internal Database URL"** - it looks like:
   ```
   postgresql://user:password@hostname:5432/dbname
   ```

### Step 2: Add DATABASE_URL to Web Service

1. Go to your Web Service dashboard
2. Click **"Environment"** tab
3. Click **"Add Environment Variable"**
4. Add:
   - **Key:** `DATABASE_URL`
   - **Value:** Paste the Internal Database URL you copied
5. Click **"Save Changes"**
6. Render will automatically redeploy your service

### Step 3: Run Migrations (CRITICAL!)

After your app is deployed and DATABASE_URL is set:

1. In your Web Service dashboard, click **"Shell"** tab
2. Run migrations:
   ```bash
   python manage.py migrate
   ```
3. Create a superuser (admin account):
   ```bash
   python manage.py createsuperuser
   ```
   Follow the prompts to create your admin username, email, and password.

### Step 4: Verify Everything Works

1. Visit your app URL: `https://your-app-name.onrender.com`
2. Test the homepage
3. Test admin panel: `https://your-app-name.onrender.com/admin`
4. Log in with your superuser credentials

---

## 🔒 Security: Update ALLOWED_HOSTS

After your app is deployed, update `ALLOWED_HOSTS` in `settings.py`:

1. Get your Render app URL (e.g., `ecodonate.onrender.com`)
2. Update `settings.py`:
   ```python
   ALLOWED_HOSTS = ['ecodonate.onrender.com']
   ```
3. Commit and push:
   ```bash
   git add Ecodonate/settings.py
   git commit -m "Update ALLOWED_HOSTS for production"
   git push origin main
   ```

---

## ✅ Checklist

- [ ] PostgreSQL database created on Render
- [ ] DATABASE_URL environment variable added to Web Service
- [ ] Migrations run successfully
- [ ] Superuser created
- [ ] App loads correctly
- [ ] Admin panel accessible
- [ ] ALLOWED_HOSTS updated with Render domain
- [ ] M-Pesa callback URL updated with Render domain

---

## 🐛 Troubleshooting

### Issue: "django.db.utils.OperationalError: could not connect to server"
**Fix:** 
- Verify DATABASE_URL is set correctly in Environment variables
- Check database is running (should show "Available" status)
- Make sure you're using the **Internal Database URL** (not External)

### Issue: "No migrations to apply"
**Fix:** 
- Check if you've run `makemigrations` first (not needed if migrations already exist)
- Verify you're connected to the correct database
- Run `python manage.py showmigrations` to see migration status

### Issue: "permission denied for database"
**Fix:** 
- Make sure you're using the Internal Database URL
- Check the database user has proper permissions
- Try recreating the database if needed

---

## 📝 Notes

- **Internal vs External Database URL:**
  - Use **Internal Database URL** for your Web Service (faster, more secure)
  - External URL is only needed if accessing from outside Render network

- **Database Backups:**
  - Free tier databases are backed up automatically
  - Consider upgrading for automatic backups on Starter+ plans

- **Local Development:**
  - Your local setup will still use SQLite (when DATABASE_URL is not set)
  - This is handled automatically by the dj-database-url configuration

---

## 🎉 You're All Set!

Once migrations are run and superuser is created, your app is fully deployed and ready to use!

