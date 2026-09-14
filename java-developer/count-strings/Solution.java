import java.io.*;
import java.math.*;
import java.security.*;
import java.text.*;
import java.util.*;
import java.util.concurrent.*;
import java.util.function.*;
import java.util.regex.*;
import java.util.stream.*;
import static java.util.stream.Collectors.joining;
import static java.util.stream.Collectors.toList;

class Result {

    static final long MOD = 1_000_000_007L;

    // =====================================================================
    // ETAPA 1: Representacao da AST (Arvore Sintatica Abstrata)
    // =====================================================================
    // Cada no representa uma sub-expressao regular.
    // Tipos: CHAR_A, CHAR_B (folhas), CONCAT, UNION (dois filhos), STAR (um filho).
    // =====================================================================

    static final int CHAR_A = 0;
    static final int CHAR_B = 1;
    static final int CONCAT = 2;
    static final int UNION  = 3;
    static final int STAR   = 4;

    static int[] nodeType;        // tipo de cada no da AST
    static int[] nodeLeft;        // filho esquerdo (ou unico filho para STAR)
    static int[] nodeRight;       // filho direito (nao usado para STAR/CHAR)
    static int nodeCount;

    static int newNode(int type, int left, int right) {
        int id = nodeCount++;
        nodeType[id] = type;
        nodeLeft[id] = left;
        nodeRight[id] = right;
        return id;
    }

    // =====================================================================
    // ETAPA 1: Parser de Descida Recursiva
    // =====================================================================
    // Gramatica:
    //   R -> 'a' | 'b' | '(' R R ')' | '(' R '|' R ')' | '(' R '*' ')'
    //
    // Ao encontrar '(', fazemos parse de R1 e verificamos o proximo caractere:
    //   '|' -> UNION(R1, R2)
    //   '*' -> STAR(R1)
    //   outro -> CONCAT(R1, R2)
    // =====================================================================

    static int parsePos;

    static int parse(String s) {
        char c = s.charAt(parsePos);
        if (c == 'a') {
            parsePos++;
            return newNode(CHAR_A, -1, -1);
        }
        if (c == 'b') {
            parsePos++;
            return newNode(CHAR_B, -1, -1);
        }
        // Deve ser '('
        parsePos++; // consome '('
        int r1 = parse(s);
        char next = s.charAt(parsePos);
        if (next == '|') {
            parsePos++; // consome '|'
            int r2 = parse(s);
            parsePos++; // consome ')'
            return newNode(UNION, r1, r2);
        }
        if (next == '*') {
            parsePos++; // consome '*'
            parsePos++; // consome ')'
            return newNode(STAR, r1, -1);
        }
        // Concatenacao: R1 R2
        int r2 = parse(s);
        parsePos++; // consome ')'
        return newNode(CONCAT, r1, r2);
    }

    // =====================================================================
    // ETAPA 2: Construcao de Thompson (AST -> NFA)
    // =====================================================================
    // Cada no da AST gera um fragmento de NFA com um estado inicial (start)
    // e um estado de aceitacao (accept).
    //
    // Transicoes sao armazenadas em listas de adjacencia:
    //   - transChar[estado] = lista de {caractere(0=a,1=b), destino}
    //   - transEps[estado]  = lista de destinos via epsilon (transicao vazia)
    //
    // CHAR(c):   start --c--> accept
    // CONCAT:    R1.accept --eps--> R2.start
    // UNION:     s --eps--> R1.start, s --eps--> R2.start,
    //            R1.accept --eps--> a, R2.accept --eps--> a
    // STAR:      s --eps--> R1.start, R1.accept --eps--> R1.start,
    //            s --eps--> a, R1.accept --eps--> a
    // =====================================================================

    static int nfaStateCount;
    static List<int[]>[] transChar;
    static List<Integer>[] transEps;

    @SuppressWarnings("unchecked")
    static void initNFA(int maxStates) {
        nfaStateCount = 0;
        transChar = new List[maxStates];
        transEps = new List[maxStates];
        for (int i = 0; i < maxStates; i++) {
            transChar[i] = new ArrayList<>();
            transEps[i] = new ArrayList<>();
        }
    }

    static int newNFAState() {
        return nfaStateCount++;
    }

