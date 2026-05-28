# API概览

## API标准及多语言预置SDK

本产品（`通义拍照解题辅导/2025-07-07`）的 OpenAPI 采用 ROA 签名机制，具体签名方式请参见[签名机制说明](https://help.aliyun.com/zh/sdk/product-overview/v3-request-structure-and-signature)。我们已为开发者封装了主流编程语言的 SDK，您可通过 [下载 SDK](https://api.aliyun.com/api-tools/sdk/EduTutor?version=2025-07-07) 快速调用 API，无需关注签名等底层实现细节，显著降低开发门槛与集成复杂度。

## 自定义签名场景

若您的业务场景有特殊需求，需通过自签名方式对接 API，建议优先咨询我们的技术支持团队（服务钉钉群：147535001692），获取专业指导以确保高效接入。

## 账号与安全准备

阿里云账号具备对所有资源的完全管理权限。一旦 AccessKey 泄露，所有相关资源都将面临未经授权访问的风险。为确保安全，建议创建一个仅具备 API 访问权限的 [RAM 用户](https://help.aliyun.com/zh/ram/user-guide/create-a-ram-user)并配置其 AccessKey，同时基于最小权限原则 (PoLP) 配置 RAM 策略。仅在明确需要阿里云账号权限的特定场景下，才使用阿里云账号。

## API目录

API

标题

API概述

[CutQuestions](https://help.aliyun.com/zh/model-studio/api-edututor-2025-07-07-cutquestions)

试卷切题

切题及题目结构化接口，客户输入试卷或整页题目图片，算法返回每个题目的位置信息以及结构化（题干、选项、答案等）信息。

[AnswerSSE](https://help.aliyun.com/zh/model-studio/api-edututor-2025-07-07-answersse)

解题辅导

流式答题解析接口，客户输入需要解答题题目文本或图片，算法会返回题目详细的解答内容。
