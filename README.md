# TurfEase - Sports Turf Booking System

A full-featured sports turf booking platform built with Django. Users can browse turfs, book time slots, and manage their reservations. Admins get a dedicated dashboard to manage turfs, bookings, users, and maintenance schedules.

## Features

- **User Registration & Login** — Separate auth flows for users and admins
- **Browse Turfs** — Search and filter available turfs by name or location
- **Book Turfs** — Select date, time, and team size (5-a-side / 7-a-side)
- **Booking Confirmation** — Review booking details before confirming
- **Booking History** — View, paginate, and cancel upcoming bookings
- **User Profile** — View and update account details
- **Admin Dashboard** — Stats, manage turfs, bookings, users, maintenance
- **Maintenance Blocks** — Admins can block time slots for turf maintenance
- **Double-Booking Prevention** — Atomic transactions prevent conflicting bookings
- **Dark / Light Theme** — Light theme for users, dark theme for admins
- **Responsive Design** — Works on desktop and mobile

## Tech Stack

- Python 3.11
- Django 5.2
- SQLite (development)
- HTML / CSS (no JavaScript frameworks)

## Setup

```bash
# Clone the repository
git clone https://github.com/shonu01/TurfEase.git
cd TurfEase

# Create virtual environment
python -m venv venv
venv\Scripts\activate        # Windows
# source venv/bin/activate   # macOS/Linux

# Install dependencies
pip install -r requirements.txt

# Run migrations
python manage.py migrate

# Create superuser
python manage.py createsuperuser

# Start development server
python manage.py runserver
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
