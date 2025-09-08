import pandas as pd
from quality_anal_tool import QualityAnalTool

def complete_check(df: pd.DataFrame, tool: QualityAnalTool):
    # === 按列逐一添加完整性检查规则（忽略最后3列） ===
    for col in df.columns[:-3]:  # 忽略最后3列
        def make_rule(c):
            return lambda df: df[c].isnull()

        tool.add_rule(
            dimension="Complete",
            rule_func=make_rule(col),
            description=f"检查列 {col} 是否存在缺失值",
            cols=[col]
        )

def data_quality_anal(df: pd.DataFrame) -> pd.DataFrame:
    tool = QualityAnalTool(df)

    # Complete
    complete_check(df, tool)

    # 运行检查
    results = tool.run()
    tool.summary(results, outfile="quality_report.ans")

    return results


if __name__ == '__main__':
    df = pd.read_csv("data/Yellow_Tax_Trip_Records.csv")
    data_quality_anal(df)
