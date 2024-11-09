FROM python:3.12.3

# Set working directory
WORKDIR /app

# Copy only requirements first (bessere Nutzung von Docker Caching)
COPY requirements.txt .

# Install dependencies
RUN pip install --upgrade pip && pip install -r requirements.txt

# Copy the rest of the application code
COPY . .

# Install ffmpeg (da es sich selten ändert, verschiebt man es häufig vor den Application-Code)
RUN apt-get update && apt-get install -y ffmpeg && apt-get clean

# Make the backend script executable
RUN chmod +x /app/compose/run-backend.sh

# Expose the port
EXPOSE 8000

# Run the backend
CMD ["/app/compose/run-backend.sh"]


# FROM python:3.12.3

# WORKDIR /app

# COPY . .

# RUN apt-get update && apt-get install -y ffmpeg

# RUN /usr/local/bin/python -m pip install --upgrade pip

# RUN pip install -r requirements.txt

# RUN chmod +x /app/compose/run-backend.sh

# CMD [ "/app/compose/run-backend.sh" ]

# EXPOSE 8000