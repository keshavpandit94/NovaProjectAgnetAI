# Curl Examples — Auth & Chat

Set variables (PowerShell):

```powershell
$BASE_URL = "http://127.0.0.1:8000"
```

1) Signup (create user)

```bash
curl -X POST "$BASE_URL/api/v1/auth/signup" \
  -H "Content-Type: application/json" \
  -d '{"email":"user@example.com","username":"user1","name":"User","dob":"1990-01-01","password":"password123"}'
```

2) Login (obtain access token)

```bash
curl -X POST "$BASE_URL/api/v1/auth/login" \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "username=user@example.com&password=password123"

# The response will contain {"access_token":"...","token_type":"bearer"}
# Save the token into a variable (PowerShell example):
# $TOKEN = "<paste-token-here>"
```

3) Chat (no image)

```bash
curl -X POST "$BASE_URL/api/v1/chat/" \
  -H "Authorization: Bearer <ACCESS_TOKEN>" \
  -F "user_input_text=Tell me a joke"
```

4) Chat (with image)

```bash
curl -X POST "$BASE_URL/api/v1/chat/" \
  -H "Authorization: Bearer <ACCESS_TOKEN>" \
  -F "user_input_text=Describe this image" \
  -F "image_file=@C:/path/to/image.jpg"
```

Notes:
- Replace `<ACCESS_TOKEN>` with the `access_token` value returned from login.
- If you're testing as an anonymous user, omit the `Authorization` header.
- For PowerShell, use `-F "image_file=@C:\path\to\image.jpg"` (ensure the path is correct).
