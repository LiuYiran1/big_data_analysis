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
            "Consistent": [],
        }

    def add_rule(self, dimension: str, rule_func, description: str, cols: list = None):
        """
        添加检查规则
        :param cols:
        :param dimension: 质量维度 ("Accurate", "Complete", "Unique", "Up-to-date", "Consistent")
        :param rule_func: 规则函数，接受df返回布尔Series，True表示该行不符合规则
        :param description: 规则描述
        """
        if dimension not in self.rules:
            raise ValueError(f"未知维度: {dimension}")
        self.rules[dimension].append((rule_func, description, cols))

    def run(self):
        # 执行所有规则，返回一个结果字典
        results = {}
        for dim, checks in self.rules.items():
            dim_results = []
            for func, desc, cols in checks:
                mask = func(self.df)
                bad_data = self.df[mask].copy()

                # 只保留违规列
                # 尝试自动识别列名：如果 lambda 用到了某些列，可以把列名加到 desc 里传进来
                # 这里简单点：找出在描述里提到的列
                if cols:
                    bad_data = bad_data[cols]

                dim_results.append({
                    "rule": desc,
                    "violation_count": mask.sum(),
                    "violations": bad_data
                })
            results[dim] = dim_results
        return results

    def summary(self, results):
        """
        打印检查结果，包括违规详情
        """
        for dim, checks in results.items():
            print(f"\n=== {dim} 检查结果 ===")
            for res in checks:
                print(f"规则: {res['rule']}")
                print(f"不符合行数: {res['violation_count']}")
                if res['violation_count'] > 0:  # 有违规才打印
                    print("违规详情:")
                    print(res['violations'].to_string(index=False))

