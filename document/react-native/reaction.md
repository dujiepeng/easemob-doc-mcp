# 消息表情回复

<Toc />

环信即时通讯 IM 提供消息表情回复（下文统称 “Reaction”）功能。用户可以在单聊和群聊中对消息添加、删除表情。表情可以直观地表达情绪，利用 Reaction 可以提升用户的使用体验。同时在群组中，利用 Reaction 可以发起投票，根据不同表情的追加数量来确认投票。

## 技术原理

环信即时通讯 IM SDK 支持你通过调用 API 在项目中实现如下功能：

- 在消息上添加 Reaction
- 删除消息的 Reaction
- 获取消息的 Reaction 列表
- 获取 Reaction 详情

Reaction 场景示例如下：

![img](/images/ios/reactions.png)

分别展示如何添加 Reaction，群聊中 Reaction 的效果，以及查看 Reaction 列表。

## 前提条件

开始前，请确保满足以下条件：

1. 完成 `1.0.5 或以上版本` SDK 初始化，详见 [初始化](initialization.html)文档。
2. 了解环信即时通讯 IM API 的 [使用限制](/product/limitation.html)。
3. 已在[环信控制台](https://console.easemob.com/user/login)开通 Reaction 功能。

## 实现方法

### 在消息上添加 Reaction

调用 `addReaction` 在消息上添加 Reaction。对于单聊会话，对端用户会收到 `onMessageReactionDidChange` 事件，而群聊会话中，除操作者之外的其他群组成员均会收到该事件。该事件中的信息包括会话 ID、消息 ID，该消息的 Reaction 列表、Reaction 操作列表（列明添加者的用户 ID、添加的 Reaction 的 ID 以及明确该操作为添加操作）。

对于同一条 Reaction，一个用户只能添加一次，重复添加会报错误 1301。

示例代码如下：

```typescript
// reaction: Reaction ID
// msgId: 消息 ID
// 在指定消息上添加 Reaction
ChatClient.getInstance()
  .chatManager.addReaction(reaction, msgId)
  .then((result) => {
    console.log("success: ", result);
  })
  .catch((error) => {
    console.log("fail: ", error);
  });
```

### 删除消息的 Reaction

调用 `removeReaction` 删除消息的 Reaction。对于单聊会话，对端用户会收到 `onMessageReactionDidChange` 事件，而群聊会话中，除操作者之外的其他群组成员均会收到该事件。该事件中的信息包括会话 ID、消息 ID，该消息的 Reaction 列表和 Reaction 操作列表（列明删除者的用户 ID、删除的 Reaction 的 ID 以及明确该操作为删除操作）。

示例代码如下：

```typescript
// reaction: Reaction ID
// msgId: 消息 ID
ChatClient.getInstance()
  .chatManager.removeReaction(reaction, msgId)
  .then((result) => {
    console.log("success: ", result);
  })
  .catch((error) => {
    console.log("fail: ", error);
  });
```

### 获取消息的 Reaction 列表

调用 `getReactionList` 方法可以从服务器获取指定消息的 Reaction 概览列表，列表内容包含 Reaction 内容，添加或移除 Reaction 的用户数量，以及添加或移除 Reaction 的前三个用户的用户 ID。

对应消息 `ChatMessage` 有便捷的访问方式 `reactionList`。

示例代码如下：

```typescript
// msgId: 消息 ID
ChatClient.getInstance()
  .chatManager.getReactionList(msgId)
  .then((result) => {
    console.log("success: ", result);
  })
  .catch((error) => {
    console.log("fail: ", error);
  });
```

消息的快捷访问方式。示例如下：

```typescript
// 通过消息快捷访问 Reaction 列表
const msg = ChatMessage.createTextMessage(targetId, content);
msg.reactionList
  .then((result) => {
    console.log("success: ", result);
  })
  .catch((error) => {
    console.log("fail: ", error);
  });
```

### 获取 Reaction 详情

调用 `fetchReactionDetail` 方法可以从服务器获取指定 Reaction 的详情，包括 Reaction 内容，添加或移除 Reaction 的用户数量以及添加或移除 Reaction 的全部用户列表。示例代码如下：

```typescript
// reaction: Reaction ID
// msgId: 消息 ID
// pageSize: 单次请求返回的成员数，取值范围为 [1, 50]
// cursor: 开始获取数据的游标位置，首次调用方法时传 `null` 或空字符串
ChatClient.getInstance()
  .chatManager.fetchReactionDetail(msgId, reaction, cursor, pageSize)
  .then((result) => {
    console.log("success: ", result);
  })
  .catch((error) => {
    console.log("fail: ", error);
  });
```

### 管理 Reaction 监听

```typescript
// 监听 Reaction 更新
class ChatMessageEvent implements ChatMessageEventListener {
  onMessageReactionDidChange(_list: ChatMessageReactionEvent[]): void {
    throw new Error("Method not implemented.");
  }
  // 其他回调接收省略，实际开发中需要添加
}

// 注册监听器
const listener = new ChatMessageEvent();
ChatClient.getInstance().chatManager.addMessageListener(listener);

// 移除监听器
ChatClient.getInstance().chatManager.removeMessageListener(listener);

// 移除所有监听器
ChatClient.getInstance().chatManager.removeAllMessageListener();
```