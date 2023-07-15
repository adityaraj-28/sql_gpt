from langchain import OpenAI, SQLDatabase, SQLDatabaseChain, PromptTemplate

from service.mysql import MySQL


class FoduService:
    def __init__(self):
        self.db = SQLDatabase.from_uri("mysql+pymysql://root:root@127.0.0.1/hackathon")
        self.llm = OpenAI(temperature=0, verbose=True)
        self.db_chain = SQLDatabaseChain.from_llm(self.llm, self.db, verbose=True, return_intermediate_steps=True)
        self.default_queries = [
            "select `Investment Industry Preference`, `Investment Stage Preference`, `Investment Geography Preference`, `Sign Up Status`, `App Version`, `Is Chrome Extension Adopted`, `Last Desktop Session Date`, `Last Mobile Session Date` from user_meta_data where `User Name` collate utf8mb4_general_ci = '{user_name}' and `Organization Name` collate utf8mb4_general_ci = '{org_name}'",
            """
                SELECT uud.`Number of Lists Owned` as nolw, uud.`Number of Screeners Owned` as noso
FROM `user_meta_data` umd
JOIN `user_usage_data` uud ON umd.`User ID` = uud.`User ID`
WHERE umd.`User Name` collate utf8mb4_general_ci = '{user_name}' AND umd.`Organization Name` collate utf8mb4_general_ci = '{org_name}';
            """


        ]


    def generate_result(self, query):
        result = self.db_chain(query)
        imt_steps = result['intermediate_steps']
        sql_query = imt_steps[1]
        sql_result = imt_steps[3]
        answer = imt_steps[5]
        return {
            "SQLQuery": sql_query,
            "SQLResult": sql_result,
            "Answer": answer
        }

    def generate_summary(self, user_name, org_name):
        res = []
        index = 1
        for query in self.default_queries:
            dct = MySQL().execute(index, query.format(user_name=user_name, org_name=org_name))
            if dct is None:
                return []
            if index == 1:
                res.extend(self.convert1(dct, user_name, org_name))
            elif index == 2:
                res.extend(self.convert2(dct))
            index = index + 1
        return res

    def convert1(self, dct, user_name, org_name):
        s1 = "{} from {} has Investment Industry Preference {}, Investment Stage Preference {} and Investment Geography Preference {}".format(user_name, org_name, dct["Investment Industry Preference"], dct["Investment Stage Preference"], dct["Investment Geography Preference"])
        c1 = "signed"
        if dct["Sign Up Status"] == "Not signed up":
            c1 = "not signed"
        c2 = "app not"
        if dct["App Version"] != "App not installed":
            c2 = "app version " + dct["App Version"]
        c3 = "adopted"
        if dct["Is Chrome Extension Adopted"] == 'Yes':
            c3 = "not adopted"
        s2 = "User has {} on platform, has {} installed and chrome extension is {}".format(c1, c2, c3)
        s3 = "User's last desktop session is {} and last mobile session is {}".format(dct["Last Desktop Session Date"], dct["Last Mobile Session Date"])
        return [s1, s2, s3]

    def convert2(self, dct):
        return ["User has {} lists and {} screeners".format(dct['nolw'], dct['noso'])]

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
