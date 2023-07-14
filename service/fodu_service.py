from langchain import OpenAI, SQLDatabase, SQLDatabaseChain, PromptTemplate
import json


class FoduService:
    def __init__(self):
        self.db = SQLDatabase.from_uri("mysql+pymysql://root:root@127.0.0.1/hackathon")
        self.llm = OpenAI(temperature=0, verbose=True)
        self.db_chain = SQLDatabaseChain.from_llm(self.llm, self.db, verbose=True, return_intermediate_steps=True)

    def generate_result(self, query):
        # result = self.db_chain(query)
        # imt_steps = result['intermediate_steps']
        # sql_query = imt_steps[1]
        # sql_result = imt_steps[3]
        # answer = imt_steps[5]
        # return {
        #     "SQLQuery": sql_query,
        #     "SQLResult": sql_result,
        #     "Answer": answer
        # }
        return {
            "Answer": "The user id of Ava Miller is 2135.",
            "SQLQuery": "SELECT `User ID` FROM user_meta_data WHERE `User Name` = 'Ava Miller' LIMIT 5;",
            "SQLResult": "[(2135,)]"
        }

    @staticmethod
    def convert_string_to_json(input_string):
        json_obj = {}
        lines = input_string.strip().split('\n')

        for line in lines:
            print('line printed =>' + line)
            if line.startswith('SQLQuery:'):
                query = line[len('SQLQuery:'):].strip()
                json_obj['SQLQuery'] = query
            elif line.startswith('SQLResult:'):
                result = line[len('SQLResult:'):].strip()
                json_obj['SQLResult'] = result
            elif line.startswith('Answer:'):
                answer = line[len('Answer:'):].strip()
                json_obj['Answer'] = answer

        return json_obj
