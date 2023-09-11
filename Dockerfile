# Use an official Python runtime as the base image
FROM python:3.9-slim

# Set the working directory in the container
WORKDIR /usr/src/app

# Copy the requirements file into the container
COPY requirements.txt .

# Install the required Python libraries and git
RUN pip install --no-cache-dir -r requirements.txt && \
    apt-get update && \
    apt-get install -y git

# Clone the espnfantasyfootball repository
RUN git clone https://github.com/tbryan2/espnfantasyfootball.git

# Set the working directory to the cloned repository
WORKDIR /usr/src/app/espnfantasyfootball/espnfantasyfootball

# Set environment variables for leagueid, username, and password
ENV LEAGUE_ID=""
ENV SWID=""
ENV ESPN_S2=""

# Command to run the script with environment variables
CMD ["python", "pull_data.py"]
