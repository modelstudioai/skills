# 接入图像生成模型

在 Agent 工具中调用 Token Plan 图像生成模型，根据文字描述生成图片并下载到本地。

## 支持的模型

模型

说明

`qwen-image-3.0-pro`

千问图像生成与编辑 3.0 Pro，支持文生图和图生图

`qwen-image-2.0-pro`

千问图像生成 2.0 Pro（团队版专属）

`qwen-image-2.0`

千问图像生成 2.0（团队版专属）

`wan2.7-image`

万相图像生成

`wan2.7-image-pro`

万相图像生成 Pro

更多模型以[个人版](https://help.aliyun.com/zh/model-studio/token-plan-personal-overview#tppo-h-models)和[团队版](https://help.aliyun.com/zh/model-studio/token-plan-team-overview#tpto-h-models)支持的模型为准。

## 前提

-   已订阅 Token Plan，并获取以 `sk-sp-` 开头的 API Key。获取方式见[接入概览](https://help.aliyun.com/zh/model-studio/token-plan-integration-overview#tp-ext-prereq)。
-   使用的 AI 编程工具支持 Slash Command。其他工具的配置路径见[其他工具](https://help.aliyun.com/zh/model-studio/token-plan-integration-overview#tp-ext-tools)。

## 接口

`POST https://token-plan.cn-beijing.maas.aliyuncs.com/api/v1/services/aigc/multimodal-generation/generation`

请求头使用 `Authorization: Bearer $ANTHROPIC_AUTH_TOKEN`。请求体和响应字段见下文。

## 步骤一：创建 Slash Command

将套餐 API Key 配置为环境变量 `$ANTHROPIC_AUTH_TOKEN`。

在项目根目录创建 `.claude/commands/text-to-image.md`，写入以下内容：

```
调用 Token Plan 图像生成 API，根据描述生成图片并下载到本地。

图片描述：$ARGUMENTS

## 步骤

1. 从描述中提取 prompt（图片描述）、model（默认 qwen-image-3.0-pro）、size（默认 1024*1024）。如果描述中明确指定了模型，使用指定的模型名。
2. 使用 Bash 工具执行以下命令生成图片：

```bash
curl -s -X POST "https://token-plan.cn-beijing.maas.aliyuncs.com/api/v1/services/aigc/multimodal-generation/generation" \
  -H "Authorization: Bearer $ANTHROPIC_AUTH_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "model": "<model>",
    "input": {"messages": [{"role": "user", "content": [{"text": "<prompt>"}]}]},
    "parameters": {"size": "<size>"}
  }'
```

3. 从返回 JSON 的 `output.choices[0].message.content[0].image` 提取图片 URL。
4. 用 `curl -s -o "generated_$(date +%Y%m%d_%H%M%S).png" "<URL>"` 下载图片。
5. 输出生成的图片文件路径。
```

## 步骤二：生成图片

在 Claude Code 中输入 `/text-to-image 画一只猫`。如需使用其他模型，在指令中写明模型名，例如 `/text-to-image 用 wan2.7-image 画一只猫`。

## 请求参数

参数

必选

说明

`model`

是

图像生成模型 ID。

`input.messages[0].content[0].text`

是

图片描述。

`parameters.size`

否

图片尺寸，例如 `1024*1024`。不指定时由模型自动选择。

更多参数见[千问图像生成与编辑 API](raw/model-api-reference/image-generation/qwen-image-api-reference/qwen-image-generation-and-editing-api-reference.md)。

## 返回结果

-   图片 URL：`output.choices[0].message.content[0].image`。
-   用量：`usage.image_count`、`usage.width`、`usage.height`。
-   图片 URL 有时效，生成后及时下载。

## 限制

-   图片尺寸和模型支持范围以各模型文档为准。
-   计费按实际输出图片数量计算，具体以控制台[用量统计](https://bailian.console.aliyun.com/cn-beijing/subscription/token-plan/personal)为准。

## 其他工具

其他工具的扩展机制和配置路径见[接入概览](https://help.aliyun.com/zh/model-studio/token-plan-integration-overview#tp-ext-tools)。将上面的 Slash Command 内容保存到对应路径即可。
