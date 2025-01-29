from langchain_openai import ChatOpenAI
from langchain.prompts import ChatPromptTemplate
from rich import print as pprint

import os
import sys
sys.path.append(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'config'))
from config.config import Config
from langchain.prompts import MessagesPlaceholder
from langchain.agents import (AgentExecutor, create_openai_functions_agent)
sys.path.append(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'models'))
from function_handler import available_tools

config = Config(lambda_role='lambda_main')

class LangChainModel:
    """
    LangChainModel - 負責 AI 對話處理，使用 OpenAI GPT 與外部工具提供回應
    """
    def __init__(self):
        """
        初始化 LangChain AI 模型，並加載可用工具
        """
        self.chat_model = ChatOpenAI(model=os.getenv('OPENAI_MODEL_NAME', 'gpt-4o-mini'), api_key=config.OPENAI_API_KEY)
        self.tools = available_tools()

    def get_prompt(self, history_message):
        """
        建立 AI 互動的 Prompt，確保 AI 回應符合球館客服機器人的角色
        :param history_message: 用戶的歷史對話記錄
        :return: ChatPromptTemplate 物件
        """
        if history_message is None:
            history_message = []
        prompt_content = [
            ('system', '你是裕民桌球場專屬客服機器人'),
            ('system', '注意事項:'),
            ('system', '1. 嚴禁回答跟球館資訊不相關的問題'),
            ('system', '2. 確認回覆有完整回答用戶問題，並且回覆有禮貌，但不要過於嚴肅'),
            ('system', '3. 若需回覆金額答案，數字單位為萬或元'),
            ('system', '4. 從funtion取得的數值必須完整、正確、詳細呈現'),
            ('system', '5. 回答結果請用Markdown格式'),
            MessagesPlaceholder(variable_name='agent_scratchpad')] + history_message + [('human', '{input}')]
        return ChatPromptTemplate.from_messages(prompt_content)

    def get_response(self, message, history_message):
        """
        取得 AI 針對用戶訊息的回應
        :param message: 用戶輸入的訊息
        :param history_message: 用戶的聊天歷史
        :return: AI 產生的回應
        """
        prompt = self.get_prompt(history_message)
        agent = create_openai_functions_agent(llm=self.chat_model, tools=self.tools, prompt=prompt)
        agent_executor = AgentExecutor(agent=agent, tools=self.tools, verbose=True)
        
        try:
            response = agent_executor.invoke({
                "input": message,
                "agent_scratchpad": []
            })
            return response['output']

        except Exception as e:
            pprint(f"[red]Error during agent execution: {e}[/red]")
            return "抱歉，目前無法處理您的問題，請稍後再試。"




