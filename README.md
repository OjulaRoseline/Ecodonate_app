# Eco-Donate Platform 

**Crowdfund Community Projects Aligned with UN Sustainable Development Goals (SDGs)**

Eco-Donate is a Django-based web platform that allows users to create, browse, and donate to sustainability-focused community projects tied to the UN Sustainable Development Goals. It features user authentication, full CRUD operations for projects, and a simulated M-Pesa payment flow for donations — making it especially relevant for financial inclusion in regions like Kenya/Africa.

---

## Key Features 

- **User Authentication** → Register, login, and logout (Django built-in)
- **CRUD for Projects** → Create, read, update, and delete SDG-aligned projects (only creators can edit/delete)
- **Project Browsing** → List view with filters, progress bars, and responsive cards
- **M-Pesa Payment Simulation** → Fake STK Push flow: Enter phone number → "Confirm payment" → Donation recorded and project funded amount updated
- **SDG Integration** → Each project linked to one of the 17 UN SDGs
- **Responsive Design** → Bootstrap 5-powered UI for mobile/desktop
- **Real-time Progress Tracking** → Visual progress bars showing donation percentages toward project goals

---

## Tech Stack 

| Component | Technology |
|-----------|-----------|
| **Backend** | Django (Python) |
| **Frontend** | Bootstrap 5, Django Templates |
| **Database** | SQLite (default, easy to switch to PostgreSQL) |
| **Authentication** | Django Auth |
| **Payment Simulation** | Daraja API (M-Pesa) - Sandbox environment |

---

## Installation & Setup 

### 1. Clone the Repository

```bash
git clone https://github.com/OjulaRoseline/Ecodonate_app.git
cd Ecodonate
```

### 2. Create and Activate Virtual Environment

**On Windows:**
```bash
python -m venv venv
venv\Scripts\activate
```

**On macOS/Linux:**
```bash
python -m venv venv
source venv/bin/activate
```

### 3. Install Dependencies

```bash
pip install django
pip install python-dotenv
pip install requests
```

Or install from requirements file (if available):
```bash
pip install -r requirements.txt
```

### 4. Apply Database Migrations

```bash
cd Ecodonate
python manage.py makemigrations
python manage.py migrate
```

### 5. Create a Superuser (Admin Access)

```bash
python manage.py createsuperuser
```

Follow the prompts to create your admin account.

### 6. Run the Development Server

```bash
python manage.py runserver
```

Visit **http://127.0.0.1:8000/** in your browser.

---

## Usage 

### For Users:
1. **Register/Login** → Create an account or log in
2. **Browse Projects** → View all SDG-aligned projects with progress bars
3. **Create a Project** → Start your own sustainability initiative
   - Set a funding target
   - Link to an SDG goal
   - Add description and images
4. **Donate to Projects** → Support projects you believe in
   - Enter donation amount and phone number
   - Simulate M-Pesa payment
   - See your impact reflected immediately

### For Admins:
1. Visit `/admin` to access Django admin panel
2. Manage users, projects, and donations
3. Seed sample data quickly
4. Monitor platform activity

---

## Project Structure 

```
Ecodonate/
├── Ecodonate/                    # Project settings
│   ├── settings.py              # Django configuration
│   ├── urls.py                  # Main URL routing
│   └── wsgi.py                  # WSGI application
├── sdg_platform/                # Main app
│   ├── models.py                # SDGProject, Donation models
│   ├── views.py                 # Business logic (CRUD, M-Pesa)
│   ├── forms.py                 # DonationForm
│   ├── urls.py                  # App URL routing
│   ├── admin.py                 # Admin configuration
│   └── templates/               # HTML templates
│       └── sdg_platform/
│           ├── project_list.html
│           └── project_details.html
├── templates/                   # Base templates
│   └── base.html
├── manage.py                    # Django management script
├── db.sqlite3                   # Database (SQLite)
├── .env                         # Environment variables
└── README.md                    # This file
```

---

## Models Overview 

