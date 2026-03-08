"""
对话历史记忆模块
使用简单的文件存储实现跨会话记忆
"""
import json
import os
from pathlib import Path
from datetime import datetime

class ConversationMemory:
    """对话记忆系统"""
    
    def __init__(self, storage_path: str = None):
        self.storage_path = Path(storage_path or Path(__file__).parent.parent / "data" / "memories")
        self.storage_path.mkdir(parents=True, exist_ok=True)
        
    def _get_memory_file(self, session_id: str) -> Path:
        """获取会话记忆文件"""
        return self.storage_path / f"{session_id}.json"
    
    def save_message(self, session_id: str, role: str, content: str):
        """保存单条消息"""
        memory_file = self._get_memory_file(session_id)
        
        # 读取现有记忆
        if memory_file.exists():
            memories = json.loads(memory_file.read_text(encoding="utf-8"))
        else:
            memories = {"session_id": session_id, "messages": [], "created_at": datetime.now().isoformat()}
        
        # 添加新消息
        memories["messages"].append({
            "role": role,
            "content": content,
            "timestamp": datetime.now().isoformat()
        })
        
        # 限制保存的消息数量
        memories["messages"] = memories["messages"][-50:]
        
        # 写入文件
        memory_file.write_text(json.dumps(memories, ensure_ascii=False, indent=2), encoding="utf-8")
    
    def get_history(self, session_id: str, limit: int = 10) -> list:
        """获取会话历史"""
        memory_file = self._get_memory_file(session_id)
        
        if not memory_file.exists():
            return []
        
        memories = json.loads(memory_file.read_text(encoding="utf-8"))
        return memories["messages"][-limit:]
    
    def get_summary(self, session_id: str) -> str:
        """获取会话摘要"""
        messages = self.get_history(session_id, limit=20)
        
        if not messages:
            return ""
        
        # 简单摘要：提取用户问题的关键词
        topics = []
        for msg in messages:
            if msg["role"] == "user":
                # 简单处理：取前20个字符作为摘要
                topic = msg["content"][:30] + "..." if len(msg["content"]) > 30 else msg["content"]
                topics.append(topic)
        
        return "; ".join(topics[-5:])
    
    def clear(self, session_id: str):
        """清空会话记忆"""
        memory_file = self._get_memory_file(session_id)
        if memory_file.exists():
            memory_file.unlink()
    
    def add_user_profile(self, session_id: str, key: str, value: str):
        """记录用户画像信息"""
        memory_file = self._get_memory_file(session_id)
        
        if memory_file.exists():
            memories = json.loads(memory_file.read_text(encoding="utf-8"))
        else:
            memories = {"session_id": session_id, "messages": [], "profile": {}}
        
        if "profile" not in memories:
            memories["profile"] = {}
        
        memories["profile"][key] = value
        memory_file.write_text(json.dumps(memories, ensure_ascii=False, indent=2), encoding="utf-8")
    
    def get_profile(self, session_id: str) -> dict:
        """获取用户画像"""
        memory_file = self._get_memory_file(session_id)
        
        if not memory_file.exists():
            return {}
        
        memories = json.loads(memory_file.read_text(encoding="utf-8"))
        return memories.get("profile", {})


# 导出单例
memory = ConversationMemory()
