# 限流说明

记忆库 API 的请求频率限制

记忆库 API 的限流为阿里云账号级别。

API 接口

限流

全部接口

总计不超过 3000 QPM

事实记忆 add 接口

120 QPM

事实记忆 search 接口

300 QPM

超出限流时返回 HTTP `429`，建议使用退避重试策略。

如需扩容限流额度，请[提交工单](https://smartservice.console.aliyun.com/service/create-ticket)申请。

**重要**计费规则参见[计费说明](raw/application-user-guide/memory-library-overview/integration-overview/billing.md)。
