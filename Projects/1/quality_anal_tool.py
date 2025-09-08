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
                if cols:
                    bad_data = bad_data[cols]

                dim_results.append({
                    "rule": desc,
                    "violation_count": mask.sum(),
                    "violations": bad_data
                })
            results[dim] = dim_results
        return results

    def summary(self, results, outfile: str = None, need_details: bool = False):
        """
        打印或写入检查结果，包括违规详情
        :param results: run() 的返回值
        :param outfile: 可选，文件路径。如果提供则输出到文件
        """
        output_lines = []

        for dim, checks in results.items():
            output_lines.append(f"\n=== {dim} 检查结果 ===")
            for res in checks:
                output_lines.append(f"规则: {res['rule']}")
                output_lines.append(f"不符合行数: {res['violation_count']}")
                if res['violation_count'] > 0 and need_details:
                    output_lines.append("违规详情:")
                    output_lines.append(res['violations'].to_string(index=False))

        # 如果指定了输出文件，就写入文件
        if outfile:
            with open(outfile, "w", encoding="utf-8") as f:
                f.write("\n".join(output_lines))
        else:
            # 默认打印到控制台
            print("\n".join(output_lines))


