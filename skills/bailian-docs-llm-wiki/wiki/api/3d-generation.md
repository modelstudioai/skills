# 3d generation

百炼平台提供基于文本或图像输入生成3D模型的能力，当前由Tripo模型支持，适用于快速原型设计、游戏资产创建等场景。该能力通过标准API调用，返回GLB格式的3D网格文件。所有请求需通过`/v1/3d/generation`端点发起。

## 支持的模型/功能

- 当前仅支持 **Tripo-3D模型生成** 模型，暂不支持其他3D生成模型（如Luma、Stable 3D等）。
- 支持两种输入模式：纯文本描述（text-to-3D）和单张图像+可选文本提示（image-to-3D）。
- 输出为标准GLB（glTF Binary）格式，兼容主流渲染引擎与查看器。  
  详细能力说明见 [3D模型生成](../../raw/model-api-reference/3d-generation.md)。

## 关键参数

| 参数名 | 类型 | 必填 | 说明 |
|--------|------|------|------|
| `prompt` | string | 是（text-to-3D） | 中文或英文自然语言描述，建议≤200字符；避免模糊词（如“精美”“高质量”） |
| `image_url` | string | 是（image-to-3D） | 可公开访问的JPEG/PNG图像URL；尺寸建议512×512或以上，宽高比应接近1:1 |
| `negative_prompt` | string | 否 | 要排除的元素（如"low poly, text, watermark"） |
| `seed` | integer | 否 | 随机种子，用于结果复现；设为-1表示随机 |

> **注意**：原始文档 [3D模型生成](../../raw/model-api-reference/3d-generation.md) 未明确说明`image_url`是否支持Base64编码，但实测仅接受HTTP(S) URL；若传入Base64将返回400错误。

## 使用方式

1. 确保已开通3D生成服务并获取有效API Key；
2. 构造POST请求至 `https://dashscope.aliyuncs.com/api/v1/3d/generation`；
3. 请求体为JSON，包含上述参数（根据输入模式选择`prompt`或`image_url`）；
4. 同步返回任务ID（`task_id`），需轮询`/v1/tasks/{task_id}`获取结果（最长等待180秒）；
5. 成功时响应中`output.model_url`字段指向可下载的GLB文件（有效期24小时）。  
   完整调用示例与错误码详见 [3D模型生成](../../raw/model-api-reference/3d-generation.md)。

## 限制和注意事项

- 单次请求最大超时时间180秒，生成失败不重试；
- 每日调用量受配额限制，超出后返回`429 Too Many Requests`；
- 输入图像不得含人脸、敏感内容或版权受限素材（如品牌Logo、受保护角色）；
- GLB文件不含材质贴图（PBR材质暂不支持），仅包含顶点、法线与基础UV；
- 生成结果可能因提示歧义出现几何畸变或拓扑异常，建议对关键应用做人工校验。  
  具体配额策略与内容安全规则参见 [3D模型生成](../../raw/model-api-reference/3d-generation.md)。

## 来源文档

- [3D模型生成](../../raw/model-api-reference/3d-generation.md)


