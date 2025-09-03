import pandas as pd

class QualityAnalTool:
    def __init__(self, df: pd.DataFrame):
        # 从5个维度分析数据
        self.df = df
        self.rules = {
            "Accurate": [], # [(rule_func, description), ...]
            "Complete": [],
            "Unique": [],
            "Up-to-date": [],
            "Consistent": []
        }

    def add_rule(self, dimension: str, rule_func, description: str):
        """
        添加检查规则
        :param dimension: 质量维度 ("Accurate", "Complete", "Unique", "Up-to-date", "Consistent")
        :param rule_func: 规则函数，接受df返回布尔Series，True表示该行不符合规则
        :param description: 规则描述
        """
        if dimension not in self.rules:
            raise ValueError(f"未知维度: {dimension}")
        self.rules[dimension].append((rule_func, description))

    def run(self):
        # 执行所有规则，返回一个结果字典
        results = {}
        for dim, checks in self.rules.items():
            dim_results = []
            for func, desc in checks:
                mask = func(self.df)
                bad_data = self.df[mask]
                dim_results.append({
                    "rule": desc,
                    "violation_count": mask.sum(),
                    "violations": bad_data
                })
            results[dim] = dim_results
        return results

    def summary(self, results):
        """
        简要打印检查结果
        """
        for dim, checks in results.items():
            print(f"\n=== {dim} 检查结果 ===")
            for res in checks:
                print(f"规则: {res['rule']}")
                print(f"不符合行数: {res['violation_count']}")
