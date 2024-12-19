# Task 2 – Setup Starter Kit and Run on Local Server

## Deliverable 1
1. Setup the starter kit on your local machine.
2. Run the starter kit on your local server.
3. Take a screenshot of the starter kit running on your localhost.
4. In your GitHub repository, create a subdirectory called `/submission-lab1`.
5. Add a file named `Lab1-task1.md` in this directory and attach your screenshot.

## Deliverable 2
1. Provide a link to the GitHub repository where the files are located.
2. In your GitHub repository, create a subdirectory called `/submissionlab1`.
3. Create a file named `lab1-task2.md` in this directory.
4. Attach screenshots for each feature in `lab1-task2.md`.
5. Provide any setup instructions that may be required by the test evaluator.
6. Include a `requirements.txt` file to ensure evaluators can run your code.

## Example Directory Structure
```
submission-lab1/
├── app             # Contains the main application code
├── lab1            # Contains settings, routes and resources
├── static          # Contains static files like CSS, JavaScript, and images
├── templates       # Contains HTML templates for the application
├── venv-lab1       # Virtual environment for the project
├── Lab1-task1.md   # Markdown file for Task 1 deliverables
├── Lab1-task2.md   # Markdown file for Task 2 deliverables
├── requirements.txt # File listing project dependencies
```

## Setup Instructions

1. **Clone the Repository**:
    ```sh
    git clone https://github.com/henry-nobi/django-developer-v4.0
    cd submission-lab1
    ```

2. **Create a Virtual Environment**:
    ```sh
    python3 -m venv venv
    # Linux/Mac OS: 
    source venv/bin/activate  
    # Windows:
    venv\Scripts\activate
    ```

3. **Install Dependencies**:
    ```sh
    pip install -r requirements.txt
    ```
4. **Run the Server**:
    ```sh
    python manage.py runserver
    ```

5. **Access the Application**:
    Open your web browser and go to `http://127.0.0.1:8000/`.

## Screenshot of the starter kit running on localhost

  ![Deliverable 1 - localhost](/submission-lab1/screenshots/lab1-task2-localhost.png)
  
  ![Deliverable 1 - localhost page](/submission-lab1/screenshots/lab1-task2-localhost-page.png)

## Feature Screenshots

- **Feature Home page**:

    ![Feature home page](/submission-lab1/screenshots/lab1-task1.png)
