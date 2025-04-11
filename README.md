# Birthday Reminder API on Render

This is a simple FastAPI server for managing birthday reminders. It provides endpoints to add, update, and query birthdays, with support for checking birthdays in the current week or month.

## API Endpoints

- `GET /` - Check if API is running
- `GET /birthdays` - Get all birthdays
- `POST /birthdays` - Add a new birthday
- `PUT /birthdays/{name}` - Update an existing birthday
- `GET /birthdays/week` - Get birthdays in the next 7 days
- `GET /birthdays/month` - Get birthdays in the current month

## Deployment on Render

1. Create a new Web Service on Render
2. Link to your repository
3. Use the following settings:
   - **Environment**: Python 3
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `uvicorn app:app --host 0.0.0.0 --port $PORT`

## Local Development

1. Install dependencies:

   ```bash
   pip install -r requirements.txt
   ```

2. Run the server:
   ```bash
   uvicorn app:app --reload
   ```

The server will be available at `http://localhost:8000`

## API Usage Example

Add a birthday:

```bash
curl -X POST http://localhost:8000/birthdays \
  -H "Content-Type: application/json" \
  -d '{"name":"John Doe","date":"2024-06-15"}'
```

Get birthdays this month:

```bash
curl http://localhost:8000/birthdays/month
```
