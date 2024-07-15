# TODO List

## Overview

This project has been enhanced with additional features, including a new FastAPI service that interacts with a locally deployed MongoDB container. The application now comprises a backend service built with FastAPI for general operations, a second FastAPI service for MongoDB interactions, and a frontend interface developed using Streamlit.

## Features

- **Get Full TODO List**: Retrieve all current tasks in the TODO list.
- **Get Single Task**: Fetch a single task based on its unique ID.
- **Add Task**: Add a new task to the TODO list with details such as title, description, priority, 
and due date.
- **Update Task**: Update old task details.
- **Delete Single Task**: Delete a single task from your list.
- **Delete TODO-List**: Delete entire TODO-List.

## Installation with Docker

To set up the project using Docker, including the MongoDB container, follow these steps:

1. Clone the repository to your local machine.
2. Ensure you have Docker and Docker Compose installed.
3. Navigate to the project directory.
4. Run `docker-compose up --build` in your terminal to build and start the containers, including the MongoDB container with its volume mounted to the `data` directory in your project.

This setup will start all backend services, the MongoDB container, and the Streamlit frontend, and the backend FastAPI as defined in your `docker-compose.yaml` file.

## Usage

Once the Docker containers are up and running, you can interact with the application as follows:

- The original FastAPI backend is accessible through HTTP requests on `http://localhost:8080`.
- The new FastAPI service for MongoDB interactions is available on `http://localhost:8081`.
- The Streamlit frontend can be accessed by visiting `http://localhost:8501` in your web browser.
- The local MongoDB container can be accessed on `mongodb://localhost:27017`

## Development

This project uses FastAPI for backend services, including interactions with MongoDB, and Streamlit for the frontend. For development:

- Refer to the [FastAPI documentation](https://fastapi.tiangolo.com/) for backend development.
- For MongoDB interaction, ensure familiarity with MongoDB operations and the FastAPI database library `pymongo`.
- Visit the [Streamlit documentation](https://docs.streamlit.io/) for frontend development guidance.

Remember to check the `docker-compose.yaml` file for service configurations and the `data` directory for MongoDB data persistence.

## Contributing

Contributions are welcome! Please feel free to submit a pull request.
