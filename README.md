# TurfEase - Sports Turf Booking System

A full-featured sports turf booking platform built with Django. Users can browse turfs, book time slots, and manage their reservations. Admins get a dedicated dashboard to manage turfs, bookings, users, and maintenance schedules.

## Features

- **User Registration & Login** — Separate auth flows for users and admins
- **Browse Turfs** — Search and filter available turfs by name or location
- **Book Turfs** — Select date, time, and team size (5-a-side / 7-a-side / 11-a-side)
- **Booking Confirmation** — Review booking details before confirming
- **Booking History** — View, paginate, and cancel upcoming bookings
- **Cancelled Booking Receipts** — Printable refund receipts for maintenance cancellations
- **In-App Notifications** — Users get notified when bookings are auto-cancelled
- **User Profile** — View and update account details
- **Admin Dashboard** — Stats, manage turfs, bookings, users, maintenance, cancelled bookings
- **Maintenance Blocks** — Admins can block time slots; conflicting bookings are auto-cancelled with full cashback
- **Double-Booking Prevention** — Atomic transactions prevent conflicting bookings
- **CSV Export** — Export booking data from the admin dashboard
- **Email Validation** — Only Gmail addresses allowed; duplicate emails rejected
- **Dark / Light Theme** — Light theme for users, dark theme for admins
- **Responsive Design** — Works on desktop and mobile

## Tech Stack

- Python 3.10+
- Django 5.2
- SQLite (file-based — no database server needed)
- Pillow (image handling)
- HTML / CSS (no JavaScript frameworks)

---

## Setup Guide (New PC — Step by Step)

### Prerequisites

- **Windows / macOS / Linux**
- **Python 3.10 or above** — Download from [python.org/downloads](https://python.org/downloads)
  > **Important (Windows):** During installation, check **"Add Python to PATH"** before clicking Install.

### Step 1: Download the Project

**Option A — From GitHub (ZIP):**
1. Go to the GitHub repository
2. Click **Code → Download ZIP**
3. Extract the ZIP to any folder (e.g. `Desktop\Turfease`)

**Option B — Using Git:**
```bash
git clone https://github.com/shonu01/TurfEase.git
cd TurfEase
```

### Step 2: Open Terminal in the Project Folder

**Windows:**
1. Open the **Turfease** folder in File Explorer
2. Click the **address bar** at the top
3. Type `cmd` and press **Enter**

**macOS / Linux:**
```bash
cd /path/to/Turfease
```

### Step 3: Create a Virtual Environment

```bash
python -m venv venv
```

### Step 4: Activate the Virtual Environment

**Windows:**
```bash
venv\Scripts\activate
```

**macOS / Linux:**
```bash
source venv/bin/activate
```

> You should see `(venv)` at the beginning of your terminal line.

### Step 5: Install Dependencies

```bash
pip install -r requirements.txt
```

### Step 6: Set Up the Database

```bash
python manage.py migrate
```

> This project uses **SQLite** — a single file (`db.sqlite3`). No MySQL/PostgreSQL installation needed.

### Step 7: Create an Admin Account

```bash
python manage.py createsuperuser
```

Enter a username, email, and password when prompted.

> **Note:** If the ZIP already contains a `db.sqlite3` file with existing data, you can skip Steps 6 & 7 and use the existing accounts.

### Step 8: Start the Server

```bash
python manage.py runserver
```

### Step 9: Open in Browser

| Page | URL |
|------|-----|
| Home | http://127.0.0.1:8000/ |
| Register | http://127.0.0.1:8000/register/ |
| User Login | http://127.0.0.1:8000/login/ |
| Admin Login | http://127.0.0.1:8000/admin-login/ |
| Admin Dashboard | http://127.0.0.1:8000/dashboard/ |

---

## Running Again (After Restart)

Open terminal in the project folder, then:

```bash
venv\Scripts\activate
python manage.py runserver
```

## Stopping the Server

Press **Ctrl + C** in the terminal.

---

## Project Structure

```
Turfease/
├── accounts/        # User registration, login, profile
├── bookings/        # Booking logic, cancellations, notifications
├── dashboard/       # Admin dashboard views
├── turfs/           # Turf & maintenance models/forms
├── templates/       # All HTML templates
├── static/          # CSS, images, JS
├── media/           # Uploaded turf images
├── turfease/        # Django project settings & URLs
├── db.sqlite3       # SQLite database (auto-created)
├── manage.py        # Django management script
└── requirements.txt # Python dependencies
```

## URLs

| URL | Description |
|-----|-------------|
| `/` | Homepage |
| `/register/` | User registration |
| `/login/` | User login |
| `/admin-login/` | Admin login |
| `/turfs/` | Browse all turfs |
| `/bookings/history/` | User booking history |
| `/bookings/profile/` | User profile |
| `/admin-dashboard/` | Admin dashboard |

## Default Admin Account

- Username: `admin`
- Password: `admin123`

## Project Structure

```
TurfEase/
├── accounts/        # User auth (register, login, profile)
├── bookings/        # Booking logic and history
├── dashboard/       # Admin dashboard views
├── turfs/           # Turf models, listing, detail
├── templates/       # All HTML templates
├── static/css/      # Stylesheet
├── turfease/        # Project settings & URLs
├── manage.py
└── requirements.txt
```
