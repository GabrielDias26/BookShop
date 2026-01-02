import sys
import requests

BASE_URL = "http://127.0.0.1:8000"

# ------------------ CONEXÃO ------------------

def testar_conexao():
    try:
        r = requests.get(f"{BASE_URL}/")
        if r.status_code == 200:
            print(" Conectado ao servidor ADM FastAPI\n")
        else:
            print(" Servidor respondeu:", r.status_code)
    except requests.exceptions.RequestException as e:
        print(" Servidor offline:", e)
        sys.exit()

# ------------------ FUNÇÕES ADM ------------------

def listar_livros():
    r = requests.get(f"{BASE_URL}/livros/")
    if r.status_code != 200:
        print(" Erro ao listar livros\n")
        return

    livros = r.json()
    if not livros:
        print("\n Nenhum livro cadastrado\n")
        return

    print("\n=== LIVROS CADASTRADOS ===")
    for l in livros:
        print(f"ID: {l['id']} | {l['nome']} | R$ {l['preco']:.2f}")
    print("==========================\n")

def adicionar_livro():
    print("\n Adicionando Novo Livro")

    try:
        payload = {
            "nome": input("Nome: ").strip(),
            "marca": input("Marca: ").strip(),
            "preco": float(input("Preço: ").strip()),
            "estoque": int(input("Estoque: ").strip()),
            "volume": input("Volume: ").strip(),
            "descricao": input("Descrição: ").strip(),
            "imagem_url": input("Imagem (opcional): ").strip()
        }
    except ValueError:
        print(" Preço ou estoque inválido\n")
        return

    r = requests.post(f"{BASE_URL}/livros/", json=payload)

    if r.status_code == 200:
        print(" Livro adicionado com sucesso!\n")
    else:
        print(" Erro ao adicionar livro:")
        print(r.text, "\n")

def deletar_livro():
    listar_livros()
    livro_id = input("Digite o ID do livro a deletar: ").strip()

    if not livro_id.isdigit():
        print(" ID inválido\n")
        return

    r = requests.delete(f"{BASE_URL}/livros/{livro_id}")

    if r.status_code == 200:
        print(f" Livro {livro_id} deletado com sucesso!\n")
    else:
        print(" Erro ao deletar livro:")
        print(r.text, "\n")

# ------------------ MENU ------------------

def menu():
    while True:
        print("""
==========================
 BookShop - ADMIN
==========================
1 - Listar livros
2 - Adicionar livro
3 - Deletar livro
0 - Sair
""")
        op = input("Escolha: ").strip()

        if op == "1":
            listar_livros()
        elif op == "2":
            adicionar_livro()
        elif op == "3":
            deletar_livro()
        elif op == "0":
            print(" Saindo...")
            sys.exit()
        else:
            print(" Opção inválida\n")

# ------------------ MAIN ------------------

if __name__ == "__main__":
    testar_conexao()
    menu()
