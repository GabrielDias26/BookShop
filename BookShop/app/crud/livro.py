from sqlalchemy.orm import Session  # sessão do SQLAlchemy
from app.models.livro import livro as LivroModel  # modelo ORM do livro
from app.schemas import livro as schemas_livro  # schemas Pydantic para validação
from fastapi import HTTPException  # para lançar erros HTTP

# Cria um livro no banco
def criar_livro(db: Session, livro):
    # converte Pydantic para dicionário se necessário
    if hasattr(livro, "model_dump"):
        livro_data = livro.model_dump()
    else:
        livro_data = livro

    novo = LivroModel(**livro_data)  # cria objeto ORM
    db.add(novo)                      # adiciona à sessão
    db.commit()                        # salva no banco
    db.refresh(novo)                   # atualiza objeto com valores do DB
    return novo                        # retorna o objeto criado

# Retorna todos os livros
def listar_livros(db: Session):
    return db.query(LivroModel).all()

# Busca um livro específico pelo ID
def buscar_livro(db: Session, livro_id: int):
    livro_obj = db.query(LivroModel).filter(LivroModel.id == livro_id).first()
    if not livro_obj:
        raise HTTPException(status_code=404, detail="livro não encontrado")
    return livro_obj

# Atualiza os dados de um livro
def atualizar_livro(db: Session, livro_id: int, dados: schemas_livro.livroCreate):
    livro_obj = db.query(LivroModel).filter(LivroModel.id == livro_id).first()
    if not livro_obj:
        raise HTTPException(status_code=404, detail="livro não encontrado")

    # atualiza cada atributo do livro
    for key, value in dados.model_dump().items():
        setattr(livro_obj, key, value)

    db.commit()       # salva alterações
    db.refresh(livro_obj)  # atualiza objeto com valores do DB
    return livro_obj

# Deleta um livro pelo ID
def deletar_livro(db: Session, livro_id: int):
    livro_obj = db.query(LivroModel).filter(LivroModel.id == livro_id).first()
    if not livro_obj:
        raise HTTPException(status_code=404, detail="livro não encontrado")
    db.delete(livro_obj)
    db.commit()

# Lista livros em destaque, com limite padrão 4
def listar_destaques(db: Session, limite: int = 4):
    return db.query(LivroModel).limit(limite).all()
