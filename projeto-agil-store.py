import json
import os
import uuid

ARQUIVO_INVENTARIO = "inventario_agilstore.json"

def carregar_inventario():
    if os.path.exists(ARQUIVO_INVENTARIO):
        try:
            with open(ARQUIVO_INVENTARIO, "r") as arquivo:
                return json.load(arquivo)
        except json.JSONDecodeError:
            print("Erro: O arquivo de inventário está corrompido. Um novo arquivo será criado.")
            return []
    return []

def salvar_inventario(lista_produtos):
    try:
        with open(ARQUIVO_INVENTARIO, "w") as arquivo:
            json.dump(lista_produtos, arquivo, indent=4)
    except IOError as e:
        print(f"Erro ao salvar dados no arquivo: {e}")

def adicionar_novo_produto(lista_produtos):
    nome_produto = input("Nome do produto: ")
    categoria_produto = input("Categoria do produto: ")
    while True:
        try:
            preco_produto = float(input("Preço do produto: "))
            if preco_produto < 0:
                print("O preço não pode ser negativo. Tente novamente.")
                continue
            break
        except ValueError:
            print("Por favor, insira um valor numérico válido para o preço.")
    while True:
        try:
            quantidade_estoque = int(input("Quantidade em estoque: "))
            if quantidade_estoque < 0:
                print("A quantidade não pode ser negativa. Tente novamente.")
                continue
            break
        except ValueError:
            print("Por favor, insira um valor inteiro válido para a quantidade.")
    novo_produto = {
        "id": str(uuid.uuid4()),
        "nome": nome_produto,
        "categoria": categoria_produto,
        "preco": preco_produto,
        "quantidade": quantidade_estoque
    }
    lista_produtos.append(novo_produto)
    salvar_inventario(lista_produtos)
    print(f"Produto '{nome_produto}' adicionado com sucesso!")

def listar_todos_produtos(lista_produtos):
    if not lista_produtos:
        print("Nenhum produto encontrado no inventário.")
        return
    print("\nInventário de Produtos:")
    print(f"{'ID':<36} | {'Nome':<20} | {'Categoria':<15} | {'Preço':<10} | {'Quantidade':<10}")
    print("-" * 100)
    for produto in lista_produtos:
        print(f"{produto['id']:<36} | {produto['nome']:<20} | {produto['categoria']:<15} | R$ {produto['preco']:<10.2f} | {produto['quantidade']:<10}")
    print("-" * 100)

def buscar_produto_por_id_ou_nome(lista_produtos):
    termo_busca = input("Digite o ID ou parte do nome do produto: ").lower()
    produtos_encontrados = [produto for produto in lista_produtos if termo_busca in produto["id"].lower() or termo_busca in produto["nome"].lower()]
    if produtos_encontrados:
        print("\nProdutos encontrados:")
        for produto in produtos_encontrados:
            print(f"ID: {produto['id']}")
            print(f"Nome: {produto['nome']}")
            print(f"Categoria: {produto['categoria']}")
            print(f"Preço: R$ {produto['preco']:.2f}")
            print(f"Quantidade: {produto['quantidade']}")
            print("-" * 40)
    else:
        print("Nenhum produto encontrado com o critério de busca.")

def atualizar_dados_produto(lista_produtos):
    id_produto = input("Digite o ID do produto a ser atualizado: ")
    produto_selecionado = next((produto for produto in lista_produtos if produto["id"] == id_produto), None)
    if produto_selecionado:
        print(f"Produto encontrado: {produto_selecionado['nome']}")
        print("Deixe o campo vazio para manter o valor atual.")
        novo_nome_produto = input(f"Novo nome [{produto_selecionado['nome']}]: ") or produto_selecionado['nome']
        nova_categoria_produto = input(f"Nova categoria [{produto_selecionado['categoria']}]: ") or produto_selecionado['categoria']
        try:
            novo_preco_produto = input(f"Novo preço (atual: R$ {produto_selecionado['preco']:.2f}): ")
            novo_preco_produto = float(novo_preco_produto) if novo_preco_produto else produto_selecionado['preco']
        except ValueError:
            print("Preço inválido. Mantendo o valor atual.")
            novo_preco_produto = produto_selecionado['preco']
        try:
            nova_quantidade_estoque = input(f"Nova quantidade (atual: {produto_selecionado['quantidade']}): ")
            nova_quantidade_estoque = int(nova_quantidade_estoque) if nova_quantidade_estoque else produto_selecionado['quantidade']
        except ValueError:
            print("Quantidade inválida. Mantendo o valor atual.")
            nova_quantidade_estoque = produto_selecionado['quantidade']
        produto_selecionado.update({
            "nome": novo_nome_produto,
            "categoria": nova_categoria_produto,
            "preco": novo_preco_produto,
            "quantidade": nova_quantidade_estoque
        })
        salvar_inventario(lista_produtos)
        print("Produto atualizado com sucesso!")
    else:
        print("Produto não encontrado.")

def excluir_produto_por_id(lista_produtos):
    id_produto = input("Digite o ID do produto a ser excluído: ")
    produto_selecionado = next((produto for produto in lista_produtos if produto["id"] == id_produto), None)
    if produto_selecionado:
        confirmar_exclusao = input(f"Tem certeza que deseja excluir o produto '{produto_selecionado['nome']}'? (s/n): ").lower()
        if confirmar_exclusao == "s":
            lista_produtos.remove(produto_selecionado)
            salvar_inventario(lista_produtos)
            print("Produto excluído com sucesso!")
        else:
            print("Ação cancelada.")
    else:
        print("Produto não encontrado.")

def executar_menu_principal():
    lista_produtos = carregar_inventario()
    while True:
        print("\nMenu Principal:")
        print("1. Adicionar Produto")
        print("2. Listar Produtos")
        print("3. Buscar Produto")
        print("4. Atualizar Produto")
        print("5. Excluir Produto")
        print("6. Sair")
        opcao_menu = input("Escolha uma opção: ")
        if opcao_menu == "1":
            adicionar_novo_produto(lista_produtos)
        elif opcao_menu == "2":
            listar_todos_produtos(lista_produtos)
        elif opcao_menu == "3":
            buscar_produto_por_id_ou_nome(lista_produtos)
        elif opcao_menu == "4":
            atualizar_dados_produto(lista_produtos)
        elif opcao_menu == "5":
            excluir_produto_por_id(lista_produtos)
        elif opcao_menu == "6":
            print("Encerrando a aplicação...")
            break
        else:
            print("Opção inválida. Tente novamente.")

if __name__ == "__main__":
    executar_menu_principal()
