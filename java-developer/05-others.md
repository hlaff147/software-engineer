# Other Topics (Kafka, Kubernetes, Docker, SQL)

## 28. What is the difference between Kafka topics and partitions?

| Aspect | Topic | Partition |
|--------|-------|-----------|
| **Definition** | Logical category/feed name | Physical division of a topic |
| **Purpose** | Organize messages by type | Enable parallelism and scaling |
| **Ordering** | No ordering guarantee | Guaranteed order within partition |
| **Consumers** | Multiple groups can subscribe | One consumer per partition per group |

```
Topic: "orders" (3 partitions)
┌─────────────────────────────────────────┐
│  Partition 0: [msg1] [msg4] [msg7] ...  │  → Consumer 1
│  Partition 1: [msg2] [msg5] [msg8] ...  │  → Consumer 2
│  Partition 2: [msg3] [msg6] [msg9] ...  │  → Consumer 3
└─────────────────────────────────────────┘
```

**Key points:**
- **Topics** = logical grouping (e.g., `user-events`, `orders`)
- **Partitions** = parallelism unit (more partitions = higher throughput)
- Messages with same key → same partition (ordering preserved)
- Replication factor applies per partition

```java
// Send to specific partition via key
producer.send(new ProducerRecord<>("orders", orderId, orderJson));
// All orders with same orderId go to same partition
```

---

## 29. How do StatefulSets in Kubernetes differ from Deployments?

| Aspect | Deployment | StatefulSet |
|--------|------------|-------------|
| **Pod identity** | Random names (pod-xyz123) | Stable names (pod-0, pod-1) |
| **Storage** | Shared or ephemeral | Persistent per pod |
| **Scaling** | Parallel | Sequential (ordered) |
| **Network** | Random DNS | Stable DNS per pod |
| **Use case** | Stateless apps | Databases, Kafka, Zookeeper |

**Deployment:**
```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: web-app
spec:
  replicas: 3
  template:
    spec:
      containers:
        - name: app
          image: nginx
```

**StatefulSet:**
```yaml
apiVersion: apps/v1
kind: StatefulSet
metadata:
  name: postgres
spec:
  serviceName: "postgres"
  replicas: 3
  template:
    spec:
      containers:
        - name: postgres
          image: postgres:15
          volumeMounts:
            - name: data
              mountPath: /var/lib/postgresql/data
  volumeClaimTemplates:
    - metadata:
        name: data
      spec:
        accessModes: ["ReadWriteOnce"]
        resources:
          requests:
            storage: 10Gi
```

**StatefulSet DNS:** `postgres-0.postgres.namespace.svc.cluster.local`

---

## 30. SQL query to get the 2nd highest salary in a department

```sql
-- Method 1: Using DENSE_RANK() (handles ties)
SELECT department_id, employee_name, salary
FROM (
    SELECT 
        department_id,
        employee_name,
        salary,
        DENSE_RANK() OVER (PARTITION BY department_id ORDER BY salary DESC) as rank
    FROM employees
) ranked
WHERE rank = 2;

-- Method 2: Using LIMIT/OFFSET (per department with subquery)
SELECT e.department_id, e.employee_name, e.salary
FROM employees e
WHERE e.salary = (
    SELECT DISTINCT salary 
    FROM employees 
    WHERE department_id = e.department_id
    ORDER BY salary DESC
    LIMIT 1 OFFSET 1
);

-- Method 3: Using correlated subquery
SELECT e1.department_id, e1.employee_name, e1.salary
FROM employees e1
WHERE 1 = (
    SELECT COUNT(DISTINCT e2.salary)
    FROM employees e2
    WHERE e2.department_id = e1.department_id
      AND e2.salary > e1.salary
);

-- Method 4: Using CTE (Common Table Expression)
WITH RankedSalaries AS (
    SELECT 
        department_id,
        employee_name,
        salary,
        ROW_NUMBER() OVER (PARTITION BY department_id ORDER BY salary DESC) as rn
    FROM employees
)
SELECT department_id, employee_name, salary
FROM RankedSalaries
WHERE rn = 2;
```

**Note:** Use `DENSE_RANK()` if ties should share the same rank.

---

## 31. What are readiness probes in Kubernetes, and how do they differ from liveness probes?

| Aspect | Liveness Probe | Readiness Probe |
|--------|----------------|-----------------|
| **Purpose** | Is the container alive? | Is the container ready to serve? |
| **Failure action** | Restart container | Remove from Service endpoints |
| **Use case** | Detect deadlocks | Warm-up, dependency checks |

