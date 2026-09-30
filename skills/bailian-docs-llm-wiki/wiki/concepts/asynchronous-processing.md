# 异步处理

异步处理是百炼平台对耗时较长的 AI 任务（如视频生成、3D 建模、大文件解析与翻译等）所采用的标准执行模式：客户端提交任务后立即获得唯一任务标识（`task_id` 或 `biz_id`），服务端在后台异步执行，客户端通过轮询或事件回调方式获取最终结果。该模式解耦请求与响应，保障系统稳定性与高并发能力，避免 HTTP 连接超时和资源阻塞。

## 在百炼平台的不同场景中，这个概念如何使用

异步处理是以下六类核心能力的**统一交互范式**，适用于所有计算密集型、I/O 延迟高或结果生成周期不可预测的任务：

- **视频生成（Video Generation）**：所有文生/图生/参考生视频、数字人驱动、风格重绘等均强制异步。必须携带请求头 `X-DashScope-Async: enable`，否则返回明确错误 `"current user api does not support synchronous calls"`；任务 ID 有效期为 24 小时。
- **3D 模型生成（3D Generation）**：Tripo 模型仅支持异步调用，且严格限定于华北2（北京）地域；任务创建后需轮询 `/api/v1/tasks/{task_id}`，状态流转为 `PENDING → RUNNING → SUCCEEDED/FAILED`。
- **文档与音视频解析（ParseX）**：所有 Parse（解析）与 Extract（字段抽取）任务均基于 `biz_id` 实现异步交付；解析结果默认保留 30 天，复用解析结果进行抽取时须在 7 天内完成。
- **通用模型 API（More About Models）**：图像生成（如 `wanx2.1-t2i-turbo`）、语音转写（如 `paraformer-16k-1`）等长耗时模型明确归类为“异步模型”，支持轮询查询与事件驱动两种结果获取方式。
- **多模态翻译（Qwen-MT-Uni）**：同步模式仅限文本、小图、短音频（≤30 秒）；大文档（≤200 页）、长音频（3 秒–60 分钟）必须启用异步模式，通过 `X-DashScope-Async: enable` 触发。
- **跨能力统一抽象**：无论底层是视频渲染、神经辐射场重建还是大模型推理，平台对外暴露一致的异步生命周期：提交 → 等待 → 查询/通知 → 获取输出（含 `output.results`、`pbr_model_url`、`TranslatedFileUrl` 等结构化结果）。

> ✅ 共同特征：  
> - 所有异步接口均返回唯一任务标识（`task_id` 或 `biz_id`），**不可重复提交相同标识**；  
> - 任务状态查询接口统一为 `GET /api/v1/tasks/{id}`（模型类）或 `GET /parse/result?biz_id=xxx`（ParseX 类）；  
> - 结果 URL（如视频地址、GLB 文件、翻译后 PDF）均为临时链接，有效期通常为 2 小时，需及时下载或持久化。

## 关键参数和配置

| 参数 / 配置 | 作用 | 是否必需 | 说明 |
|-------------|------|----------|------|
| `X-DashScope-Async: enable` | 启用异步模式的开关请求头 | ✅ 所有异步模型调用必填 | 缺失将直接报错；不区分大小写，但值必须为 `enable`（非 `true`/`1`） |
| `task_id` / `biz_id` | 异步任务唯一标识符 | ✅ 轮询时必填 | UUID 格式字符串；`task_id` 用于模型类 API（如视频、3D），`biz_id` 用于 ParseX 类 API；两者命名空间隔离，不可混用 |
| 轮询间隔策略 | 控制查询频率，避免触发限流 | ⚠️ 强烈建议 | 基础轮询建议 ≥15 秒；生产环境推荐指数退避（如 1s → 2s → 4s → 8s）；高频轮询请改用事件回调 |
| 事件回调（EventBridge） | 替代轮询的低开销方案 | ❌ 可选 | 配置 HTTP 回调 URL 或 RocketMQ 主题，接收 `dashscope:System:AsyncTaskFinish` 事件；规避 QPS 限制与连接管理复杂度 |
| 地域一致性 | 异步任务执行与查询的地域约束 | ✅ 强制要求 | API Key、Endpoint、模型开通地域三者必须完全一致；跨地域调用将失败（如北京 Key 调用新加坡 Endpoint） |

> 💡 提示：  
> - 所有异步任务默认保留期为 **24 小时**（个别服务如 ParseX 解析结果为 30 天），超期后 `GET /api/v1/tasks/{id}` 返回 `task_status: "UNKNOWN"`，无法恢复；  
> - 不要自行拼接或缓存任务查询 URL，应始终使用响应体中返回的完整 `task_id` 和标准路径；  
> - 错误响应中 `request_id` 是排查问题的关键线索，务必记录并关联日志。

## 面向开发者，简洁实用

- **第一步：确认是否需要异步**  
  查阅对应模型文档 —— 若描述中出现“异步调用”、“轮询获取结果”、“`X-DashScope-Async`”或“任务 ID”，即必须走异步流程。

- **第二步：构造请求**  
  ```bash
  curl -X POST 'https://{WorkspaceId}.{region}.maas.aliyuncs.com/.../submit' \
    -H 'Authorization: Bearer sk-xxx' \
    -H 'Content-Type: application/json' \
    -H 'X-DashScope-Async: enable' \  # ← 关键！漏掉即失败
    -d '{"model": "...", "input": {...}}'
  ```
  成功响应必含 `"task_id"` 或 `"biz_id"` 字段。

- **第三步：安全轮询或配置回调**  
  - ✅ 推荐：实现带退避的轮询（Python 示例）：
    ```python
    import time, random
    task_id = response["task_id"]
    for i in range(10):  # 最多尝试10次
        res = requests.get(f"https://.../api/v1/tasks/{task_id}", headers=headers)
        if res.json().get("task_status") == "SUCCEEDED":
            print(res.json()["output"]["results"])
            break
        time.sleep(min(2 ** i + random.uniform(0, 1), 30))  # 指数退避，上限30秒
    ```
  - ✅ 生产首选：配置 EventBridge HTTP 回调，收到 `AsyncTaskFinish` 事件后主动拉取结果，彻底消除轮询开销。

- **第四步：处理结果与清理**  
  - 解析 `output.results` 中的结构化数据（如 `video_url`, `pbr_model_url`, `TranslatedFileUrl`）；  
  - 所有临时 URL 有效期仅 **2 小时**，请立即下载或转存至自有存储；  
  - 记录 `task_id` + `request_id` 用于审计与问题定位；  
  - 无需手动“删除”任务 —— 到期自动清理。

> 🚫 避坑指南：  
> - 不要省略 `X-DashScope-Async: enable`；  
> - 不要跨地域混用 API Key 与 Endpoint；  
> - 不要高频轮询（>20 QPS），会触发限流；  
> - 不要假设 `task_id` 永久有效 —— 24 小时后失效；  
> - 不要尝试用同步接口（如 `/chat/completions`）调用异步模型 —— 协议不兼容。

## 关联主题页

- [video generation api](../api/video-generation-api.md)
- [3d generation](../api/3d-generation.md)
- [getting started overview](../guides/getting-started-overview.md)
- [api overview](../api/api-overview.md)
- [more about models](../api/more-about-models.md)
- [qwen mt translation models](../api/qwen-mt-translation-models.md)


