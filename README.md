# sius-project

How to run?
---------------
1. run `docker-compose up` in resources/ directory
2. set in project correct IP addresses (in methods: `testStatsDReporting()` and `testDynomite()`)
  
  `docker inspect --format '{{range .NetworkSettings.Networks}}{{.IPAddress}}{{end}}' <CONTAINER_ID>`
  
  (only if you're using `docker-compose` to run!)
3. set correct data source (Graphite) in Grafana (login/pass: admin/admin):

  `docker inspect --format '{{range .NetworkSettings.Networks}}{{.IPAddress}}{{end}}' resources_graphite_1`
  (Data Sources -> Add data source --- access: `direct`, url (e.g): `http://172.18.0.4`)
4. you can import dashboard (`resources/grafana.json`) in Grafana
