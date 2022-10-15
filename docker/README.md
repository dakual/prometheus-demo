## Monitoring up and running with Docker Compose, Prometheus and Grafana
Prometheus is an open-source monitoring application. It scrapes HTTP endpoints to collect metrics exposed in a simple text format.

### Configuration Prometheus
"scrape_configs" tell Prometheus where our applications are. Here we use "static_configs" hard-code some endpoints.

"rule_files" tells Prometheus where to search for the alert rules. 

"scrape_interval" defines how often to check for new metric values.

> prometheus/prometheus.yml
```yaml
global:
  scrape_interval: 30s
  scrape_timeout: 10s

alerting:
  alertmanagers:
    - static_configs:
      - targets: ["alertmanager:9093"]
      
rule_files:
  - /etc/prometheus/rules.yml

scrape_configs:
  - job_name: services
    metrics_path: /metrics
    static_configs:
      - targets:
          - 'prometheus:9090'
          - 'example:564'
        labels:
          sunucu: 'Web servers'
```

> /etc/prometheus/rules.yml
```yaml
groups:
- name: TestAlerts
  rules:
    - alert: InstanceDown 
      expr: up{job="services"} < 1 
      for: 5m
      labels:
        severity: critical
      annotations:
        summary: "Instance {{ $labels.instance }} down"
        description: "{{ $labels.instance }} of job {{ $labels.job }} has been down for more than 5 minutes."
```
This file contains rules which Prometheus evaluates periodically.


### Configuration Alertmanager
AlertManager takes care of handling alerts, grouping them, deduplicating them, and routing them to the appropriate services like email, chat, and PagerDuty. It can also silence and inhibit certain alerts during planned events or downtime.

> alertmanager/alertmanager.conf
```yaml
global:
  resolve_timeout: 1m

route:
  receiver: "default"

receivers:
  - name: "default"
    webhook_configs:
      - url: http://localhost:8080/send/sms
        send_resolved: true
```

### Configuration Grafana
> grafana/provisioning/datasources/datasources.yml
```yaml
apiVersion: 1

datasources:
  - name: 'prometheus'
    type: 'prometheus'
    access: 'proxy'
    url: 'http://prometheus:9090'

```

### Start Prometheus
```
docker-compose up -d
```
Grafana at http://localhost:3000/ (username/password is admin/admin)
Prometheus at http://localhost:9090/
AlertManager at http://localhost:9093/


### Reload configuration
If we use "--web.enable-lifecycle" we can reload configuration files without restarting Prometheus and Alertmanager.
```
curl -X POST http://localhost:9000/-/reload
curl -X POST http://localhost:9093/-/reload
```