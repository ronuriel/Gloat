Algorithm:
The matcher service get a job and returns the best candidates for this job.
Best candidates are defined by title match to the job’s title and/or having the largest number of skill matching to the job’s skills


Instructions:
1. Extract the zip file and reach to the extracted directory in your command line.
2. install Django:  python -m pip install Django
3. Install rest_framework:  pip install djangorestframework
4. Run the server:  python manage.py runserver
5. Open your web browser on this route: http://127.0.0.1:8000/candidate_finder?id=[job_id]

I added my sample SQLite database for testing.
