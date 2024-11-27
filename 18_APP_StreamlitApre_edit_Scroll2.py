#Na linha de comandos ir para o caminho do script
#Correr a instrução na linha de comandos: streamlit run nomedaapp.py

import streamlit as st
import mysql.connector
from mysql.connector import Error

# Função para obter os produtos da base de dados
def listar_produtos():
    try:
        mydb = mysql.connector.connect(
            host="localhost",
            user="root",
            password="",
            database="dbtestestabelas"
        )
        
        mycursor = mydb.cursor()
        
        mycursor.execute("SELECT * FROM Produtos")
        
        registos = mycursor.fetchall()
        return registos
    except Error as err:
        st.error(f"Erro ao listar os produtos: {err}")
        return []
    finally:
        if mydb.is_connected():
            mycursor.close()
            mydb.close()

# Função para atualizar um produto 
def atualizar_produto(id_produto, nome, descricao, preco, quantidade):
    try:
        mydb = mysql.connector.connect(
            host="localhost",
            user="root",
            password="",
            database="dbtestestabelas"
        )
        mycursor = mydb.cursor()
        sql = """
        UPDATE Produtos 
        SET Produto_nome = %s, Produto_descrit = %s, Produto_preco = %s, Produto_quantidade = %s 
        WHERE Produto_id = %s
        """
        valores = (nome, descricao, preco, quantidade, id_produto)
        mycursor.execute(sql, valores)
        mydb.commit()
        st.success("Produto atualizado com sucesso!")
    except Error as err:
        st.error(f"Erro ao atualizar o produto: {err}")
    finally:
        if mydb.is_connected():
            mycursor.close()
            mydb.close()

# Função para adicionar um novo produto na tabela produtos da base de dados
def adicionar_produto(nome, descricao, preco, quantidade):
    try:
        mydb = mysql.connector.connect(
            host="localhost",
            user="root",
            password="",
            database="dbtestestabelas"
        )
        mycursor = mydb.cursor()
        
        sql = """
        INSERT INTO Produtos (Produto_nome, Produto_descrit, Produto_preco, Produto_quantidade)
        VALUES (%s, %s, %s, %s)
        """
        
        valores = (nome, descricao, preco, quantidade)
        mycursor.execute(sql, valores)
        mydb.commit()
        st.success("Produto adicionado com sucesso!")
    except Error as err:
        st.error(f"Erro ao adicionar o produto: {err}")
    finally:
        if mydb.is_connected():
            mycursor.close()
            mydb.close()

# Configuração da página
st.set_page_config(page_title="Gestão de Produtos", layout="wide")
st.title("Gestão de Produtos")

# Layout de colunas
col1, col2 = st.columns([1, 2])  # Coluna esquerda menor para a lista

# Estado para armazenar dados do produto selecionado
if 'produto_selecionado' not in st.session_state:
    st.session_state['produto_selecionado'] = None

# Coluna 1: Lista de Produtos
with col1:
    st.header("Lista de Produtos")
    produtos = listar_produtos()

    if produtos:
        for produto in produtos:
            if st.button(f"Selecionar: {produto[1]} (ID {produto[0]})", key=f"produto_{produto[0]}"):
                st.session_state['produto_selecionado'] = produto
    else:
        st.write("Nenhum produto encontrado.")

# Coluna 2: Formulários
with col2:
    produto = st.session_state['produto_selecionado']

    # Formulário de edição de produtos
    st.header("Editar Produto")
    if produto:
        st.write(f"**Editar Produto ID {produto[0]}**")
        with st.form("form_editar"):
            nome = st.text_input("Nome", produto[1])
            descricao = st.text_area("Descrição", produto[2])
            preco = st.number_input("Preço", min_value=0.0, step=0.01, value=float(produto[3]))
            quantidade = st.number_input("Quantidade", min_value=0, step=1, value=int(produto[4]))

            enviado = st.form_submit_button("Atualizar Produto")
            if enviado:
                if nome and descricao and preco and quantidade:
                    atualizar_produto(produto[0], nome, descricao, preco, quantidade)
                    st.session_state['produto_selecionado'] = None  # Reset após atualizar
                else:
                    st.error("Todos os campos devem ser preenchidos!")
    else:
        st.write("Selecione um produto na lista para editar.")

    # Formulário para adicionar novo produto
    st.header("Adicionar Novo Produto")
    with st.form("form_adicionar"):
        novo_nome = st.text_input("Nome do Produto")
        nova_descricao = st.text_area("Descrição do Produto")
        novo_preco = st.number_input("Preço", min_value=0.0, step=0.01)
        nova_quantidade = st.number_input("Quantidade", min_value=0, step=1)

        adicionado = st.form_submit_button("Adicionar Produto")
        if adicionado:
            if novo_nome and nova_descricao and novo_preco and nova_quantidade:
                adicionar_produto(novo_nome, nova_descricao, novo_preco, nova_quantidade)
            else:
                st.error("Todos os campos devem ser preenchidos!")
