# SQL Query Generator with Gemini Pro model

This is a simple demonstration project where we use the Gemini Pro model to generate SQL query code directly from plain english question. The users can access the app and enter their questions, the LLM model will then convert them into SQL code which is used directly to fetch the relevant informations from the database and display them to the users.

## Potential implications and use cases

* **Streamlined Database Interactions**: By leveraging natural language processing capabilities, this project simplifies the process of querying databases, potentially reducing the need for expertise in SQL syntax.
  
* **Enhanced User Experience**: Users without a deep understanding of SQL can interact with databases more intuitively, enabling a broader range of individuals to access and analyze data.

* **Efficiency in Development**: Developers can prototype and iterate on database queries more rapidly, as they can simply express their intentions in plain English rather than writing out complex SQL statements.

* **Use cases**: enhanced reporting capabilities for businesses, efficient data exploration for researchers, integration into interactive dashboards for developers, educational purposes for students,... 

## Limitations

* **Scope of Queries**: The effectiveness of the generated SQL may be limited to certain types of queries or databases. Complex or specialized queries may not be accurately translated from natural language to SQL.

* **Model Accuracy**: The quality of the SQL code generated depends on the accuracy and coverage of the underlying LLM model. Inaccurate or incomplete translations may lead to unexpected results or errors.

* **Security Considerations**: It's ok to use this approach for retrieving informations from the database but it can't be used to add/update the database informations as the generated SQL queries could be wrong (LLMs are not 100% accurate all the time) or have malicious intention (SQL injection attack), a proper validation and sanitization of user input would be necessary to mitigate those risks.

# How to run

* To be able to use the Gemini Pro model you must get an API key from [link](https://ai.google.dev/gemini-api/docs/api-key).

* Clone the repository:

```bash
git clone https://github.com/kaymen99/GenAI-playground.git
cd GenAI-playground/sql-retriever-gemini-pro
```

* Install all the dependencies (you should create a virtual environment first) :

```bash
pip install -r requirements.txt
```

* Create a `.env` file in the root directory and add your Gemini API key as follows:

```ini
GEMINI_APY_KEY="xxxxxxxxxxxxxxxxxxxxxxxxxxxxx"
```

* Start the app by running:

```bash
streamlit run main.py
```

* If you want to create another database, just go to the `database.py` file and change the database structure/data (you can also integrate with an existing database), then you'll need to run .

```bash
python run database.py
```

### Techstack Used:

- Python
- Streamlit
- Gemini Pro model
