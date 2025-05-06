from faker import Faker
import random
from datetime import datetime
from supabase import create_client, Client

#bia
supabase_url = 'https://ddvbdgmjahgybinwufbx.supabase.co'
supabase_key = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImRkdmJkZ21qYWhneWJpbnd1ZmJ4Iiwicm9sZSI6ImFub24iLCJpYXQiOjE3NDUzNjIyNzgsImV4cCI6MjA2MDkzODI3OH0.Iyr8uPRx3uo4KdUQxBlwpaHIr1MTxHBPWCW2BTQIlqM'

#laura
#supabase_url = 'https://bgaldydhkrrtwxiivwtr.supabase.co'
#supabase_key = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImJnYWxkeWRoa3JydHd4aWl2d3RyIiwicm9sZSI6InNlcnZpY2Vfcm9sZSIsImlhdCI6MTczODcwOTMxNywiZXhwIjoyMDU0Mjg1MzE3fQ.wSJss4EPy3w8jBmBUPBiNovEK3xQuoZmdZV5JOsvK4U'

supabase: Client = create_client(supabase_url, supabase_key)
faker = Faker('pt_BR')  #inicializar faker

#CARTAO
cartao = []

for quantidade_cartao in range(20):  #tem mais cartao que cliente para dar para cada pessoa pode ter mais de um cartao mas ninguem pode ter o mesmo cartao
  cvv = faker.unique.credit_card_security_code()
  numero_cartao = faker.credit_card_number()
  data_validade = faker.credit_card_expire()
  cartao.append({
      "cvv": cvv,
      "numero": numero_cartao,
      "validade": data_validade,
  })

#inserir cartao no supabase

for qtd_cartao in cartao:
  try:
    response = supabase.table('cartao').insert(qtd_cartao).execute()
    print(f"Cartao {qtd_cartao['numero']} adicionado com sucesso!")
  except Exception as e:
    print(f"Erro ao adicionar cartao {qtd_cartao['numero']}: {e}")

#CLIENTE
cliente = []
cpfCliente = []  #para guardar todos os cpf do clientes e dps pegar cpfs aleatorios dentre eles para associar aos cartoes
for quantidade_cliente in range(10):
  cpf_cliente = faker.unique.cpf()
  nome_cliente = faker.name()
  telefone_cliente = faker.phone_number()
  cep_cliente = faker.postcode()
  email_cliente = faker.email()
  senha_cliente = faker.password()
  genero = [ "feminimo", "masculino", "nao-binario", "genero-fluido", "agenero", "travesti"]
  genero_cliente = random.choice(genero)
  cliente.append({
      "cpf_cliente": cpf_cliente,
      "nome_cliente": nome_cliente,
      "telefone": telefone_cliente,
      "cep": cep_cliente,
      "email": email_cliente,
      "senha": senha_cliente,
      "genero": genero_cliente,
  })
  cpfCliente.append(cpf_cliente)

#inserir cliente no supabase
for cliente in cliente:
  try:
    response = supabase.table('cliente').insert(cliente).execute()
    print(
        f"cliente {cliente['nome_cliente']} com cpf {cliente['cpf_cliente']} adicionado com sucesso!"
    )
  except Exception as e:
    print(f"Erro ao adicionar cliente com cpf {cliente['cpf_cliente']}: {e}")

#update cartao com cpf de cliente

# Atualizar os 10 (pq tem 10 clientes) primeiros cartões garantindo 1 por cliente
for i in range(10):
  numero_cartao = cartao[i]["numero"]
  cpf = cpfCliente[i]
  try:
    supabase.table("cartao").update({
        "cpf_titular": cpf
    }).match({"numero": numero_cartao}).execute()
    print(f"Cartão {numero_cartao} associado ao CPF {cpf}")
  except Exception as e:
    print(f"Erro ao associar cartão {numero_cartao} ao CPF {cpf}: {e}")

# Distribuir os 10 cartões restantes aleatoriamente entre os 10 clientes (totalizando 20 cartoes, quantidade inicial)
for i in range(10, 20):
  numero_cartao = cartao[i]["numero"]
  cpf = random.choice(cpfCliente)
  try:
    supabase.table("cartao").update({
        "cpf_titular": cpf
    }).match({"numero": numero_cartao}).execute()
    print(f"Cartão {numero_cartao} adicional associado ao CPF {cpf}")
  except Exception as e:
    print(f"Erro ao associar cartão {numero_cartao} ao CPF {cpf}: {e}")
