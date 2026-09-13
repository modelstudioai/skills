# application gallery

应用广场是百炼平台提供的预置应用集合，面向开发者提供开箱即用的行业级 Agent 和[多模态](../concepts/multi-modal.md)解决方案。所有应用均基于通义系列大模型构建，支持一键部署、参数微调与私有化集成。应用列表持续更新，具体能力以 [原文标题](../../raw/application-user-guide/application-gallery.md) 为准。

## 支持的模型与功能

应用广场中的应用底层依赖通义千问（Qwen）系列语言模型、通义万相（Tongyi Wanxiang）[多模态](../concepts/multi-modal.md)模型、通义听悟（Tongyi Tingwu）语音模型等，覆盖以下典型能力：

- 文本理解与生成：如通义点金（金融分析）、析言GBI（商业智能问答）  
- [多模态](../concepts/multi-modal.md)交互：如通义拍照解题辅导（图像+文本联合推理）、通义多模态翻译（图文音跨模态转换）  
- 搜索与知识增强：如通义深度搜索、千问联网检索Agent（实时网页检索+RAG）  
- 语音与对话系统：如通义听悟Agent、伶鹊CCAI系列（语音对话机器人、客服对话Agent）  
- UI 自动化：通义 UI Agent（基于截图理解并操作网页/APP界面）  

全部官方应用清单及对应能力说明详见 [原文标题](../../raw/application-user-guide/application-gallery.md)。

## 关键参数

各应用在部署时可配置以下通用参数（部分应用支持扩展参数）：

- `model_id`: 指定基础模型（如 `qwen-max`, `qwen-plus`, `qwen-vl-plus`），需与应用类型兼容；不填则使用默认推荐模型  
- `temperature`: 控制输出随机性（0.0–1.0），默认 `0.5`；对确定性任务（如法务、金融）建议设为 `0.1–0.3`  
- `max_output_tokens`: 输出长度上限，范围 `128–8192`，不同应用有硬性限制（例如 UI Agent 默认上限为 `2048`）  
- `enable_search`: 布尔值，仅适用于支持联网检索的应用（如千问联网检索Agent），启用后自动调用百炼内置搜索插件  

参数兼容性与默认值请严格参照 [原文标题](../../raw/application-user-guide/application-gallery.md) 中各应用的详情页说明。

## 使用方式

1. **控制台部署**：登录百炼控制台 → 进入「应用广场」→ 点击目标应用卡片 → 「立即部署」→ 配置参数 → 创建应用实例  
2. **API 调用**：通过 `POST /v1/applications/{app_id}/chat` 接口发起请求，`messages` 字段格式与标准 Chat Completion 一致，支持 `files` 数组上传图片/音频（需 Base64 编码或 OSS URL）  
3. **SDK 集成**：Python SDK 示例：
   ```python
   from alibabacloud_bailian20231219.client import Client
   client = Client(...)
   response = client.chat(app_id="app-xxx", messages=[{"role":"user","content":"..."}], temperature=0.2)
   ```

> **注意**：部分应用（如通义法睿、通义数据挖掘）当前仅支持控制台部署，暂未开放 API 调用能力，该限制与 [原文标题](../../raw/application-user-guide/application-gallery.md) 中列出的链接跳转目标一致，但实际 API 文档未同步更新 —— 开发者应以控制台「部署」按钮是否可用为准。

## 限制和注意事项

- 所有应用均需绑定有效工作空间（Workspace），且调用频次受工作空间配额限制（QPS/日调用量）  
- 文件类输入（如拍照解题、文档挖掘）单次请求最多支持 10 个文件，总大小不超过 100 MB  
- 多模态应用（如通义万相相关套件）不支持 `stream=True` 流式响应，必须等待完整结果返回  
- 应用 ID（`app_id`）全局唯一，但不可复用：删除后原 ID 不再可用，需重新部署获取新 ID  
- 非官方应用（用户自建）不纳入本广场管理，其生命周期与权限模型独立  

如遇应用状态异常或参数不生效，请优先检查工作空间配额与模型服务可用性，并确认所用参数与 [原文标题](../../raw/application-user-guide/application-gallery.md) 描述一致。

## 来源文档

- [应用广场](../../raw/application-user-guide/application-gallery.md)


