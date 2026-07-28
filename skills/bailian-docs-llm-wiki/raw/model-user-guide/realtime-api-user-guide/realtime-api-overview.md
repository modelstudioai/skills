# Realtime API简介

Realtime API 是一系列针对性能、延迟、抗弱网、对接成本、适配性提供多种对接方式的方法，供客户灵活选择。

## **概述**

Realtime API 支持 **WebSocket**、**WebRTC** 和 **AOQ（AI over QUIC）**三种传输协议，开发者可以根据业务场景灵活选择。

**维度**

**WebSocket**

**WebRTC**

**AOQ**

适用场景

服务端集成、快速原型验证

浏览器端互动、传统音视频通话

AI 多模态实时交互、弱网场景、混合数据传输

浏览器兼容性

原生支持

原生支持

不支持

接入难度

极低

中等

低

弱网对抗

差

良好

极致

数据类型

文本/音频/图像

音视频 + 文本

音视频 + 文本

建连速度

慢

慢

快

回声消除/降噪

无，需客户端自行处理

内置

内置

AI 场景适配

基础，适合纯文本或低实时性场景

传统设计，AI 场景需额外适配

原生为 AI 多模态数据特征深度定制

端侧平台支持

全平台（任何支持 WebSocket 的环境）

浏览器、移动端

Android / iOS / HarmonyOS

开发者可根据实际需求选择协议方案：

-   **WebSocket 方案**：适合服务端集成、快速原型验证、对接入门槛要求极低的场景。通过 DashScope SDK 可快速实现实时语音对话。
    
-   **WebRTC 方案**：适合需要浏览器原生支持、已有 WebRTC 基础设施的传统音视频通话场景，内置回声消除和降噪能力。
    
-   **AOQ 方案**：适合对延迟、弱网对抗、多模态数据传输有极致要求的 AI 实时交互场景，同时内置回声消除和降噪能力，尤其是移动端原生应用。
    

## **模型/应用支持力度**

不同协议对模型和应用的支持情况如下：

**模型/应用类型**

**模型**

**AOQ**

**WebRTC**

**WebSocket**

实时全模态

qwen3.5-omni-plus-realtime

支持

支持

支持

qwen3.5-omni-flash-realtime

支持

支持

支持

qwen3.5-livetranslate-flash-realtime

支持

支持

支持

多模态开发套件

multimodal-dialog

不支持

支持

支持

实时语音识别

Fun-ASR系列模型

不支持

不支持

支持

实时语音合成

CosyVoice系列模型

不支持

不支持

支持

实时语音对话

qwen-audio-3.0-realtime-plus、qwen-audio-3.0-realtime-flash

不支持

不支持

支持

**说明**

模型的名称、上下文、价格、快照版本等信息请参见[阿里云百炼控制台](https://bailian.console.aliyun.com/cn-beijing#/home)；并发限流条件请参考[限流](https://help.aliyun.com/zh/model-studio/rate-limit)。