    /**
     * Constroi o fragmento NFA para o no da AST e retorna {start, accept}.
     */
    static int[] buildNFA(int node) {
        int type = nodeType[node];
        switch (type) {
            case CHAR_A: {
                int s = newNFAState(), a = newNFAState();
                transChar[s].add(new int[]{0, a}); // transicao com 'a'
                return new int[]{s, a};
            }
            case CHAR_B: {
                int s = newNFAState(), a = newNFAState();
                transChar[s].add(new int[]{1, a}); // transicao com 'b'
                return new int[]{s, a};
            }
            case CONCAT: {
                int[] r1 = buildNFA(nodeLeft[node]);
                int[] r2 = buildNFA(nodeRight[node]);
                transEps[r1[1]].add(r2[0]); // R1.accept --eps--> R2.start
                return new int[]{r1[0], r2[1]};
            }
            case UNION: {
                int s = newNFAState(), a = newNFAState();
                int[] r1 = buildNFA(nodeLeft[node]);
                int[] r2 = buildNFA(nodeRight[node]);
                transEps[s].add(r1[0]); // s --eps--> R1.start
                transEps[s].add(r2[0]); // s --eps--> R2.start
                transEps[r1[1]].add(a); // R1.accept --eps--> a
                transEps[r2[1]].add(a); // R2.accept --eps--> a
                return new int[]{s, a};
            }
            case STAR: {
                int s = newNFAState(), a = newNFAState();
                int[] r1 = buildNFA(nodeLeft[node]);
                transEps[s].add(r1[0]);    // s --eps--> R1.start
                transEps[r1[1]].add(r1[0]);// R1.accept --eps--> R1.start (loop)
                transEps[s].add(a);        // s --eps--> a (aceita string vazia)
                transEps[r1[1]].add(a);    // R1.accept --eps--> a
                return new int[]{s, a};
            }
        }
        return null; // nunca alcancado
    }

    // =====================================================================
    // ETAPA 3: Construcao de Subconjuntos (NFA -> DFA)
    // =====================================================================
    // Um NFA pode ter multiplos caminhos para a mesma string, o que causa
    // contagem duplicada. Para evitar isso, convertemos o NFA em um DFA
    // onde cada string tem EXATAMENTE um caminho.
    //
    // Cada estado do DFA e um CONJUNTO de estados do NFA (BitSet).
    // Usamos BFS para explorar apenas os conjuntos alcancaveis.
    //
    // Fecho-epsilon (epsilon closure): dado um conjunto de estados NFA, computa
    // todos os estados alcancaveis apenas por transicoes epsilon.
    // =====================================================================

    /**
     * Calcula o fecho-epsilon de um conjunto de estados NFA.
     */
    static BitSet epsilonClosure(BitSet states) {
        BitSet closure = (BitSet) states.clone();
        Deque<Integer> stack = new ArrayDeque<>();
        for (int i = closure.nextSetBit(0); i >= 0; i = closure.nextSetBit(i + 1)) {
            stack.push(i);
        }
        while (!stack.isEmpty()) {
            int s = stack.pop();
            for (int t : transEps[s]) {
                if (!closure.get(t)) {
                    closure.set(t);
                    stack.push(t);
                }
            }
        }
        return closure;
    }

    /**
     * Constroi o DFA a partir do NFA usando construcao de subconjuntos.
     * Retorna: {dfaStateCount, dfaTrans[][], dfaAccept[]}
     * dfaTrans[estado][caractere] = proximo estado (-1 se dead/inexistente)
     */
    static int dfaCount;
    static int[][] dfaTrans;
    static boolean[] dfaAccept;

    static void buildDFA(int nfaStart, int nfaAcceptState) {
        Map<BitSet, Integer> stateMap = new HashMap<>();
        List<BitSet> stateList = new ArrayList<>();
        Queue<Integer> queue = new LinkedList<>();

        // Estado DFA inicial = fecho-epsilon do estado inicial do NFA
        BitSet startSet = new BitSet();
        startSet.set(nfaStart);
        startSet = epsilonClosure(startSet);

        stateMap.put(startSet, 0);
        stateList.add(startSet);
        queue.add(0);
        dfaCount = 1;

        // Listas dinamicas (nao sabemos o tamanho final do DFA)
        List<int[]> transList = new ArrayList<>();
        List<Boolean> acceptList = new ArrayList<>();

        transList.add(new int[]{-1, -1});
        acceptList.add(startSet.get(nfaAcceptState));

        while (!queue.isEmpty()) {
            int curId = queue.poll();
            BitSet curSet = stateList.get(curId);

            for (int c = 0; c < 2; c++) { // 0 = 'a', 1 = 'b'
                BitSet nextSet = new BitSet();
                // Para cada estado NFA no conjunto atual, seguir transicao com c
                for (int s = curSet.nextSetBit(0); s >= 0; s = curSet.nextSetBit(s + 1)) {
                    for (int[] tr : transChar[s]) {
                        if (tr[0] == c) {
                            nextSet.set(tr[1]);
                        }
                    }
                }
                if (!nextSet.isEmpty()) {
                    nextSet = epsilonClosure(nextSet);
                    Integer nextId = stateMap.get(nextSet);
                    if (nextId == null) {
                        nextId = dfaCount++;
                        stateMap.put(nextSet, nextId);
                        stateList.add(nextSet);
                        queue.add(nextId);
                        transList.add(new int[]{-1, -1});
                        acceptList.add(nextSet.get(nfaAcceptState));
                    }
                    transList.get(curId)[c] = nextId;
                }
            }
        }

        // Converte listas para arrays
        dfaTrans = transList.toArray(new int[0][]);
        dfaAccept = new boolean[dfaCount];
        for (int i = 0; i < dfaCount; i++) {
            dfaAccept[i] = acceptList.get(i);
        }
    }

