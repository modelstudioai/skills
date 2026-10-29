# model compression

模型压缩是百炼平台提供的轻量化模型部署能力，支持在保持推理精度的前提下显著降低模型体积与显存占用，适用于边缘设备或高并发低延迟场景。该功能基于量化、剪枝等技术实现，目前仅面向已上线的生产环境模型开放。详细原理与适用范围参见 [模型压缩](../../raw/model-user-guide/model-compression.md)。

## 支持的模型/功能

- 仅支持已通过「模型上线」流程发布的生产模型（`status=online`），不支持草稿、测试中或下线模型；
- 当前支持 INT4/INT8 量化压缩，暂不支持结构化剪枝、知识蒸馏等高级压缩方式；
- 压缩后模型可直接用于 `model.chat` 和 `model.invoke` 接口调用，无需修改客户端代码；  
- 多模态模型暂未开放压缩支持，具体兼容列表见 [模型压缩](../../raw/model-api-reference/model-production/model-compression-api-overview/model-compression-introduction.md)。

## 关键参数

| 参数名 | 类型 | 必填 | 说明 |
|--------|------|------|------|
| `compression_type` | string | 是 | 取值：`int4` 或 `int8`；`int4` 压缩比更高但可能轻微影响长文本生成稳定性 |
| `calibration_dataset` | string | 否 | 校准数据集 ID（如 `calib-202405-v1`），仅 `int4` 必需；若未提供，系统使用默认校准集 |
| `enable_fused_attention` | boolean | 否 | 默认 `true`，启用融合注意力优化以提升压缩后吞吐；设为 `false` 可用于调试精度问题 |

> **注意**：原始文档 [模型压缩](../../raw/model-user-guide/model-compression.md) 中提及“支持动态量化”，但该能力已于 v2.3.0 版本移除，当前所有压缩均为静态量化——请以 [模型压缩](../../raw/model-api-reference/model-production/model-compression-api-overview/model-compression-introduction.md) 的 API 描述为准。

## 使用方式

1. 确保目标模型状态为 `online`，且所属工作空间具有 `model:compress` 权限；
2. 调用压缩接口（POST `/v1/models/{model_id}/compression`），示例：
   ```bash
   curl -X POST "https://dashscope.aliyuncs.com/api/v1/models/my-llm-7b/compression" \
     -H "Authorization: Bearer $API_KEY" \
     -H "Content-Type: application/json" \
     -d '{"compression_type":"int4","calibration_dataset":"calib-202405-v1"}'
   ```
3. 接口返回 `task_id`，通过 `GET /v1/tasks/{task_id}` 查询进度；成功后生成新模型版本（ID 含 `-compressed` 后缀）；
4. 使用新模型 ID 发起推理请求，行为与原模型一致。

## 限制和注意事项

- 单次压缩任务最长运行 60 分钟，超时自动失败；
- `int4` 压缩要求模型参数量 ≥ 1B，否则返回 `INVALID_MODEL_SIZE` 错误；
- 压缩过程会占用临时 GPU 资源，同一工作空间内最多并行 2 个压缩任务；
- 压缩后模型不支持微调或权重导出，仅限在线推理；如需导出，请先取消压缩再下载原始权重——详见 [模型压缩](../../raw/model-user-guide/model-compression.md)。

## 来源文档

- [模型压缩](../../raw/model-user-guide/model-compression.md)


