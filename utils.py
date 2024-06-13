from langchain_community.llms import Tongyi
import os
from langchain_experimental.agents.agent_toolkits import  create_pandas_dataframe_agent
import json
PROMPT_TEMPLATE = """
你是一位数据分析助手，你的回应内容取决于用户的请求内容。

1. 对于文字回答的问题，按照这样的格式回答：
   {"answer": "<你的答案写在这里>"}
例如：
   {"answer": "订单量最高的产品ID是'MNWC3-067'"}

2. 如果用户需要一个表格，按照这样的格式回答：
   {"table": {"columns": ["column1", "column2", ...], "data": [[value1, value2, ...], [value1, value2, ...], ...]}}

3. 如果用户的请求适合返回条形图，按照这样的格式回答：
   {"bar": {"columns": ["A", "B", "C", ...], "data": [34, 21, 91, ...]}}

4. 如果用户的请求适合返回折线图，按照这样的格式回答：
   {"line": {"columns": ["A", "B", "C", ...], "data": [34, 21, 91, ...]}}

5. 如果用户的请求适合返回散点图，按照这样的格式回答：
   {"scatter": {"columns": ["A", "B", "C", ...], "data": [34, 21, 91, ...]}}
注意：我们只支持三种类型的图表："bar", "line" 和 "scatter"。


请将所有输出作为JSON字符串返回。请注意不要省略任何数据，并且要将"columns"列表和数据列表中的所有字符串都用双引号包围。
只需要按照求返回数据，不需要在对话中绘制图形。
例如：{"columns": ["Products", "Orders"], "data": [["32085Lip", 245], ["76439Eye", 178]]}

你要处理的用户请求如下： 
"""
def dataframe_agent(api_key,df,query):
    # 设置 API-KEY
    os.environ["DASHSCOPE_API_KEY"] = api_key
    # 使用 Tongyi LLM，并设置温度
    llm = Tongyi(temperature=0)
    agent=create_pandas_dataframe_agent(llm=llm,
                     df=df,
                     agent_executor_kwargs={"handle_parsing_errors":True},
                     verbose=True)
    prompt=PROMPT_TEMPLATE+query
    response=agent.invoke({"input":prompt})
    print("打印返回结果1")
    print(response)
    response_dict=json.loads(response["output"])
    print("打印返回结果2")
    print(response)
    return response_dict

# import pandas as pd
# df=pd.read_csv("personal_data.csv")
# print(dataframe_agent(os.getenv("DASHSCOPE_API_KEY"),df,"数据里出现最多的职业是什么？"))

