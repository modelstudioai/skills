# 概述

Sandbox 是阿里云百炼提供的云端安全沙箱，为 AI 智能体提供隔离的代码执行、浏览器操作与文件处理环境，兼容 E2B SDK/API 协议接入。

Sandbox 为 AI 智能体提供云端隔离运行环境。每个实例拥有独立的计算资源、文件系统与网络，可在其中执行代码、运行命令、操作浏览器与读写文件，兼容 [E2B](https://e2b.dev/docs) SDK/API 协议。

## 核心概念

**概念**

**说明**

模版（Template）

沙箱的运行环境配置，包含基础镜像、资源规格、文件挂载、网络策略、环境变量与生命周期。创建后通过 `templateCode` 引用，可创建多个实例。

实例（Sandbox）

基于模版启动的一次运行实例，拥有独立的运行环境与网络隔离。创建后通过 `sandboxID` 引用。

基础镜像（Image）

预置运行时的镜像。当前提供代码解释器、浏览器、全能型三种。

## 基础镜像

**镜像**

**说明**

**适用场景**

代码解释器

轻量代码执行环境，支持 Python / Node.js

代码执行、数据分析、脚本运行

浏览器

浏览器执行环境，可进行 UI 操作

网页自动化、截图、UI 测试

全能型

集成多种运行时的镜像

需要多语言或综合能力的任务

## 实例生命周期

-   **创建**：基于模版启动实例，进入运行状态。
-   **暂停**：空闲时暂停实例，保留文件系统与内存状态。
-   **恢复**：连接已暂停的实例，从暂停点继续运行。
-   **释放**：不再使用时释放实例，回收资源。

**说明**实例的空闲超时与最大存活时间在模版的生命周期配置中设定，最长保持 7 天。

## 接入方式

-   **控制台**：在[快速开始](raw/application-user-guide/sandbox/sandbox-quick-start.md)页创建模版并生成 API Key，几分钟内完成从创建到调用。
-   **E2B SDK**：使用 E2B 官方 SDK，配合阿里云百炼沙箱接入地址与 API Key 调用，详见 [实例管理与使用](raw/application-user-guide/sandbox/sandbox-sdk.md)。
-   **API**：通过兼容 E2B 协议的 REST API 管理实例与模版，详见 [Sandbox API](raw/application-api-reference/sandbox-api/sandbox-api-overview.md)。

## 下一步

-   [快速开始](raw/application-user-guide/sandbox/sandbox-quick-start.md)：创建模版、生成密钥并完成首次调用
-   [模版管理](raw/application-user-guide/sandbox/sandbox-templates.md)：配置镜像、资源规格与生命周期
-   [实例管理与使用](raw/application-user-guide/sandbox/sandbox-sdk.md)：使用 E2B SDK 管理实例与数据面操作
