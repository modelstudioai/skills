# 常见问题

Token Plan 个人版的额度、购买、订阅和接入常见问题。

## **额度与限额**

### 5 小时限额和 7 天限额是什么意思？

Token Plan 个人版采用 5 小时和每 7 天两层固定窗口限额，限额单位为 Credits。两层限额独立计算，任一层触顶即暂停服务，需等待对应窗口周期结束后额度重置。窗口期内未用完的额度不结转至下一周期。

-   **5 小时限额**：自首次调用起开启 5 小时计时窗口，窗口期内累计消耗达到限额后暂停服务，需等待满 5 小时后额度重置。
    
    例如：Standard 套餐的 5 小时限额为 3,000 Credits。您在 7 月 20 日 10:00 首次调用，系统开启窗口（10:00 ~ 15:00）。10:00 消耗 2,000 Credits，11:00 消耗 1,000 Credits，累计 3,000 Credits 触顶暂停。需等到 15:00 窗口结束，额度重置为 3,000 Credits，服务恢复。
    
-   **7 天限额**：自首次调用起开启 7 天计时窗口，窗口期内累计消耗达到限额后暂停服务，需等待满 7 天后额度重置。
    
    例如：Standard 套餐的 7 天限额为 10,000 Credits。您在 7 月 20 日首次调用，系统开启窗口（7 月 20 日 ~ 7 月 27 日）。7 月 20 日消耗 4,000 Credits，7 月 22 日消耗 6,000 Credits，累计 10,000 Credits 触顶暂停。需等到 7 月 27 日窗口结束，额度重置为 10,000 Credits，服务恢复。
    

各档位限额如下：

**档位**

**5 小时限额**

**7 天限额**

Lite 套餐

700 Credits

2,500 Credits

Standard 套餐

3,000 Credits

10,000 Credits

Pro 套餐

12,000 Credits

40,000 Credits

### 5 小时限额到了但7 天限额还有余量，还能继续使用吗？

不能。任一层限额触顶即暂停服务，可购买用量包补充额度、使用额度重置功能，或等待对应窗口周期结束后额度自动重置。

### 7 天限额是固定日期重置吗？

不是。7 天限额采用固定窗口机制，自首次调用起计时 7 天，到期后额度重置。重置时间取决于您首次调用的时间，而非固定的日历日期（如每周一）。

### 额度用完了怎么办？

限额用完后调用会被阻断，不会按量计费。恢复方式：

-   等待额度释放。
    
-   升级套餐。
    
-   购买用量包，获得不受 5 小时和 7 天限额约束的额外额度。
    

### 用量包和套餐是什么关系？需要先买套餐吗？

用量包是套餐的补充，提供不受套餐限额约束的额外 Credits，需先订阅有效套餐后才能购买，最多同时持有 5 个。

### 用量包的额度有 5 小时/周限制吗？

没有。用量包额度不受套餐的 5 小时和 7 天窗口限额约束，购买后即可使用。

### 用量包有效期多久？

用量包有效期为 1 个月，到期后未使用的额度自动作废，不支持退款。

## **接入报错**

### 常见报错及解决方案

**报错信息**

**可能原因**

**解决方案**

401 InvalidApiKey: No API-key provided.

请求头中未携带 API Key

生成 API Key 并在工具中完成配置

401 InvalidApiKey: Invalid API-key provided.

误用了按量计费的 API Key 或 Coding Plan 的 Key；订阅过期；Key 复制不完整

确认使用 Token Plan 个人版专属 API Key，确保完整且无空格

404 model 'xxx' not found or not supported

模型名称拼写错误或不在支持列表

确认模型名称区分大小写，与套餐支持的模型 ID 一致。

401 invalid access token or token expired

误用了 Coding Plan 或其他计费模式的 Base URL

使用 Token Plan 个人版专属 Base URL

401 Incorrect API key provided

误用了百炼通用 Base URL（dashscope.aliyuncs.com）

使用 Token Plan 个人版专属 Base URL

429 Requests rate limit exceeded

短时间内请求过于密集

等待一分钟后重试，降低请求频率

429 Allocated quota exceeded

5 小时或7 天限额用尽

等待窗口释放额度

## **并发与性能**

### 最多支持多少个 Agent 并发？

并发能力与套餐档位相关：

**档位**

**建议并发**

Lite 套餐

可同时支持 1-2 个 Agent 并发运行

Standard 套餐

可同时支持 3-4 个 Agent 并发运行

Pro 套餐

可同时支持 6-8 个 Agent 并发运行

### 高峰期响应会变慢吗？

高峰期可能出现排队等待。如需更稳定的吞吐，可升级到更高档位或使用团队版。

## **使用规则**

### "禁止 API 生产自动化调用"具体是什么意思？

Token Plan 个人版仅供个人通过官方指定工具（如 Cursor、Claude Code、Windsurf 等）进行交互式开发。不允许将 API Key 用于生产环境的自动化服务、批量脚本或后台定时任务等非交互场景。

### 多人共用一个账号可以吗？

不可以。Token Plan 个人版限单人使用，不允许多人共用同一账号或 API Key。如需多人协作，请使用 Token Plan 团队版。

## **购买与订阅**

### RAM 用户可以使用 Token Plan 吗？

可以，需由主账号完成以下授权：

1.  在 [RAM 控制台](https://ram.console.aliyun.com/)为该 RAM 用户授予 `AliyunTokenPlanReadOnlyAccess`（只读）或 `AliyunTokenPlanFullAccess`（管理）系统策略，同时授予 `AliyunBSSReadOnlyAccess` 系统策略。
    
2.  在百炼控制台[账号管理](https://bailian.console.aliyun.com/cn-beijing?tab=plan#/efm/subscription/uac-admin/organization/members/list)页面，为该 RAM 用户分配管理员或订阅套餐权限。
    

### 可以升配吗？升配后额度怎么算？

支持从低档位升级到更高档位。升级按剩余时长补缴差价，升级后每 5 小时限额和每 7 天限额立即提升至新档位对应额度。

### 可以降配吗？

不支持降配。如需更换为更低档位，可在订阅到期后重新购买。

### 自动续费怎么取消？

登录[百炼控制台 Token Plan](https://bailian.console.aliyun.com/cn-beijing?tab=plan#/efm/subscription/token-plan) 页面，在订阅管理中关闭自动续费。
