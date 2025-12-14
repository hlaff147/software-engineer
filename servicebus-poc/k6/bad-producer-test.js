import http from 'k6/http';
import { check, sleep } from 'k6';
import { Counter, Trend, Rate } from 'k6/metrics';

// ========================================
// k6 Load Test - Bad Producer (Resource Leak)
// ========================================
// Este teste demonstra o impacto de criar conexões sem fechar.
// O BadProducerController NUNCA fecha as conexões, causando:
// - Memory leak progressivo
// - Thread explosion
// - Eventual OutOfMemoryError
// ========================================

// Métricas customizadas
const connectionErrors = new Counter('connection_errors');
const leakedConnections = new Counter('leaked_connections');
const responseTime = new Trend('response_time_ms');
const successRate = new Rate('success_rate');

// Configuração do teste - AJUSTADA para emulador lento no Mac M1/M2
export const options = {
    scenarios: {
        bad_producer_test: {
            executor: 'ramping-vus',
            startVUs: 0,
            stages: [
                { duration: '10s', target: 2 },   // Ramp up lento
                { duration: '30s', target: 3 },   // Carga leve
                { duration: '20s', target: 5 },   // Carga moderada
                { duration: '10s', target: 0 },   // Ramp down
            ],
            gracefulRampDown: '5s',
        },
    },
    thresholds: {
        http_req_failed: ['rate<0.8'],  // Toleramos até 80% de falhas no emulador lento
        http_req_duration: ['p(95)<60000'],  // p95 < 60s (emulador é muito lento)
    },
};

const BASE_URL = __ENV.BASE_URL || 'http://localhost:8080';
const ENDPOINT = '/api/v1/bad-producer';

export function setup() {
    console.log('🔬 Iniciando teste de carga no BAD PRODUCER');
    console.log('⚠️  Este endpoint cria conexões que NUNCA são fechadas!');
    console.log(`📍 URL: ${BASE_URL}${ENDPOINT}`);

    // Limpar conexões vazadas anteriores
    const cleanupRes = http.post(`${BASE_URL}/api/v1/bad-producer/cleanup`);
    console.log(`🧹 Cleanup inicial: ${cleanupRes.status}`);

    return { startTime: new Date().toISOString() };
}

export default function () {
    const payload = JSON.stringify({
        content: `Message from VU ${__VU} at ${new Date().toISOString()}`,
        iteration: __ITER,
    });

    const params = {
        headers: {
            'Content-Type': 'application/json',
        },
        timeout: '60s',
    };

    const startTime = Date.now();
    const res = http.post(`${BASE_URL}${ENDPOINT}`, payload, params);
    const duration = Date.now() - startTime;

    // Registrar métricas
    responseTime.add(duration);

    const success = check(res, {
        'status is 200': (r) => r.status === 200,
        'response contains leak info': (r) => r.body && r.body.includes('LEAK'),
    });

    successRate.add(success);

    if (!success) {
        connectionErrors.add(1);
        console.log(`❌ Erro na iteração ${__ITER}: ${res.status} - ${res.body}`);
    } else {
        leakedConnections.add(1);
    }

    // Pequeno delay entre requests
    sleep(0.1 + Math.random() * 0.2);
}

export function teardown(data) {
    console.log('\n📊 Teste finalizado!');
    console.log(`⏱️  Início: ${data.startTime}`);
    console.log(`⏱️  Fim: ${new Date().toISOString()}`);

    // Obter estatísticas de vazamento
    const statsRes = http.get(`${BASE_URL}/api/v1/bad-producer/stats`);
    console.log(`\n☠️ Estado final dos vazamentos:\n${statsRes.body}`);
}

// Handler para exportar dados em JSON
export function handleSummary(data) {
    const timestamp = new Date().toISOString().replace(/[:.]/g, '-');
    return {
        [`analysis/results/bad_producer_${timestamp}.json`]: JSON.stringify(data, null, 2),
        stdout: textSummary(data, { indent: ' ', enableColors: true }),
    };
}

function textSummary(data, options) {
    const { metrics } = data;
    let output = '\n╔════════════════════════════════════════════════════════════╗\n';
    output += '║           BAD PRODUCER - RESULTADOS DO TESTE              ║\n';
    output += '╚════════════════════════════════════════════════════════════╝\n\n';

    if (metrics.http_reqs) {
        output += `📨 Total de Requests: ${metrics.http_reqs.values.count}\n`;
    }
    if (metrics.http_req_duration) {
        output += `⏱️  Latência média: ${metrics.http_req_duration.values.avg.toFixed(2)}ms\n`;
        output += `⏱️  Latência p95: ${metrics.http_req_duration.values['p(95)'].toFixed(2)}ms\n`;
    }
    if (metrics.http_req_failed) {
        output += `❌ Taxa de Falhas: ${(metrics.http_req_failed.values.rate * 100).toFixed(2)}%\n`;
    }
    if (metrics.leaked_connections) {
        output += `☠️  Conexões Vazadas: ${metrics.leaked_connections.values.count}\n`;
    }

    return output;
}
