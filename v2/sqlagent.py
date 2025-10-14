from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import JsonOutputParser
from databasemanager import DatabaseManager
from llm_manager import LLMManager

class SQLAgent:
    def __init__(self):
        self.db_manager = DatabaseManager()
        self.llm_manager = LLMManager()

    def parse_question(self, state: dict) -> dict:
        """Parse user question and identify relevant tables and columns."""
        question = state['question']
        schema = self.db_manager.get_schema()

        prompt = ChatPromptTemplate.from_messages([
            ("system", '''You are a data analyst that can help summarize SQL tables and parse user questions about a database. 
                Given the question and database schema, identify the relevant tables and columns. 
                If the question is not relevant to the database or if there is not enough information to answer the question, set is_relevant to false.

                Your response should be in the following JSON format:
                {{
                    "is_relevant": boolean,
                    "relevant_tables": [
                        {{
                            "table_name": string,
                            "columns": [string],
                            "noun_columns": [string]
                        }}
                    ]
                }}
                '''),
                            ("human", "===Database schema:\n{schema}\n\n===User question:\n{question}\n\nIdentify relevant tables and columns:")
        ])

        output_parser = JsonOutputParser()
        print(schema)
        response = self.llm_manager.invoke(prompt, schema=schema, question=question)
        parsed_response = output_parser.parse(response)
        return {"parsed_question": parsed_response}

    def get_unique_nouns(self, state: dict) -> dict:
        """Find unique nouns in relevant tables and columns."""
        parsed_question = state['parsed_question']
        print(parsed_question)
        if not parsed_question['is_relevant']:
            return {"unique_nouns": []}

        unique_nouns = set()
        for table_info in parsed_question['relevant_tables']:
            table_name = table_info['table_name']
            noun_columns = table_info['noun_columns']
            
            if noun_columns:
                column_names = ', '.join(f"`{col}`" for col in noun_columns)
                query = f"SELECT DISTINCT {column_names} FROM `{table_name}`"
                results = self.db_manager.execute_query(query)
                for row in results:
                    unique_nouns.update(str(value) for value in row if value)

        return {"unique_nouns": list(unique_nouns)}

    def generate_sql(self, state: dict) -> dict:
        """Generate SQL query based on parsed question and unique nouns."""
        question = state['question']
        # parsed_question = state['parsed_question']
        # unique_nouns = state['unique_nouns']

        # if not parsed_question['is_relevant']:
        #     return {"sql_query": "NOT_RELEVANT", "is_relevant": False}
        print("HITTING SCHEMA")
        schema = self.db_manager.get_schema()
        print(schema==None)
        prompt = ChatPromptTemplate.from_messages([
            ("system", '''
                You are an AI assistant that generates SQL queries based on user questions and database schema. Generate a valid SQL query to answer the user's question.
                
                the lab_seg table contains data where each row is a unique assay laboratory combination. 
                Data such as market share, turn around time, and other columns some of which are prefixed by LAB LEVEL are the same for all instances of the same lab. 
                Other columns pertain to the individual assays each lab offers. Be sure to check that data is not duplicated at the lab level when returning certain results.

                If there is not enough information to write a SQL query, respond with "NOT_ENOUGH_INFO".


                THE RESULTS SHOULD ONLY BE IN THE FOLLOWING FORMAT, SO MAKE SURE TO ONLY GIVE TWO OR THREE COLUMNS:
                [[x, y]]
                or 
                [[label, x, y]]
                            
                For questions like "plot a distribution of the fares for men and women", count the frequency of each fare and plot it. The x axis should be the fare and the y axis should be the count of people who paid that fare.
                SKIP ALL ROWS WHERE ANY COLUMN IS NULL or "N/A" or "".
                Just give the query string. Do not format it. Make sure to use the correct spellings of nouns as provided in the unique nouns list. All the table and column names should be enclosed in backticks.
                
                If the question involves a more than 1 nested query or involves transforming the data beyond basic aggregations then this questions is out of scope for this application and repond with "EXPERT_REDIRECT"
                If the question asks for a strategic recommendation the question is out of scope for this application and repond with "EXPERT_REDIRECT"
                '''),
                            ("human", '''===Database schema:
                {schema}

                ===User question:
                {question}

                Generate SQL query string'''),
        ])

        response = self.llm_manager.invoke(prompt, schema=schema, question=question) #parsed_question=parsed_question, unique_nouns=unique_nouns)
        
        if response.strip() == "NOT_ENOUGH_INFO":
            return {"sql_query": "NOT_RELEVANT"}
        elif response.strip() == "EXPERT_REDIRECT":
            return {"sql_query": "EXPERT_REDIRECT"}
        else:
            return {"sql_query": response}

    def validate_and_fix_sql(self, state: dict) -> dict:
        """Validate and fix the generated SQL query."""
        sql_query = state['sql_query']

        if sql_query == "NOT_RELEVANT":
            return {"sql_query": "NOT_RELEVANT", "sql_valid": False}
        elif sql_query == "EXPERT_REDIRECT":
            return {"sql_query": "EXPERT_REDIRECT", "sql_valid": None}
        
        schema = self.db_manager.get_schema()

        prompt = ChatPromptTemplate.from_messages([
            ("system", '''
You are an AI assistant that validates and fixes SQL queries. Your task is to:
1. Check if the SQL query is valid.
2. Ensure all table and column names are correctly spelled and exist in the schema. All the table and column names should be enclosed in backticks.
3. If there are any issues, fix them and provide the corrected SQL query.
4. If no issues are found, return the original query.

Respond in JSON format with the following structure. Only respond with the JSON:
{{
    "valid": boolean,
    "issues": string or null,
    "corrected_query": string
}}
'''),
            ("human", '''===Database schema:
{schema}

===Generated SQL query:
{sql_query}

Respond in JSON format with the following structure. Only respond with the JSON:
{{
    "valid": boolean,
    "issues": string or null,
    "corrected_query": string
}}

For example:
1. {{
    "valid": true,
    "issues": null,
    "corrected_query": "None"
}}
             
2. {{
    "valid": false,
    "issues": "Column USERS does not exist",
    "corrected_query": "SELECT * FROM \`users\` WHERE age > 25"
}}

3. {{
    "valid": false,
    "issues": "Column names and table names should be enclosed in backticks if they contain spaces or special characters",
    "corrected_query": "SELECT * FROM \`gross income\` WHERE \`age\` > 25"
}}
             
'''),
        ])

        output_parser = JsonOutputParser()
        response = self.llm_manager.invoke(prompt, schema=schema, sql_query=sql_query)
        result = output_parser.parse(response)

        if result["valid"] and result["issues"] is None:
            return {"sql_query": sql_query, "sql_valid": True}
        else:
            return {
                "sql_query": result["corrected_query"],
                "sql_valid": result["valid"],
                "sql_issues": result["issues"]
            }

    def execute_sql(self, state: dict) -> dict:
        """Execute SQL query and return results."""
        query = state['sql_query']
        print("EXECUTING")
        print(query)
        if query == "NOT_RELEVANT":
            return {"results": "NOT_RELEVANT"}
        elif query == "EXPERT_REDIRECT":
            return {"results": "EXPERT_REDIRECT"}

        try:
            results = self.db_manager.execute_query(query)
            print("RESULTS")
            print(results)
            return {"results": results}
        except Exception as e:
            return {"error": str(e)}

    def format_results(self, state: dict) -> dict:
        """Format query results into a human-readable response."""
        question = state['question']
        results = state['results']

        if results == "NOT_RELEVANT":
            return {"answer": "Sorry, I can only give answers relevant to the database."}
        if results == "EXPERT_REDIRECT":
            return {"answer": "This is a complicated question, please reach out to your ISC for assistance."}
            #TODO make it so it will automatically send an alter or email to the ISC for the project 

        prompt = ChatPromptTemplate.from_messages([
            ("system", "You are an AI assistant that formats database query results into a human-readable response. Give a conclusion to the user's question based on the query results. Do not give the answer in markdown format. Only give the answer in one line."),
            ("human", "User question: {question}\n\nQuery results: {results}\n\nFormatted response:"),
        ])

        response = self.llm_manager.invoke(prompt, question=question, results=results)
        return {"answer": response}

    def choose_visualization(self, state: dict) -> dict:
        """Choose an appropriate visualization for the data."""
        question = state['question']
        results = state['results']
        sql_query = state['sql_query']

        if results == "NOT_RELEVANT":
            return {"visualization": "none", "visualization_reasoning": "No visualization needed for irrelevant questions."}
        if results == "EXPERT_REDIRECT":
            return {"visualization": "none", "visualization_reasoning": "Question requires ISC assistance."}

        prompt = ChatPromptTemplate.from_messages([
            ("system", '''
                You are an AI assistant that recommends appropriate data visualizations. Based on the user's question, SQL query, and query results, suggest the most suitable type of graph or chart to visualize the data. If no visualization is appropriate, indicate that.

                Available chart types and their use cases:
                - Bar Graphs: Best for comparing categorical data or showing changes over time when categories are discrete and the number of categories is more than 2. Use for questions like "What are the sales figures for each product?" or "How does the population of cities compare? or "What percentage of each city is male?"
                - Horizontal Bar Graphs: Best for comparing categorical data or showing changes over time when the number of categories is small or the disparity between categories is large. Use for questions like "Show the revenue of A and B?" or "How does the population of 2 cities compare?" or "How many men and women got promoted?" or "What percentage of men and what percentage of women got promoted?" when the disparity between categories is large.
                - Scatter Plots: Useful for identifying relationships or correlations between two numerical variables or plotting distributions of data. Best used when both x axis and y axis are continuous. Use for questions like "Plot a distribution of the fares (where the x axis is the fare and the y axis is the count of people who paid that fare)" or "Is there a relationship between advertising spend and sales?" or "How do height and weight correlate in the dataset? Do not use it for questions that do not have a continuous x axis."
                - Pie Charts: Ideal for showing proportions or percentages within a whole. Use for questions like "What is the market share distribution among different companies?" or "What percentage of the total revenue comes from each product?"
                - Line Graphs: Best for showing trends and distributionsover time. Best used when both x axis and y axis are continuous. Used for questions like "How have website visits changed over the year?" or "What is the trend in temperature over the past decade?". Do not use it for questions that do not have a continuous x axis or a time based x axis.

                Consider these types of questions when recommending a visualization:
                1. Aggregations and Summarizations (e.g., "What is the average revenue by month?" - Line Graph)
                2. Comparisons (e.g., "Compare the sales figures of Product A and Product B over the last year." - Line or Column Graph)
                3. Plotting Distributions (e.g., "Plot a distribution of the age of users" - Scatter Plot)
                4. Trends Over Time (e.g., "What is the trend in the number of active users over the past year?" - Line Graph)
                5. Proportions (e.g., "What is the market share of the products?" - Pie Chart)
                6. Correlations (e.g., "Is there a correlation between marketing spend and revenue?" - Scatter Plot)

                Provide your response in the following format:
                Recommended Visualization: [Chart type or "None"]. ONLY use the following names: bar, horizontal_bar, line, pie, scatter, none
                Reason: [Brief explanation for your recommendation]

            '''),
            ("human", '''
        User question: {question}
        SQL query: {sql_query}
        Query results: {results}

        Recommend a visualization:'''),
        ])

        response = self.llm_manager.invoke(prompt, question=question, sql_query=sql_query, results=results)
        
        lines = response.split('\n')
        visualization = lines[0].split(': ')[1]
        reason = lines[1].split(': ')[1]

        #print(lines)
        print(visualization)
        print(reason)

        return {"visualization": visualization, "visualization_reason": reason}
    
    