### SDGProject
```python
- title: CharField
- description: TextField
- sdg_goal: IntegerField (choices: 1-17 UN SDGs)
- target_amount: DecimalField
- current_amount: DecimalField
- image_url: URLField (for project thumbnail)
- creator: ForeignKey(User)
- created_at: DateTimeField
- percentage_funded: @property (calculated)
```

### Donation
```python
- project: ForeignKey(SDGProject)
- user: ForeignKey(User, nullable)
- amount: DecimalField
- phone_number: CharField
- timestamp: DateTimeField
```

---

## M-Pesa Integration 

The platform simulates M-Pesa STK Push flow using the **Daraja API** (sandbox environment):

1. **Initiation** → User enters amount and phone number
2. **Token Generation** → Backend fetches M-Pesa access token
3. **STK Push** → Simulated prompt sent to user
4. **Confirmation** → User "confirms" payment on confirmation page
5. **Database Update** → Project and donation records updated

**Note:** This is a sandbox/simulation. For production, integrate with real M-Pesa credentials.

---

## Environment Variables 

Create a `.env` file in the project root:

```env
SECRET_KEY=your-django-secret-key
DEBUG=True
ALLOWED_HOSTS=127.0.0.1,localhost

# M-Pesa Daraja API (Sandbox)
CONSUMER_KEY=your_consumer_key
CONSUMER_SECRET=your_consumer_secret
BUSINESS_SHORT_CODE=your_short_code
LIPA_NA_MPESA_PASSKEY=your_passkey
PAYMENT_CALLBACK_URL=http://127.0.0.1:8000/api/mpesa/callback/
```

---

## API Endpoints 

| Method | Endpoint | Purpose |
|--------|----------|---------|
| GET | `/` | List all projects |
| GET | `/project/<id>/` | View project details |
| POST | `/donate/start/<id>/` | Start donation process |
| POST | `/donate/confirm/` | Confirm payment |
| POST | `/donate/complete/` | Complete and record donation |
| POST | `/donate/mpesa_stk/<id>/` | Initiate M-Pesa STK Push |
| POST | `/donate/callback/` | M-Pesa callback endpoint |

---

## Future Improvements 🚀

- [x] **Real M-Pesa Integration** → ✅ Connected to live M-Pesa Daraja API (Sandbox & Production Ready)
- [ ] **Email Notifications** → Send confirmation emails for donations
- [ ] **Advanced Filtering** → Filter projects by SDG, funding status, date
- [ ] **User Profiles** → Showcase creator achievements and impact
- [ ] **Analytics Dashboard** → Track funding trends, top projects, top donors
- [ ] **Social Features** → Comments, project updates, social sharing
- [ ] **Automated Testing** → Unit tests, integration tests, CI/CD pipeline
- [ ] **API Endpoints** → RESTful API for mobile apps
- [ ] **Internationalization (i18n)** → Multi-language support
- [ ] **Database Optimization** → Switch to PostgreSQL for production
- [ ] **File Upload** → Allow users to upload project images directly
- [ ] **Payment History** → Donor dashboard to track contributions

---

## Contributing 

We welcome contributions! Please follow these steps:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/your-feature`)
3. Commit your changes (`git commit -m 'Add your feature'`)
4. Push to the branch (`git push origin feature/your-feature`)
5. Open a Pull Request

---

## License 

This project is licensed under the **MIT License** — see the LICENSE file for details.

---

## Contact & Support 

- **Repository:** [GitHub - Ecodonate_app](https://github.com/OjulaRoseline/Ecodonate_app)
- **Issues:** Report bugs or request features via GitHub Issues
- **Email:** [Your contact email]

---

## Acknowledgments 

- UN Sustainable Development Goals (SDGs) — For inspiring global action
- Django Community — For the amazing framework
- Bootstrap — For responsive UI components
- Daraja API — For M-Pesa sandbox integration

---

**Happy Donating! **

*Help fund sustainable projects and contribute to a better future for communities worldwide.*
