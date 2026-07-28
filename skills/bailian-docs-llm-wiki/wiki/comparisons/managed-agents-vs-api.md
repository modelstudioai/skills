# 托管 Agent 使用方式对比：控制台 vs API

百炼平台的 Managed Agents 支持两种使用方式：通过**控制台（可视化向导）**完成配置与调试，或通过 **REST API / SDK** 以编程方式全流程编排。两种方式底层共用同一套资源模型（Agent、Environment、Session、Event），但在操作入口、适用场景和集成深度上存在显著差异。本页帮助开发者根据团队技术栈和业务需求做出选型。

## 关键维度对比

| 维度 | 控制台 | API / SDK |
|------|--------|-----------|
| **操作入口** | 百炼控制台 Web UI，向导式交互 | REST API + 官方 SDK（Python/Node.js 等） |
| **认证方式** | 登录阿里云账号，控制台会话鉴权 | HTTP Header `Authorization: Bearer <api-key>` |
| **API Endpoint** | 不涉及（内部调用） | `https://{workspace_id}.{region}.maas.aliyuncs.com/api/v1/agentstudio` |
| **支持地域** | 控制台页面同步 | 当前仅支持 `cn-beijing` |
| **Agent 配置** | 填写表单：名称、模型、系统提示词、工具勾选 | `POST /agents`，JSON body 定义全部字段 |
| **Environment 配置** | 向导默认云端托管沙箱，可选预装依赖 | `POST /environments`，支持 `config.packages` 预装 apt/pip |
| **Session 创建** | 向导自动绑定 Agent ID + Environment ID | `POST /sessions`，手动指定 `agent_id` 与 `environment_id` |
| **事件交互** | 预览调试标签页直接对话，支持按事件类型筛选 | `POST /sessions/{id}/events` 发送消息；`GET /sessions/{id}/events/stream` SSE 订阅 |
| **版本管理** | 每次保存自动递增版本，UI 可查版本历史 | `GET /agents/{agent_id}/versions` 分页查询；更新时需携带 `version` 作乐观锁 |
| **文件挂载** | 直接上传本地文件到沙箱（≤10 MB/文件） | 先 `POST /files` 上传审核，审核通过后挂载到会话（≤20 MB/文件，工作空间总量 ≤100 GB） |
| **Skill 管理** | 控制台页面上传 zip 包、查看审核状态 | `POST /skills` 创建；`POST /skills/{id}/versions` 上传新版本；挂载时必须指定 `version` |
| **调试能力** | 内置预览调试标签页，事件流可视化过滤（User/Agent/Tool/Tool_output/Error/Model/System） | 需自行解析 SSE 事件流，适合集成到自动化测试或监控系统 |
| **自动化/CI 集成** | 不适合（手动操作为主） | 原生支持，可嵌入 CI/CD 流水线 |
| **资源软归档** | 控制台提供归档操作 | `POST /agents/{id}/archive`、`POST /sessions/{id}/archive` 等 |
| **错误追踪** | 控制台展示错误事件 | 每次响应携带 `x-request-id`，提工单时附上可加速定位 |

## 四步典型流程对比

两种方式的核心流程完全对应，区别仅在操作载体：

| 步骤 | 控制台 | API |
|------|--------|-----|
| 1. 配置智能体 | 填写名称、选择模型（如 `qwen3-max`）、输入系统提示词、勾选工具 | `POST /agents`，指定 `model`、`system_prompt`、`tools` |
| 2. 配置运行环境 | 向导选择默认沙箱，可选预装依赖 | `POST /environments`，`config.packages` 声明 apt/pip 依赖和网络策略 |
| 3. 发起会话 | 向导自动绑定，点击"开始"即创建 Session | `POST /sessions`，绑定 `agent_id` + `environment_id` |
| 4. 交互与接收响应 | 预览调试标签页直接输入消息，实时查看工具执行过程 | `POST /sessions/{id}/events` 发送消息；`GET /sessions/{id}/events/stream` 接收 SSE 事件 |

## 文件配额差异

| 限制项 | 控制台上传 | API 上传 |
|--------|-----------|---------|
| 单文件大小 | ≤ 10 MB | ≤ 20 MB |
| 工作空间总容量 | 文档未单独说明 | ≤ 100 GB |
| 文件保留期 | 文档未单独说明 | 30 天 |
| 审核流程 | 自动（上传后即挂载） | 异步审核（`checking` → `available` / `rejected` / `type_rejected`），仅 `available` 可挂载 |

## 适用场景建议

### 推荐使用控制台的场景

- **快速原型验证**：首次体验 Managed Agents，5 分钟内跑通端到端流程，无需写代码。
- **提示词调优**：通过预览调试标签页反复迭代系统提示词，实时观察工具执行轨迹。
- **非技术成员协作**：产品经理、运营人员需要配置或查看 Agent 行为，无需了解 API 细节。
- **故障排查**：按事件类型（Tool_output、Error 等）筛选，快速定位执行异常。

### 推荐使用 API / SDK 的场景

- **生产环境集成**：将 Agent 调用嵌入业务系统（后端服务、数据处理流水线、自动化脚本）。
- **CI/CD 自动化**：通过 API 创建/归档 Agent、批量跑测试用例、断言 SSE 事件流输出。
- **动态资源挂载**：在会话运行中通过 `POST /sessions/{id}/resources` 实时追加文件，无需重启。
- **版本管理与灰度**：精确控制 Agent `version`、Skill `version`，实现灰度发布与回滚。
- **大规模并发**：程序化创建多个 Session 并行执行，控制台不支持批量操作。

## 技术选型建议

1. **探索期**：先用控制台完成 Agent 配置和调试，确认提示词和工具组合有效后，再通过 API 固化到代码。
2. **生产期**：API 方式为首选；控制台保留用于监控和应急调试。
3. **混用模式**：在控制台创建并调试 Agent（获得 `agent_id`），在代码中直接引用该 ID 创建 Session——控制台和 API 操作的是同一套资源，可自由混用。
4. **注意模型名称一致性**：控制台向导示例中出现 `qwen3.7-plus`，而 API 代码示例使用 `qwen3-max`，请以控制台模型下拉列表中实际可选的模型 ID 为准。

## 被对比主题页

- [managed agents](../guides/managed-agents.md)
- [managed agents api](../api/managed-agents-api.md)


