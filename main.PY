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

for quantidade_cartao in range(30):  #tem mais cartao que cliente para dar para cada pessoa pode ter mais de um cartao mas ninguem pode ter o mesmo cartao
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
for quantidade_cliente in range(20):
  cpf_cliente = faker.unique.cpf()
  nome_cliente = faker.name()
  telefone_cliente = faker.phone_number()
  cep_cliente = faker.postcode()
  email_cliente = faker.email()
  senha_cliente = faker.password()
  genero = [
      "feminimo", "masculino", "nao-binario", "genero-fluido", "agenero",
      "travesti"]
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
    print(f"cliente {cliente['nome_cliente']} adicionado com sucesso!")
  except Exception as e:
    print(f"Erro ao adicionar cliente com cpf {cliente['cpf_cliente']}: {e}")

#update cartao com cpf de cliente

# Atualizar os 20 (pq tem 20 clientes) primeiros cartões garantindo 1 por cliente
for i in range(20):
  numero_cartao = cartao[i][
      "numero"]  #referente a posicao do cartao na lista de cartoes(que diz respeito aos cartoes na tabela)
  cpf = cpfCliente[i]
  try:
    supabase.table("cartao").update({
        "cpf_titular": cpf
    }).match({
        "numero": numero_cartao
    }).execute()
    print(f"Cartão {numero_cartao} associado ao CPF {cpf}")
  except Exception as e:
    print(f"Erro ao associar cartão {numero_cartao} ao CPF {cpf}: {e}")

# Distribuir os 10 cartões restantes aleatoriamente entre os 10 clientes (totalizando 20 cartoes, quantidade inicial)
for i in range(20, 30):
  numero_cartao = cartao[i]["numero"]
  cpf = random.choice(cpfCliente)
  try:
    supabase.table("cartao").update({
        "cpf_titular": cpf
    }).match({
        "numero": numero_cartao
    }).execute()
    print(f"Cartão {numero_cartao} adicional associado ao CPF {cpf}")
  except Exception as e:
    print(f"Erro ao associar cartão {numero_cartao} ao CPF {cpf}: {e}")

#INGREDIENTE
nome_ingredientes = [
    "pão italiano", "pão de hamburguer", "pão de hotdog", "carne bovina",
    "carne suína", "carne de frango", "queijo mussarela", "queijo prato",
    "queijo cheddar", "queijo gorgonzola", "tomate", "alface", "rucula",
    "cebola", "picles", "molho especial", "molho barbecue", "molho maionese",
    "molho mostarda", "molho ketchup", "molho maionese", "batata",
    "cebola roxa", "pimentão", "azeitona", "milho", "ervilha",
    "frango desfiado", "calabresa", "bacon", "ovo", "presunto",
    "peito de peru", "peito de frango", "peito de peru", "peito de frango",
    "peito de peru"
]

id_ingredientes = []  #para depois iterar sobre eles e associar ao produto ingrediente
id_ingrediente = faker.unique.random_int(min=10000, max=99999)

for nomeIngrediente in nome_ingredientes:
  id_ingrediente = faker.unique.random_int(min=10000, max=99999)
  validade_ingrediente = faker.date_between(start_date='today',
                                            end_date='+10y').isoformat()
  calorias_ingrediente = random.randint(10, 500)
  preco_ingrediente = round(random.uniform(0.1, 10.0), 2)
  id_ingredientes.append(id_ingrediente)
  try:
    response = supabase.table('ingrediente').insert({
        "id_ingrediente": id_ingrediente,
        "nome_ingrediente": nomeIngrediente,
        "validade": validade_ingrediente,
        "calorias": calorias_ingrediente,
        "preço": preco_ingrediente
    }).execute()
    print(f"Ingrediente {nomeIngrediente} adicionado com sucesso!")
  except Exception as e:
    print(f"Erro ao adicionar ingrediente {nomeIngrediente}: {e}")

#PRODUTO

nome_produtos = [
    "X-Burguer", "X-Salada", "X-Bacon", "X-Frango", "X-Calabresa", "X-Egg",
    "X-Egg Bacon", "X-Tudo", "X-Especial,", "X-Burguer Maxter", "X-rancho",
    "X-fazenda", "X-incrivel", "X-burguer do chef", "X-feriado"
]

id_produtos = []  #para depois iterar sobre eles e associar ao produto ingrediente

for nomeProduto in nome_produtos:
  codigo_produto = faker.unique.random_int(min=10000, max=99999)
  preco_produto = round(random.uniform(10.0, 50.0), 2)
  tamanho_imagem = random.randint(100, 500)
  id_produtos.append(codigo_produto)
  try:
    response = supabase.table('produto').insert({
        "id_produto":
        codigo_produto,
        "nome_produto":
        nomeProduto,
        "preco":
        preco_produto,
        "tamanho_imagem":
        tamanho_imagem
    }).execute()
    print(f"Produto {nomeProduto} adicionado com sucesso!")
  except Exception as e:
    print(f"Erro ao adicionar produto {nomeProduto}: {e}")

#PRODUTO INGREDIENTE
unidade_de_medida = ["kg", "g", "ml", "l", "unidade"]

#todo produto tem que ter no minimo um ingrediente

