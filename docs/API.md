# API 参考文档

**版本:** 1.0
**更新:** 2026-04-10

---

## 概述

本文档描述老庄与小花官网的 API 接口。

**Base URL:** `https://dengpao.pages.dev/api`

---

## 通用说明

### 请求格式

```http
Content-Type: application/json
```

### 响应格式

```json
{
  "success": true,
  "data": { ... },
  "message": "操作成功"
}
```

### 错误响应

```json
{
  "success": false,
  "error": {
    "code": "VALIDATION_ERROR",
    "message": "输入验证失败"
  }
}
```

---

## 评论系统

### 获取评论列表

获取分页的评论列表。

**Endpoint:** `GET /comments`

**Query Parameters:**

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| page | integer | 否 | 页码，默认 1 |
| limit | integer | 否 | 每页数量，默认 10 |

**Example Request:**
```http
GET /comments?page=1&limit=10
```

**Example Response:**
```json
{
  "success": true,
  "data": {
    "comments": [
      {
        "id": "cmt_abc123",
        "nickname": "AI龙虾 🦞",
        "content": "这个网站真棒！",
        "location": "北京",
        "created_at": "2026-04-10T12:00:00Z",
        "replies": []
      }
    ],
    "pagination": {
      "page": 1,
      "limit": 10,
      "total": 42,
      "total_pages": 5
    }
  }
}
```

---

### 提交评论

提交新的评论。

**Endpoint:** `POST /comments`

**Request Body:**

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| nickname | string | 是 | 昵称，最多 20 字符 |
| content | string | 是 | 评论内容，最多 500 字符 |
| location | string | 否 | 位置信息 |

**Example Request:**
```http
POST /comments
Content-Type: application/json

{
  "nickname": "游客",
  "content": "写得真好！",
  "location": "上海"
}
```

**Example Response:**
```json
{
  "success": true,
  "data": {
    "id": "cmt_xyz789",
    "nickname": "游客",
    "content": "写得真好！",
    "location": "上海",
    "created_at": "2026-04-10T14:00:00Z"
  },
  "message": "评论提交成功"
}
```

---

### 提交回复

对已有评论进行回复。

**Endpoint:** `POST /comments/:id/replies`

**Path Parameters:**

| 参数 | 类型 | 说明 |
|------|------|------|
| id | string | 父评论 ID |

**Request Body:**

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| nickname | string | 是 | 回复者昵称 |
| content | string | 是 | 回复内容 |

**Example Request:**
```http
POST /comments/cmt_abc123/replies
Content-Type: application/json

{
  "nickname": "小花",
  "content": "谢谢支持！"
}
```

**Example Response:**
```json
{
  "success": true,
  "data": {
    "id": "reply_456",
    "nickname": "小花",
    "content": "谢谢支持！",
    "created_at": "2026-04-10T15:00:00Z"
  },
  "message": "回复提交成功"
}
```

---

## 相册 API

### 获取照片列表

获取按年份分组的照片列表。

**Endpoint:** `GET /photos`

**Query Parameters:**

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| year | string | 否 | 年份筛选，如 "2018" |
| limit | integer | 否 | 每组返回数量，默认 20 |

**Example Request:**
```http
GET /photos?year=2018&limit=10
```

**Example Response:**
```json
{
  "success": true,
  "data": {
    "years": ["2013", "2014", "2015", ...],
    "photos": {
      "2018": [
        {
          "file": "IMG_0008.JPG",
          "folder": "2018年",
          "thumbnail": "/thumbnails/IMG_0008.JPG",
          "original": "/images/IMG_0008.JPG"
        }
      ]
    },
    "total": 340
  }
}
```

---

## 错误代码

| 代码 | HTTP 状态 | 说明 |
|------|-----------|------|
| VALIDATION_ERROR | 400 | 输入验证失败 |
| UNAUTHORIZED | 401 | 未授权访问 |
| NOT_FOUND | 404 | 资源不存在 |
| RATE_LIMITED | 429 | 请求过于频繁 |
| SERVER_ERROR | 500 | 服务器内部错误 |

---

*文档版本: 1.0 | 最后更新: 2026-04-10*
