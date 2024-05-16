FROM tiangolo/uvicorn-gunicorn-fastapi:python3.9

WORKDIR /app

COPY ./app /app/app
COPY ./requirements.txt /app/requirements.txt
COPY ./.env /app/.env

RUN pip install --no-cache-dir -r /app/requirements.txt

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "80"]



# Use a specific version of the base image for stability
FROM tiangolo/uvicorn-gunicorn-fastapi:python3.9-2022-03-22

# Set the working directory inside the container
WORKDIR /app

# Copy only requirements first to leverage Docker cache
COPY ./requirements.txt /app/requirements.txt

# Install dependencies
RUN pip install --no-cache-dir -r /app/requirements.txt

# Copy the rest of the application code
COPY ./app /app/app
COPY ./.env /app/.env


# Expose the port that the app runs on
EXPOSE 80

# Define the command to run the application
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "80"]
