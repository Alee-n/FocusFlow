# FocusFlow API Documentation

## Base URL

```
http://127.0.0.1:5000
```

---

# Health Check

## GET /api/health

Checks API status.

### Response

```json
{
  "status": "running",
  "message": "FocusFlow API is working"
}
```

Authentication: No

---

# Login

## POST /api/login

Generates JWT token.

### Request

```json
{
  "username": "admin"
}
```

### Response

```json
{
  "success": true,
  "access_token": "jwt-token"
}
```

Authentication: No

---

# Generate Plan

## POST /api/generate-plan

Generates personalized focus plan.

### Request

```json
{
  "task": "Study",
  "time": 120,
  "energy": "high",
  "mode": "AI"
}
```

### Response

```json
{
  "success": true,
  "data": {}
}
```

Authentication: No

---

# Add Session

## POST /api/add

Adds a session record.

### Request

```json
{
  "task": "Study DSA",
  "time": 90,
  "energy": "high",
  "mode": "AI"
}
```

### Response

```json
{
  "message": "Session saved successfully"
}
```

Authentication: No

---

# Session History

## GET /api/history

Returns session statistics.

### Response

```json
{
  "user": "lia",
  "total_sessions": 10
}
```

Authentication: Yes (JWT)

---

# Admin Endpoint

## GET /api/admin

Accessible only by admin users.

### Response

```json
{
  "success": true,
  "message": "Welcome Admin"
}
```

Authentication: Yes (JWT + Admin Role)