    // =====================================================================
    // ETAPA 4: Exponenciacao de Matrizes
    // =====================================================================
    // Com o DFA construido, montamos a matriz de transicao M[N x N] onde:
    //   M[i][j] = quantidade de caracteres {a,b} que levam do estado i ao j
    //             (valor 0, 1 ou 2)
    //
    // Calculamos M^L usando exponenciacao rapida (O(N^3 log L)):
    //   - Resultado inicia como matriz identidade I
    //   - Enquanto L > 0: se L impar, resultado *= M; M *= M; L /= 2
    //
    // Resposta = soma M^L[start][j] para todo j de aceitacao, mod 10^9+7
    // =====================================================================

    /**
     * Multiplicacao de matrizes mod MOD.
     * Otimizacao: pula quando A[i][k] == 0 para evitar multiplicacoes inuteis.
     */
    static long[][] matMul(long[][] A, long[][] B, int n) {
        long[][] C = new long[n][n];
        for (int i = 0; i < n; i++) {
            for (int k = 0; k < n; k++) {
                if (A[i][k] == 0) continue; // otimizacao de esparsidade
                for (int j = 0; j < n; j++) {
                    C[i][j] = (C[i][j] + A[i][k] * B[k][j]) % MOD;
                }
            }
        }
        return C;
    }

    /**
     * Exponenciacao rapida de matrizes: calcula M^power mod MOD.
     */
    static long[][] matPow(long[][] M, int n, long power) {
        // Inicia com a matriz identidade
        long[][] result = new long[n][n];
        for (int i = 0; i < n; i++) result[i][i] = 1;

        while (power > 0) {
            if ((power & 1) == 1) {
                result = matMul(result, M, n);
            }
            M = matMul(M, M, n);
            power >>= 1;
        }
        return result;
    }

    // =====================================================================
    // Funcao principal: countStrings
    // =====================================================================

    public static int countStrings(String r, int l) {
        // --- Etapa 1: Parsing da regex -> AST ---
        int maxNodes = r.length() + 2;
        nodeType = new int[maxNodes];
        nodeLeft = new int[maxNodes];
        nodeRight = new int[maxNodes];
        nodeCount = 0;
        parsePos = 0;
        int root = parse(r);

        // --- Etapa 2: Construcao de Thompson (AST -> NFA) ---
        int maxStates = r.length() * 2 + 10;
        initNFA(maxStates);
        int[] nfa = buildNFA(root);
        int nfaStart = nfa[0];
        int nfaAccept = nfa[1];

        // --- Etapa 3: Construcao de Subconjuntos (NFA -> DFA) ---
        buildDFA(nfaStart, nfaAccept);

        // --- Etapa 4: Montar matriz de transicao e exponenciar ---
        int n = dfaCount;
        long[][] M = new long[n][n];
        for (int i = 0; i < n; i++) {
            for (int c = 0; c < 2; c++) {
                int j = dfaTrans[i][c];
                if (j != -1) {
                    M[i][j] = (M[i][j] + 1) % MOD;
                }
            }
        }

        long[][] ML = matPow(M, n, l);

        // Somar M^L[start=0][j] para todo estado j de aceitacao
        long answer = 0;
        for (int j = 0; j < n; j++) {
            if (dfaAccept[j]) {
                answer = (answer + ML[0][j]) % MOD;
            }
        }

        return (int) answer;
    }
}

public class Solution {
    public static void main(String[] args) throws IOException {
        BufferedReader bufferedReader = new BufferedReader(new InputStreamReader(System.in));
        BufferedWriter bufferedWriter = new BufferedWriter(new FileWriter(System.getenv("OUTPUT_PATH")));

        int t = Integer.parseInt(bufferedReader.readLine().trim());

        IntStream.range(0, t).forEach(tItr -> {
            try {
                String[] firstMultipleInput = bufferedReader.readLine().replaceAll("\\s+$", "").split(" ");

                String r = firstMultipleInput[0];

                int l = Integer.parseInt(firstMultipleInput[1]);

                int result = Result.countStrings(r, l);

                bufferedWriter.write(String.valueOf(result));
                bufferedWriter.newLine();
            } catch (IOException ex) {
                throw new RuntimeException(ex);
            }
        });

        bufferedReader.close();
        bufferedWriter.close();
    }
}
