# Fitness Studio Booking API (Django)

This project implements a simple Booking API for a fictional fitness studio using Django and Django REST Framework.

## Features

* View available fitness classes.
* Book a class slot.
* View all bookings by a specific email.
* Timezone-aware scheduling (classes stored in IST, responses adjustable via `tz` parameter).

## Tech Stack

* Django
* Django REST Framework
* SQLite (default database)

## Setup Instructions

1. **Clone the repo**

```bash
git clone https://github.com/yourusername/fitness-booking-api.git
cd fitness-booking-api
```

2. **Create a virtual environment**

```bash
python -m venv env
source env/bin/activate  # On Windows: env\Scripts\activate
```

3. **Install dependencies**

```bash
pip install -r requirements.txt
```

4. **Apply migrations**

```bash
python manage.py migrate
```

5. **Load sample data (optional)**

```bash
python manage.py loaddata classes.json
```

6. **Run the server**

```bash
python manage.py runserver
```

## API Endpoints

### 1. `GET /classes/`

Retrieve a list of upcoming fitness classes.

**Query Params:**

* `tz` (optional): IANA timezone string to convert class datetime (e.g., `America/New_York`, `Asia/Kolkata`)

**Example:**

```bash
curl http://localhost:8000/classes/?tz=America/New_York
```

**Response:**

```json
[
  {
    "id": 1,
    "name": "Morning Yoga",
    "datetime": "2025-06-10T09:00:00-04:00",
    "instructor": "Alexa",
    "available_slots": 10
  },
  ...
]
```

### 2. `POST /book/`

Book a spot in a class.

**Payload:**

```json
{
  "class_id": 1,
  "client_name": "John wick",
  "client_email": "john@xyz.com"
}
```

**Example:**

```bash
curl -X POST http://localhost:8000/book/ \
     -H "Content-Type: application/json" \
     -d '{"class_id": 1, "client_name": "John wick", "client_email": "john@xyz.com"}'
```

### 3. `GET /bookings/?email=<client_email>`

Get all bookings for a specific client.

**Example:**

```bash
curl http://localhost:8000/bookings/?email=john@xyz.com
```

**Response:**

```json
[
  {
    "id": 5,
    "fitness_class": 1,
    "client_name": "John wick",
    "client_email": "john@xyz.com",
    "booked_at": "2025-06-07T12:00:00Z"
  },
  ...
]
```

## Evaluation Criteria

* Code readability and structure
* API design and validation
* Timezone-aware responses
* Bonus: unit tests, logging, and proper documentation

## Deliverables

* Source code
* Sample seed data (`classes.json`)
* README.md (this file)
* Loom video walkthrough (to be submitted by Chaitanya)

---

© 2025 Fitness Studio Booking API
