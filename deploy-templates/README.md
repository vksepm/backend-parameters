# backend-parameters




![Version: 0.1.0](https://img.shields.io/badge/Version-0.1.0-informational?style=flat-square) ![Type: application](https://img.shields.io/badge/Type-application-informational?style=flat-square) ![AppVersion: 0.1.0](https://img.shields.io/badge/AppVersion-0.1.0-informational?style=flat-square) 

A Helm chart for Kubernetes

**Homepage:** <https://github.com/KubeRocketCI/template-flask.git>

## Maintainers

| Name | Email | Url |
| ---- | ------ | --- |
| DEV Team |  |  |

## Source Code

* <https://github.com/KubeRocketCI/template-flask.git>



## Values

| Key | Type | Default | Description |
|-----|------|---------|-------------|
| affinity | object | `{}` | https://kubernetes.io/docs/concepts/scheduling-eviction/assign-pod-node/#affinity-and-anti-affinity |
| autoscaling.enabled | bool | `false` |  |
| autoscaling.maxReplicas | int | `100` |  |
| autoscaling.minReplicas | int | `1` |  |
| autoscaling.targetCPUUtilizationPercentage | int | `80` |  |
| envFrom[0].configMapRef.name | string | `"cm-extra-env"` |  |
| envFrom[1].secretRef.name | string | `"secret-extra-env"` |  |
| env[0].name | string | `"BACKEND_PROFILES_ACTIVE"` |  |
| env[0].value | string | `"dev"` |  |
| env[1].name | string | `"ENV_VAR1"` |  |
| env[1].valueFrom.configMapKeyRef.key | string | `"ENV_VAR1"` |  |
| env[1].valueFrom.configMapKeyRef.name | string | `"cm-extra-config"` |  |
| env[2].name | string | `"ENV_VAR4"` |  |
| env[2].valueFrom.secretKeyRef.key | string | `"ENV_VAR4"` |  |
| env[2].valueFrom.secretKeyRef.name | string | `"secret-extra-config"` |  |
| fullnameOverride | string | `""` |  |
| image.pullPolicy | string | `"IfNotPresent"` |  |
| image.repository | string | `"backend-parameters"` |  |
| image.tag | string | `""` | Overrides the image tag whose default is the chart appVersion. |
| imagePullSecrets[0].name | string | `"regcred"` |  |
| ingress.annotations | object | `{}` |  |
| ingress.className | string | `""` |  |
| ingress.dnsWildcard | string | `"development.krci-dev.cloudmentor.academy"` |  |
| ingress.enabled | bool | `true` |  |
| ingress.hosts[0].host | string | `"edpDefault"` |  |
| ingress.hosts[0].paths[0].path | string | `"/"` |  |
| ingress.hosts[0].paths[0].pathType | string | `"ImplementationSpecific"` |  |
| ingress.tls | list | `[]` |  |
| livenessProbe.tcpSocket.port | string | `"http"` |  |
| nameOverride | string | `""` |  |
| nodeSelector | object | `{}` | https://kubernetes.io/docs/concepts/scheduling-eviction/assign-pod-node/#nodeselector |
| podAnnotations | object | `{}` |  |
| podLabels | object | `{}` |  |
| podSecurityContext | object | `{}` |  |
| readinessProbe.initialDelaySeconds | int | `20` |  |
| readinessProbe.tcpSocket.port | string | `"http"` |  |
| replicaCount | int | `1` |  |
| resources | object | `{}` |  |
| securityContext | object | `{}` |  |
| service.port | int | `8080` |  |
| service.type | string | `"ClusterIP"` |  |
| serviceAccount.annotations | object | `{}` | Annotations to add to the service account |
| serviceAccount.automount | bool | `true` | Automatically mount a ServiceAccount's API credentials? |
| serviceAccount.create | bool | `true` | Specifies whether a service account should be created |
| serviceAccount.name | string | `""` | The name of the service account to use. If not set and create is true, a name is generated using the fullname template |
| tolerations | list | `[]` | https://kubernetes.io/docs/concepts/scheduling-eviction/taint-and-toleration/ |
| volumeMounts[0].mountPath | string | `"/config"` |  |
| volumeMounts[0].name | string | `"configmap-volume"` |  |
| volumeMounts[0].readOnly | bool | `true` |  |
| volumeMounts[1].mountPath | string | `"/secret-config"` |  |
| volumeMounts[1].name | string | `"secret-volume"` |  |
| volumeMounts[1].readOnly | bool | `true` |  |
| volumes[0].configMap.defaultMode | int | `420` |  |
| volumes[0].configMap.items[0].key | string | `"application.properties"` |  |
| volumes[0].configMap.items[0].path | string | `"application.properties"` |  |
| volumes[0].configMap.name | string | `"cm-extra-config"` |  |
| volumes[0].name | string | `"configmap-volume"` |  |
| volumes[1].name | string | `"secret-volume"` |  |
| volumes[1].secret.defaultMode | int | `420` |  |
| volumes[1].secret.items[0].key | string | `"application.secret.properties"` |  |
| volumes[1].secret.items[0].path | string | `"application.secret.properties"` |  |
| volumes[1].secret.secretName | string | `"secret-extra-config"` |  |
