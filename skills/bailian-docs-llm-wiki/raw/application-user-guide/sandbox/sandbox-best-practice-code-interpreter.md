# 使用 Code Interpreter Sandbox

面向数据分析类 Agent 的最佳实践：把模型生成的分析逻辑放进隔离沙箱执行，固定脚本入口、结构化输出、依赖固化到模版，返回可解释、可下载、可审计的结果。

Code Interpreter Sandbox 面向需要运行 Python/Node 脚本、处理文件、生成结构化结果或报告产物的 Agent。数据分析类 Agent 的核心诉求，是让模型生成的分析逻辑在隔离环境中处理数据，并返回可解释、可下载、可审计的结果。在业务服务中直接执行外部数据与模型生成的代码，依赖冲突、文件残留、长时间计算、异常日志与数据权限都会变成工程问题。

Sandbox 可作为 Code Interpreter Sandbox 使用：业务系统负责上传数据、生成或选择分析脚本、校验输入输出；沙箱负责运行脚本、处理临时文件、返回结构化结果。适合智能问答、运营分析、报表生成、客服数据诊断等场景。

## 业务场景

-   上传 CSV，自动计算指标并给出摘要。
-   运营人员用自然语言触发临时分析，不把数据落到主服务运行目录。
-   报表系统把中间计算放到沙箱执行，结果文件再回传给业务系统。
-   多租户场景下，每次分析使用独立沙箱，降低数据串扰风险。

## 推荐流程

先基于代码解释器镜像（`code-interpreter-v1`）创建模版并获取 `templateCode`，详见[模版管理](raw/application-user-guide/sandbox/sandbox-templates.md)。然后把分析任务拆成四步：

1.  写入输入数据和分析脚本。
2.  使用固定入口执行脚本，例如 `python3 analyze.py`。
3.  要求脚本输出 JSON 摘要，必要时生成文件产物。
4.  读取结果并销毁沙箱。

## 交互式代码执行

需要 Notebook 类 `run_code` 体验时，使用 `e2b-code-interpreter` SDK 直接创建实例并调用 `run_code`：

```
from e2b_code_interpreter import Sandbox

ALIYUN_UID = "your aliyunUid"
BAILIAN_API_KEY = "sk-..."
BASE_URL = "https://{workspace_id}.cn-beijing.maas.aliyuncs.com/api/v1/agentstudio/sandbox"

sandbox = Sandbox.create(
    api_url=BASE_URL,
    api_key=f"e2b_{ALIYUN_UID}",
    headers={"Authorization": f"Bearer {BAILIAN_API_KEY}"},
    template="你的模版 code",
)

try:
    execution = sandbox.run_code(
        """
import json

data = [
    {"segment": "enterprise", "revenue": 2600},
    {"segment": "startup", "revenue": 680},
]

total = sum(row["revenue"] for row in data)
top_segment = max(data, key=lambda row: row["revenue"])

print(json.dumps({
    "total_revenue": total,
    "top_segment": top_segment["segment"],
    "top_segment_revenue": top_segment["revenue"],
}, ensure_ascii=False))
"""
    )
    print("".join(execution.logs.stdout or []))
finally:
    sandbox.kill()
```

`run_code` 更适合模型逐步生成和修正代码的交互式任务；固定脚本入口更适合生产链路，因为脚本版本、输入目录、超时时间和输出格式都更容易固化。

## 示例代码

以下示例在沙箱中分析分客群收入，返回总收入、贡献最高客群和摘要：

**说明**Node.js 侧固定 SDK 版本：`npm install e2b@2.31.0`，更高版本创建实例时返回 405。

```
import { Sandbox } from "e2b";

const ALIYUN_UID = "your aliyunUid";
const BAILIAN_API_KEY = "sk-...";
const BASE_URL = "https://{workspace_id}.cn-beijing.maas.aliyuncs.com/api/v1/agentstudio/sandbox";

const sandbox = await Sandbox.create("你的模版 code", {
  apiUrl: BASE_URL,
  apiKey: `e2b_${ALIYUN_UID}`,
  apiHeaders: { Authorization: `Bearer ${BAILIAN_API_KEY}` },
  envs: { TASK_TYPE: "data-analysis" },
});

try {
  await sandbox.files.makeDir("/tmp/data-analysis");
  await sandbox.files.write(
    "/tmp/data-analysis/revenue.csv",
    `date,segment,revenue
2026-07-01,enterprise,1200
2026-07-01,startup,320
2026-07-02,enterprise,1400
2026-07-02,startup,360
`,
  );
  await sandbox.files.write(
    "/tmp/data-analysis/analyze.py",
    `import csv
import json
from collections import defaultdict

revenue_by_segment = defaultdict(int)
with open("revenue.csv", newline="") as f:
    for row in csv.DictReader(f):
        revenue_by_segment[row["segment"]] += int(row["revenue"])

total = sum(revenue_by_segment.values())
top_segment, top_revenue = max(revenue_by_segment.items(), key=lambda item: item[1])

print(json.dumps({
    "total_revenue": total,
    "top_segment": top_segment,
    "top_segment_revenue": top_revenue,
    "summary": f"{top_segment} contributes {round(top_revenue / total * 100, 1)}% of revenue."
}, ensure_ascii=False))
`,
  );

  const result = await sandbox.commands.run("python3 analyze.py", {
    cwd: "/tmp/data-analysis",
    timeoutMs: 30_000,
  });
  if (result.exitCode !== 0) {
    throw new Error(result.stderr || result.stdout);
  }

  console.log(JSON.parse(result.stdout));
} finally {
  await sandbox.kill();
}
```

## 上线建议

-   输入文件限制大小、类型和路径，避免一次任务占用过多内存或磁盘。
-   输出优先使用 JSON 摘要；图表、表格、报告文件可以写入 `/tmp` 后再下载。
-   对 `stdout`、`stderr`、退出码和结果文件做统一封装，避免上层 Agent 直接解析非结构化日志。
-   对分析代码做版本化，生产系统不要只保存模型生成的自然语言解释。
-   常用依赖如 `pandas`、`openpyxl`、绘图库和业务 SDK 建议固化到模版。
-   对外输出结果与排障日志分开处理，避免把完整堆栈或敏感数据直接返回。

## 下一步

-   [实例管理与使用](raw/application-user-guide/sandbox/sandbox-sdk.md)：执行命令、运行代码与读写文件
-   [模版管理](raw/application-user-guide/sandbox/sandbox-templates.md)：基于代码解释器镜像创建模版
-   [使用 Browser Use Sandbox](raw/application-user-guide/sandbox/sandbox-best-practice-browser-use.md)：网页自动化类任务的最佳实践
