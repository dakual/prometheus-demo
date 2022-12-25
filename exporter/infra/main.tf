provider "kubernetes" {
  config_context_cluster = "minikube"
  config_path            = pathexpand(var.kube_config)
}

provider "helm" {
  kubernetes {
    config_path = pathexpand(var.kube_config)
  }
}

resource "kubernetes_namespace" "monitoring" {
  metadata {
    name = var.namespace
  }
}

resource "helm_release" "prometheus" {
  chart         = "prometheus"
  name          = "prometheus"
  namespace     = kubernetes_namespace.monitoring.metadata.0.name
  repository    = "https://prometheus-community.github.io/helm-charts"
  version       = "19.0.2"
  wait          = true
  wait_for_jobs = true
 
  depends_on = [
    kubernetes_namespace.monitoring
  ]
}

resource "kubernetes_secret" "grafana" {
  metadata {
    name      = "grafana-auth"
    namespace = kubernetes_namespace.monitoring.metadata.0.name
  }

  data = {
    admin-user     = "admin"
    admin-password = "123456"
  }
}

resource "helm_release" "grafana" {
  chart      = "grafana"
  name       = "grafana"
  repository = "https://grafana.github.io/helm-charts"
  namespace  = kubernetes_namespace.monitoring.metadata.0.name
  version    = "6.48.0"

  values = [
    templatefile("${path.module}/configs/grafana.yaml", {
      admin_existing_secret = kubernetes_secret.grafana.metadata[0].name
      admin_user_key        = "admin-user"
      admin_password_key    = "admin-password"
      prometheus_svc        = "${helm_release.prometheus.name}-server"
    })
  ]

  depends_on = [
    kubernetes_namespace.monitoring,
    helm_release.prometheus
  ]
}