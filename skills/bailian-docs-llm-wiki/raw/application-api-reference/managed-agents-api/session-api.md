# Session and Event

Session 是智能体的一次运行实例，绑定智能体与环境快照，由平台驱动状态机。Event 是会话内的原子记录，由客户端写入或经订阅服务端推送。

## 状态机

会话状态字段为 `status`，状态变化通过 SSE 的 `session_status` 事件推送，详见[订阅 Event SSE 事件流](https://help.aliyun.com/zh/model-studio/event-sse-stream)。

**状态**

**触发条件**

**下一状态**

**可执行操作**

`idle`

会话创建完成，或上一轮处理结束

收到消息 → `running`

发送消息、归档、删除

`running`

收到用户消息，智能体开始处理

完成 → `idle`；不可恢复 → `terminated`

中断、审批工具调用、回填函数结果

`terminated`

归档调用、或不可恢复错误

终态

查询事件历史、删除会话

## 会话操作

**操作**

**端点**

**说明**

[创建 Session](https://help.aliyun.com/zh/model-studio/session-create)

`POST /sessions`

创建会话，绑定智能体快照与运行环境，初始状态 `idle`

[获取 Session](https://help.aliyun.com/zh/model-studio/session-get)

`GET /sessions/{session_id}`

获取会话详情，含智能体快照与当前状态

[列出 Session](https://help.aliyun.com/zh/model-studio/session-list)

`GET /sessions`

分页列出工作空间下的会话

[更新 Session](https://help.aliyun.com/zh/model-studio/session-update)

`POST /sessions/{session_id}`

更新会话元数据（标题、metadata 等）

[归档 Session](https://help.aliyun.com/zh/model-studio/session-archive)

`POST /sessions/{session_id}/archive`

软归档；会话进入 `terminated` 终态

[删除 Session](https://help.aliyun.com/zh/model-studio/session-delete)

`DELETE /sessions/{session_id}`

硬删除；事件历史一并清除，不可恢复

## 事件操作

**操作**

**端点**

**说明**

[发送 Event](https://help.aliyun.com/zh/model-studio/event-post)

`POST /sessions/{session_id}/events`

向会话注入事件（用户消息、中断、工具审批、回填函数结果等）

[列出 Event](https://help.aliyun.com/zh/model-studio/event-list)

`GET /sessions/{session_id}/events`

分页列出会话内的事件历史

[订阅 Event SSE 事件流](https://help.aliyun.com/zh/model-studio/event-sse-stream)

`GET /sessions/{session_id}/events/stream`

SSE 长连接订阅实时事件，含 `session_status` 状态变更
