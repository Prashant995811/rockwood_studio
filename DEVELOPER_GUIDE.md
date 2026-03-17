# Developer Guide

This file is for any developer who works on the Rockwood Studio project later.

It explains:

- How the project is structured
- How to understand the code quickly
- Where to make common changes
- How to safely update features
- What to check before deploying

## 1. Project Purpose

This is a Flask-based website for an interior design and interior work company.

Main parts:

- Public website for visitors
- Admin panel for content management
- PostgreSQL database with SQLAlchemy models
- Config-driven settings for company details and branding

## 2. High-Level Architecture

The project is divided into these parts:

- `app.py`
  - Local development entry point
- `wsgi.py`
  - Production entry point for Gunicorn/Render
- `config.py`
  - Loads environment variables and app configuration
- `app/`
  - Core Flask application package
- `templates/`
  - Jinja HTML templates
- `static/`
  - CSS, JavaScript, and uploaded images

## 3. Folder Walkthrough

### Root files

- `app.py`
  - Starts the app locally with `create_app()`
- `wsgi.py`
  - Used in production deploys
- `config.py`
  - Reads `.env` values
- `requirements.txt`
  - Python dependencies
- `render.yaml`
  - Render deployment config
- `README.md`
  - Basic setup and deploy instructions

### `app/`

#### `app/__init__.py`

This is the app factory.

It:

- Creates the Flask app
- Connects template and static folders
- Initializes the database
- Registers routes
- Adds shared site settings into templates
- Creates database tables
- Runs schema updates
- Seeds default admin/settings/sample content

If the app is not starting correctly, this is one of the first files to check.

#### `app/extensions.py`

Contains shared Flask extensions.

Currently:

- `db = SQLAlchemy()`

#### `app/models/entities.py`

Contains all SQLAlchemy models.

Current models:

- `AdminUser`
- `Service`
- `Project`
- `GalleryImage`
- `Testimonial`
- `ContactInquiry`
- `SiteSetting`

Whenever a new database-backed feature is added, it usually starts here.

#### `app/forms/forms.py`

Contains WTForms forms for:

- Admin login
- Services
- Projects
- Gallery
- Testimonials
- Contact form
- Site settings

If validation needs to change, update it here.

#### `app/routes/public.py`

Contains all public website routes.

Examples:

- Home page
- About page
- Services page
- Projects page
- Gallery page
- Testimonials page
- Contact page

If a visitor-facing page is broken, check this file first.

#### `app/routes/admin.py`

Contains admin routes and CRUD logic.

This file handles:

- Admin login/logout
- Dashboard
- Create/edit/delete services
- Create/edit/delete projects
- Add/delete gallery items
- Create/edit/delete testimonials
- View contact inquiries
- Update website settings
- Upload/delete images and logo

Most content management changes happen here.

#### `app/utils/`

Utility helpers:

- `decorators.py`
  - Admin session protection
- `helpers.py`
  - Image save/delete, slug generation, settings loader, Formspree submission
- `schema.py`
  - Small schema updates for existing databases
- `seed.py`
  - Creates default admin and starter content

## 4. Template Structure

### Main layout

- `templates/base.html`
  - Shared public layout
- `templates/components/navbar.html`
  - Main public navigation
- `templates/components/footer.html`
  - Public footer

### Public pages

- `templates/home.html`
- `templates/about.html`
- `templates/services.html`
- `templates/projects.html`
- `templates/project_detail.html`
- `templates/gallery.html`
- `templates/testimonials.html`
- `templates/contact.html`

### Admin pages

- `templates/admin/base_admin.html`
  - Shared admin layout
- `templates/admin/login.html`
  - Admin login page
- `templates/admin/dashboard.html`
  - Dashboard
- `templates/admin/*`
  - CRUD and settings screens

## 5. Styling and Frontend Behavior

### CSS

- `static/css/styles.css`
  - Public website design system
- `static/css/admin.css`
  - Admin panel styles

If the whole site theme needs updating, change CSS variables near the top of these files first.

### JavaScript

- `static/js/main.js`

This file handles:

- Mobile menu toggle
- Back to top button
- Gallery lightbox
- Section reveal animations

