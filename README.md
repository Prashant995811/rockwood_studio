# Rockwood Studio Website

This project is a complete Flask website for an interior design and interior work company named **Rockwood Studio**.

It includes:

- Public website pages
- Admin login and dashboard
- PostgreSQL database integration
- CRUD management for services, projects, gallery, testimonials, and site settings
- Contact form with Formspree support and database saving

## Project Structure

```text
Rockwood Studio/
├── app.py
├── config.py
├── requirements.txt
├── .env.example
├── app/
│   ├── __init__.py
│   ├── extensions.py
│   ├── models/
│   ├── forms/
│   ├── routes/
│   └── utils/
├── templates/
├── static/
└── instance/
```

## 1. Create a Virtual Environment

Windows:

```powershell
python -m venv venv
venv\Scripts\activate
```

## 2. Install Requirements

```powershell
pip install -r requirements.txt
```

## 3. Setup PostgreSQL

1. Install PostgreSQL on your system.
2. Open PostgreSQL or pgAdmin.
3. Create a database named `rockwood_studio`.

Example SQL:

```sql
CREATE DATABASE rockwood_studio;
```

## 4. Add Environment Variables

1. Copy `.env.example` to `.env`
2. Update the values

Example:

```env
SECRET_KEY=your_secret_key
DATABASE_URL=postgresql://postgres:password@localhost:5432/rockwood_studio
DEFAULT_ADMIN_USERNAME=admin
DEFAULT_ADMIN_PASSWORD=admin123
FORMSPREE_ENDPOINT=https://formspree.io/f/your-form-id
```

## 5. Run the App

```powershell
python app.py
```

Then open:

```text
http://127.0.0.1:5000
```

## 6. Default Admin Login

Admin login URL:

```text
http://127.0.0.1:5000/admin/login
```

Default admin credentials come from your `.env` file:

- Username: `DEFAULT_ADMIN_USERNAME`
- Password: `DEFAULT_ADMIN_PASSWORD`

The app creates the first admin user automatically on first run.

## 7. How Content Management Works

After login, the admin can manage:

- Services
- Projects
- Gallery images
- Testimonials
- Contact inquiries
- Website settings

You can change:

- Company name
- Tagline
- Contact details
- Hero text
- Footer text
- Social links
- Google map embed URL

## 8. Contact Form Setup

The contact form does two things:

1. Saves every inquiry into PostgreSQL
2. Sends the same inquiry to Formspree

To make email notifications work:

1. Create a form on Formspree
2. Copy the endpoint
3. Add the endpoint to `FORMSPREE_ENDPOINT` in `.env`

If Formspree is not configured, the inquiry is still saved in the database.

## 9. Notes

- Uploaded images are stored in `static/uploads/`
- The app uses SQLAlchemy models and automatically creates tables on first run
- You can customize styles from `static/css/styles.css` and `static/css/admin.css`

## 10. Future Improvements

- Add pagination in admin tables
- Add image delete from storage when records are removed
- Add richer SEO metadata per page
- Add database migrations with Flask-Migrate

## 11. Free Deployment

As of March 16, 2026, the easiest free setup for this project is:

- Frontend + Flask app on Render
- PostgreSQL on Neon

Why this setup:

- Render supports free Python web services
- Neon offers a free PostgreSQL database
- This avoids Render free Postgres expiry limits

### Option A: Recommended Free Setup

#### 1. Push your code to GitHub

Create a GitHub repository and push this project.

#### 2. Create a free Neon database

1. Sign up at Neon
2. Create a new PostgreSQL project
3. Copy the connection string
4. Replace the password placeholder if Neon asks you to

Then keep this value ready for `DATABASE_URL`.

#### 3. Deploy the app on Render

1. Sign up at Render
2. Click `New` -> `Blueprint`
3. Select your GitHub repository
4. Render will detect the included `render.yaml`

Set these environment variables in Render:

- `DATABASE_URL` = your Neon connection string
- `DEFAULT_ADMIN_PASSWORD` = your chosen admin password
- `FORMSPREE_ENDPOINT` = your Formspree endpoint

Render will auto-generate:

- `SECRET_KEY`

Render start command:

```text
gunicorn wsgi:app
```

#### 4. Open your deployed website

After deploy finishes, Render will give you a URL like:

```text
https://your-app-name.onrender.com
```

Admin login will be:

```text
https://your-app-name.onrender.com/admin/login
```

### Important Free Plan Notes

Render free web service:

- Spins down after 15 minutes of inactivity
- Wakes up on the next request
- First request after idle can be slow

Neon free database:

- Free PostgreSQL storage and monthly compute limits apply
- Good for demos, portfolio sites, and small projects

### Official Docs

- Render Flask deploy: https://render.com/docs/deploy-flask
- Render free tier: https://render.com/docs/free
- Neon pricing: https://neon.com/pricing
