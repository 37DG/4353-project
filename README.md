# Team Nelson
-----------------------------------------
Here is the demo for our project

[![Watch the video](https://img.youtube.com/vi/yQ2K8-CZ75A/0.jpg)](https://www.youtube.com/watch?v=yQ2K8-CZ75A)

-----------------------------------------
# Folder Purpose
project v0.2: This is the folder contains necessary assets for implementation of project v0.2 if you want to run on Docker.

project v0.3: This is the folder contains our codes and Vernon's(closest city to Nelson) code for implementation of project v0.3 if you want to run on Docker.

project v0.4: This is the folder contains necessary assets for implementation of project v0.4 if you want to run on Docker

software design project2.0: Self use only.

-----------------------------------------
Instruction for project v0.2.

In order to run it on docker
Docker Compose setup
1. In a terminal, navigate to BASE_DIR/project v0.2/project v0.2 with docker/
2. Create a .env file based on .env.example. Ensure all variables are filled.
3. Type 'docker compose up' in the terminal
4. The website should be accessible from URI:8000

NOTE: If any changes are made involving the database (like MYSQL_ROOT_PASSWORD), use 'docker compose down --volumes' then 'docker compose up'.

----------------------------------------

Instruction for project v0.3.

How to run:

1. Clone the repository. The project MUST be run on a local Docker. Github Codespaces or similar cloud systems are not supported.
2. Modify .env if necessary. Do not touch .env files or other configurations located further in the project and Vernon folders.
3. Type 'docker compose up' in a terminal located in this folder. This will load 4 containers: Nelson, Vernon, MySQL, and PostgreSQL.
4. If no errors occur, the website should be accessible from http://localhost:8000
   
NOTE: If any changes are made involving the database (like MYSQL_ROOT_PASSWORD), use 'docker compose down --volumes' then 'docker compose up'.

----------------------------------------

Instruction for project v0.4. (same as project v0.3)

How to run:

1. Clone the repository. The project MUST be run on a local Docker. Github Codespaces or similar cloud systems are not supported.
2. Modify .env if necessary. Do not touch .env files or other configurations located further in the project and Vernon folders.
3. Type 'docker compose up' in a terminal located in this folder. This will load 4 containers: Nelson, Vernon, MySQL, and PostgreSQL.
4. If no errors occur, the website should be accessible from http://localhost:8000
   
NOTE: If any changes are made involving the database (like MYSQL_ROOT_PASSWORD), use 'docker compose down --volumes' then 'docker compose up'.
