"""
鸠摩罗什 Agent - 混合模式: 规则 + AI
"""
import os
import re
from pathlib import Path
from typing import Optional, List, Dict, Any
from dotenv import load_dotenv

# 加载环境变量
load_dotenv(Path(__file__).parent.parent.parent / "config" / ".env")

from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage, AIMessage, SystemMessage
from langchain_core.tools import tool

# 导入工具
from app.tools.search import search_web
from app.tools.weather import get_weather, get_buddhist_calendar
from app.tools.calendar import get_calendar, list_buddhist_holidays

# 导入知识库
from app.knowledge import knowledge_base


class JiumoAgent:
    """鸠摩罗什 Agent - 混合模式"""
    
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
        
        # 初始化 LLM
        self.llm = ChatOpenAI(
            model=self.model,
            api_key=self.api_key,
            base_url=self.base_url,
            temperature=self.temperature
        )
        
        # 加载人格设定
        self.soul = self._load_soul()
        
        # 对话历史
        self.conversation_history: List[Dict[str, str]] = []
        
        # 关键词匹配规则
        self.tool_rules = [
            (["天气", "温度", "下雨", "晴天", "气候"], get_weather, "city"),
            (["佛历", "佛教节日", "佛诞", "浴佛节", "成道日", "盂兰盆", "菩萨圣诞", "出家日", "成道日"], list_buddhist_holidays, None),
            (["日历", "日期", "今天", "明天", "昨天", "星期", "农历"], get_calendar, None),
            (["搜索", "新闻", "最新", "查一下", "请问"], search_web, "query"),
        ]
        
    def _load_soul(self) -> str:
        """加载人格设定"""
        soul_path = Path(__file__).parent.parent.parent / "soul.md"
        if soul_path.exists():
            return soul_path.read_text(encoding="utf-8")
        return ""
    
    def _match_tool(self, query: str):
        """根据关键词匹配工具"""
        query_lower = query.lower()
        
        for keywords, tool_func, param_type in self.tool_rules:
            for kw in keywords:
                if kw in query_lower:
                    # 返回工具函数和参数类型
                    return (tool_func, param_type)
        
        return None
    
    def _get_knowledge_context(self, query: str) -> str:
        """获取知识库上下文"""
        answer = knowledge_base.get_answer(query)
        if answer:
            return f"\n\n【知识库参考】\n{answer}"
        return ""
    
    def chat(self, user_message: str, session_id: str = "default") -> str:
        """处理对话"""
        
        # 1. 先检查是否需要调用工具
        match_result = self._match_tool(user_message)
        
        tool_result = ""
        if match_result:
            tool_func, param_type = match_result
            
            try:
                if param_type == "city":
                    # 需要城市参数，尝试提取
                    tool_result = tool_func.invoke(user_message)
                elif param_type == "query":
                    # 需要搜索关键词
                    tool_result = tool_func.invoke(user_message)
                elif param_type is None:
                    # 不需要参数
                    tool_result = tool_func.invoke({})
                else:
                    tool_result = tool_func.invoke(user_message)
                    
                print(f"[Tool used: {tool_func.name}] {tool_result[:100]}...")
            except Exception as e:
                print(f"[Tool error: {e}]")
                tool_result = f"查询出错: {str(e)}"
        
        # 2. 构建系统提示
        system_prompt = f"""你是鸠摩罗什，东晋时期的著名佛经翻译家和高僧。

{self.soul}

## 行为准则
1. 始终以鸠摩罗什大师的身份和语气与用户对话
2. 保持慈悲、智慧、温和的风格
3. 善用比喻解释佛理，但不强制灌输

"""
        
        # 3. 添加工具结果到上下文
        if tool_result:
            system_prompt += f"\n【查询结果】\n{tool_result}\n\n请基于以上查询结果回答用户。如果查询结果中有相关信息，请优先使用。\n"
        
        # 4. 获取知识库上下文
        knowledge_context = self._get_knowledge_context(user_message)
        if knowledge_context:
            system_prompt += knowledge_context
        
        # 5. 构建消息列表
        messages = [
            SystemMessage(content=system_prompt)
        ]
        
        # 添加历史（最近6轮）
        for msg in self.conversation_history[-6:]:
            if msg["role"] == "user":
                messages.append(HumanMessage(content=msg["content"]))
            else:
                messages.append(AIMessage(content=msg["content"]))
        
        # 添加当前消息
        messages.append(HumanMessage(content=user_message))
        
        # 6. 调用 LLM
        try:
            response = self.llm.invoke(messages)
            assistant_reply = response.content
        except Exception as e:
            print(f"LLM error: {e}")
            # 回退: 直接基于工具结果回答
            if tool_result:
                assistant_reply = tool_result
            else:
                assistant_reply = f"阿弥陀佛，贫僧今日修行略有不适，请施主见谅。"
        
        # 7. 记录历史
        self.conversation_history.append({"role": "user", "content": user_message})
        self.conversation_history.append({"role": "assistant", "content": assistant_reply})
        
        return assistant_reply
    
    def clear_history(self):
        """清空对话历史"""
        self.conversation_history = []


def create_jiumo_agent(api_key: str = None) -> JiumoAgent:
    """创建 Agent 实例"""
    return JiumoAgent(api_key=api_key)
