"""
佛经知识库模块
"""
from pathlib import Path
import json

class BuddhistKnowledgeBase:
    """佛经知识库"""
    
    def __init__(self, data_path: str = None):
        self.data_path = data_path or Path(__file__).parent / "data"
        self.qa_pairs = []
        self._load_data()
    
    def _load_data(self):
        """加载知识数据"""
        # 模拟加载，实际应该从文件/数据库加载
        self.qa_pairs = [
            {
                "question": "什么是金刚经的核心思想？",
                "answer": "金刚经核心思想是「应无所住而生其心」，强调不住相布施，不执着于一切相。佛告须菩提：「凡所有相，皆是虚妄」，教导我们看破表象，回归本性。",
                "source": "金刚经"
            },
            {
                "question": "心经讲的是什么？",
                "answer": "心经全称《般若波罗蜜多心经》，核心讲述「色即是空，空即是色」的般若智慧。观世音菩萨告诉舍利弗：诸法空相，不生不灭，不垢不净，是故空中无色，无受想行识。",
                "source": "心经"
            },
            {
                "question": "鸠摩罗什翻译了哪些佛经？",
                "answer": "鸠摩罗什大师是伟大的佛经翻译家，主要译作包括：《金刚经》、《心经》、《维摩诘经》、《妙法莲华经》、《阿弥陀经》、《楞严经》（部分）等。他的译文优美流畅，影响深远。",
                "source": "佛教历史"
            },
            {
                "question": "什么是空性？",
                "answer": "空性是佛教的核心概念，指一切现象没有独立不变的实体。不是说「什么都没有」，而是说一切事物都是因缘和合而成，没有自性。比如桌子，由木材、铁钉、木工等因缘构成，离开了这些因缘，就没有「桌子」这个实体。",
                "source": "般若学"
            },
            {
                "question": "如何理解诸行无常？",
                "answer": "诸行无常是说一切现象都在不断变化中，没有永恒不变的事物。我们的身体在衰老，念头在流动，四季在更替，国家在兴衰。正是因为无常，一切才有可能改变，修行才能有希望。",
                "source": "三法印"
            },
            {
                "question": "什么是因果报应？",
                "answer": "因果律是佛教的基本法则，种善因得善果，种恶因得恶果。行善积德，现在和未来都会得到好的回报；为非作歹，终将自食其果。但因果不是宿命论，我们可以通过当下的选择改变未来。",
                "source": "因果经"
            },
            {
                "question": "如何开始禅修？",
                "answer": "禅修入门可以从数息观开始：坐端正，专注于呼吸，数出入息从一到十，杂念起时轻轻把注意力带回呼吸。不必追求特殊境界，保持觉知就是修行。每日坚持15-30分钟即可。",
                "source": "禅修指南"
            },
            {
                "question": "什么是慈悲心？",
                "answer": "慈悲心是佛教修行的核心。慈是给予众生快乐，悲是拔除众生痛苦。真正的慈悲没有分别心，对待他人如自己一般。发菩提心就是发起慈悲愿力：「众生度尽，方成正觉」。",
                "source": "大乘佛教"
            }
        ]
    
    def search(self, query: str, top_k: int = 3) -> list:
        """简单关键词搜索"""
        query_lower = query.lower()
        results = []
        
        for qa in self.qa_pairs:
            # 简单匹配：检查问题是否包含查询词
            score = 0
            for word in query_lower.split():
                if word in qa["question"].lower():
                    score += 1
                if word in qa["answer"].lower():
                    score += 0.5
            
            if score > 0:
                results.append((score, qa))
        
        # 按分数排序
        results.sort(key=lambda x: x[0], reverse=True)
        return [qa for _, qa in results[:top_k]]
    
    def get_answer(self, query: str) -> str:
        """获取最佳答案"""
        results = self.search(query)
        if results:
            best = results[0]
            return f"【{best['source']}】\n\n{best['answer']}"
        return None


# 导出单例
knowledge_base = BuddhistKnowledgeBase()
