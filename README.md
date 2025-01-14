1. Create env
    * `python -m venv modules`

2. Activate env [From cmd in windows]
    * `modules\Scripts\activate`

3. Activate env [From MAC or linux]
    * `source modules/bin/activate`
4. Install dep
    * `pip install -r requirements.txt`

5. Run in local
    * `uvicorn main:app --reload`
    * `uvicorn main:app --reload --port 8001` 

6. Deactivate env
    * `deactivate`


