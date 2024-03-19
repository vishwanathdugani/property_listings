# Property Listings Project

This project consists of a frontend and a backend service, encapsulated within Docker containers to streamline development and deployment. The frontend service provides a user interface for property listings, while the backend service manages the API and database interactions.

## Prerequisites

- Docker and Docker Compose must be installed on your system. For installation instructions, refer to the [official Docker documentation](https://docs.docker.com/get-docker/).

## Getting Started

Follow these steps to get the project up and running on your local machine.

### Clone the Repository

First, clone the repository to your local machine using the following command:

```bash
git clone git@github.com:vishwanathdugani/property_listings.git
```

Navigate into the project directory:

```bash
cd property_listings
```

### Start the Services

Run the following command to build and start the services using Docker Compose:

```bash
docker-compose up --build
```

This command builds the images for the frontend and backend services and starts them.

### Accessing the Services

- **Frontend:** The frontend service can be accessed at [http://localhost:8080](http://localhost:8080). Use the credentials `admin` for the username and `password` for the password to log in.

- **Backend:** The backend service is available at [http://localhost:8000](http://localhost:8000).
- **Backend API documentation:** The backend service documentation is available at [http://localhost:8000/docs](http://localhost:8000/docs).

## Future Improvements

- **Database Normalization:** Improving the database schema to normalize the data structure, which can enhance performance and scalability.

- **Security Enhancements:** Currently, the project utilizes basic security protocols. Future iterations should focus on implementing more robust security measures to ensure data protection and safe user interactions.

- **Testing:** Comprehensive testing for both the APIs and user interface has not been conducted. Implementing automated tests will ensure the reliability and stability of the application.
- **Caching :** Implememation of caching mechanisms would greatly improve the speed of the application

## Support

If you encounter any issues or have questions, please reach out to me on the Slack channel for assistance.

