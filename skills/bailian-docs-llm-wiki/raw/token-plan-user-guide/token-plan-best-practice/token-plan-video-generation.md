# 接入视频生成模型

在 Agent 工具中调用 Token Plan 视频生成模型，提交异步任务并在生成完成后下载视频。

## 支持的模型

模型

输入

说明

`happyhorse-1.1-t2v`

文本

文生视频

`happyhorse-1.1-i2v`

首帧图片、文本

图生视频

`happyhorse-1.1-r2v`

参考图片、文本

参考生视频

`wan3.0-video`

文本、图片或参考素材

全能视频生成

更多模型以 [个人版](https://help.aliyun.com/zh/model-studio/token-plan-personal-overview#tppo-h-models)和[团队版](https://help.aliyun.com/zh/model-studio/token-plan-team-overview#tpto-h-models)支持的模型 为准。

## 前提

-   已订阅 Token Plan，并获取以 `sk-sp-` 开头的 API Key。获取方式见[接入概览](https://help.aliyun.com/zh/model-studio/token-plan-integration-overview#tp-ext-prereq)。
-   本地已安装 Python 3.9 及以上版本。
-   使用的 AI 编程工具支持 Slash Command。其他工具的配置路径见[其他工具](https://help.aliyun.com/zh/model-studio/token-plan-integration-overview#tp-ext-tools)。

## 接口

提交任务：`POST https://token-plan.cn-beijing.maas.aliyuncs.com/api/v1/services/aigc/video-generation/video-synthesis`

查询任务：`GET https://token-plan.cn-beijing.maas.aliyuncs.com/api/v1/tasks/{task_id}`

请求头使用 `Authorization: Bearer $ANTHROPIC_AUTH_TOKEN`。提交任务时还需要 `X-DashScope-Async: enable`。

## 步骤一：创建 Slash Command

将套餐 API Key 配置为环境变量 `$ANTHROPIC_AUTH_TOKEN`。

在项目根目录创建 `.claude/commands/text-to-video.md`，写入以下内容：

```
调用 Token Plan 视频生成 API，提交文生视频任务，等待完成后下载视频。

视频描述：$ARGUMENTS

## 步骤

1. 从描述中提取 prompt（视频描述）、model（默认 happyhorse-1.1-t2v）、resolution（默认 720P）、ratio（默认 16:9）、duration（默认 5）。如果描述中明确指定了模型，使用指定的模型名。
2. 安装依赖：pip install requests
3. 使用 Bash 工具执行以下 Python 脚本提交任务、轮询状态并下载视频。脚本优先读取 TOKEN_PLAN_API_KEY，其次读取 ANTHROPIC_AUTH_TOKEN；不要展示 Key，也不要写入文件或日志。

```python
import json
import os
import sys
import time
from pathlib import Path

import requests

prompt = " ".join(sys.argv[1:])
key = os.environ.get("TOKEN_PLAN_API_KEY") or os.environ.get("ANTHROPIC_AUTH_TOKEN")
if not key:
    raise SystemExit("Token Plan API Key not found.")

base_url = "https://token-plan.cn-beijing.maas.aliyuncs.com"
headers = {"Authorization": f"Bearer {key}", "Content-Type": "application/json"}

response = requests.post(
    f"{base_url}/api/v1/services/aigc/video-generation/video-synthesis",
    headers={**headers, "X-DashScope-Async": "enable"},
    json={
        "model": "happyhorse-1.1-t2v",
        "input": {"prompt": prompt},
        "parameters": {"resolution": "720P", "ratio": "16:9", "duration": 5},
    },
    timeout=60,
)
if not response.ok:
    raise SystemExit(f"{response.status_code}: {response.text}")
task_id = response.json()["output"]["task_id"]
print(f"任务已提交：{task_id}")

while True:
    time.sleep(10)
    result = requests.get(f"{base_url}/api/v1/tasks/{task_id}", headers=headers, timeout=60)
    if not result.ok:
        raise SystemExit(f"{result.status_code}: {result.text}")
    data = result.json()
    status = data["output"]["task_status"]
    if status == "SUCCEEDED":
        video_url = data["output"]["video_url"]
        output = f"generated_{time.strftime('%Y%m%d_%H%M%S')}.mp4"
        video = requests.get(video_url, timeout=120)
        video.raise_for_status()
        Path(output).write_bytes(video.content)
        print(output)
        break
    if status in {"FAILED", "CANCELED", "UNKNOWN"}:
        raise SystemExit(json.dumps(data, ensure_ascii=False, indent=2))
    print(f"任务状态：{status}")
```

4. 输出下载后的视频文件路径。
```

## 步骤二：生成视频

在 Claude Code 中输入 `/text-to-video 一只白色的猫在阳台上晒太阳`。如需调整时长、分辨率或宽高比，在指令中写明即可，例如 `/text-to-video 生成 10 秒、1080P、9:16 的城市夜景`。

## 请求参数

参数

必选

说明

`model`

是

视频生成模型 ID。

`input.prompt`

是

视频描述。

`parameters.resolution`

否

分辨率，支持 `480P`、`720P`、`1080P`，默认 `1080P`。

`parameters.ratio`

否

宽高比，支持 `16:9`、`9:16`、`1:1` 等，默认 `16:9`。

`parameters.duration`

否

时长，取值范围 3 到 15 秒，默认 5 秒。

更多参数见 [HappyHorse 文生视频 API](raw/model-api-reference/video-generation-api/happyhorse-api-reference/happyhorse-text-to-video-api-reference.md)。

## 返回结果

-   提交任务后返回 `output.task_id` 和 `output.task_status`。
-   轮询 `GET /api/v1/tasks/{task_id}`，状态为 `SUCCEEDED` 时返回 `output.video_url`。
-   任务状态包括 `PENDING`、`RUNNING`、`SUCCEEDED`、`FAILED`、`CANCELED` 和 `UNKNOWN`。
-   视频 URL 有时效，生成后及时下载。

## 限制

-   视频生成是异步任务，提交后需要轮询结果。`task_id` 有效期为 24 小时。
-   不同模型支持的输入类型、分辨率、时长和宽高比不同，以对应模型文档为准。
-   视频生成消耗高于图像和语音合成，具体以控制台[用量统计](https://bailian.console.aliyun.com/cn-beijing/subscription/token-plan/personal)为准。

## 其他工具

其他工具的扩展机制和配置路径见[接入概览](https://help.aliyun.com/zh/model-studio/token-plan-integration-overview#tp-ext-tools)。将上面的 Slash Command 内容保存到对应路径即可。
