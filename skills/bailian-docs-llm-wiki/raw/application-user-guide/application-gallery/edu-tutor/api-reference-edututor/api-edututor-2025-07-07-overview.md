# API概览

## API标准及多语言预置SDK

本产品（`EduTutor/2025-07-07`）的OpenAPI采用[ROA](https://help.aliyun.com/zh/sdk/product-overview/roa-mechanism)签名风格。我们已经为开发者封装了常见编程语言的SDK，开发者可通过[下载SDK](https://api.aliyun.com/api-tools/sdk/EduTutor?version=2025-07-07)直接调用本产品OpenAPI而无需关心技术细节。如果现有SDK不能满足使用需求，可通过签名机制进行自签名对接。由于自签名细节非常复杂，需花费 5个工作日左右。因此建议加入我们的服务钉钉群（147535001692），在专家指导下进行签名对接。

在使用API前，您需要准备好身份账号及访问密钥（AccessKey），才能有效通过客户端工具（SDK、CLI等）访问API。细节请参见[获取AccessKey](https://help.aliyun.com/zh/ram/user-guide/create-an-accesskey-pair)。

## 自定义签名场景

若您的业务场景有特殊需求，需通过自签名方式对接 API，建议优先咨询我们的技术支持团队（服务钉钉群：147535001692），获取专业指导以确保高效接入。

## 账号与安全准备

阿里云账号具备对所有资源的完全管理权限。一旦 AccessKey 泄露，所有相关资源都将面临未经授权访问的风险。为确保安全，建议创建一个仅具备 API 访问权限的[RAM用户](https://help.aliyun.com/zh/ram/user-guide/create-a-ram-user)并配置其 AccessKey，同时基于最小权限原则 (PoLP) 配置 RAM 策略。仅在明确需要阿里云账号权限的特定场景下，才使用阿里云账号。

## API目录

API

标题

API概述

[CutQuestions](raw/application-user-guide/application-gallery/edu-tutor/api-reference-edututor/api-edututor-2025-07-07-dir/api-edututor-2025-07-07-cutquestions.md)

试卷切题

切题及题目结构化接口，客户输入试卷或整页题目图片，算法返回每个题目的位置信息以及结构化（题干、选项、答案等）信息。

[AnswerSSE](raw/application-user-guide/application-gallery/edu-tutor/api-reference-edututor/api-edututor-2025-07-07-dir/api-edututor-2025-07-07-answersse.md)

解题辅导

流式答题解析接口，客户输入需要解答题题目文本或图片，算法会返回题目详细的解答内容。
