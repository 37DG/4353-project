# Team Nelson

-----------------------------------------
In order to run it on docker
Docker Compose setup
1. In a terminal, navigate to BASE_DIR/project v0.2/project v0.2 with docker/
2. Create a .env file based on .env.example. Ensure all variables are filled.
3. Type 'docker compose up' in the terminal
4. The website should be accessible from URI:8000

NOTE: If any changes are made involving the database (like MYSQL_ROOT_PASSWORD), use 'docker compose down --volumes' then 'docker compose up'.