for idProduto_ProdutoIngrediente in id_produtos:
  quantidadeIngredientes = random.randint(1, 12)
  #  print("qtd ingredientes: ", quantidadeIngredientes)

  for qtdIngredientes in range(quantidadeIngredientes):
    idIngrediente_porProduto = random.choice(id_ingredientes)
    quantidade_ingredienteTabela = random.randint(1, 10)

    try:
      response = supabase.table('produtoingrediente').insert({
          "id_produto":
          idProduto_ProdutoIngrediente,
          "id_ingrediente":
          idIngrediente_porProduto,
          "quantidade_ingrediente":
          random.randint(1, 10),
          "unidade_de_medida":
          random.choice(unidade_de_medida)
      }).execute()
      print(
          f"Produto {idProduto_ProdutoIngrediente} associado ao ingrediente {idIngrediente_porProduto} com sucesso!"
      )
    except Exception as e:
      print(
          f"Erro ao associar produto {idProduto_ProdutoIngrediente} ao ingrediente {idIngrediente_porProduto}: {e}"
      )
      break
''' 
#todos produtos tem todos ingredientes

for idProduto in id_produtos:
  for idIngrediente in id_ingredientes:
    quantidade_ingrediente = random.randint(1, 10)
    try:
      response = supabase.table('produtoingrediente').insert({
          "id_produto":
          idProduto,
          "id_ingrediente":
          idIngrediente,
          "quantidade_ingrediente":
          quantidade_ingrediente,
          "unidade_de_medida":
          random.choice(unidade_de_medida)
      }).execute()
      print(
          f"Produto {idProduto} associado ao ingrediente {idIngrediente} com sucesso!"
      )
    except Exception as e:
      print(
          f"Erro ao associar produto {idProduto} ao ingrediente {idIngrediente}: {e}"
      )
'''

#FILIAL
filiais = []

for _ in range(35):  #quantidade de filiais maior que quantidade de gerentes para todo gerente ter pelo menos uma filial
  codigo_filial = faker.unique.random_int(min=10000, max=99999)
  nome_filial = faker.company()
  cep_filial = faker.postcode()


#FILIAL PRODUTO

for filial in filiais:
    codigo_filial = filial["codigo_filial"]
    produtos_escolhidos = random.sample(id_produtos, k=random.randint(1,15))  # de 1 a 15 produtos 
    for id_produto in produtos_escolhidos:
        try:
            supabase.table('filialproduto').insert({
                "codigo_filial": codigo_filial,
                "id_produto": id_produto
            }).execute()
            print(f"Filial {codigo_filial} associada ao produto {id_produto} com sucesso!")
        except Exception as e:
            print(f"Erro ao associar filial {codigo_filial} ao produto {id_produto}: {e}")


#PEDIDO E AVALIACAO

listaComentario = []

for pedidoComprado in range(13):
  data_compra = faker.date_between(start_date='-1y',
                                   end_date='today').isoformat()
  nota_pedido = random.randint(1, 10)
  comentario = faker.sentence(nb_words=10)
  try:
    response = supabase.table('pedido_e_avaliacao').insert({
        "data":
        data_compra,
        "nota":
        nota_pedido,
        "comentario":
        comentario
    }).execute()
    print(f"Pedido adicionado com sucesso!")

    listaComentario.append({"comentario": comentario})

  except Exception as e:
    print(f"Erro ao adicionar pedido: {e}")

#atualizar pedido e avaliacao com cpf do cliente
for i in range(13):
  comentariosMatch = listaComentario[i]["comentario"]  #usa comentario para fazer o match e associar ao cpf do cliente na tabela
  cpf = random.choice(cpfCliente)# associar aleatoriamente algum cliente da lista cpf cliemte assim um cliente consegue avaliar 0 ou +! pedido
  try:
    supabase.table("pedido_e_avaliacao").update({
        "cpf_cliente": cpf
    }).match({
        "comentario": comentariosMatch
    }).execute()
    print(f"Comentario {comentariosMatch} associado ao cliente {cpf}")
  except Exception as e:
    print(
        f"Erro ao associar comentario {comentariosMatch} ao cliente {cpf}: {e}"
    )

#atualizar pedido e avaliacao com id produto
for i in range(13):
  comentariosMatch = listaComentario[i]["comentario"]
  id_produtos_pedidosEAvaliacao = random.choice(id_produtos)
  try:
    supabase.table("pedido_e_avaliacao").update({
        "id_produto": id_produtos_pedidosEAvaliacao
    }).match({
        "comentario": comentariosMatch
    }).execute()
    print(
        f"Comentario {comentariosMatch} associado ao produto {id_produtos_pedidosEAvaliacao}"
    )
  except Exception as e:
    print(
        f"Erro ao associar comentario {comentariosMatch} ao produto {id_produtos_pedidosEAvaliacao}: {e}"
    )

#atualizar pedido e avaliacao com codigo filial
for i in range(13):
  comentariosMatch = listaComentario[i]["comentario"]
  codigo_filial_pedidoEAvaliacao = random.choice(filiais)["codigo_filial"]
  try:
    supabase.table("pedido_e_avaliacao").update({
        "codigo_filial":
        codigo_filial_pedidoEAvaliacao
    }).match({
        "comentario": comentariosMatch
    }).execute()
    print(
        f"Comentario {comentariosMatch} associado a filial {codigo_filial_pedidoEAvaliacao }"
    )
  except Exception as e:
    print(
        f"Erro ao associar comentario {comentariosMatch} a filial {codigo_filial_pedidoEAvaliacao }: {e}"
    )
