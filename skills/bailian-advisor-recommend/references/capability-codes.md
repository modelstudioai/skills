# 能力代码与偏好推断

## 能力代码表

模型的 `capabilities[]` 字段使用以下代码：

| 代码 | 含义 |
| --- | --- |
| TG | 文本生成 |
| Reasoning | 推理 |
| VU | 视觉理解 |
| IG | 图像生成 |
| VG | 视频生成 |
| TTS | 语音合成 |
| ASR | 语音识别 |
| Realtime-ASR | 实时语音识别 |
| Realtime-Text-to-Speech | 实时语音合成 |
| Realtime-Audio-Translate | 实时音频翻译 |
| Realtime-Omni | 实时全模态 |
| Multimodal-Omni | 全模态 |
| ME | 多模态嵌入 |
| TR | 翻译 |
| 3D-generation | 3D 生成 |

## 需求提取字段

从用户描述中提取以下结构化信息：

| 字段 | 说明 |
| --- | --- |
| inputModality | 输入模态：Text / Image / Video / Audio |
| outputModality | 输出模态 |
| requiredCapabilities | 所需能力（见上方能力代码表） |
| requiredFeatures | 所需特性（function-calling / web-search / structured-outputs 等） |
| budget | 预算倾向：low / medium / high |
| qualityPreference | 质量偏好：flagship / balanced / cost-optimized |
| contextNeed | 上下文需求：standard / large / extra-large |
| complexity | 单模型完成(single) 或 多模型协同(pipeline) |

## 偏好推断规则

只在用户明确表达或场景强烈暗示时偏离默认值：

| 用户信号 | 推断 |
| --- | --- |
| "低成本"、"便宜"、"省钱" | budget:low |
| "最好的"、"高精度"、"不计成本" | qualityPreference:flagship |
| 高并发场景（如"日均百万请求"） | budget:low |
| 企业级 + 准确率优先 | budget:high, qualityPreference:flagship |
| 个人学习/试玩 | budget:low, qualityPreference:cost-optimized |
| 无明确倾向 | budget:medium, qualityPreference:balanced |
