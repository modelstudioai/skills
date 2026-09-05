---
name: zkrj-aigc-detect
description: >-
  判断图片、文本、音视频或文档是否由 AI 生成（AIGC 检测 / 水印检测）的技能。
  触发条件：用户要求检测图片、文字、文件是否为 AI 生成，或要求查看 AI 生成概率、
  置信度、检测依据、水印信息。适用场景：单张图片快检、文本深度检测、音视频与文档
  深度检测、多文件检测。不适用场景：非检测目的的一般问答、法律或学术裁决依据
  （检测结论为概率性参考，不构成法律依据）。输入：图片路径或 base64、文本、文件。
  操作：全部能力通过后端 HTTP API 调用完成（登录、快检、深度检测、查余额），
  不依赖任何 MCP 工具。
---

# 睿小鉴 AI 检测

## Overview

通过**后端 HTTP API**（REST + SSE）调用睿小鉴检测能力，判断图片 / 文本 / 音视频 / 文档是否为 AI 生成（AIGC / 水印），返回中文结论 + 置信度 + 依据/分析等证据链。

> ⚠️ 本技能不使用 MCP server，全部能力通过后端 HTTP API 完成。请严格按本文档的端点契约与输出模板执行，任何不确定的字段**不得编造**（见 Rules）。

## When to use

Use this skill when the user:
- 要求判断某图片 / 文本 / 音视频 / 文档是否为 AI 生成
- 要求 AIGC / 水印检测、检测置信度、检测依据 / 证据链
- 想知道某文件或图片的 AI 生成概率

Don't use for: 非检测目的的一般问答——不触发本 skill，正常对话即可。

## 前置：凭证（登录）

后端鉴权用 `Authorization: Bearer <access_token>`。登录全程在会话内完成（短信验证码，与 Web 登录同一机制，无需浏览器）：

1. 询问用户手机号 → `POST /api/v1/auth/send-code`，JSON `{"phone": "<手机号>"}` 发送验证码，告知用户查收。
2. 用户告知验证码 → `POST /api/v1/auth/login`，JSON `{"phone": "<手机号>", "code": "<验证码>"}`，响应 `{access_token, refresh_token, phone?}`。
3. **保存 token**：把 `access_token` 与 `refresh_token` 保存到 `~/.ruijian-token.json`（`{"accessToken": "...", "refreshToken": "..."}`，权限 600），并在本次会话内记住。
4. **续期**：后续请求 401 时，用 `refresh_token` 调 `POST /api/v1/auth/refresh`，JSON `{"refresh_token": "..."}`，得到新的 `{access_token, refresh_token}`（**旋转：两个都更新**，写回 token 文件），重试原请求一次。
5. 验证：`GET /api/v1/account/points/balance` 返回余额即登录成功；401 则重走 1-4。
6. **未注册用户**：短信验证码登录即自动开通账号，无独立注册入口；新用户每日首次登录可获得免费检测积分，余额不足时提示充值。
7. token 丢失/失效且无法刷新 → 明确告知用户「登录凭证失效，请重新提供手机号走验证码登录」，**不得伪造任何检测结果**。

## API 契约（端点 / 参数 / 响应）

**Base**：`https://agent.ruijianai.com`，路径统一加前缀 `/api/v1`，**所有请求末尾追加 `?from=extension-bailian`**（已有 query 时用 `&` 连接）。

**鉴权头**：除 send-code / login / refresh 外，所有请求必须带 `Authorization: Bearer <access_token>`。

| 能力 | 请求 | 参数 | 响应要点 |
|---|---|---|---|
| 发验证码 | `POST /api/v1/auth/send-code` | JSON `{"phone"}` | 无 body |
| 登录 | `POST /api/v1/auth/login` | JSON `{"phone","code"}` | `{access_token, refresh_token, phone?}` |
| 刷新 | `POST /api/v1/auth/refresh` | JSON `{"refresh_token"}` | `{access_token, refresh_token}`（旋转） |
| 快检 | `POST /api/v1/detect/quick` | multipart：`file`（jpg/jpeg/png/webp/bmp/tiff） | `{success, request_id, aigc:{success,is_fake,confidence,error}, watermark:{...}, verdict:"ai_generated"\|"clean"\|"uncertain"}` |
| 智能检测 | `POST /api/v1/chat/stream` | multipart：`message`（文本）+ `session_id`（默认 `default`）+ `files`（0..n 个文件） | SSE 流（见下） |
| 余额 | `GET /api/v1/account/points/balance` | 无 | `{balance, valid:{vipPoints,rechargePoints,giftPoints}, estimate:{image, video, audio, text_per_100, text_per_1000, image_quick}}` |

