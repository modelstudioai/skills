# model deployment 1

`model deployment 1` 是百炼平台提供的基础[模型部署](../concepts/model-deployment.md)能力，面向开发者提供多种部署模式以适配不同性能、成本与隔离性需求。它支持从快速验证到生产级服务的全周期部署场景，覆盖模型导入、API 发布、流量路由等关键环节。该能力在 [模型部署 (raw/model-user-guide/model-deployment-1.md)](../../raw/model-user-guide/model-deployment-1.md) 中首次系统定义。

## 支持的模型/功能

- **部署模式**：支持专属部署、PTU 预置吞吐部署、独占算力部署（MU/DTU）、[Token](../concepts/token.md) 按量部署四类核心模式，分别适用于高稳定性要求、长上下文+缓存优化、强资源隔离、弹性计费等场景。  
- **模型来源**：支持通过 [模型导入](https://help.aliyun.com/zh/model-studio/model-import) 接入自定义模型，也支持直接部署百炼官方托管模型（见 [我的模型](https://help.aliyun.com/zh/model-studio/my-model-center)）。  
- **服务集成**：提供标准 RESTful API 接口，并支持 [模型路由](https://help.aliyun.com/zh/model-studio/model-routing) 实现多模型灰度与 A/B 测试。所有部署流程均可通过 [API 部署指南](https://help.aliyun.com/zh/model-studio/model-deployment-quick-start) 快速上手——该指南内容与 [模型部署 (raw/model-user-guide/model-deployment-1.md)](../../raw/model-user-guide/model-deployment-1.md) 的能力范围一致。

## 关键参数

| 参数 | 类型 | 说明 | 是否必需 |
|------|------|------|----------|
| `model_id` | string | 模型唯一标识，来自 [我的模型](https://help.aliyun.com/zh/model-studio/my-model-center) 或导入后生成 | 是 |
| `deployment_type` | enum | 取值：`dedicated` / `ptu` / `dtu` / `token`，对应四类部署模式 | 是 |
| `instance_count` | int | 实例数（仅 `dedicated` 和 `dtu` 模式生效）；`ptu` 模式由 `ptu_capacity` 控制吞吐 | 否（默认 1） |
| `ptu_capacity` | int | PTU 模式下预置吞吐单位（1 PTU ≈ 10 QPS@1k token），需在 [PTU 预置吞吐部署](https://help.aliyun.com/zh/model-studio/ptu-long-input-and-cache) 文档中查表换算 | 仅 `ptu` 模式必需 |

> **注意**：原始文档中 `deployment_type=mu` 的提法已过时，当前统一归入 `dtu` 类型；实际配置请以控制台或 OpenAPI Schema 为准，避免参考旧版 [独占算力部署（MU/DTU）](https://help.aliyun.com/zh/model-studio/dtu-model-deployment) 页面中 MU 独立分类的描述。

## 使用方式

1. 登录百炼控制台 → 进入「[模型部署](../concepts/model-deployment.md)」页；
2. 选择目标模型（来自 [我的模型](https://help.aliyun.com/zh/model-studio/my-model-center) 或已导入模型）；
3. 选择部署类型，填写关键参数（如 `instance_count` 或 `ptu_capacity`）；
4. 点击「部署」，等待状态变为 `Running` 后，即可调用返回的 endpoint；
5. 全流程操作细节详见 [API 部署指南](https://help.aliyun.com/zh/model-studio/model-deployment-quick-start)，该指南与 [模型部署 (raw/model-user-guide/model-deployment-1.md)](../../raw/model-user-guide/model-deployment-1.md) 的能力边界完全对齐。

## 限制和注意事项

- [Token](../concepts/token.md) 按量模式不支持流式响应（`stream=true`）；
- PTU 模式下最大上下文长度受 `ptu_capacity` 与模型原生限制双重约束，需结合 [PTU 预置吞吐部署](https://help.aliyun.com/zh/model-studio/ptu-long-input-and-cache) 中的规格表校验；
- 所有部署实例默认开启自动扩缩容（除 `dedicated` 模式外），缩容冷却期为 5 分钟；
- 模型导入后需完成「校验」与「构建」步骤方可部署，该流程依赖 [模型导入](https://help.aliyun.com/zh/model-studio/model-import) 文档定义的规范。

## 来源文档

- [模型部署](../../raw/model-user-guide/model-deployment-1.md)



