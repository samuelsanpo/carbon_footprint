# carbon_footprint
Carbon Footprint is a platform developed in Python language, in technical terms it has a 
backend service developed with the Flask library and an interactive frontend developed with 
the help of the streamlit library, the information is being saved in a JSON file. The platform 
has a start section that will then guide the organizations to take a form where they can, with a 
few simple questions, determine the carbon footprint your organization is generating, the data will be 
saved and reported so that the user can easily access it later in  the reports area, the user also has 
an analysis area where they can see their results compared to other organizations that have saved their record. 


To execute the project, just follow these steps.
Before starting, verify that you have Python installed on your computer.

1) Create environment for backend 

a. Locate the project folder in the console and with the cd command, move to backend.
   -cd backend
b. Install the virtual environment.

    -For Mac OS /Linux
    python3 -m venv env

    -For Windows
    python -m venv env

c.Activate the environment

    -For Mac OS /Linux
    source env/bin/activate

    -For Windows
    env\Scripts\activate

d.Install the libraries listed in the requirements file.
    pip install -r requirements.txt

e. Run the project it will run automatically on port 5000
    python app.py


2)Create environmet for frontend

a. Locate the project folder in the console and with the cd command, move to frontend.
   -cd frontend
b. Install the virtual environment.

    -For Mac OS /Linux
    python3 -m venv env

    -For Windows
    python -m venv env

c.Activate the environment

    -For Mac OS /Linux
    source env/bin/activate

    -For Windows
    env\Scripts\activate

d.Install the libraries listed in the requirements file.
    pip install -r requirements.txt

e. Run the project.
    streamlit run app.py





In case you have any problems with the libraries, these are the libraries used in each project.

----frontend
pip install streamlit
pip install streamlit-extras
pip install panda
pip install matpilob

--backend
pip install flask
pip install fpdf

