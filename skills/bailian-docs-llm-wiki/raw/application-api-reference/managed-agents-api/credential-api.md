# Credential

密钥（Credential）API 提供保险箱内具体密钥的创建、查询、更新、归档与删除操作。auth 当前仅支持 environment\_variable 类型。

<a id="概述"></a>

<a id="h-credential-overview"></a>

## 概述

Credential 是 Vault 内的具体密钥条目，通过 `auth` 描述认证信息，当前仅支持 `environment_variable` 一种类型。`secret_value` 等敏感值仅写入时传入，响应中不返回明文。归档为软操作，归档后 Credential 不再注入会话，但仍可查询和恢复；删除为硬删除，不可恢复。

<a id="credential-操作"></a>

<a id="h-credential-ops"></a>

## Credential 操作

| 操作 | 端点 | 说明 |
| --- | --- | --- |
| [创建 Credential](credential-api/credential-create.md) | `POST /vaults/{vault_id}/credentials` | 在指定 Vault 中创建一个 Credential |
| [获取 Credential](credential-api/credential-get.md) | `GET /vaults/{vault_id}/credentials/{credential_id}` | 获取详情，auth 中的敏感值已脱敏 |
| [列出 Credential](credential-api/credential-list.md) | `GET /vaults/{vault_id}/credentials` | 分页列出指定 Vault 下的 Credential |
| [更新 Credential](credential-api/credential-update.md) | `POST /vaults/{vault_id}/credentials/{credential_id}` | 更新 display\_name、auth、metadata；auth 的 type 和 secret\_name 不可修改 |
| [归档 Credential](credential-api/credential-archive.md) | `POST /vaults/{vault_id}/credentials/{credential_id}/archive` | 软归档，不再注入会话，仍可查询和恢复 |
| [删除 Credential](credential-api/credential-delete.md) | `DELETE /vaults/{vault_id}/credentials/{credential_id}` | 硬删除，不可恢复 |
