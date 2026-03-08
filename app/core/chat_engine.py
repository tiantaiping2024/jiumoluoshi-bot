"""
鸠摩罗什Bot 核心对话引擎
"""
import os
from pathlib import Path
from dotenv import load_dotenv
from openai import OpenAI
from app.knowledge import knowledge_base

# 加载环境变量
load_dotenv(Path(__file__).parent.parent / "config" / ".env")

class JiumoChatEngine:
    """对话引擎核心类"""
    
    def __init__(self, api_key: str = None):
        self.client = OpenAI(
            api_key=api_key or os.getenv("DEEPSEEK_API_KEY"),
            base_url="https://api.deepseek.com"
        )
        self.soul_path = Path(__file__).parent.parent / "soul.md"
        self.conversation_history = []
        self.knowledge = knowledge_base
        
    def load_soul(self) -> str:
        """加载人格设定"""
        if self.soul_path.exists():
            return self.soul_path.read_text(encoding="utf-8")
        return ""
    
    def build_system_prompt(self) -> str:
        """构建系统Prompt"""
        soul_content = self.load_soul()
        return f"""你是鸠摩罗什，东晋时期的著名佛经翻译家和高僧。

{soul_content}

请始终以鸠摩罗什大师的身份和语气与用户对话。保持慈悲、智慧、温和的风格。
善用比喻解释佛理，但不强制灌输。

当用户询问佛经、佛教知识相关问题时，可以参考知识库中的内容。"""
    
    def _search_knowledge(self, query: str) -> str:
        """检索知识库"""
        results = self.knowledge.search(query)
        if results:
            context = "\n\n".join([
                f"参考：{r['answer']}"
                for r in results[:2]
            ])
            return context
        return None
    
    def chat(self, user_message: str, use_knowledge: bool = True) -> str:
        """处理用户对话"""
        # 先检索知识库
        knowledge_context = ""
        if use_knowledge:
            kb_answer = self.knowledge.get_answer(user_message)
            if kb_answer:
                knowledge_context = f"\n\n{ kb_answer}\n"
        
        messages = []
        
        # 系统提示
        messages.append({
            "role": "system",
            "content": self.build_system_prompt() + knowledge_context
        })
        
        # 对话历史
        for msg in self.conversation_history[-10:]:
            messages.append(msg)
        
        # 当前消息
        messages.append({
            "role": "user", 
            "content": user_message
        })
        
        # 调用API
        response = self.client.chat.completions.create(
            model="deepseek-chat",
            messages=messages,
            temperature=0.7,
            max_tokens=2000,
            stream=False
        )
        
        assistant_reply = response.choices[0].message.content
        
        # 记录对话历史
        self.conversation_history.append({"role": "user", "content": user_message})
        self.conversation_history.append({"role": "assistant", "content": assistant_reply})
        
        return assistant_reply
    
    def clear_history(self):
        """清空对话历史"""
        self.conversation_history = []


# 导出单例
chat_engine = JiumoChatEngine()
