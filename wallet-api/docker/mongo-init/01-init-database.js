// Inicialização do banco de dados MongoDB
// Este script é executado automaticamente quando o container MongoDB é criado

print('🚀 Inicializando banco de dados Wallet API...');

// Conectar ao banco de dados
db = db.getSiblingDB('wallet');

// Criar usuário da aplicação
db.createUser({
  user: 'wallet_user',
  pwd: 'wallet_pass',
  roles: [
    {
      role: 'readWrite',
      db: 'wallet'
    }
  ]
});

print('✅ Usuário wallet_user criado com sucesso');

// Criar índices para a coleção wallets
db.wallets.createIndex(
  { "userId": 1, "currency": 1 }, 
  { 
    unique: true, 
    name: "unique_user_currency_idx",
    background: true 
  }
);

print('✅ Índice único userId+currency criado na coleção wallets');

// Criar índices para a coleção ledger_entries
db.ledger_entries.createIndex(
  { "walletId": 1, "occurredAt": -1 }, 
  { 
    name: "wallet_occurred_at_idx",
    background: true 
  }
);

db.ledger_entries.createIndex(
  { "transferId": 1 }, 
  { 
    name: "transfer_id_idx",
    background: true 
  }
);

db.ledger_entries.createIndex(
  { "operation": 1, "occurredAt": -1 }, 
  { 
    name: "operation_occurred_at_idx",
    background: true 
  }
);

print('✅ Índices criados na coleção ledger_entries');

// Criar dados de exemplo (opcional - apenas para desenvolvimento)
print('📝 Criando dados de exemplo...');

// Carteira de exemplo
const exampleWallet = {
  userId: "demo-user",
  currency: "BRL",
  balance: 0,
  status: "ACTIVE",
  createdAt: new Date(),
  updatedAt: new Date()
};

const walletResult = db.wallets.insertOne(exampleWallet);
const walletId = walletResult.insertedId.toString();

print(`✅ Carteira de exemplo criada: ${walletId}`);

// Entrada de depósito de exemplo
const exampleLedgerEntry = {
  walletId: walletId,
  transferId: null,
  operation: "DEPOSIT",
  amount: 10000, // R$ 100.00 em centavos
  occurredAt: new Date(),
  resultingBalance: 10000,
  metadata: {
    description: "Depósito inicial de exemplo",
    source: "DEMO"
  }
};

db.ledger_entries.insertOne(exampleLedgerEntry);

// Atualizar saldo da carteira
db.wallets.updateOne(
  { _id: walletResult.insertedId },
  { 
    $set: { 
      balance: 10000,
      updatedAt: new Date()
    }
  }
);

print('✅ Entrada de exemplo criada no ledger');

print('🎉 Inicialização do banco de dados concluída com sucesso!');
print('📊 Base de dados pronta para uso da Wallet API');
print('');
print('👤 Usuário da aplicação: wallet_user');
print('📁 Database: wallet');
print('📋 Coleções: wallets, ledger_entries');
print('🔍 Índices: unique_user_currency, wallet_occurred_at, transfer_id, operation_occurred_at');
