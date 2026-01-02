import sys
import requests

BASE_URL = "http://127.0.0.1:8000"

# ------------------ CONEXÃO ------------------

def testar_conexao():
    try:
        r = requests.get(f"{BASE_URL}/")
        if r.status_code == 200:
            print("✅ Conectado ao servidor FastAPI")
        else:
            print("⚠️ Servidor respondeu:", r.status_code)
    except requests.exceptions.RequestException as e:
        print("❌ Servidor offline:", e)
        sys.exit()

# ------------------ LIVROS ------------------

def listar_livros():
    r = requests.get(f"{BASE_URL}/livros/")
    livros = r.json()

    if not livros:
        print("\n⚠️ Nenhum livro cadastrado\n")
        return

    print("\n=== LIVROS ===")
    for l in livros:
        print(f"ID: {l['id']} | {l['nome']} | R$ {l['preco']:.2f}")
    print("==============\n")

def adicionar_livro():
    print("\nNovo livro")
    payload = {
        "nome": input("Nome: "),
        "marca": input("Marca: "),
        "preco": float(input("Preço: ")),
        "estoque": int(input("Estoque: ")),
        "volume": input("Volume: "),
        "descricao": input("Descrição: "),
        "imagem_url": input("Imagem (opcional): ")
    }

    r = requests.post(f"{BASE_URL}/livros/", json=payload)
    if r.status_code == 200:
        print("✅ Livro adicionado\n")
    else:
        print("❌ Erro:", r.text)

def buscar_livro():
    livro_id = input("ID do livro: ")
    r = requests.get(f"{BASE_URL}/livros/{livro_id}")

    if r.status_code == 200:
        l = r.json()
        print("\nLivro encontrado:")
        for k, v in l.items():
            print(f"{k}: {v}")
        print()
    else:
        print("❌ Livro não encontrado\n")

def deletar_livro():
    livro_id = input("ID do livro: ")
    r = requests.delete(f"{BASE_URL}/livros/{livro_id}")

    if r.status_code == 200:
        print("🗑️ Livro deletado\n")
    else:
        print("❌ Erro:", r.text)

# ------------------ MENU ------------------

def menu():
    while True:
        print("""
==========================
📚 BookShop - ADMIN
==========================
1 - Listar livros
2 - Adicionar livro
3 - Buscar livro
4 - Deletar livro
0 - Sair
""")
        op = input("Escolha: ")

        if op == "1":
            listar_livros()
        elif op == "2":
            adicionar_livro()
        elif op == "3":
            buscar_livro()
        elif op == "4":
            deletar_livro()
        elif op == "0":
            sys.exit()
        else:
            print("❌ Opção inválida\n")

# ------------------ MAIN ------------------

if __name__ == "__main__":
    testar_conexao()
    menu()
