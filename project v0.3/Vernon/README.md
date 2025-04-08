# Team Vernon

## COSC 4353 Project

### How to Run the Program

You can run this program using the **Dockerfile**. Follow the steps below to get started.

---

### Step 1: Create the `.env` File

```
CLIENT_ID=eb69d6cc-2944-470e-902e-83b87798b51b
CLIENT_SECRET=Y7y8Q~SbTsxzFAJiv~bgWKatw12XZdPQpPNRWdwV


# Use bellow variables if you are working on localhost. Comment out if using Docker
# DB_HOST=localhost
# DB_PORT=5433
# DB_NAME=postgres
# DB_USER=postgres
# DB_PASSWORD=your_password
```

- Important:

* Uncomment the DB\_ variable if you are working with localhost and update it to match with the database that you are working with

### Step 2: Run docker-compose.yml

run the following command:

```
docker-compose up
```

### Step 3: Access the website

```
http://localhost:5002/
```
