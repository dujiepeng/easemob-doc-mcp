# 修改消息

## 功能说明

### 功能开通

若使用该功能，需联系环信商务开通。

### 功能描述

环信即时通讯 IM 支持在服务端修改单聊、群组聊天和聊天室中发送成功的消息：

 - 文本消息：支持修改消息内容字段 `msg` 和扩展字段 `ext`。
 - 自定义消息：支持修改 `customEvent` 、`customExts` 和扩展字段 `ext`。
 - 图片/语音/视频/文件/位置消息：仅支持修改扩展字段 `ext`。
 - 命令消息：不支持修改。

### 消息修改后的生命周期

修改消息没有时间限制，即只要这条消息仍在服务端存储就可以修改。消息修改后，消息生命周期（在服务端的保存时间）会重新计算，例如，消息可在服务器上保存 180 天，用户在消息发送后的第 30 天（服务器上的保存时间剩余 150 天）修改了消息，修改成功后该消息还可以在服务器上保存 180 天。

### 消息修改后的变化

对于修改后的消息，消息体中除了内容或扩展字段变化，还新增了修改者的用户 ID、修改时间和修改次数属性。除消息体外，该消息的其他信息（例如，消息发送方、接收方）均不会发生变化。

### 接口调用频率上限

100 次/秒/App Key

## 前提条件

要调用环信即时通讯 REST API，请确保满足以下要求：

- 已在环信即时通讯控制台 [开通配置环信即时通讯 IM 服务](enable_and_configure_IM.html)。
- 了解环信 IM REST API 的调用频率限制，详见 [接口频率限制](limitationapi.html)。

## 认证方式

环信即时通讯 REST API 要求 Bearer HTTP 认证。每次发送 HTTP 请求时，都必须在请求头部填入如下 `Authorization` 字段：

`Authorization: Bearer YourAppToken`

为提高项目的安全性，环信使用 Token（动态密钥）对即将登录即时通讯系统的用户进行鉴权。本文涉及的所有消息管理 REST API 都需要使用 App Token 的鉴权方式，详见 [使用 App Token 鉴权](easemob_app_token.html)。

## HTTP 请求

```http
PUT https://{host}/{org_name}/{app_name}/messages/rewrite/{msg_id}
```

### 路径参数

