# 获取历史消息

<Toc />

本文介绍环信即时通讯 IM HarmonyOS SDK 如何从服务器和本地获取历史消息。

- 环信即时通讯 IM 提供消息漫游功能，即将用户的所有会话的历史消息保存在消息服务器，用户在任何一个终端设备上都能获取到历史信息，使用户在多个设备切换使用的情况下也能保持一致的会话场景。

- SDK 内部使用 SQLite 保存本地消息，你可以获取本地消息。

## 技术原理

环信即时通讯 IM HarmonyOS SDK 提供 `ChatManager` 和 `Conversation` 类支持获取服务器和本地的消息，包含如下主要方法：

- `ChatManager#fetchHistoryMessages`：根据 `FetchMessageOption` 类从服务端分页获取指定会话的历史消息；
- `ChatManager#fetchHistoryMessages`：根据 `searchOptions.from` 字段从服务器获取群组中指定成员（而非全部成员）发送的消息；
- `Conversation#searchMessagesByKeywords`：从本地获取群组中指定成员（而非全部成员）发送的消息；
- `Conversation#getAllMessages`：从本地读取指定会话的消息；
- `ChatManager#getMessage`：根据消息 ID 获取单个本地消息；
- `Conversation#getMsgCountInRange`：获取本地数据库中单个会话在某个时间段内的全部消息数。

## 前提条件

开始前，请确保满足以下条件：

- 完成 SDK 初始化并连接到服务器，详见 [快速开始](quickstart.html)。
- 了解环信即时通讯 IM API 的使用限制，详见 [使用限制](/product/limitation.html)。

## 实现方法

### 从服务器获取指定会话的消息

你可以调用 `fetchHistoryMessages` 方法基于 `FetchMessageOption` 类从服务端分页拉取单聊和群组聊天的历史消息。为确保数据可靠，我们建议你每次获取 20 条消息，最大不超过 50。分页查询时，若满足查询条件的消息总数大于 `pageSize` 的数量，则返回 `pageSize` 数量的消息，若小于 `pageSize` 的数量，返回实际条数。消息查询完毕时，返回的消息条数小于 `pageSize` 的数量。

通过设置 `FetchMessageOption` 类，你可以根据以下条件拉取历史消息：

- 消息发送方；
- 消息类型；
- 消息时间段；
- 消息搜索方向；
- 是否将拉取的消息保存到数据库；
- 对于群组聊天，你可以设置 `from` 参数拉取群组中单个成员发送的历史消息。

:::tip
1. **默认可获取单聊和群组聊天的历史消息。若要获取聊天室的历史消息，需联系环信商务。**
2. 自 1.5.0 版本开始，获取单聊历史消息时会读取服务端保存的消息送达状态和已读状态。该功能默认关闭，如果需要，请联系环信商务开通。
3. 历史消息在服务器上的存储时间与产品的套餐包相关，详见 [IM 套餐包功能详情](/product/product_package_feature.html)。
:::

```typescript
ChatClient.getInstance().chatManager()?.fetchHistoryMessages(conversationId, conversationType, pageSize, cursor, fetchMessageOption).then((result) => {
  //自 HarmonyOS SDK 1.7.0 版本开始，拉取到最后一页时，返回的 `CursorResult#getNextCursor` 由字符串 `undefined` 改为空字符串。
  let cursor = result.getNextCursor();
  let list = result.getResult();
  if (cursor && list.length === pageSize) {
    // logic of getting more historical messages
  }
})
```
 
### 从服务器获取指定群成员发送的消息

自 1.7.0 版本开始，对于单个群组会话，你可以从服务器获取指定成员（而非全部成员）发送的消息。

```typescript
ChatClient.getInstance().chatManager()?.fetchHistoryMessages({
  conversationId: this.conversationId,
  conversationType: this.conversationType,
  pageSize: 50,
  searchOptions: {
    searchDirection: SearchDirection.DOWN,
    isSave: true,
    from: [this.groupMember1, this.groupMember2]
  }
}).then((result) => {
  // success logic
});
```

### 从本地获取指定群成员发送的消息

自 1.7.0 版本开始，对于单个群组会话，你可以从本地获取指定成员（而非全部成员）发送的消息。

```typescript
let conversation = ChatClient.getInstance().chatManager()?.getConversation(this.conversationId);
if (conversation) {
  let froms = [this.groupMember1, this.groupMember2];
  conversation.searchMessagesByKeywords(this.keywords, this.timestamp, this.maxCount, froms, this.direction, this.searchScope)
    .then(messages => {
      // success logic
    }).catch((e: ChatError) => {
      // failure logic
  });
}
```

### 从本地读取指定会话的消息

你可以调用 `getAllMessages` 方法获取指定会话在内存中的所有消息。如果内存中为空，SDK 再从本地数据库中加载最近一条消息。

你也可以调用 `loadMoreMsgFromDB` 方法从本地数据库中分页加载消息，加载的消息会基于消息中的时间戳放入当前会话的内存中。

```typescript
EMConversation conversation = EMClient.getInstance().chatManager().getConversation(username);
List<EMMessage> messages = conversation.getAllMessages();
// startMsgId：查询的起始消息 ID。SDK 从该消息 ID 开始按消息时间戳的逆序加载。如果传入消息的 ID 为空，SDK 从最新消息开始按消息时间戳的逆序获取。
// pageSize：每页期望加载的消息数。取值范围为 [1,400]。
List<EMMessage> messages = conversation.loadMoreMsgFromDB(startMsgId, pagesize);
```

### 根据消息 ID 获取单个本地消息

你可以调用 `getMessage` 方法根据消息 ID 获取本地存储的指定消息。如果消息不存在会返回空值。

```typescript
// msgId：要获取消息的消息 ID。
let msg = ChatClient.getInstance().chatManager()?.getMessage(msgId);
if (msg) {
    // success logic
}
```

### 获取会话在一定时间内的消息数

你可以调用 `getMsgCountInRange` 方法从 SDK 本地数据库中获取会话在某个时间段内的全部消息数。

```typescript
//conversationId：会话 ID
let conversation = ChatClient.getInstance().chatManager()?.getConversation(conversationId);
if (!conversation) {
  return;
}
// startTimestamp：起始时间戳(包含)，单位为毫秒。
// endTimestamp：结束时间戳(包含)，单位为毫秒。
const msgCount = conversation.getMsgCountInRange(startTimestamp, endTimestamp);
```