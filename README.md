# Projeto de envio de mensagens via whatsapp usando Python, Supabase e Z-API

Este projeto em Python envia mensagens personalizadas via Whatsapp para contatos em um banco de dados Supabase usando a Z-API.

# Explicação:
- Busca contatos do banco de dados criado no Supabase
- Envia mensagem personalizada: `"Olá {{nome_contato}}, tudo bem com você?"`
- Envia para até três números diferentes
- Com logs simples de sucesso ou falha no envio

# Requisitos
- Criar ou utilizar conta já criada no Supabase (https://supabase.com) e construir tabela `contatos` com colunas: id (int8), nome, telefone 
- Conta Z-API (https://www.z-api.io) com instance, token e account security token 
- Baixar Visual Studio Code
- Mínimo Python 3.8 ou superior
- Após instalar o Python, ativar a opção "Add Python to PATH" (Adicionar Python ao PATH) para utilizar bibliotecas externas

# Setup
1. Criar tabela `contatos` no Supabase:
   - Coluna `id` → int8, Primary Key, Is Identity 
   - Coluna `nome` → text
   - Coluna `telefone` → text
2. Preencher `.env` com suas chaves do Supabase e Z-API
3. Instalar bibliotecas:
   - pip install -r requirements.txt
   - pip install requests
   - pip install python-dotenv
   - pip install supabase
   
4. Rodar o código:
   python main.py
   

# Observações
- Z-API exige número no formato internacional: ex. `5511999999999`
- NÃO pode comitar `.env` em repositórios públicos.
- O uso de text em vez de int para o telefone no Supabase foi para permitir que fosse utilizado o +55 (DDI do Brasil) para não perder informação completa do número.
