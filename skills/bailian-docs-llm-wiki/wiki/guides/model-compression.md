# model compression

模型压缩是百炼平台提供的轻量化能力，用于减小大语言模型的体积、降低推理显存占用并提升推理速度，适用于边缘部署、移动端或资源受限场景。该功能基于量化、剪枝等技术实现，支持在不显著损失精度的前提下生成更小的模型变体。所有压缩操作均在百炼控制台或 API 中完成，无需用户自行训练或修改模型结构。

## 支持的模型/功能

- 当前仅支持 Qwen 系列开源模型（如 `qwen2-7b`, `qwen2-1.5b`）的 INT4 量化压缩；  
- 不支持 Llama、Phi 等非 Qwen 架构模型，亦不支持 LoRA 微调后模型的压缩（[模型压缩](../../raw/model-user-guide/model-compression.md)）；  
- 压缩后模型保留原始 tokenizer 和生成接口兼容性，可直接用于 `model.chat()` 或 `model.generate()` 调用（[模型压缩](../../raw/model-user-guide/model-compression/model-compression-introduction.md)）。

## 关键参数

| 参数名 | 类型 | 必填 | 说明 |
|--------|------|------|------|
| `target_format` | string | 是 | 目标格式，目前仅支持 `"awq"`（推荐）和 `"gptq"`；`"awq"` 压缩后精度损失更小且推理更快 |
| `bits` | int | 是 | 量化位数，仅支持 `4`（INT4），不支持 2-bit 或 8-bit |
| `group_size` | int | 否 | 分组大小，默认 `128`；设为 `-1` 表示全通道量化（仅 `awq` 支持） |

> **注意**：文档 [模型压缩](../../raw/model-user-guide/model-compression/model-compression-introduction.md) 中提及 `"bits: 8"` 示例已过时，实际 API 拒绝 `bits != 4` 的请求，以当前控制台文档为准。

## 使用方式

1. 在百炼控制台「模型管理」→「模型压缩」页选择源模型；  
2. 配置 `target_format` 和 `bits`，点击「开始压缩」；  
3. 压缩任务完成后，系统生成新模型 ID（形如 `qwen2-7b-int4-awq-20240520`），可在模型列表中查看并部署；  
4. SDK 调用示例：
   ```python
   from dashscope import Generation
   response = Generation.call(
       model="qwen2-7b-int4-awq-20240520",
       input={"messages": [{"role": "user", "content": "你好"}]},
       api_key="YOUR_API_KEY"
   )
   ```

## 限制和注意事项

- 单次压缩任务最长耗时 90 分钟，超时将自动终止；  
- 压缩后模型不支持进一步微调（fine-tuning），仅限推理使用；  
- 不同 `target_format` 的输出模型不可互换加载（例如 AWQ 格式模型不能用 GPTQ 加载器加载）；  
- 原始模型需处于「已发布」状态，草稿或私有未发布模型无法触发压缩流程（[模型压缩](../../raw/model-user-guide/model-compression.md)）。

## 来源文档

- [模型压缩](../../raw/model-user-guide/model-compression.md)


