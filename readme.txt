Python project for Orca Security
================================

Contents of the project:
pythonProject
    |
    |-> data
          |
          |-> input-0.json
              input-1.json
              input-2.json
              input-3.json
              input-4.json
              input-5.json
              input-6.json
    |
    |-> ds
          |
          |-> __init__.py
              lru_cache.py
              queue.py
    |
    |-> logs
    |
    |-> tests
          |
          |-> test_cache.py
              test_model.py
    |
    |-> venv

    main.py
    model.py
    readme.txt


How to run:
    First, change directory to the project folder.

    Then activate the virtual environment by the activate script:
    source ./venv/Scripts/activate

    Then install the requirement by:
    pip install -r requirements.txt

    Finally, run the application using this command:
    python.exe main.py -db <json file name>
    example:
    C:\Users\ghoum\PycharmProjects\pythonProject\venv\Scripts\python.exe C:\Users\ghoum\PycharmProjects\pythonProject\main.py -db data/input-6.json



