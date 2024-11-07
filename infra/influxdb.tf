resource "kubernetes_namespace" "influxdb" {
  metadata {
    name = "influxdb"
  }
}

resource "kubernetes_service_account" "influxdb" {
  metadata {
    name      = "influxdb"
    namespace = kubernetes_namespace.influxdb.metadata[0].name
  }
}

resource "kubernetes_persistent_volume_claim" "influxdb" {
  metadata {
    name      = "influxdb-data"
    namespace = kubernetes_namespace.influxdb.metadata[0].name
  }
  spec {
    access_modes = ["ReadWriteOnce"]
    resources {
      requests = {
        storage = "100Gi"
      }
    }
  }

}

resource "kubernetes_secret" "influxdb" {
  metadata {
    name      = "influxdb"
    namespace = kubernetes_namespace.influxdb.metadata[0].name
  }
  data = {
    DOCKER_INFLUXDB_INIT_PASSWORD = "thefunktion"
  }
}

resource "kubernetes_deployment" "influxdb" {
  metadata {
    name      = "influxdb"
    namespace = kubernetes_namespace.influxdb.metadata[0].name
    labels = {
      app = "influxdb"
    }
  }
  spec {
    replicas = 1
    strategy {
      type = "Recreate"
    }
    selector {
      match_labels = {
        app = "influxdb"
      }
    }
    template {

      metadata {
        labels = {
          app = "influxdb"
        }
      }
      spec {
        service_account_name = "influxdb"
        security_context {
          fs_group = "1000"
        }
        container {

          image = "influxdb:2.7.10-alpine"
          name  = "influxdb"
          env {
            name  = "DOCKER_INFLUXDB_INIT_MODE"
            value = "setup"
          }
          env {
            name  = "DOCKER_INFLUXDB_INIT_ORG"
            value = "influxdata"
          }
          env {
            name  = "DOCKER_INFLUXDB_INIT_BUCKET"
            value = "default"
          }
          env {
            name  = "DOCKER_INFLUXDB_INIT_USERNAME"
            value = "thefunktion"
          }
          env {
            name  = "INFLUXD_BOLT_PATH"
            value = "/var/lib/influxdb2/influxd.bolt"
          }
          env_from {
            secret_ref {
              name = kubernetes_secret.influxdb.metadata[0].name
            }
          }
          port {
            container_port = 8086
            name           = "influxdb"
            protocol       = "TCP"
          }
          volume_mount {
            mount_path = "/var/lib/influxdb2"
            name       = "data"
          }
          liveness_probe {
            http_get {
              path = "/health"
              port = "influxdb"
            }
            initial_delay_seconds = 30
            period_seconds        = 10
          }
          readiness_probe {
            http_get {
              path = "/health"
              port = "influxdb"
            }
            initial_delay_seconds = 5
            period_seconds        = 5
          }
          startup_probe {
            http_get {
              path = "/health"
              port = "influxdb"
            }
            failure_threshold = 30
            period_seconds    = 10
          }
        }


        volume {
          name = "data"
          persistent_volume_claim {
            claim_name = "influxdb-data"
          }
        }
      }

    }

  }
}

resource "kubernetes_service" "influxdb" {
  metadata {
    name      = "influxdb"
    namespace = kubernetes_namespace.influxdb.metadata[0].name
  }
  spec {
    selector = {
      app = "influxdb"
    }
    type = "ClusterIP"
    port {
      port        = 8086
      target_port = 8086
    }
  }
}


