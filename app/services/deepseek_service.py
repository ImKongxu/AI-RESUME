import os
from openai import OpenAI
import asyncio

class DeepSeekService:
    def __init__(self):
        """初始化DeepSeek API客户端"""
        # 从环境变量获取API密钥
        api_key = os.environ.get('DEEPSEEK_API_KEY')
        if not api_key:
            raise ValueError("未设置DEEPSEEK_API_KEY环境变量")
            
        self.client = OpenAI(
            api_key=api_key,
            base_url="https://api.deepseek.com"
        )
        # 定义默认的系统提示词，统一要求Markdown格式
        self.default_system_prompt = "你是一个经验丰富的简历助手，擅长根据用户输入生成专业的简历，用户将给你他们的个人信息，以及工作经验，参赛经历等，你将使用这些信息生成一份对于需求的简历，请直接以Markdown格式返回，不添加其他任何语句"
        self.revise_system_prompt = "你是一名专业的简历编辑，根据用户的修改要求优化现有简历内容，请直接返回Markdown格式的优化后内容，不添加其他任何语句"
    
    def send_message(self, message, system_prompt=None):
        """
        发送消息到DeepSeek API并获取响应
        
        参数:
            message (str): 用户要发送的消息内容
            system_prompt (str): 系统提示词，指导AI的行为
                                    
        返回:
            str: AI生成的Markdown格式响应内容
        """
        # 如果没有提供系统提示词，则使用默认的
        if system_prompt is None:
            system_prompt = self.default_system_prompt
        
        response = self.client.chat.completions.create(
            model="deepseek-chat",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": message},
            ],
            stream=False
        )
        return response.choices[0].message.content
    
    async def send_message_async(self, message, system_prompt=None):
        """
        异步发送消息到DeepSeek API并获取响应
        
        参数:
            message (str): 用户要发送的消息内容
            system_prompt (str): 系统提示词，指导AI的行为
                                    
        返回:
            str: AI生成的Markdown格式响应内容
        """
        # 如果没有提供系统提示词，则使用默认的
        if system_prompt is None:
            system_prompt = self.default_system_prompt
            
        # 使用线程池执行同步调用，避免阻塞事件循环
        loop = asyncio.get_event_loop()
        return await loop.run_in_executor(
            None,  # 使用默认线程池
            self.send_message,  # 要执行的同步函数
            message,  # 函数参数
            system_prompt  # 函数参数
        )