# 示例代码获取与输出规则

> `recommend.mjs`（默认）与 `recall-rank.mjs --with-samples` 已经把示例内嵌进
> `candidates[].samples`，常规路径**不需要**单独调 get-samples.mjs。
> 只有在"用户已确定模型、只要代码"时才直接跑：
>
> ```bash
> node scripts/get-samples.mjs <model-id> [<model-id>...]
> ```

## samples 数据结构

模型的 `detailPath` 指向其 group 文件（如 `models/groups/glm-4.5.json`），
文件里每个 item 有 `samples` 字段：

```
samples:
  openai:                          # OpenAI 兼容接口（优先使用）
    completionsAPI / default:      # API 类型
      curl: "..."                  # curl 示例
      python: "..."                # Python 示例
      nodejs: "..."                # Node.js 示例
      docUrl: "..."                # 文档链接
  dashscope:                       # DashScope 原生接口
    default:
      curl: "..."
      python: "..."
      java: "..."
      docUrl: "..."
```

脚本输出的 `samples.source` 标明来源：`openai` / `dashscope` / `fallback`
（group 文件里没有示例时，构造最简 OpenAI 兼容示例）。

## 输出规则

1. 优先 `samples.openai`，其次 `samples.dashscope`，都没有才用 fallback
2. 优先给 Python 示例，其次 curl
3. 示例含 `enable_thinking: true` 或 `reasoning_content` 流式思考循环时，**去掉思考相关逻辑**，给用户最简洁的调用方式（除非用户明确要看思考过程）
4. **base_url 必须原样取自 samples，禁止编造或改写域名**。百炼存在多种端点形态（`dashscope.aliyuncs.com`、按量计费的 `[workspace-id].<region>.maas.aliyuncs.com`、Token Plan 的 `token-plan.<region>.maas.aliyuncs.com`），猜错会导致 401/404，且无法从模型名反推
5. 脚本输出含 `endpointNote` 时，**必须把该提示写进回答**：示例端点里的 `[workspace-id]` 占位符要替换为真实 Workspace ID，并与 API Key、地域严格匹配（获取方式见输出里的链接）
6. 示例形态要与 `callModes` 一致：只有 `async` 的模型给"创建任务 + 轮询"示例，不要给同步返回；`realtime` 模型走实时接口而非 chat/completions
7. 消息内容按用户场景改写（如代码类需求给编程 prompt），但**模型名、base_url、鉴权头保持 samples 原样**

## 推荐输出格式

每个推荐模型必须包含：

1. **模型名称和 ID**
2. **推荐理由** — 关联用户具体需求
3. **亮点** — 关键优势标签（`specs.features`）
4. **规格信息** — 上下文窗口、最大输出、定价（`specs`）
5. **调用示例代码** — `samples`（优先 Python，附 curl）

### pipeline 场景输出格式

```
方案概述：一句话说明

步骤 1：xxx
  推荐模型 + 理由 + 示例代码

步骤 2：xxx
  推荐模型 + 理由 + 示例代码
  （模态不兼容时明确提示）
```
