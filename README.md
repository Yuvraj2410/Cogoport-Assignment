# Cogoport-Assignment
 
# Configuration Management System API

## Overview

This project is a robust and scalable FastAPI application designed to manage a Configuration Management System for onboarding organizations from different countries. The API supports CRUD (Create, Read, Update, Delete) operations for managing country-specific configurations.

## Features

1. **CRUD Operations**: Provides endpoints to create, read, update, and delete configurations.
2. **Data Validation**: Utilizes Pydantic models for request and response validation.
3. **Error Handling**: Implements comprehensive error handling using FastAPI's exception mechanisms.
4. **Database Integration**: Uses PostgreSQL as the database with SQLAlchemy ORM for data persistence.
5. **Security**: Database connection details are managed using environment variables.

## Getting Started

### Prerequisites

- Python 3.7+
- PostgreSQL

### Installation

1. **Clone the repository**:
    ```sh
    git clone https://github.com/yourusername/configuration-management-system.git
    cd configuration-management-system
    ```

2. **Install dependencies**:
    ```sh
    pip install -r requirements.txt
    ```

3. **Set up environment variables**:
    Create a `.env` file in the root directory and add your database URL.
    ```
    DATABASE_URL=postgresql://user:password@localhost/dbname
    ```

4. **Run the application**:
    ```sh
    uvicorn main:app --reload
    ```

##Comments and Docstrings
The code includes comments and docstrings to explain its purpose and behavior. Environment variables are used for database connection details to enhance security and flexibility.
