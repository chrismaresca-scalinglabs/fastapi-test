# Use a specific version of the base image for stability
FROM tiangolo/uvicorn-gunicorn-fastapi:python3.11

# Set the working directory inside the container
WORKDIR /app

# Copy only requirements first to leverage Docker cache
COPY ./requirements.txt /app/requirements.txt
COPY ./key.json /app/key.json


# Install dependencies
RUN pip install --no-cache-dir -r /app/requirements.txt

# Copy the rest of the application code
COPY ./app /app/app
COPY ./.env /app/.env


# Expose the port that the app runs on
EXPOSE 8001

# Define the command to run the application
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8001"]
