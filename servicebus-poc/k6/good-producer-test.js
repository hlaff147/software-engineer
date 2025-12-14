import http from 'k6/http';
import { check, sleep } from 'k6';
import { Counter, Trend, Rate } from 'k6/metrics';

// ========================================
// k6 Load Test - Good Producer (Best Practice)
// ========================================
// Este teste demonstra a implementação correta com conexão reutilizada.
// O GoodProducerController usa um singleton ServiceBusSenderClient,
// resultando em:
// - Uso estável de memória
// - Número constante de threads
// - Performance consistente
// ========================================

// Métricas customizadas
const connectionErrors = new Counter('connection_errors');
const messagesSuccessful = new Counter('messages_successful');
const responseTime = new Trend('response_time_ms');
const successRate = new Rate('success_rate');

// Configuração do teste - AJUSTADA para emulador lento no Mac M1/M2
export const options = {
    scenarios: {
        good_producer_test: {
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
        http_req_failed: ['rate<0.3'],  // Good producer deve ter menos de 30% de falhas
        http_req_duration: ['p(95)<30000'],  // p95 < 30s
    },
};

const BASE_URL = __ENV.BASE_URL || 'http://localhost:8080';
const ENDPOINT = '/api/v1/good-producer';

export function setup() {
    console.log('✅ Iniciando teste de carga no GOOD PRODUCER');
    console.log('💚 Este endpoint reutiliza a mesma conexão para todos os requests!');
    console.log(`📍 URL: ${BASE_URL}${ENDPOINT}`);

    // Reset counter
    const resetRes = http.post(`${BASE_URL}/api/v1/good-producer/reset-counter`);
    console.log(`🔄 Reset counter: ${resetRes.status}`);

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
        'response confirms shared connection': (r) => r.body && r.body.includes('compartilhada'),
    });

    successRate.add(success);

    if (!success) {
        connectionErrors.add(1);
        console.log(`❌ Erro na iteração ${__ITER}: ${res.status} - ${res.body}`);
    } else {
        messagesSuccessful.add(1);
    }

    // Mesmo delay do bad-producer para comparação justa
    sleep(0.1 + Math.random() * 0.2);
}

export function teardown(data) {
    console.log('\n📊 Teste finalizado!');
    console.log(`⏱️  Início: ${data.startTime}`);
    console.log(`⏱️  Fim: ${new Date().toISOString()}`);
}

// Handler para exportar dados em JSON
export function handleSummary(data) {
    const timestamp = new Date().toISOString().replace(/[:.]/g, '-');
    return {
        [`analysis/results/good_producer_${timestamp}.json`]: JSON.stringify(data, null, 2),
        stdout: textSummary(data, { indent: ' ', enableColors: true }),
    };
}

function textSummary(data, options) {
    const { metrics } = data;
    let output = '\n╔════════════════════════════════════════════════════════════╗\n';
    output += '║          GOOD PRODUCER - RESULTADOS DO TESTE              ║\n';
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
    if (metrics.messages_successful) {
        output += `✅ Mensagens Enviadas: ${metrics.messages_successful.values.count}\n`;
    }

    return output;
}
