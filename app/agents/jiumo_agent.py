"""
鸠摩罗什 Agent - 简化版
使用 OpenAI API 直接调用 DeepSeek
"""
import os
import re
from pathlib import Path
from typing import Optional, List, Dict, Any
from dotenv import load_dotenv
import openai

# 加载环境变量
load_dotenv(Path(__file__).parent.parent.parent / "config" / ".env")


class JiumoAgent:
    """鸠摩罗什 Agent - 简化版"""
    
    def __init__(
        self,
        api_key: str = None,
        model: str = "deepseek-chat",
        base_url: str = "https://api.deepseek.com",
        temperature: float = 0.7
    ):
        self.api_key = api_key or os.getenv("DEEPSEEK_API_KEY")
        self.model = model
        self.base_url = base_url
        self.temperature = temperature
        
        # 初始化 OpenAI 客户端
        self.client = openai.OpenAI(
            api_key=self.api_key,
            base_url=self.base_url
        )
        
        # 加载人格设定
        self.soul = self._load_soul()
        
        # 对话历史
        self.conversation_history: List[Dict[str, str]] = []
        
        # 系统提示
        self.system_prompt = self._build_system_prompt()
        
    def _load_soul(self) -> str:
        """加载人格设定"""
        soul_path = Path(__file__).parent.parent.parent / "soul.md"
        if soul_path.exists():
            return soul_path.read_text(encoding="utf-8")
        return ""
    
    def _build_system_prompt(self) -> str:
        """构建系统提示"""
        return f"""你是鸠摩罗什，一位东晋时期的高僧，佛经翻译家。你应该用佛教哲学回答问题，但不要过于死板。

人格设定：
{self.soul}

回答要求：
1. 保持禅意、平和的语气
2. 适当引用佛教经典
3. 回答要简洁有智慧
4. 可以用比喻和故事说明道理
5. 如果用户问的是事实性问题，可以直接回答
6. 不要总是说"阿弥陀佛"，适度使用

你是一位德高望重的高僧，回答问题要有深度和智慧。"""
    
    def chat(self, message: str, session_id: str = "default") -> str:
        """处理对话"""
        try:
            # 构建消息
            messages = [
                {"role": "system", "content": self.system_prompt}
            ]
            
            # 添加历史记录
            for msg in self.conversation_history[-10:]:
                messages.append(msg)
            
            # 添加当前消息
            messages.append({"role": "user", "content": message})
            
            # 调用 API
            response = self.client.chat.completions.create(
                model=self.model,
                messages=messages,
                temperature=self.temperature,
                max_tokens=500
            )
            
            reply = response.choices[0].message.content
            
            # 保存对话历史
            self.conversation_history.append({"role": "user", "content": message})
            self.conversation_history.append({"role": "assistant", "content": reply})
            
            return reply
            
        except Exception as e:
            print(f"Chat error: {e}")
            return f"阿弥陀佛，施主所说：{message}。贫衲已记下。"


def create_jiumo_agent():
    """创建 Agent 实例"""
    return JiumoAgent()
