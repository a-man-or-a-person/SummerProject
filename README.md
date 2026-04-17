# URL Shortener Service

## Project Overview
A URL Shortener service that converts long URLs into short, manageable links. Built using FastAPI, Redis, and SQLAlchemy, this service enables efficient storing and retrieval of shortened URLs.

## Features
- URL shortening
- Custom aliases for shortened URLs
- Expiration date for links
- URL redirection
- Statistics for shortened URLs (e.g., number of hits)

## Technology Stack
- **Backend**: FastAPI
- **Database**: SQLAlchemy with a relational database (e.g., PostgreSQL)
- **Cache**: Redis for fast URL retrieval
- **Testing**: Pytest
- **Deployment**: Docker for containerization

## Project Structure
```
url_shortener/
│
├── app/
│   ├── main.py         # Entry point
│   ├── models.py       # Database models
│   ├── routers.py      # API routes
│   ├── services.py     # Business logic
│   ├── db.py          # Database connection
│   └── cache.py       # Redis cache integration
│
├── tests/              # Test cases
├── Dockerfile           # Dockerfile for building the image
├── requirements.txt     # Python package dependencies
└── README.md           # Project documentation
```

## Installation Instructions
1. Clone the repository:
   ```bash
   git clone https://github.com/a-man-or-a-person/SummerProject.git
   cd SummerProject
   ```
2. Create a virtual environment and activate it:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows use `venv\Scripts\activate`
   ```
3. Install the dependencies:
   ```bash
   pip install -r requirements.txt
   ```
4. Set up the database and cache as per your local environment.

## Environment Variables Configuration
- `DATABASE_URL`: Database connection string (e.g., PostgreSQL)
- `REDIS_URL`: URL for the Redis cache
- `SHORT_URL_DOMAIN`: Domain to use for the shortened URLs
- `SECRET_KEY`: Secret key for signing tokens (ensure it is kept confidential).

## Running the Application
Run the following command to start the service:
```bash
uvicorn app.main:app --reload
```