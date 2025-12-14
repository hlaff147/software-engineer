#!/usr/bin/env python3
"""
Coletor de Métricas JVM para análise de Load Tests
===================================================
Este script faz polling das métricas do Spring Actuator durante os testes
e salva em CSV para análise posterior no Jupyter.

Uso:
    python metrics_collector.py --duration 120 --interval 2 --output metrics.csv
"""

import argparse
import csv
import time
import requests
from datetime import datetime
import sys
import signal

# Configuração padrão
DEFAULT_ACTUATOR_URL = "http://localhost:8080/actuator"
DEFAULT_INTERVAL = 2  # segundos
DEFAULT_DURATION = 120  # segundos
DEFAULT_OUTPUT = "jvm_metrics.csv"

# Métricas a coletar do Prometheus endpoint
METRICS_TO_COLLECT = [
    # Memória Heap
    "jvm_memory_used_bytes",
    "jvm_memory_max_bytes",
    "jvm_memory_committed_bytes",
    
    # Garbage Collection
    "jvm_gc_pause_seconds_count",
    "jvm_gc_pause_seconds_sum",
    "jvm_gc_memory_allocated_bytes_total",
    
    # Threads
    "jvm_threads_live_threads",
    "jvm_threads_peak_threads",
    "jvm_threads_daemon_threads",
    
    # CPU
    "process_cpu_usage",
    "system_cpu_usage",
    
    # Classes carregadas
    "jvm_classes_loaded_classes",
]