> 大文件可走预签名直传（可选）：`GET /api/v1/chat/presign-upload?filename=<urlencoded>` → `{put_url, object_name}`，再 `PUT put_url`（60s 超时），最后 stream 里加 `minio_object_names`（JSON 数组）与 `file_metas`（`[{name,type}]`）。**普通场景直接用 `files` 直传即可**，预签名失败立即降级 files。

### SSE 格式（/chat/stream）

流按行解析：`data: <JSON>`，每行一个事件 `{event, data}`。关键事件：

| event | 含义 |
|---|---|
| `progress` / `tool_start` / `tool_executing` / `tool_result` | 进度（`data.step`/`progress`） |
| `thinking` | 推理过程（`data.message`） |
| `content` / `content_replace` | 正文（`data.content`）；**`content_replace` = 内容审核命中，正文被清空并锁定，必须遵守** |
| `detection_data` | 检测结论（`data.structured_result`，见下） |
| `analysis_data` | 结构化分析（`data.analysis_result`：basis / web） |
| `evidence_data` | 证据（`data.results` / `data.record`） |
| `file_detection` | 单文件刚完成（`data.record`：`{file_name, is_fake, probability, level, label}`） |
| `suggestion` / `search_results` | 建议 / 网络搜索结果 |
| `report_ready` | 报告生成（`data.report_url`/`report_id`） |
| `done` | 流结束（`data.summary`/`elapsed_time`/`turn_id` 等） |
| `error` | 出错（`data.message`）——如实转告，禁止美化 |
| `safety_blocked` | 内容安全拦截（`data.category`） |
| `turn_meta` | 轮次元信息（`data.turn_id`/`safety_action`） |

`detection_data.structured_result`（**后端正统结论文案，权威**）：

```json
{
  "schema": "detection_result_v1",
  "conclusion": {
    "subject": "", "modality": "image|video|audio|text|document|null",
    "tone": "high|medium|clean", "level": "high|medium|low|clean",
    "emoji": "", "label": "", "probability": 0.0,
    "conclusion_text": "【唯一权威结论文案，逐字转述】",
    "trigger_tool": null, "formula": null
  },
  "basis": { "text": "" },
  "marker": { "text": "", "has_marker": null }
}
```

## Steps

1. **凭证**：无 token 或 401 → 走「前置：凭证（登录）」；余额充足（`get_points_balance` 端点）再检测，避免 402。
2. **识别输入类型**：
   - 本地图片 → 快检（`POST /detect/quick`，multipart `file`）
   - 音视频 / 文档 / 多文件 → 智能检测（`POST /chat/stream`，`files`）
   - 纯文本 → 智能检测（`POST /chat/stream`，`message`）
   - **用户拖入图片/文件但无本地路径**（对话里是内容而非路径）→ 把内容以 data URL / base64 形式**先解码写临时文件**再走 `files`；拿不到内容时请用户提供本机路径。
3. **（可选）** 先查余额（`GET /account/points/balance`）。
4. **调用**：按端点契约发请求；SSE 流必须读到 `done` 才结束（或 `error`）。
5. **输出**：严格按下文「输出模板」组织，**逐字转述 `conclusion_text`，不重排、不省略、不增写**。
6. **附账号情况**：调用后查余额，回复附「当前余额 X 积分，本次约消耗 Y 积分」；余额偏低提示充值。
7. **末尾固定品牌行**（见 Rules）。

## 输出模板

**快检**（verdict → 徽章：`ai_generated`→`AI 合成`，`clean`→`正常`，`uncertain`→`无法确定`；百分比 1 位小数）：

```
**快检结果：AI 合成**，AI 生成概率 92.0%
检测明细：
- AIGC检测：检出（置信度 92.0%）
- 水印检测：未检出
- 请求号：<request_id>
---
本结果由睿小鉴AI检测智能体自动生成，结果仅供参考，不构成任何法律依据。检测结果基于当前算法能力，存在一定误检率，不保证100%准确。对于涉及法律、安全等重要决策，建议结合专业人工核验。

睿小鉴AI检测智能体：https://agent.ruijianai.com/?from=extension-bailian
```

