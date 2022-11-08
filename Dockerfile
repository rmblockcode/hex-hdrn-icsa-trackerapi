# Start from the official Python base image.

FROM python:3.9

# Set the current working directory to /code
WORKDIR /code

# Copy the file with the requirements to the /code directory
COPY ./requirements.txt /code/requirements.txt

# Install the package dependencies in the requirements file
RUN pip install --no-cache-dir -r /code/requirements.txt

# Copy the . directory inside the /code directory
COPY . /code/app

# Set the command to run the uvicorn server
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "80"]