Keep this file simple. Avoid adding heavy frontend frameworks unless the project direction changes.

## 6. How Data Flows

### Public visitor flow

1. Visitor opens a route from `app/routes/public.py`
2. Route queries the database
3. Data is sent to a Jinja template
4. Template renders UI using `templates/` and `static/`

### Admin content flow

1. Admin logs in through session-based auth
2. Admin opens a CRUD page
3. Form submits to route in `app/routes/admin.py`
4. Route validates form
5. Database record is created or updated
6. Optional image is uploaded to `static/uploads/`
7. Flash message confirms the result

## 7. Common Change Guide

### Change company contact details

Use Admin -> Settings.

Data is stored in:

- `SiteSetting` model

### Change theme colors

Edit:

- `static/css/styles.css`
- `static/css/admin.css` if admin should match

Start with the `:root` color variables first.

### Change logo behavior

Relevant files:

- `templates/components/navbar.html`
- `templates/admin/settings_form.html`
- `app/routes/admin.py`
- `app/models/entities.py`

### Add a new public section

Usually update:

- `app/routes/public.py`
- one or more files in `templates/`
- `static/css/styles.css`

### Add a new admin-managed content type

Usually update:

1. `app/models/entities.py`
2. `app/forms/forms.py`
3. `app/routes/admin.py`
4. `templates/admin/`
5. optional public template/routes if shown publicly

### Change image handling

Relevant files:

- `app/utils/helpers.py`
- `app/routes/admin.py`
- `static/css/styles.css`
- `static/css/admin.css`

## 8. Rules for Safe Changes

When editing this project, follow these rules:

- Keep code beginner-friendly
- Prefer clear functions over clever shortcuts
- Reuse existing patterns before adding new abstractions
- Avoid adding unnecessary dependencies
- Keep public and admin templates consistent
- When changing models, think about existing database data
- When replacing uploaded images, remove old files if no longer needed

## 9. Database Change Guidance

This project does not use Flask-Migrate yet.

That means model changes need extra care.

Current approach:

- `db.create_all()` creates missing tables
- `app/utils/schema.py` handles small safe column additions

If you add a new column to an existing table:

1. Update the model
2. Update `app/utils/schema.py` if existing databases need that column
3. Restart the app

For larger database changes, add Flask-Migrate in the future.

## 10. How to Debug Problems

### Template error

Check:

- route name in `app/routes/`
- template file exists in `templates/`
- variable names passed to `render_template`

### Image not showing

Check:

- file exists in `static/uploads/`
- correct filename saved in database
- template uses `url_for('static', filename='uploads/...')`

### Admin page not saving

Check:

- form validation in `app/forms/forms.py`
- route POST logic in `app/routes/admin.py`
- flash messages
- terminal traceback

### Database connection error

Check:

- `.env`
- `DATABASE_URL`
- PostgreSQL is running
- password is correct

### Deployment error

Check:

- `wsgi.py`
- `render.yaml`
- environment variables on the hosting platform
- production logs

## 11. Recommended Change Workflow

When making updates, follow this order:

1. Understand the feature first
2. Identify the route, model, template, and CSS involved
3. Make the smallest clean change
4. Test both public and admin impact
5. Check image handling if uploads are involved
6. Check mobile layout if UI changed
7. Confirm no broken links or missing routes

## 12. Before Deployment Checklist

- `.env` values are correct
- `DATABASE_URL` is valid
- `FORMSPREE_ENDPOINT` is set
- `requirements.txt` is updated
- `render.yaml` start command is correct
- Images load correctly
- Admin login works
- Contact form saves inquiry correctly
- Public navigation works
- No template errors in logs

## 13. Good Future Improvements

If a developer wants to improve the project later, good next steps are:

- Add Flask-Migrate
- Add pagination in admin tables
- Add gallery edit/replace feature
- Add richer SEO meta tags
- Add password change inside admin
- Add image compression on upload
- Add content ordering controls

## 14. Final Advice for Future Developers

This codebase is intentionally simple.

That is a feature, not a limitation.

When making changes:

- Prefer clarity over cleverness
- Preserve consistency
- Keep the admin experience easy
- Think about non-technical users updating content
- Test the whole flow, not just one file
