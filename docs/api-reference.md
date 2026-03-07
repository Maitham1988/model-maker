# API Reference

## Base URL

```
http://localhost:8000/api
```

## Endpoints

### Chat

#### Send Message
```http
POST /api/chat
Content-Type: application/json

{
  "conversation_id": "uuid-string",
  "message": "How do I treat a burn?"
}
```

**Response**: SSE stream (`text/event-stream`)
```
data: {"token": "For"}
data: {"token": " a"}
data: {"token": " burn"}
data: {"token": ","}
...
data: {"done": true, "conversation_id": "uuid"}
```

### Conversations

#### List Conversations
```http
GET /api/conversations
```
```json
[
  {
    "id": "uuid",
    "title": "First aid for burns",
    "created_at": "2026-03-07T10:30:00"
  }
]
```

#### Create Conversation
```http
POST /api/conversations
Content-Type: application/json

{
  "title": "New conversation"
}
```

#### Get Messages
```http
GET /api/conversations/{id}/messages
```
```json
[
  {
    "id": "uuid",
    "role": "user",
    "content": "How do I treat a burn?",
    "created_at": "2026-03-07T10:30:00"
  },
  {
    "id": "uuid",
    "role": "assistant",
    "content": "For a burn, immediately...",
    "created_at": "2026-03-07T10:30:05"
  }
]
```

#### Rename Conversation
```http
PUT /api/conversations/{id}
Content-Type: application/json

{
  "title": "Burns first aid"
}
```

#### Delete Conversation
```http
DELETE /api/conversations/{id}
```

### Memory

#### Get All Memory Facts
```http
GET /api/memory
```
```json
[
  {
    "id": "uuid",
    "fact": "User has penicillin allergy",
    "category": "medical",
    "created_at": "2026-03-07T10:00:00"
  }
]
```

#### Save Memory Fact
```http
POST /api/memory
Content-Type: application/json

{
  "fact": "User has penicillin allergy",
  "category": "medical"
}
```

#### Delete Memory Fact
```http
DELETE /api/memory/{id}
```

### Configuration

#### Get Config
```http
GET /api/config
```
```json
{
  "model_path": "/path/to/model.gguf",
  "chat_format": "chatml",
  "system_prompt": "You are a helpful medical assistant...",
  "setup_completed": true
}
```

#### Update Config
```http
PUT /api/config
Content-Type: application/json

{
  "system_prompt": "Updated prompt..."
}
```

### Setup

#### Get Setup Questions
```http
GET /api/setup
```

#### Complete Setup
```http
POST /api/setup
Content-Type: application/json

{}
```

## Error Responses

All errors return JSON:
```json
{
  "detail": "Error description"
}
```

| Status Code | Meaning |
|-------------|---------|
| 400 | Bad request (invalid input) |
| 404 | Resource not found |
| 500 | Server error (model not loaded, etc.) |

## SSE Stream Format

Chat responses use Server-Sent Events:

```
event: token
data: {"token": "word"}

event: done
data: {"done": true, "conversation_id": "uuid"}

event: error
data: {"error": "Error message"}
```

### JavaScript Client Example

```javascript
const eventSource = new EventSource('/api/chat?' + params);

eventSource.addEventListener('token', (e) => {
  const data = JSON.parse(e.data);
  appendToMessage(data.token);
});

eventSource.addEventListener('done', (e) => {
  eventSource.close();
});
```