| 参数       | 类型   | 是否必需 | 描述        |
| :--------- | :----- | :------- | :----------------------- |
| `host`     | String | 是       | 环信即时通讯 IM 分配的用于访问 RESTful API 的域名。详见 [获取环信即时通讯 IM 的信息](enable_and_configure_IM.html#获取环信即时通讯-im-的信息)。 |
| `org_name` | String | 是       | 环信即时通讯 IM 为每个公司（组织）分配的唯一标识。详见 [获取环信即时通讯 IM 的信息](enable_and_configure_IM.html#获取环信即时通讯-im-的信息)。  |
| `app_name` | String | 是       | 你在环信即时通讯云控制台创建应用时填入的应用名称。详见 [获取环信即时通讯 IM 的信息](enable_and_configure_IM.html#获取环信即时通讯-im-的信息)。  |
| `msg_id` | String| 是 | 要修改的消息的 ID。|

### 请求 header

| 参数       | 类型   | 是否必需 | 描述          |
| :-------------- | :----- | :------- | :-------------- |
| `Content-Type`  | String | 是       | 内容类型。请填 `application/json`。       |
| `Accept`        | String | 是       | 内容类型。请填 `application/json`。      |
| `Authorization` | String | 是       | App 管理员的鉴权 token，格式为 `Bearer YourAppToken`，其中 `Bearer` 为固定字符，后面为英文空格和获取到的 app token。 |

### 请求 body

| 参数            | 类型   | 是否必需 | 描述       |
| :-------------- | :----- | :------- | :--------------- |
| `user`| String | 否 | 修改消息的用户。|
| `new_msg` | JSON | 是 | 修改后的消息。|
| `new_msg.type` | String | 是 | 修改的消息类型：<br/> - `txt`：文本消息<br/> - `loc`：位置消息<br/> - `img`：图片消息 <br/> - `audio` ：音频消息<br/> - `video`：视频消息<br/> - `file`：文件消息<br/> - `custom`：自定义消息|
| `new_msg.msg` | String | 是 | 修改后的消息内容。**该字段只对文本消息生效。**|
| `new_msg.customEvent` | String | 否      | 用户自定义的事件类型。该参数的值必须满足正则表达式 `[a-zA-Z0-9-_/\.]{1,32}`，长度为 1-32 个字符。**该字段只对自定义消息生效。**  |
| `new_msg.customExts`  | JSON   | 否       | 用户自定义的事件属性，类型必须是 `Map<String,String>`，最多可以包含 16 个元素。**该字段只对自定义消息生效。** |
| `new_ext` | JSON | 否 | 修改后的消息扩展信息。该字段对文本、自定义、位置、图片、音频、视频和文件消息均有效。|
| `is_combine_ext` | Boolean | 否 | 修改后的消息扩展信息与原有扩展信息是合并还是替换。<br/> - （默认）`true`：合并<br/> - `false`：替换|

## HTTP 响应

### 响应 body

如果返回的 HTTP 状态码为 `200`，表示请求成功，响应 body 包含如下字段：

| 参数              | 类型   | 描述          |
| :---------------- | :----- | :------------------------------- |
| `path`            | String | 请求路径，属于请求 URL 的一部分，开发者无需关注。      |
| `uri`             | String | 请求 URL。     |
| `timestamp`       | Long   | HTTP 响应的 Unix 时间戳，单位为毫秒。  |
| `organization`    | String | 环信即时通讯 IM 为每个公司（组织）分配的唯一标识，与请求参数 `org_name` 相同。 |
| `application`     | String | 应用在系统内的唯一标识。该标识由系统生成，开发者无需关心。                     |
| `action`          | String | 请求方法。     |
| `data` | String | 值为 `success`，表示消息成功修改。| 
| `duration`        | Int    | 从发送 HTTP 请求到响应的时长，单位为毫秒。 |
| `applicationName` | String | 你在环信即时通讯云控制台创建应用时填入的应用名称，与请求参数 `app_name` 相同。 |

如果返回的 HTTP 状态码非 `200`，表示请求失败。你可以参考 [响应状态码](error.html) 了解可能的原因。

## 示例

### 请求示例

- 修改发送成功的文本消息：支持修改 `msg` 和 `ext` 字段

```bash
# 将 <YourAppToken> 替换为你在服务端生成的 App Token

curl -X PUT -i 'https://XXXX/XXXX/XXXX/messages/rewrite/1235807318835202004' \
-H 'Content-Type: application/json' \
-H 'Accept: application/json' \
-H 'Authorization: Bearer <YourAppToken>' \
-d '{
  "user": "user1",
  "new_msg": { 
    "type": "txt",
    "msg": "update message content"
  },
  "new_ext": { 
    "key1": "value1",
    "key2": "value2"
  },
  "is_combine_ext": true
}'
```

- 修改发送成功的自定义消息：支持修改 `customEvent`、`customExts` 和 `ext` 字段

```bash
# 将 <YourAppToken> 替换为你在服务端生成的 App Token

curl -X PUT -i 'https://XXXX/XXXX/XXXX/messages/rewrite/1235807318835202004' \
-H 'Content-Type: application/json' \
-H 'Accept: application/json' \
-H 'Authorization: Bearer <YourAppToken>' \
-d '{
  "user": "user1",
  "new_msg": { 
    "type": "custom",
    "customEvent": "custom_event",
    "customExts":{
      "ext_key1":"ext_value1"
    }
  },
  "new_ext": { 
    "key1": "value1",
    "key2": "value2"
  },
  "is_combine_ext": true
}'
```

- 修改发送成功的位置、图片、音频、视频和文件消息：支持修改 `ext` 字段
  
  例如，修改发送后的图片消息（不同类型的消息只是 `type` 字段的值不同）：

```bash
# 将 <YourAppToken> 替换为你在服务端生成的 App Token

curl -X PUT -i 'https://XXXX/XXXX/XXXX/messages/rewrite/1235807318835202004' \
-H 'Content-Type: application/json' \
-H 'Accept: application/json' \
-H 'Authorization: Bearer <YourAppToken>' \
-d '{
  "user": "user1",
  "new_msg": { 
    "type": "image"
  },
  "new_ext": { 
    "key1": "value1",
    "key2": "value2"
  },
  "is_combine_ext": true
}'
```

### 响应示例

```json
{
  "path": "/messages/rewrite/1235807318835202004",
  "uri": "https://XXXX/XXXX/XXXX/messages/rewrite/1235807318835202004",
  "timestamp": 1705372388118,
  "organization": "XXXX",
  "application": "ff678832-XXXX-XXXX-8130-58ac38cb6c15",
  "action": "put",
  "data": "success",
  "duration": 49,
  "applicationName": "XXXX"
}
```

## 错误码

调用该 REST API 如果返回的 HTTP 状态码非 `200`，表示请求失败，可能提示以下错误码：

| HTTP 状态码 | 错误类型   | 错误提示   | 可能原因      | 处理建议     |
|:---------|:-------------------|:----------------------|:------------------|:----------------------|
| 400      | invalid_request_body   | Request body is invalid. Please check body is correct.   | 请求体格式不正确。 | 检查请求体内容是否合法(字段类型是否正确)。 |
| 400      |  illegal_argument  | new_msg is required     | 请求参数 `new_msg` 是空。  | 输入正确的请求参数 `new_msg`。 |
| 400      | message_rewrite_error    | The message is of a type that is currently not supported for modification. | 请求参数 `msg.type` 内容不正确。 | 输入正确的请求参数 `msg.type`。|
| 400 | InvalidMessageIdException  | The provided message ID is not a valid number.  | 消息 ID 必须是数字。 | 消息 ID 只能传入数字。   |
| 404      | message_rewrite_error  | The message is unavailable or has expired.   | 请求参数 `msg_id` 不存在。 | 输入正确的请求参数 `msg_id`。     |
| 401      | message_rewrite_error   | You are not authorized to edit this message.   | 请求参数 `msg_id` 不正确。 |  输入正确的请求参数 `msg_id`。 |
| 403      | message_rewrite_error   | The message has reached its edit limit and cannot be modified further.   | 消息 `msg_id` 的修改次数到达上线。 | 消息修改次数限制在 10 次以内。   |
| 403      | message_rewrite_error   | The rewrite message feature is not open.   | 消息修改功能未开通。  |  联系商务开通消息修改功能。  |
| 404 | MessageUnavailableException  | The message is unavailable or has expired.   | 修改的消息不存在或者已经过期。 | 只能修改服务端存储的消息，若消息不存在或已过期，则不能修改。|
| 409         | concurrent_operation_error         | The message has been edited by another.    | 并发调用了修改消息接口修改同一消息。 | 避免同时请求修改同一消息。  |
| 500 | RewriteMessageInternalErrorException | An unknown error occurred while processing the request.   | 内部服务异常，修改消息失败。 |    |

关于其他异常，你可以参考 [响应状态码](error.html) 了解可能的原因。



