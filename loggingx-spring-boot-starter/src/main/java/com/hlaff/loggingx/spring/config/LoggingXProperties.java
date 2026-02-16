package com.hlaff.loggingx.spring.config;

import lombok.Data;
import org.springframework.boot.context.properties.ConfigurationProperties;

import java.util.ArrayList;
import java.util.List;

/**
 * Propriedades de configuração do LoggingX.
 * Permite customizar comportamento da biblioteca via application.yml/properties.
 */
@Data
@ConfigurationProperties("loggingx")
public class LoggingXProperties {

    /**
     * Se o LoggingX está habilitado (padrão: true)
     */
    private boolean enabled = true;

    /**
     * Nome do microserviço (obrigatório para identificação nos logs)
     */
    private String service = "unknown";

    /**
     * Ambiente de execução (dev, qa, prod)
     */
    private String env = "dev";

    /**
     * Versão da aplicação
     */
    private String version = "local";

    /**
     * Se deve incluir stack trace completo em logs de erro (padrão: true)
     */
    private boolean includeStacktrace = true;

    /**
     * Tamanho máximo do payload antes do truncamento (bytes)
     */
    private int maxPayloadLength = 4096;

    /**
     * Lista de chaves que devem ser mascaradas nos logs
     */
    private List<String> redactKeys = new ArrayList<>(List.of(
        "password", "token", "cpf", "email", "secret", "key", "authorization"
    ));

    /**
     * Configurações específicas para HTTP
     */
    private HttpSection http = new HttpSection();

    /**
     * Configurações específicas para Kafka
     */
    private KafkaSection kafka = new KafkaSection();

    /**
     * Configurações específicas para Azure Service Bus
     */
    private ServiceBusSection servicebus = new ServiceBusSection();

    /**
     * Configurações específicas para MongoDB
     */
    private MongoSection mongo = new MongoSection();

    /**
     * Configurações específicas para JDBC
     */
    private JdbcSection jdbc = new JdbcSection();

    /**
     * Configurações de amostragem (sampling)
     */
    private SamplingSection sampling = new SamplingSection();

    /**
     * Configurações para HTTP
     */
    @Data
    public static class HttpSection {
        /**
         * Se o conector HTTP está habilitado
         */
        private boolean enabled = true;

        /**
         * Configurações do servidor HTTP
         */
        private ServerSection server = new ServerSection();

        /**
         * Configurações do cliente HTTP
         */
        private ClientSection client = new ClientSection();

        @Data
        public static class ServerSection {
            /**
             * Se deve logar requisições HTTP recebidas
             */
            private boolean enabled = true;

            /**
             * Se deve logar corpo das requisições/respostas
             */
            private boolean logBody = false;

            /**
             * Se deve logar headers das requisições/respostas
             */
            private boolean logHeaders = false;
        }

        @Data
        public static class ClientSection {
            /**
             * Se deve logar requisições HTTP enviadas
             */
            private boolean enabled = true;

            /**
             * Se deve logar corpo das requisições/respostas
             */
            private boolean logBody = false;

            /**
             * Se deve logar headers das requisições/respostas
             */
            private boolean logHeaders = false;
        }
    }

    /**
     * Configurações para Kafka
     */
    @Data
    public static class KafkaSection {
        /**
         * Se o conector Kafka está habilitado
         */
        private boolean enabled = true;

        /**
         * Se deve logar produção de mensagens
         */
        private boolean logProducer = true;

        /**
         * Se deve logar consumo de mensagens
         */
        private boolean logConsumer = true;

        /**
         * Se deve logar payload das mensagens
         */
        private boolean logPayload = false;

        /**
         * Se deve logar headers das mensagens
         */
        private boolean logHeaders = true;
    }

    /**
     * Configurações para Azure Service Bus
     */
    @Data
    public static class ServiceBusSection {
        /**
         * Se o conector Service Bus está habilitado
         */
        private boolean enabled = true;

        /**
         * Se deve logar envio de mensagens
         */
        private boolean logProducer = true;

        /**
         * Se deve logar recebimento de mensagens
         */
        private boolean logConsumer = true;

        /**
         * Se deve logar payload das mensagens
         */
        private boolean logPayload = false;

        /**
         * Se deve logar application properties das mensagens
         */
        private boolean logApplicationProperties = true;
    }

    /**
     * Configurações para MongoDB
     */
    @Data
    public static class MongoSection {
        /**
         * Se o conector MongoDB está habilitado
         */
        private boolean enabled = true;

        /**
         * Se deve logar comandos executados
         */
        private boolean logCommands = true;

        /**
         * Se deve logar apenas comandos lentos (acima de slowThresholdMs)
         */
        private boolean slowQueriesOnly = false;

        /**
         * Threshold em ms para considerar uma query como lenta
         */
        private long slowThresholdMs = 1000;

        /**
         * Se deve logar resultado dos comandos
         */
        private boolean logResults = false;
    }

    /**
     * Configurações para JDBC
     */
    @Data
    public static class JdbcSection {
        /**
         * Se o conector JDBC está habilitado (padrão: false por performance)
         */
        private boolean enabled = false;

        /**
         * Se deve logar statements SQL
         */
        private boolean logStatements = true;

        /**
         * Se deve logar parâmetros dos statements
         */
        private boolean logParameters = false;

        /**
         * Se deve logar apenas statements lentos
         */
        private boolean slowQueriesOnly = true;

        /**
         * Threshold em ms para considerar uma query como lenta
         */
        private long slowThresholdMs = 500;
    }

    /**
     * Configurações de amostragem
     */
    @Data
    public static class SamplingSection {
        /**
         * Percentual padrão de amostragem (0-100)
         */
        private int defaultPercent = 20;

        /**
         * Regras específicas de amostragem por padrão de classe/método
         */
        private List<SamplingRule> rules = new ArrayList<>();

        @Data
        public static class SamplingRule {
            /**
             * Padrão regex para identificar classes/métodos
             */
            private String pattern;

            /**
             * Percentual de amostragem para este padrão (0-100)
             */
            private int percent;
        }
    }
}
