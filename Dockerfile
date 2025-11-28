# Use official Python image
FROM python:3.11-slim

# Set working directory inside container
WORKDIR /app

# Copy only requirements first to leverage Docker cache
COPY requirements.txt .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the project
COPY . .

# No CMD here; Docker Compose will run the scripts
# Print Python path at container start and then run scripts
# At container start, list files and then run your scripts
CMD sh -c "echo 'Folder contents:' && ls /app && python pipeline/main.py"
