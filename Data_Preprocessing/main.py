import pandas as pd
from quality_anal_tool import QualityAnalTool

def main():
    # 读取数据
    csv_path = "netflix_titles.csv"
    df = pd.read_csv(csv_path)

    # 初始化工具
    tool = QualityAnalTool(df)

    # 添加规则
    tool.add_rule("Accurate",
                  lambda d: d["release_year"] < 1900,
                  "发行年份必须大于等于1900")
    tool.add_rule("Accurate",
                  lambda d: d["duration"].isnull() | ~d["duration"].astype(str).str.contains(r'\d+'),
                  "duration字段必须包含数字")

    # 执行质量检查
    results = tool.run()
    tool.summary(results)

if __name__ == "__main__":
    main()
