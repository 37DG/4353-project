How to run:

1. Clone the repository. The project MUST be run on a local system. Github Codespaces or similar cloud systems are not supported.
2. Modify .env if necessary. Do not touch .env files or other configurations located further in the project and Vernon folders.
3. Type 'docker compose up' in a terminal located in this folder. This will load 4 containers: Nelson, Vernon, MySQL, and PostgreSQL.
4. If no errors occur, the website should be accessible from http://localhost:8000

NOTE: If any changes are made involving the database (like MYSQL_ROOT_PASSWORD), use 'docker compose down --volumes' then 'docker compose up'.
