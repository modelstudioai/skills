# specialized model

百炼平台提供专用模型（Specialized Model）用于特定领域任务。当前该类别下包含 GUI-Plus 界面交互模型，专为自动化操作计算机图形界面而设计，能够根据屏幕截图识别界面元素并生成相应的鼠标键盘操作指令。详细的接口规范请参考 [GUI-Plus API参考](../../raw/model-api-reference/specialized-model/gui-plus-interface-interaction-model.md)。

## 支持的模型

| 模型名称 | 用途 | 调用方式 |
|---------|------|---------|
| `gui-plus-2026-02-26` | 界面交互自动化（Computer Use） | [OpenAI 兼容接口](../concepts/openai-compatible-api.md) / DashScope API |

GUI-Plus 模型接收屏幕截图和用户指令作为输入，输出结构化的操作动作（如点击、输入、滚动等），适用于 RPA、自动化测试、智能助手等场景。

## 调用方式

GUI-Plus 支持通过 [OpenAI 兼容接口](../concepts/openai-compatible-api.md)调用，基础配置如下：

- **Base URL**：`https://dashscope.aliyuncs.com/compatible-mode/v1`
- **Endpoint**：`POST https://dashscope.aliyuncs.com/compatible-mode/v1/chat/completions`

调用前需要获取 API Key 并配置到环境变量 `DASHSCOPE_API_KEY`。如使用 OpenAI SDK 调用，还需安装对应语言的 SDK。

### 请求结构

请求体遵循 OpenAI Chat Completions 格式，核心要素包括：

- **system message**：包含工具定义（`computer_use` 函数签名）和响应格式要求
- **user message**：包含屏幕截图（`image_url` 类型）和用户文本指令
- **额外参数**：建议设置 `vl_high_resolution_images: true` 以启用高分辨率图片处理

根据 [GUI-Plus API参考](../../raw/model-api-reference/specialized-model/gui-plus-interface-interaction-model.md) 中的示例，支持 Python、Node.js 和 curl 三种调用方式。

## 核心功能：computer_use 工具

模型通过内置的 `computer_use` 工具函数执行界面操作，支持以下动作类型：

| 动作 | 说明 | 必需参数 |
|------|------|---------|
| `left_click` | 在指定坐标左键单击 | `coordinate` |
| `double_click` | 在指定坐标双击 | `coordinate` |
| `right_click` | 在指定坐标右键单击 | `coordinate` |
| `middle_click` | 在指定坐标中键单击 | `coordinate` |
| `mouse_move` | 移动光标到指定坐标 | `coordinate` |
| `left_click_drag` | 拖拽到指定坐标 | `coordinate` |
| `key` | 按键操作 | `keys` |
| `type` | 键盘输入文本 | `text` |
| `scroll` / `hscroll` | 垂直/水平滚动 | `pixels` |
| `wait` | 等待指定秒数 | `time` |
| `terminate` | 终止任务并报告状态 | `status`（success/failure） |
| `answer` | 回答问题 | `text` |
| `interact` | 处理弹窗交互 | `text` |

坐标参数 `coordinate` 为 `[x, y]` 格式，以像素为单位，屏幕默认分辨率为 1000x1000。

## 使用注意事项

- 点击界面元素时应瞄准元素中心位置，避免点击边缘
- 部分应用启动或执行操作后需要等待，可能需要多次截图确认操作结果
- 模型输出格式为 Action 描述 + `<tool_call>` XML 块，包含结构化的 JSON 操作指令
- 任务完成时应使用 `terminate` 动作报告最终状态
- 更多使用细节和完整参数说明参见 [GUI-Plus API参考](../../raw/model-api-reference/specialized-model/gui-plus-interface-interaction-model.md)

## 来源文档

- [GUI-Plus API参考](../../raw/model-api-reference/specialized-model/gui-plus-interface-interaction-model.md)


