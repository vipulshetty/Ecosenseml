FROM python:3.9-slim

WORKDIR /app

# Copy requirements first to leverage Docker cache
COPY requirements.txt .

# Install dependencies
# We need to make sure we have the system dependencies for scikit-learn/pandas if needed, 
# but usually slim is fine for wheels.
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application
COPY . .

# Create the dummy model if it doesn't exist (or just run it to be sure)
RUN python create_dummy_model.py

# Expose the port Hugging Face expects (7860)
EXPOSE 7860

# Run the application with Gunicorn
# Bind to 0.0.0.0:7860
CMD ["gunicorn", "-b", "0.0.0.0:7860", "app:app"]
