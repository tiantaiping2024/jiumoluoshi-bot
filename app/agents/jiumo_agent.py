"""
鸠摩罗什 Agent - 简化版
支持本地 vLLM（优先）+ 云端 DeepSeek API（备用）
"""
import os
import re
from pathlib import Path
from typing import Optional, List, Dict, Any
import openai
import requests

# 默认配置
DEEPSEEK_API_KEY = "sk-b2bc78855f1b4b21978532f879bc718f"
LOCAL_VLLM_URL = os.getenv("LOCAL_VLLM_URL", "http://localhost:8000")
USE_LOCAL_FIRST = True  # 本地优先


class JiumoAgent:
    """鸠摩罗什 Agent - 简化版"""
    
    def __init__(
        self,
        api_key: str = None,
        model: str = "deepseek-chat",
        base_url: str = "https://api.deepseek.com",
        temperature: float = 0.7
    ):
        # 优先使用参数，然后是环境变量
        self.api_key = api_key or os.getenv("DEEPSEEK_API_KEY", "") or DEEPSEEK_API_KEY
        self.model = model
        self.base_url = base_url
        self.temperature = temperature
        self.local_url = LOCAL_VLLM_URL
        self.use_local_first = USE_LOCAL_FIRST
        
        print(f"Initializing Agent with API key: {self.api_key[:10] if self.api_key else 'None'}...")
        print(f"Local vLLM URL: {self.local_url}")
        
        # 初始化 OpenAI 客户端（云端）
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
    
    def _is_local_vllm_available(self) -> bool:
        """检查本地 vLLM 是否可用"""
        try:
            response = requests.get(f"{self.local_url}/v1/models", timeout=3)
            return response.status_code == 200
        except:
            return False
    
    def _call_local_vllm(self, messages: List[Dict], max_tokens: int = 500) -> str:
        """调用本地 vLLM"""
        try:
            response = requests.post(
                f"{self.local_url}/v1/chat/completions",
                json={
                    "model": "Qwen/Qwen3-14B",
                    "messages": messages,
                    "max_tokens": max_tokens,
                    "temperature": self.temperature
                },
                timeout=60
            )
            if response.status_code == 200:
                data = response.json()
                return data["choices"][0]["message"]["content"]
            else:
                print(f"Local vLLM error: {response.status_code}")
                return None
        except Exception as e:
            print(f"Local vLLM call failed: {e}")
            return None
    
    def _call_cloud_api(self, messages: List[Dict], max_tokens: int = 500) -> str:
        """调用云端 DeepSeek API"""
        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=messages,
                temperature=self.temperature,
                max_tokens=max_tokens
            )
            return response.choices[0].message.content
        except Exception as e:
            print(f"Cloud API error: {e}")
            return None
    
    def chat(self, message: str, session_id: str = "default") -> str:
        """处理对话 - 本地优先，云端备用"""
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
            
            reply = None
            
            # 优先尝试本地 vLLM
            if self.use_local_first:
                if self._is_local_vllm_available():
                    print("Using local vLLM...")
                    reply = self._call_local_vllm(messages)
                else:
                    print("Local vLLM not available, using cloud API...")
            
            # 如果本地失败，尝试云端
            if reply is None:
                print("Using cloud DeepSeek API...")
                reply = self._call_cloud_api(messages)
            
            # 如果云端也失败，返回默认回复
            if reply is None:
                return f"阿弥陀佛，施主所说：{message}。贫衲已记下。"
            
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
