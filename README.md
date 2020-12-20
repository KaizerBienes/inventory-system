# Basic Inventory System

## Description

Basic Inventory System
- Backend and Web front end application that has basic inventory management features
- A user can create, add, edit, delete and view inventory items
- A user can search for inventory items via name

## Technology Used
|__Aspect__|__Technology Used__|
|:---------|:------------------|
|frontend|foundation.js, jQuery|
|backend|Flask (python3), pytest|
|database|SQLite|

## Requirements

|__Prerequisite__|__Download Link__|
|:---------------|:----------------|
|npm|https://nodejs.org/en/download/|
|Python 3|https://www.python.org/downloads/|

## Installation Instructions
Running will be done in two terminals for simplicity instead of runnig behind a web server so we'll need two terminals: one for the backend, and another for the frontend.


1. Clone the repository - `git clone https://github.com/KaizerBienes/inventory-system.git`

##### Backend
2. Go to the flask directory - `cd inventory-system/inventory-flask/`
3. Create a virtual environment - `python3 -m venv venv`
4. Activate the virtual environment - `. venv/bin/activate`
5. Install requirements - `pip3 install -r requirements.txt`
6. (Optional) Run tests - `python -m pytest --verbose`
7. Run the server locally - `source run.sh`

#### Frontend
8. Open another terminal
9. Go to the frontend directory - `cd inventory-system/inventory-foundation/`
10. Install frontend dependencies - `npm install`
11. Run foundation locally - `foundation watch`

## Functionalities
- Create, edit, update, and delete inventory items
- Search inventory items by category name, item name, or item number
- Includes basic tests on the flask application
- Validations on the Flask API endpoints
- Error handling on API request / response
- Validations on the Foundation forms
- Basic API tests

## Improvement suggestions
- Authentication and authorization
- Additional fields
- Unit tests
- Frontend tests
- Use frontend frameworks for maintaining components and impose reusability

## Screenshots
#### Main Inventory Screen
<img src="https://drive.google.com/uc?id=12oA8ffKe32sYoBajuJMwlgtoxCMJD7m9&sz=w500" style="width: 500px; max-width: 100%; height: auto" />

#### Update Inventory Item
<img src="https://drive.google.com/uc?id=1a-x_qTmx685t-q7oUhn0yfFLKV6FQx0s&sz=w500" style="width: 500px; max-width: 100%; height: auto" />
