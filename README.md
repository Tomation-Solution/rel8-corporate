# MAN CMS BACKEND API




# Project Setup

## Prerequisites

Ensure that you have Homebrew installed on your machine.(macOS)

## Steps to Set Up the Project

### 1. Install Python 3.11

To install Python 3.11, run the following command:

```bash
brew install python@3.11
```
(macOS)
### 2. Set Up a Virtual Environment

Create a virtual environment using Python 3.11:

```bash
python3.11 -m venv venv
```

Activate the virtual environment:

```bash
source venv/bin/activate
```

### 3. Install Python Packages

Once the virtual environment is activated, upgrade `pip` and `setuptools`, and then install the project dependencies:

```bash
pip install --upgrade pip setuptools
pip install --upgrade pip setuptools wheel
pip install cython
pip install PyYAML==6.0.1
pip install -r requirements.txt
```

### 4. Load Environment Variables

Install `python-dotenv`:

```bash
pip install python-dotenv
```

Add the following to your `settings.py` file to load environment variables from a `.env` file:

```python
from dotenv import load_dotenv
load_dotenv()  # Load environment variables from .env
```

### 5. Run Database Migrations

To apply database migrations, run:

```bash
python manage.py migrate
```

### 6. Create a Superuser

Create a superuser locally with the following credentials:

- **Email:** your email address
- **Password:** password

You can create the superuser by running the following command and providing the credentials above:

```bash
python manage.py createsuperuser
```
<!--  -->
if the createsuper cmd fails, then try
python manage.py createsuperuser --email <email> --matric_number <matric_number>
<!--  -->
#### 7.2 Start the Django Development Server

In the second terminal, run:

```bash
python manage.py runserver
```