# chatgpt-client

## Configuration

1. Go to [platform.openai.com/settings/organization/api-keys](https://platform.openai.com/settings/organization/api-keys)
2. Create an API keys
3. Add the API Key as environment variable in a `.env` file

```
OPENAI_API_KEY = "<open-api-key>"
```

## Troubleshooting

Check the available models:

    bash> curl https://api.openai.com/v1/models \
     -H "Authorization: Bearer YOUR_API_KEY"
