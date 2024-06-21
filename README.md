# TODO List Backend

## Overview

This backend service is designed to manage a TODO list, allowing users to add tasks, retrieve a single task, or get the full list of tasks. It's built using FastAPI, a modern, fast (high-performance) web framework for building APIs with Python.

## Features

- **Get Full TODO List**: Retrieve all current tasks in the TODO list.
- **Get Single Task**: Fetch a single task based on its unique ID.
- **Add Task**: Add a new task to the TODO list with details such as title, description, priority, 
and due date.
- **Delete Single Task**: Delete a single task from your list.
- **Delete TODO-List**: Delete entire TODO-List.

## Installation with Docker

To set up the project using Docker, follow these steps:

1. Clone the repository to your local machine.
2. Ensure you have Docker installed.
3. Run `docker-compose up --build` in your terminal to build and start the containers.

This will start the backend service and any other services defined in your `docker-compose.yaml` file.

The docker-compose configuration will build the Docker image for your FastAPI application, mount the current directory to the container, and forward the container's port 80 to the host's port 8080.

## Usage
Once the Docker container is running, you can interact with the API through HTTP requests on 'http://localhost:8080'.

## Development
This project uses FastAPI. For more information on developing with FastAPI, visit the official FastAPI documentation.

## Contributing
Contributions are welcome! Please feel free to submit a pull request.