class MetricsCollector:
    def __init__(self, actuator_url: str, interval: float, output_file: str):
        self.actuator_url = actuator_url
        self.prometheus_url = f"{actuator_url}/prometheus"
        self.interval = interval
        self.output_file = output_file
        self.running = True
        self.data = []
        
        # Handler para Ctrl+C
        signal.signal(signal.SIGINT, self._signal_handler)
        signal.signal(signal.SIGTERM, self._signal_handler)
    
    def _signal_handler(self, signum, frame):
        print("\n⏹️  Interrompendo coleta...")
        self.running = False
    
    def check_actuator(self) -> bool:
        """Verifica se o endpoint do Actuator está disponível."""
        try:
            response = requests.get(f"{self.actuator_url}/health", timeout=5)
            return response.status_code == 200
        except requests.exceptions.RequestException:
            return False
    
    def parse_prometheus_metrics(self, text: str) -> dict:
        """Parseia as métricas do formato Prometheus."""
        metrics = {}
        for line in text.split('\n'):
            line = line.strip()
            if not line or line.startswith('#'):
                continue
            
            # Formato: metric_name{labels} value
            if ' ' in line:
                parts = line.rsplit(' ', 1)
                metric_key = parts[0]
                try:
                    value = float(parts[1])
                except ValueError:
                    continue
                
                # Simplificar chave da métrica para CSV
                # Extrai nome base e labels importantes
                if '{' in metric_key:
                    base_name = metric_key.split('{')[0]
                    # Extrai area (heap/nonheap) se presente
                    if 'area="heap"' in metric_key:
                        metric_key = f"{base_name}_heap"
                    elif 'area="nonheap"' in metric_key:
                        metric_key = f"{base_name}_nonheap"
                    else:
                        metric_key = base_name
                
                # Guardar apenas métricas de interesse
                for wanted in METRICS_TO_COLLECT:
                    if metric_key.startswith(wanted) or wanted in metric_key:
                        # Usar a chave simplificada
                        if metric_key not in metrics or metrics[metric_key] == 0:
                            metrics[metric_key] = value
        
        return metrics
    
    def collect_metrics(self) -> dict:
        """Coleta métricas atuais do Prometheus endpoint."""
        try:
            response = requests.get(self.prometheus_url, timeout=5)
            if response.status_code == 200:
                metrics = self.parse_prometheus_metrics(response.text)
                metrics['timestamp'] = datetime.now().isoformat()
                metrics['epoch'] = time.time()
                return metrics
        except requests.exceptions.RequestException as e:
            print(f"⚠️  Erro ao coletar métricas: {e}")
        
        return {'timestamp': datetime.now().isoformat(), 'epoch': time.time(), 'error': True}
    
    def collect_leak_stats(self) -> dict:
        """Coleta estatísticas de vazamento do bad-producer."""
        try:
            response = requests.get(f"{self.actuator_url.replace('/actuator', '')}/api/v1/bad-producer/stats", timeout=5)
            if response.status_code == 200:
                # Parse simples das estatísticas
                text = response.text
                stats = {}
                if 'Conexões vazadas:' in text:
                    # Extrai número de conexões
                    for line in text.split('\n'):
                        if 'Conexões vazadas:' in line:
                            try:
                                stats['leaked_connections'] = int(line.split(':')[1].strip())
                            except:
                                pass
                return stats
        except:
            pass
        return {}
    
    def run(self, duration: float):
        """Executa a coleta de métricas por 'duration' segundos."""
        print(f"📊 Iniciando coleta de métricas JVM")
        print(f"   URL: {self.prometheus_url}")
        print(f"   Intervalo: {self.interval}s")
        print(f"   Duração: {duration}s")
        print(f"   Output: {self.output_file}")
        print("\nPressione Ctrl+C para parar antecipadamente.\n")
        
        if not self.check_actuator():
            print("❌ Erro: Actuator não está disponível!")
            print(f"   Verifique se a aplicação está rodando em {self.actuator_url}")
            return False
        
        print("✅ Actuator disponível. Iniciando coleta...\n")
        
        start_time = time.time()
        samples = 0
        
        while self.running and (time.time() - start_time) < duration:
            metrics = self.collect_metrics()
            leak_stats = self.collect_leak_stats()
            metrics.update(leak_stats)
            
            self.data.append(metrics)
            samples += 1
            
            # Progress
            elapsed = time.time() - start_time
            percent = (elapsed / duration) * 100
            
            # Mostrar algumas métricas chave
            heap_used = metrics.get('jvm_memory_used_bytes_heap', 0) / (1024 * 1024)
            threads = metrics.get('jvm_threads_live_threads', 0)
            leaked = metrics.get('leaked_connections', 0)
            
            sys.stdout.write(f"\r⏱️  {elapsed:.0f}s/{duration:.0f}s ({percent:.0f}%) | "
                           f"Heap: {heap_used:.0f}MB | Threads: {threads:.0f} | Leaked: {leaked}")
            sys.stdout.flush()
            
            time.sleep(self.interval)
        
        print(f"\n\n✅ Coleta finalizada! {samples} amostras coletadas.")
        
        # Salvar dados
        self.save_to_csv()
        return True
    
    def save_to_csv(self):
        """Salva os dados coletados em CSV."""
        if not self.data:
            print("⚠️  Nenhum dado para salvar.")
            return
        
        # Coletar todas as chaves únicas
        all_keys = set()
        for row in self.data:
            all_keys.update(row.keys())
        
        # Ordenar chaves para consistência
        fieldnames = sorted(all_keys)
        # Colocar timestamp primeiro
        if 'timestamp' in fieldnames:
            fieldnames.remove('timestamp')
            fieldnames.insert(0, 'timestamp')
        if 'epoch' in fieldnames:
            fieldnames.remove('epoch')
            fieldnames.insert(1, 'epoch')
        
        with open(self.output_file, 'w', newline='') as f:
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writeheader()
            for row in self.data:
                writer.writerow(row)
        
        print(f"💾 Dados salvos em: {self.output_file}")


def main():
    parser = argparse.ArgumentParser(
        description='Coletor de Métricas JVM para análise de Load Tests'
    )
    parser.add_argument(
        '--url', '-u',
        default=DEFAULT_ACTUATOR_URL,
        help=f'URL base do Actuator (default: {DEFAULT_ACTUATOR_URL})'
    )
    parser.add_argument(
        '--interval', '-i',
        type=float,
        default=DEFAULT_INTERVAL,
        help=f'Intervalo entre coletas em segundos (default: {DEFAULT_INTERVAL})'
    )
    parser.add_argument(
        '--duration', '-d',
        type=float,
        default=DEFAULT_DURATION,
        help=f'Duração total da coleta em segundos (default: {DEFAULT_DURATION})'
    )
    parser.add_argument(
        '--output', '-o',
        default=DEFAULT_OUTPUT,
        help=f'Arquivo de saída CSV (default: {DEFAULT_OUTPUT})'
    )
    
    args = parser.parse_args()
    
    collector = MetricsCollector(
        actuator_url=args.url,
        interval=args.interval,
        output_file=args.output
    )
    
    success = collector.run(args.duration)
    sys.exit(0 if success else 1)


if __name__ == '__main__':
    main()