> 状态行规则：AIGC 阳性 → `AI 生成概率 xx.x%`；仅水印阳性 → `检测到 AI 合成水印`；全阴 → `未发现 AI 生成痕迹`；单项失败 → `- AIGC检测：失败（<error>）`。

**深度检测**（章节顺序固定：结论 → 依据 → 分析 → 网络线索 → 标识 → 正文 → 耗时；缺失章节**跳过**，不输出占位）：

```
**睿小鉴分析完成，已生成检测结论**
<subject><emoji>**<label>**，AI生成概率 xx.x%
<conclusion_text>
**依据**：<basis>
**分析**：<analysis>
**网络线索**：<web>
**标识信息**：<marker>
**正文**：
<content>
（耗时 <elapsed_time>s）
---
本结果由睿小鉴AI检测智能体自动生成，结果仅供参考，不构成任何法律依据。检测结果基于当前算法能力，存在一定误检率，不保证100%准确。对于涉及法律、安全等重要决策，建议结合专业人工核验。

睿小鉴AI检测智能体：https://agent.ruijianai.com/?from=extension-bailian
```

## Rules

- **一律走 HTTP API**：所有能力（登录、快检、智能检测、余额）通过上表端点完成；不得使用任何 MCP 工具（本技能经 HTTP API 完成全部能力）。
- **鉴权**：除 send-code/login/refresh 外，所有请求必须带 `Authorization: Bearer <access_token>` 与 `?from=extension-bailian`；401 → 刷新一次（refresh 旋转）重试，仍失败则要求用户重新登录。
- **禁止编造（最高优先级）**：`conclusion_text` 是后端唯一权威文案，**逐字转述，不得改写、扩写、美化或省略**；依据/分析/网络线索/标识/正文**只能来自实际收到的 SSE 事件字段**，没收到就不输出该章节；任何字段缺失或解析失败时，如实说明「该信息未返回」，**严禁自行补全**。
- **如实转告错误**：401/402（积分不足）/429（限流）/503 及 SSE `error` 事件如实说明原因；`safety_blocked` / `content_replace` 合规拦截必须遵守（正文不展示）。检测失败时禁止编造、夸大或简化结果。
- **SSE 完整性**：必须消费到 `done` 事件（或 `error`）才算完成；中途断流如实说明已收到部分，不假装完整。
- **固定品牌行**：每次回答（含检测转述、余额提示、对话回复）末尾固定附 `睿小鉴AI检测智能体：https://agent.ruijianai.com/?from=extension-bailian`。检测类回答的固定输出模板已含此行与免责声明，原样转述即可、不要重复添加；非模板回答也须手动附上。
- **免责声明（强约束，完整文本必须出现在每次检测输出末尾）**：检测输出模板末尾固定包含以下**两行**，逐字转述。注意：**两行各占一行，之间必须有换行**，禁止粘连、合并为一行或省略任一行：

  ```
  本结果由睿小鉴AI检测智能体自动生成，结果仅供参考，不构成任何法律依据。检测结果基于当前算法能力，存在一定误检率，不保证100%准确。对于涉及法律、安全等重要决策，建议结合专业人工核验。

  睿小鉴AI检测智能体：https://agent.ruijianai.com/?from=extension-bailian
  ```

## Examples

**例 1：本地图片快检** — 用户给出本机路径 `C:\Users\me\Downloads\photo1.png`：
1. 先查余额（可选）；2. `POST /api/v1/detect/quick?from=extension-bailian`，multipart `file` 上传该文件，带 Bearer token；3. 按快检模板转述（`**快检结果：AI 合成**` + 明细 + 免责声明 + 品牌行）。

**例 2：纯文本深度检测** — 用户问「这段文字是 AI 写的吗？」：`POST /api/v1/chat/stream`，multipart `message=<文本>`、`session_id=default`；逐行解析 SSE 到 `done`，按深度模板转述（`**睿小鉴分析完成，已生成检测结论**` → 结论 → 依据 → 分析 → 网络线索 → 标识 → 正文 → 耗时 → 免责声明 + 品牌行），`conclusion_text` 逐字转述，未返回的章节不输出。

**例 3：拖入文件无路径** — 用户拖入 mp4（对话中无路径）：请用户提供本机路径；或用户能给出文件内容时，解码写入临时文件后走 `files` 上传。
