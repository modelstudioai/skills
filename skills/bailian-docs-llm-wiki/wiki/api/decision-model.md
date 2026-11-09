# decision model

百炼决策模型（`decision-model-preview`）是一种专为结构化决策任务设计的轻量级推理模型，一次前向计算即可同步返回分类、是非判断、有序评分及其概率分布与置信度，**不生成文本**。适用于工单分流、内容审核、智能体完成度校验、任务路由等高频、低延迟、强确定性的业务场景。其接口协议遵循 TypeSafe System One 标准，与百炼平台其他模型能力解耦，可独立集成。

## 支持的模型与功能

- 当前唯一支持的模型为 `decision-model-preview`，属于预览版（Preview），正式 GA 版本尚未发布。
- 支持三类结构化问题类型：
  - `choice`：多选一分类（如「派单团队」），返回选中选项名、各选项概率分布及整体置信度；
  - `noul`（yes/no/uncertain/likely）：是非二元判断（如「是否需升级」），返回 `P(yes)` 概率值（浮点数，0–1）；
  - `score`：有序量表打分（如「严重度 1–4 级」），返回概率加权期望等级索引（可为小数，如 `2.25`）、各级概率及置信度。
- 所有类型均返回完整 `probabilities` 分布，便于下游做阈值控制或不确定性感知；`choice` 与 `score` 额外返回 `confidence` 字段，`noul` 不提供置信度（因其输出即为概率本身）。
- 详细能力说明见 [决策模型 API](../../raw/model-api-reference/decision-model/decision-model-api.md)。

## 关键参数

| 参数 | 类型 | 位置 | 必填 | 说明 |
|------|------|------|------|------|
| `model` | `String` | Body | ✅ | 固定为 `"decision-model-preview"` |
| `state` | `String / Object / Array` | Body | ✅ | 待决策的原始输入，支持纯文本、JSON 对象或数组；对象将被序列化后送入模型 |
| `questions` | `Object` | Body | ✅ | 键为自定义问题 ID，值为问题对象；每个问题必须指定 `type`（`choice`/`noul`/`score`）及对应 `criteria`（详见下文） |
| `Authorization` | `String` | Header | ✅ | `Bearer $DASHSCOPE_API_KEY`，API Key 需提前配置为环境变量 |
| `Content-Type` | `String` | Header | ✅ | 必须为 `"application/json"` |

**`questions` 中各类型 `criteria` 要求**：
- `choice`：`criteria` 为 `{"key": "desc"}` 映射（1–255 项），**建议补全 `other` 作为兜底选项**；
- `noul`：`criteria` 可选，若提供应为 `{"true": "...", "false": "..."}` 形式，用于引导模型理解语义；
- `score`：`criteria` 为字符串数组（2–255 项），按等级从低到高排列，**强烈建议使用 3–7 级且每级描述可清晰区分**。

更多参数细节与约束请参考 [决策模型 API](../../raw/model-api-reference/decision-model/decision-model-api.md) 中的“请求参数”章节。

## 使用方式

### SDK 调用（推荐）
- **Python**：需 DashScope SDK ≥ `2.0.1`，使用 `client.decision.create()` 方法。旧版本无 `decision` 接口，调用将抛出 `AttributeError`。[安装 SDK](../../raw/model-api-reference/preparations/install-sdk.md)。
- **Java**：需 DashScope SDK ≥ `2.23.3`，使用 `com.alibaba.dashscope.decision` 包。Maven 坐标：`com.alibaba:dashscope-sdk-java:2.23.3`。
- SDK 自动拼接 endpoint（如 `https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/compatible-mode/v1/systemone`），无需手动构造 URL。

### 通用 TypeSafe SDK
- 安装 `typesafe-sdk`（`pip install typesafe-sdk`），设置 `base_url` 为 `https://{WorkspaceId}.{region}.maas.aliyuncs.com/compatible-mode`，调用 `client.system_one()` 即可。
- 此方式适用于已接入 TypeSafe 协议的现有系统，兼容性更强。

### curl 直连
- 直接 POST 到 `/compatible-mode/v1/systemone`，需手动替换 `{WorkspaceId}` 并配置地域域名（如北京为 `cn-beijing`，新加坡为 `ap-southeast-1`）。
- 示例见 [决策模型 API](../../raw/model-api-reference/decision-model/decision-model-api.md) 中的“curl”小节。

> **注意**：文档中提到“在线体验”可通过 Playground 进行，但该 Playground 地址 `https://bailian.console.aliyun.com/systemone_playground` 当前已下线，实际访问会跳转至百炼控制台首页，不再提供决策模型专属交互界面。开发者应以 SDK 或 API 调用为准。

## 限制和注意事项

- **问题数量上限**：单次请求最多 16 个 `questions`，延迟随问题数近线性增长；
- **上下文长度**：`state` 输入上限为 65536 token，超长将直接拒绝（HTTP 400）；
- **选项与等级限制**：
  - `choice` 最多支持 255 个选项；
  - `score` 最多支持 255 级，但**建议仅用 3–7 级**，过多等级易导致模型区分能力下降；
- **返回字段差异**：
  - `choice` 和 `score` 返回 `confidence`，`noul` 不返回（因其输出 `noul` 字段本身就是概率）；
  - `score` 返回 `legend` 字段映射等级索引到描述，`choice` 的选项描述在请求 `criteria` 中已给出，响应中不重复返回；
- **错误处理**：调用失败时，Python SDK 抛出 `DashScopeError`，Java SDK 抛出 `ApiException`；完整错误码见 [错误信息](../../raw/model-api-reference/preparations/error-code.md)。

## 来源文档

- [决策模型 API](../../raw/model-api-reference/decision-model/decision-model-api.md)


