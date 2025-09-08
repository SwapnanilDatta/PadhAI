# Deploy to Render (Free Tier)

Render offers free hosting with some limitations but good for testing.

## Prerequisites
- GitHub account
- Render account (sign up at render.com)

## Step 1: Create render.yaml

Create this file in your project root:

```yaml
# render.yaml
services:
  - type: web
    name: meeting-app
    env: python
    buildCommand: "pip install -r requirements.txt && python meeting_app/manage_production.py collectstatic --noinput"
    startCommand: "cd meeting_app && daphne meeting_app.asgi:application --port $PORT --bind 0.0.0.0"
    envVars:
      - key: SECRET_KEY
        generateValue: true
      - key: DEBUG
        value: False
      - key: DJANGO_SETTINGS_MODULE
        value: meeting_app.settings_production
      - key: ALLOWED_HOSTS
        value: meeting-app.onrender.com
    
  - type: redis
    name: meeting-app-redis
    ipAllowList: []
    
databases:
  - name: meeting-app-db
    databaseName: meeting_app
    user: meeting_app_user