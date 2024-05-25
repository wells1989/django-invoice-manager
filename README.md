## Contents

- [Description](#description)
- [SetUp](#SetUp)
- [UI](#UI)
- [Project Notes](#project-notes)
- [Contributions](#contributions)
- [Licenses](#licenses)

## Description

### Overview
- The Django Invoice Manager is a web application designed to simplify invoice management for freelancers.
- The project was designed around CI / CD, utilising TDD and GitHub actions to securely and quickly build / test the application.
- The application is containerized using Docker, allowing for easy setup and deployment with Docker Compose, and it was also deployed using Google Kubernetes Service in Development

### Features

- Create and Edit Invoices: Easily create new invoices and edit existing ones through a simple and intuitive UI.
- View Invoice and Earnings Statistics: Visualize your earnings by client, month and currency through D3JS charts and graphs.
- Track Payment and Status History: Keep track of payment statuses and history for each invoice to ensure timely payments.
- Save Invoices as PDF: Generate and save invoices in PDF format for easy sharing and record-keeping.

## SetUp
### Prerequisites
- Docker
- Docker Compose

### Installation
- Clone the repository:

```
git clone https://github.com/wells1989/django-invoice-manager.git

cd django-invoice-manager
```

- Copy the example environment file and customize it (as the docker-compose file uses environment variables to set the Postgres database:

```
cp .env.example .env
```
 .env example:

```
DB_NAME=my_database_name
DB_USER=my_database_user
DB_PASSWORD=my_database_password
DB_HOST=localhost
DB_PORT=5432
```
- Docker compose (database migrations included in docker-compose)
```
docker-compose up --build
```

- Create a superuser to access the admin interface:
```
cd mysite

python manage.py createsuperuser
```

- run pytests

```
cd mysite
pytest
```

- Access the application:

    - **UI:** http://localhost:8000
    - **Admin:** http://localhost:8000/admin

## UI
- Viewing your earnings broken down by currency, client and month:

![Screenshot (818)](https://github.com/wells1989/Full-stack-blog/assets/122035759/158764ce-074f-475a-b6e4-dac68a9d3ddd)
![Screenshot (824)](https://github.com/wells1989/Full-stack-blog/assets/122035759/f8e9ec35-0759-408c-8169-5c6e2b639596)

- Editing your freelancer details / login credentials:

![Screenshot (819)](https://github.com/wells1989/Full-stack-blog/assets/122035759/d1dfa53b-b623-40d0-833e-d8b3a604f437)

- Creating a new invoice (with new or existing clients)
![Screenshot (822)](https://github.com/wells1989/Full-stack-blog/assets/122035759/50c7de54-810a-4445-8781-291eb1eaf36d)

- Invoice Management / Editing:

![Screenshot (820)](https://github.com/wells1989/Full-stack-blog/assets/122035759/b6ad0ce9-02bc-4894-a78f-370e821b3eed)

- Viewing payment / status history of invoices:

![Screenshot (823)](https://github.com/wells1989/Full-stack-blog/assets/122035759/c01c26c9-be3f-4d95-9a89-d4d21138790e)

### Project Notes
- To integrate a more automated process regarding application testing and pull / push requests. This was completed using a CI / CD pipeline with pytest and GitHub Action Workflows
- To enable ease of use for a fully functioning Django app Docker was used
- This app was built during a DevOps bootcamp so cloud services (namely Google Cloud) was used to test deployment using the Google Kubernetes Service with Cloud database integration

### Contributions
Contributions / suggestions are welcome! Please follow these steps to contribute:

- Fork the repository.
- Create a new branch (git checkout -b feature/your-feature).
- Make your changes.
- Commit your changes (git commit -m 'Add some feature').
- Push to the branch (git push origin feature/your-feature).
- Open a pull request. (note the GitHub workflow which will automatically run pytest on the code, see /mysite/test/... for test details

### Licenses
This project is licensed under the MIT License. See the LICENSE file for details.
