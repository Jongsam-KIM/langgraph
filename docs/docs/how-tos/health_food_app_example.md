# Health Food App Example

This guide shows how to run a small FastAPI demo that mimics a global health food
distribution app. The example code lives in `examples/health_food_app/main.py`.

Install the dependencies and start the server:

```bash
pip install fastapi uvicorn
uvicorn examples.health_food_app.main:app --reload
```

Once running, visit `http://localhost:8000/docs` to explore the API.
