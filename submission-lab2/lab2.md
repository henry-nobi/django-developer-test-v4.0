# Project Documentation Outline
## Theme
Kadso
[Download Theme](https://www.buzzerboysites.com/html_kits/kadso.zip)

## GitHub Link
- [Project Repository](https://github.com/henry-nobi/django-developer-test-v4.0/blob/main/submission-lab2)

## Environment Setup
Ensure you have Python 3.13.1 installed on your system. You can download it from the [official Python website](https://www.python.org/downloads/release/python-3131/).

## How to Run
1. Clone the repository:
    ```bash
    git clone https://github.com/henry-nobi/django-developer-test-v4.0.git
    cd submission-lab2
    ```
2. Create a virtual environment and activate it:
    ```bash
    python -m venv venv
    source venv/bin/activate  
    # On Windows use `venv\Scripts\activate`
    ```
3. Install the required dependencies:
    ```bash
    pip install -r requirements.txt
4. Copy the example environment file and modify the configurations as needed:
    ```bash
    cp .env.example .env
    ```
    > **Note**: Contact me to get the `.env` file with the necessary configurations if needed.
5. Apply migrations:
    ```bash
    python manage.py migrate
    ```
    > **Note**: This step is required only for the first time you set up the project or when there are new migrations.

6. Seed the database:
    ```bash
    python manage.py seed_db
    ```
    > **Note**: This step is required only for the first time you set up the project or when you need to reset the database.

7. Run the development server:
    ```bash
    python manage.py runserver 8888
    ```

8. See the result in your browser at [http://localhost:8888](http://localhost:8888)

## How to Compile Language
1. Generate the locale files:
    ```bash
    django-admin makemessages --all --ignore="env/*" --ignore="venv/*" --extension=html,py
    ```
2. Compile the messages:
    ```bash
    django-admin compilemessages -i "locale/*"
    ```
## How to Seed Database
1. Seed the database with initial data:
    ```bash
    python manage.py seed_db
    ```
    > **Note**: You can modify the seeding data in `app/fixtures/initial_data.json`.

## Features

## Test
After seeding the database, you can use the following test account to log in:
- **Email**: system@example.com
- **Password**: @345678

## Demo Video
Watch the demo video to see the application in action: [Demo Video](https://drive.google.com/file/d/1wt-XI1pkIbAZKnVN7kAeph6zZC9KXtYp/view?usp=sharing)

### Order of Demo
1. Login
2. Change Password
3. Change Language
4. Change Profile
5. Logout
6. Reset Password
7. Other UIs
8. Action when not logged in

### Login
- **Title**: User Login
- **Description**: Allows users to log into the system using their email and password.
- **Image**: ![Login](/submission-research2/screenshots/login.png)

### Change Password
- **Title**: Change Password
- **Description**: Allows users to change their current password to a new one.
- **Image**: ![Change Password](/submission-research2/screenshots/change-pwd.png)

### Multilingualism
- **Title**: Multilingual Support
- **Description**: The system supports multiple languages, allowing users to switch between different languages.
- **Image**: ![Multilingual](/submission-research2/screenshots/language.png)

### Change Profile
- **Title**: Change Profile
- **Description**: Allows users to update their profile information including display name, avatar, and default language.
- **Image**: ![Change Profile](/submission-research2/screenshots/change-profile.png)

### Logout
- **Title**: User Logout
- **Description**: Allows users to log out of the system securely.
- **Image**: ![Logout](/submission-research2/screenshots/logout.png)

### Reset Forgotten Password
- **Title**: Reset Forgotten Password
- **Description**: Allows users to reset their password if they have forgotten it by receiving a reset link via email.
- **Image**: ![Reset Password](/submission-research2/screenshots/reset-pwd.png)

### Local IDE Demonstration
- **Title**: Local IDE Demonstration
- **Description**: Shows the application running in a local development environment to demonstrate that it is working as a Django application.
- **Image**: ![Local IDE](/submission-research2/screenshots/local-ide.png)
