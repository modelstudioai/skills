# model compression

模型压缩是百炼平台提供的轻量化[模型部署](../concepts/model-deployment.md)能力，通过量化、剪枝等技术降低模型体积与推理延迟，适用于边缘设备或高并发场景。该功能集成在模型服务 API 中，支持按需启用，无需修改模型结构。详细原理与适用场景可参考 [模型压缩](../../raw/model-user-guide/model-compression.md)。

## 支持的模型/功能

- 当前仅支持 Qwen 系列（Qwen1.5、Qwen2、Qwen2.5）及 Llama 系列（Llama2、Llama3）的 FP16 基座模型进行 4-bit 量化压缩；
- 支持动态 KV Cache 压缩与权重对称/非对称 INT4 量化，不支持 LoRA 微调权重的联合压缩；
- 推理时自动加载压缩后权重，无需额外转换步骤。更多兼容性说明见 [模型压缩](../../raw/model-user-guide/model-compression.md)。

## 关键参数

| 参数名 | 类型 | 默认值 | 说明 |
|--------|------|--------|------|
| `compression` | string | `none` | 可选值：`none`、`awq`（推荐）、`gptq`；`awq` 在百炼 v3.2+ 中为默认量化后端 |
| `quantization_bit` | int | `4` | 仅当 `compression != "none"` 时生效；目前仅支持 `4` |
| `quantization_group_size` | int | `128` | AWQ 分组大小，建议保持默认；过小可能导致精度下降 |

> **注意**：原始文档 [模型压缩](../../raw/model-user-guide/model-compression.md) 中提及支持 `bitsandbytes` 后端，但该后端已在 v3.1 版本中弃用，实际调用将自动降级为 AWQ，开发者应避免显式指定 `bnb` 相关配置。

## 使用方式

在 `model.deploy()` 或 `model.invoke()` 的 `parameters` 字段中传入压缩配置：

```python
model.invoke(
    input={"prompt": "你好"},
    parameters={
        "compression": "awq",
        "quantization_bit": 4
    }
)
```

部署时启用压缩需在 `model.deploy()` 中设置 `compression_config`（而非 `parameters`）：

```python
model.deploy(
    compression_config={
        "method": "awq",
        "bit": 4
    }
)
```

完整示例与错误码说明请参阅 [模型压缩](../../raw/model-user-guide/model-compression.md)。

## 限制和注意事项

- 压缩模型仅支持同步推理（`invoke`），不支持异步任务（`async_invoke`）或流式响应（`stream=True`）；
- 启用压缩后，GPU 显存占用降低约 50–60%，但首 token 延迟可能增加 10–15%（取决于序列长度）；
- 模型版本必须为平台已发布的官方压缩镜像（如 `qwen2-7b-instruct-awq`），自定义训练模型需先通过百炼控制台完成压缩镜像构建。

## 来源文档

- [模型压缩](../../raw/model-user-guide/model-compression.md)


