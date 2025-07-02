# 使用环信 App Token 鉴权

<Toc />

环信提供的 REST API 需要 app token (管理员权限 token) 才能使用，即发送 HTTP 请求时需要携带 app token。本文介绍如何获取 app token。

另外，环信 Server SDK 提供了用户、消息、群组、聊天室等资源的操作管理能力，详见 [Java Server SDK](/document/server-side/java_server_sdk.html)。

## 获取管理员权限 Token

获取 token 时，服务器会返回 token 有效期，即响应中的 `expires_in` 字段的值。由于网络延迟等原因，系统不保证 token 在此值表示的有效期内绝对有效。如果发现 token 使用异常，如返回 HTTP 状态码 401，请重新获取新的 token。

:::tip
请不要频繁向服务器发送获取 token 的请求，同一账号发送此请求超过一定频率会被服务器封禁。
:::

### HTTP 请求

```http
POST https://{host}/{org_name}/{app_name}/token
```

#### 路径参数

| 参数       | 类型   | 是否必需 | 描述                                                                                                                                            |
| :--------- | :----- | :------- | :---------------------------------------------------------------------------------------------------------------------------------------------- |
| `host`     | String | 是       | 环信即时通讯 IM 分配的用于访问 RESTful API 的域名。详见 [获取环信即时通讯 IM 的信息](enable_and_configure_IM.html#获取环信即时通讯-im-的信息)。 |
| `org_name` | String | 是       | 环信即时通讯 IM 为每个公司（组织）分配的唯一标识。详见 [获取环信即时通讯 IM 的信息](enable_and_configure_IM.html#获取环信即时通讯-im-的信息)。  |
| `app_name` | String | 是       | 你在环信即时通讯云控制台创建应用时填入的应用名称。详见 [获取环信即时通讯 IM 的信息](enable_and_configure_IM.html#获取环信即时通讯-im-的信息)。  |

#### 请求 header

| 参数           | 类型   | 是否必需 | 描述                                |
| :------------- | :----- | :------- | :---------------------------------- |
| `Content-Type` | String | 是       | 内容类型。请填 `application/json`。 |
| `Accept`       | String | 是       | 内容类型。请填 `application/json`。 |

#### 请求 body

| 参数            | 类型   | 是否必需 | 描述                                                                                                                                                                                                             |
| :-------------- | :----- | :------- | :--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `grant_type`    | String | 是       | 授权方式。该参数设置为固定字符串 `client_credentials`，即客户端凭证模式。                                                                                                                                        |
| `client_id`     | String | 是       | App 的 `client_id`，用于生成 app token 调用 REST API。详见 [环信即时通讯云控制台](https://console.easemob.com/user/login/)的`应用详情`页面。                                                                     |
| `client_secret` | String | 是       | App 的 `client_secret`，用于生成 app token 调用 REST API。详见 [环信即时通讯云控制台](https://console.easemob.com/user/login/)的`应用详情`页面。                                                                 |
| `ttl`           | Long   | 否       | token 有效期，单位为秒。<br/> - 若传入该参数，token 有效期以传入的值为准。<br/> - 若不传该参数，以 [环信即时通讯云控制台](https://console.easemob.com/user/login/)的`用户认证`页面的 token 有效期的设置为准。<br/> - 若设置为 `0`，则 token 永久有效。 <br/>注意：VIP 5 集群该参数单位为毫秒。|

### HTTP 响应

#### 响应 body

如果返回的 HTTP 状态码为 `200`，表示成功返回 token。响应 body 包含如下字段：

| 参数           | 类型   | 描述                                                 |
| :------------- | :----- | :--------------------------------------------------- |
| `access_token` | String | 有效的 Token 字符串。                                |
| `expires_in`   | Long   | Token 有效时间，单位为秒，在有效期内不需要重复获取。 |
| `application`  | String | 当前 App 的 UUID 值。                                |

如果返回的 HTTP 状态码非 `200`，表示请求失败。你可以参考 [响应状态码](/document/server-side/error.html) 了解可能的原因。

### 示例

#### 请求示例

```shell
curl -X POST -H 'Content-Type: application/json' -H 'Accept: application/json' -d '{
   "grant_type": "client_credentials",
   "client_id": "YXA6i-Ak8Ol4Eei2l11ZjV-EAg",
   "client_secret": "YXA6VunqiNxoB7IwXHInk1cGiXOOJfc",
   "ttl": 1024000
 }' 'http://a1.easemob.com/easemob-demo/testapp/token'
```

#### 响应示例

```json
{
  "access_token": "YWMte3bGuOukEeiTkNP4grL7iwAAAAAAAAAAAAAAAAAAAAGL4CTw6XgR6LaXXVmNX4QCAgMAAAFnKdc-ZgBPGgBFTrLhhyK8woMEI005emtrLJFJV6aoxsZSioSIZkr5kw",
  "expires_in": 1024000,
  "application": "8be024f0-e978-11e8-b697-5d598d5f8402"
}
```

#### 错误码

如果返回的 HTTP 状态码非 `200`，表示请求失败，可能提示以下错误码：

| HTTP 状态码 | 错误类型     | 错误提示         | 可能原因           | 处理建议       |
| :---------- | :-------- | :-------------- | :------------ | :----|
| 400         | illegal_argument    | client_id must be provided.        | 请求 body 中没有传 `client_id`。| 详见 [环信即时通讯云控制台](https://console.easemob.com/user/login/)的 **应用详情** 页面中 app key 对应的 **Client ID** 参数。 |
| 400         | illegal_argument                   | client_secret must be provided    | 请求 body 中没有传 `client_secret`。 | 详见 [环信即时通讯云控制台](https://console.easemob.com/user/login/)的 **应用详情** 页面中 app key 对应的 **ClientSecret** 参数。 |
| 400         | invalid_grant                      | client_id does not match   | app key 对应的 `client_id` 与请求 body 中传入的 `client_id` 不匹配。 | 详见 [环信即时通讯云控制台](https://console.easemob.com/user/login/)的 **应用详情** 页面中 app key 对应的 **Client ID** 参数，确保请求 body 中传入的与该参数一致。 |
| 400         | invalid_grant                      | client_secret does not match     | app key 对应的 `client_secret` 与请求 body 中传入的 `client_secret` 不匹配。 | 详见 [环信即时通讯云控制台](https://console.easemob.com/user/login/)的 **应用详情** 页面中 app key 对应的 **ClientSecret** 参数，确保请求 body 中传入的与该参数一致。 |
| 404         | organization_application_not_found | Could not find application for XXX/XXX from URI: XXX/XXX/users | App key  不存在。  | 检查 `orgName` 和 `appName` 是否正确或[创建应用](/product/enable_and_configure_IM.html#创建应用)。 |
