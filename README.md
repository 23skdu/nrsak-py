#python tool template
build into a docker and run from there
```
$ docker build -t nrsak-py:0.1 
```
## then, example command and output
```
$ docker run -e NR_KEY=XXXXXXXXXXXXXX nrsak-py:0.1 nrsak.py GetSummary | jq
{
  "applications": [
    {
      "id": XXXXXXXXXXXX,
      "name": "Python Agent Test",
      "language": "python",
      "health_status": "gray",
      "reporting": false,
      "settings": {
        "app_apdex_threshold": 0.5,
        "end_user_apdex_threshold": 7,
        "enable_real_user_monitoring": true,
        "use_server_side_config": false
      },
      "links": {
        "application_instances": [],
        "servers": [],
        "application_hosts": []
      }
    },
```

