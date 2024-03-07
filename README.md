#python tool template
build into a docker and run from there
```
$ docker build -t nrsak-py:0.1 
```
## then, example command and output
```
$ docker run -e NR_KEY=XXXXXXXXXXXXXX nrsak-py:0.1 nrsak.py GetSummary | jq '.applications[].name'
"Python Agent Test"
"Python Application"
```
