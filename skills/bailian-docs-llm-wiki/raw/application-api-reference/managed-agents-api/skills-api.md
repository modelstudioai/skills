# Skill

技能以 zip 包封装工具组合与文档。上传后经安全扫描方可挂载到智能体，挂载时锁定具体版本号。

## 扫描状态

新建技能或上传新版本后进入安全扫描，`status` 状态流转如下：

**状态**

**含义**

`checking`

扫描中，暂不可挂载

`active`

扫描通过，可挂载到智能体

`rejected`

命中安全风险，不可挂载；版本详情中 `additional_properties.error_info` 给出按文件路径列出的问题

`deleted`

技能已删除

挂载在智能体上完成，详见 Agent 的 `skills` 字段。挂载时必须指定具体的 `version`（不支持 `latest`），后续上传新版本不影响已挂载的智能体。

## 技能操作

**操作**

**端点**

**说明**

[创建 Skill](https://help.aliyun.com/zh/model-studio/skill-create)

`POST /skills`

用已上传的 zip 包 `file_id` 创建技能

[查询 Skill](https://help.aliyun.com/zh/model-studio/skill-get)

`GET /skills/{skill_id}`

获取技能元数据与最新版本号

[列出 Skill](https://help.aliyun.com/zh/model-studio/skill-list)

`GET /skills`

分页列出技能，支持按 `source` 过滤自建/官方

[删除 Skill](https://help.aliyun.com/zh/model-studio/skill-delete)

`DELETE /skills/{skill_id}`

删除技能及全部版本；已挂载旧版本的智能体不受影响

## 版本操作

**操作**

**端点**

**说明**

[上传 Skill 新版本](https://help.aliyun.com/zh/model-studio/skill-version-create)

`POST /skills/{skill_id}/versions`

用新的 zip 包 `file_id` 上传新版本；已挂载旧版本不受影响

[列出 Skill 版本](https://help.aliyun.com/zh/model-studio/skill-version-list)

`GET /skills/{skill_id}/versions`

分页列出该技能的全部版本，按版本号倒序

[查询 Skill 版本](https://help.aliyun.com/zh/model-studio/skill-version-get)

`GET /skills/{skill_id}/versions/{version}`

查询指定版本的元数据与扫描状态

[下载 Skill 包](https://help.aliyun.com/zh/model-studio/skill-version-download)

`GET /skills/{skill_id}/versions/{version}/content`

返回 OSS 预签名 URL（2 小时有效），用于下载 zip 包
