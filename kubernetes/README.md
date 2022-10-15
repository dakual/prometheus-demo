```sh
helm repo add prometheus-community https://prometheus-community.github.io/helm-charts
helm repo add grafana https://grafana.github.io/helm-charts
helm repo update
```

```sh
kubectl create namespace monitoring
```

```sh
helm install prometheus prometheus-community/prometheus --namespace monitoring
```

```sh
helm install grafana grafana/grafana --namespace monitoring
```