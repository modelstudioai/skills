# asset center page

资产中心是百炼平台中统一管理模型资产（如微调模型、推理服务、Prompt 模板等）的核心页面，为开发者提供可视化的资产生命周期操作界面。用户可通过该页面完成资产的创建、部署、版本管理、权限配置及监控查看。所有资产均与工作空间和项目上下文强绑定，确保环境隔离与访问可控。

## 支持的模型/功能

- 支持托管以下类型资产：微调后的 LLM 模型（Qwen 系列、GLM 系列等）、自定义推理服务（通过容器镜像或函数方式部署）、Prompt 工程模板（含变量注入与测试沙箱）、向量知识库索引包（支持 FAISS/HNSW 格式）  
- 提供资产级操作：一键部署为 API 服务、版本回滚、灰度发布、调用日志查询、QPS/延迟监控图表  
- 支持与 [资产中心](raw/model-user-guide/asset-center-page/asset-center.md) 的深度集成，包括资产元数据自动同步与跨项目引用能力  

## 关键参数

| 参数名 | 类型 | 必填 | 说明 |
|--------|------|------|------|
| `asset_type` | string | 是 | 取值：`fine_tuned_model` / `inference_service` / `prompt_template` / `vector_index` |
| `version` | string | 否 | 语义化版本号（如 `v1.2.0`），未指定时默认为 `latest`；若为 `draft` 则仅限当前工作空间可见 |
| `visibility` | string | 否 | 取值：`private`（默认）、`workspace`、`public`（需管理员审批） |
| `runtime_config` | object | 否 | 依赖 `asset_type`，例如 `inference_service` 需指定 `cpu`, `memory`, `timeout`；详见 [资产中心](raw/model-user-guide/asset-center-page/asset-center.md) 中的 runtime schema 定义 |

## 使用方式

1. **Web 界面操作**：进入「模型开发」→「资产中心」，点击「+ 新建资产」，按向导选择类型并上传/配置内容  
2. **API 调用**（推荐自动化场景）：
   ```bash
   curl -X POST https://dashscope.aliyuncs.com/api/v1/assets \
     -H "Authorization: Bearer $API_KEY" \
     -H "Content-Type: application/json" \
     -d '{
           "asset_type": "fine_tuned_model",
           "source_model_id": "qwen2-7b-instruct-ft-20240510",
           "version": "v1.0.0",
           "visibility": "workspace"
         }'
   ```
3. **CLI 工具集成**：使用 `bailian-cli asset push --config asset.yaml`，配置文件结构需与 [资产中心](raw/model-user-guide/asset-center-page/asset-center.md) 所述 schema 严格一致  

## 限制和注意事项

- 单个工作空间内，同一 `asset_type` + `name` 组合最多保留 100 个历史版本（含 draft）；超出后需手动清理旧版本  
- `prompt_template` 类型资产不支持嵌套引用其他 prompt 模板（即无 `include` 语法），此行为与早期文档描述存在差异  
> **注意**：原始文档 [资产中心](raw/model-user-guide/asset-center-page/asset-center.md) 中曾提及支持 `include`，但该特性已于 v2.3.0 版本移除，当前仅保留静态变量注入能力  
- 向量知识库索引包上传大小上限为 2 GB，且必须为 `.tar.gz` 压缩包，内部目录结构须符合 [资产中心](raw/model-user-guide/asset-center-page/asset-center.md) 规定的 `index/` + `metadata.json` 格式  
- 所有资产部署后默认启用自动扩缩容（min=1, max=10 实例），如需固定实例数，须在 `runtime_config` 中显式设置 `autoscaling: false`

## 来源文档

- [资产中心](../../raw/model-user-guide/asset-center-page.md)


