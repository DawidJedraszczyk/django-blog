# Base image
FROM python:3.10-slim

# Set the working directory
WORKDIR /app

# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the Django app code to the container
COPY . .

# Expose port 8000 for Django development server
EXPOSE 8000

# Create .env file
RUN echo "POSTGRES_DB=django_blog" > .env && \
    echo "POSTGRES_USER=OPERATION_SYSTEM_USER" >> .env && \
    echo "POSTGRES_PASSWORD=PASSWORD" >> .env && \
    echo "POSTGRES_HOST=localhost" >> .env && \
    echo "EMAIL_HOST_USER=duduslol2016@gmail.com" >> .env && \
    echo "EMAIL_HOST_PASSWORD=ftro gtmu jppt lcao" >> .env

# Run Django commands
CMD ["sh", "-c", "python manage.py migrate && python manage.py populate_data && python manage.py runserver 0.0.0.0:8000"]