```yaml
apiVersion: v1
kind: Pod
spec:
  containers:
    - name: app
      image: myapp
      
      # Liveness: restart if unhealthy
      livenessProbe:
        httpGet:
          path: /healthz
          port: 8080
        initialDelaySeconds: 30
        periodSeconds: 10
        failureThreshold: 3
      
      # Readiness: remove from load balancer if not ready
      readinessProbe:
        httpGet:
          path: /ready
          port: 8080
        initialDelaySeconds: 5
        periodSeconds: 5
        failureThreshold: 3
      
      # Startup: for slow-starting containers (K8s 1.20+)
      startupProbe:
        httpGet:
          path: /healthz
          port: 8080
        failureThreshold: 30
        periodSeconds: 10
```

**Spring Boot implementation:**
```java
@Component
public class ReadinessIndicator implements HealthIndicator {
    @Override
    public Health health() {
        if (cacheWarmedUp && databaseConnected) {
            return Health.up().build();
        }
        return Health.down().build();
    }
}
```

---

## 32. How do you implement request tracing across multiple microservices?

**Use Distributed Tracing (OpenTelemetry/Jaeger/Zipkin):**

```xml
<!-- Spring Boot with Micrometer Tracing -->
<dependency>
    <groupId>io.micrometer</groupId>
    <artifactId>micrometer-tracing-bridge-otel</artifactId>
</dependency>
<dependency>
    <groupId>io.opentelemetry</groupId>
    <artifactId>opentelemetry-exporter-zipkin</artifactId>
</dependency>
```

```yaml
management:
  tracing:
    sampling:
      probability: 1.0  # 100% in dev, lower in prod
  zipkin:
    tracing:
      endpoint: http://zipkin:9411/api/v2/spans
```

**Trace context propagation:**
```
Service A → Service B → Service C
    │           │           │
    └─ traceId: abc123 ─────┘
       spanId:  span1   span2   span3
```

**How it works:**
1. First service generates `traceId` and `spanId`
2. Headers propagated: `traceparent: 00-{traceId}-{spanId}-01`
3. Each service creates child span with same `traceId`
4. All spans sent to collector (Jaeger/Zipkin)

```java
// Manual span creation (optional)
@Autowired
private Tracer tracer;

public void processOrder(Order order) {
    Span span = tracer.nextSpan().name("process-order").start();
    try (Tracer.SpanInScope ws = tracer.withSpan(span)) {
        // Add custom tags
        span.tag("orderId", order.getId());
        // Business logic
    } finally {
        span.end();
    }
}
```

---

## 33. What is the difference between Docker volumes and bind mounts?

| Aspect | Volumes | Bind Mounts |
|--------|---------|-------------|
| **Location** | Managed by Docker (`/var/lib/docker/volumes/`) | Anywhere on host |
| **Portability** | Yes (works across hosts) | No (host path dependent) |
| **Management** | Docker CLI (`docker volume`) | Manual |
| **Performance** | Optimized for containers | Depends on host FS |
| **Best for** | Persistent data (DBs) | Development (source code) |

**Volume:**
```bash
# Create named volume
docker volume create mydata

# Use in container
docker run -v mydata:/app/data myimage

# Or in compose
volumes:
  - mydata:/var/lib/postgresql/data

volumes:
  mydata:
```

**Bind Mount:**
```bash
# Mount host directory
docker run -v /host/path:/container/path myimage

# Or in compose (development)
volumes:
  - ./src:/app/src
  - ./config:/app/config:ro  # read-only
```

**Best practices:**
- **Volumes** for databases, persistent state
- **Bind mounts** for development hot-reload
- **tmpfs** for sensitive data (in-memory only)

---

## 34. How do you implement rolling updates in Kubernetes?

**Deployment strategy:**
```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: myapp
spec:
  replicas: 4
  strategy:
    type: RollingUpdate
    rollingUpdate:
      maxUnavailable: 1    # Max pods down during update
      maxSurge: 1          # Max extra pods during update
  template:
    spec:
      containers:
        - name: app
          image: myapp:v2
          readinessProbe:  # Critical for safe rollouts
            httpGet:
              path: /ready
              port: 8080
```

**Update process:**
```
Initial: [v1] [v1] [v1] [v1]  (4 replicas)

Step 1:  [v1] [v1] [v1] [v1] [v2]  (maxSurge: 1 new pod)
Step 2:  [v1] [v1] [v1] [v2]       (terminate 1 old, maxUnavailable: 1)
Step 3:  [v1] [v1] [v1] [v2] [v2]  (add new)
...
Final:   [v2] [v2] [v2] [v2]       (all updated)
```

**Commands:**
```bash
# Trigger update by changing image
kubectl set image deployment/myapp app=myapp:v2

# Or apply updated manifest
kubectl apply -f deployment.yaml

# Watch rollout
kubectl rollout status deployment/myapp

# Rollback if issues
kubectl rollout undo deployment/myapp

# Rollback to specific revision
kubectl rollout undo deployment/myapp --to-revision=2

# History
kubectl rollout history deployment/myapp
```

**Best practices:**
1. Always have `readinessProbe` configured
2. Use `PodDisruptionBudget` for high availability
3. Set resource limits
4. Use `kubectl rollout pause/resume` for canary testing
