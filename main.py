import json
from requests import request
from datetime import datetime, timedelta
import re
import random


# Obter a data atual
data_atual = datetime.now()

# Retirando horas
data_hoje = data_atual.strftime("%Y-%m-%d")

# Adicionar dois meses
data_nova = data_atual + timedelta(days=2*30)

# Converter para Str
data_previsao = data_nova.strftime('%d/%m/%Y')

#TODO - Verificar se existe pedido em aberrto

#SECTION - CREDENCIAIS

#NOTE - PEDIDO OK
token_parceiro = "Token parceiro do sistema Pedido Ok"
token_pedido_ok = "Token do sistema do Pedido Ok" 


url_pedidos = "https://api.pedidook.com.br/v1/pedidos/"
url_produtos = "https://api.pedidook.com.br/v1/produtos/"
url_vendedores = 'https://api.pedidook.com.br/v1/vendedores/'

#NOTE - OMIE
app_key = "Api key do erp Omie"
app_secret = "Api secre do erp Omie"
endpoint = "https://app.omie.com.br/api/v1/geral/clientes/"
endpoint_pedido = "https://app.omie.com.br/api/v1/produtos/pedidovenda/"
endpoint_produtos = "https://app.omie.com.br/api/v1/geral/produtos/"
endpoint_vendedores= 'https://app.omie.com.br/api/v1/geral/vendedores/'
endpoint_parcelas = 'https://app.omie.com.br/api/v1/geral/parcelas/'





def cadastrar_clientes(dados_cliente):
        """
        //NOTE - Cadastro de cliente
        Cadastra um cliente no sistema Omie

        Args:
            email (str): email do cliente vindo do Pedido Ok
            razao_social (str): nome do cliente
            cpf (int): cpf do cliente a ser cadastrado
        """
        
        
        
        url = "https://app.omie.com.br/api/v1/geral/clientes/"
        payload = json.dumps({
                                "call": "IncluirCliente",
                                "app_key": app_key,
                                "app_secret": app_secret,
                                "param": [ 
                                        {
                                        "codigo_cliente_integracao": dados_cliente["id"],
                                        "codigo_cliente_omie": dados_cliente["cnpj_cpf"],
                                        "email": dados_cliente["email"],
                                        "razao_social":dados_cliente["razao_social"],
                                        "cnpj_cpf": dados_cliente["cnpj_cpf"],
                                        "endereco": dados_cliente["rua"],
                                        "endereco_numero": dados_cliente["numero"],
                                        "bairro": dados_cliente["bairro"],
                                        "estado": dados_cliente["uf"],
                                        "cidade": dados_cliente["cidade"],
                                        "cep": dados_cliente["cep"]
                                        }
                                    ]
                                })
        headers = {
            "Content-Type": "application/json"
        }
        try:
            response = request("POST", url=url, headers=headers, data=payload)
        except Exception as error: 
            raise Exception(f'Erro ao cadastrar cliente - {error}')
        
        response = response.json()
       
        if 'codigo_cliente_omie' in response:
            print(' cliente omie - Cadastrado')
            return response['codigo_cliente_omie']

        elif response['faultcode'] == 'SOAP-ENV:Client-101' or response['faultcode'] == 'SOAP-ENV:Client-102':
            faultstring = response['faultstring']
            # Extrair o número após o 'nCod' usando uma expressão regular
            match = re.search(r'nCod \[(\d+)\]', faultstring)
            if match:
                ncod = match.group(1)
                return ncod
            else:
                print("Número nCod não encontrado no response.")




def listar_cliente_omie(pagina: int):

    """
    Lista todos os cliente do Omie

    return;
        - Json

    """

    payload = json.dumps({
    'call': 'ListarClientes',
    'app_key': app_key,
    'app_secret': app_secret,
    'param': [
        {   
            "pagina": pagina,
            "registros_por_pagina": 500,
            "apenas_importado_api": "N",
              

        }
    ]
    })
    headers = {
        'Content-Type': 'application/json'
    }

    try:
        response = request(method='POST', url=endpoint, headers=headers, data=payload)
    except Exception as error:
        raise Exception(f'Error ao listar clientes Omie - {error}')
    
    if response.status_code == 200:
        return response.json()
    else:
        pass




def lista_produtos_pedido_ok():
    
    """
    Lista todos os produtos do Pedido Ok

    return;
        - Json

    """

    headers = {
    'Content-Type': 'application/json',
    'token_pedidook': token_pedido_ok,
    'token_parceiro': token_parceiro ,
}
    try:
        response = request(method='GET', url=url_produtos, headers=headers)
    except Exception as error:
        raise Exception(f'Erro ao listar produtos Pedido OK - {error}')
       
    
    if response.status_code == 200:
        return response.json()
    else:
        pass


def listar_produtos_omie(pagina: int):

    """
    Lista todos os produtos do Omie

    return;
        - Json

    """

    payload = json.dumps({
    'call': 'ListarProdutos',
    'app_key': app_key,
    'app_secret': app_secret,
    'param': [
        {
            "pagina": pagina,
            "registros_por_pagina": 500,
            "apenas_importado_api": "N",
            "filtrar_apenas_omiepdv": "N"
              

        }
    ]
    })
    headers = {
        'Content-Type': 'application/json'
    }

    try:
        response = request(method='POST', url=endpoint_produtos, headers=headers, data=payload)
    except Exception as error:
        raise Exception(f'Error ao listar produtos Omie - {error}')
    if response.status_code == 200:
        return response.json()
    else:
        pass



#NOTE - Obtendo todos pedidos do PEDIDO OK
def get_pedidos_ok():
    """
    Obtem todos os pedidos do PEDIDO OK

    return;
        - Json
    
    """
    headers = {
    'token_parceiro': token_parceiro,
    'token_pedidook': token_pedido_ok,
    'Content-Type': 'application/json'
    }

    try:
        response = request(method='GET', url=url_pedidos, headers=headers)
    except Exception as error:
        raise Exception(f'Erro ao Listar pedidos Omie - {error}')

   
    if response.status_code == 200:
        return response.json()
    else:
        pass



def incluir_pedido(pedido_pedido_ok):

    """
    Inclui pedido no Omie
    Recebe um dicionário com os dados do pedido

    """

    
    #FIXME - ESPERAR CLIENTE INFORMAR CODIGO CONTA CORRENTE
    payload = json.dumps({
    'call': 'AdicionarPedido',
    'app_key': app_key,
    'app_secret': app_secret,
    'param': [
        {
            "codigo_cliente":  pedido_pedido_ok["codigo_cliente_omie"], 
           # "codigo_cliente_integracao": pedido_pedido_ok["cnpj_cpf"],
            "codigo_pedido_integracao": pedido_pedido_ok["id_pedido"],
            "codVend": pedido_pedido_ok["cod_vendedor"],
            "data_previsao": data_previsao,      
            "etapa": "10",
            "codigo_parcela": pedido_pedido_ok["codigo_parcela"],
            "codigo_categoria": "1.01.01",
            "codigo_conta_corrente"	: "999", #FIXME - Aguardando resposta
            "numero_pedido_cliente": pedido_pedido_ok["numero"],
            #"contato": pedido_pedido_ok["contatos"],
            "consumidor_final": "S",
            "utilizar_emails":"S",
            #"codVend": pedido_pedido_ok["id_vendedor"],
            "itens": pedido_pedido_ok["itens"],
            



            }
        ]
    })
    headers = {
        'Content-Type': 'application/json'
    }

    try:
        response = request(method='POST', url=endpoint_pedido, headers=headers, data=payload)
       
    except Exception as error:
        raise Exception(f'Erro ao Incluir Pedido no Omie - {error}')

    print(response.json())
    if response.status_code == 200:
        print('Pedido cadastrado com sucesso')
        return response.json()
    else:
        pass




#NOTE - Obtendo todos os clientes do PEDIDO OK
def get_dados_clientes_pedido_ok(pagina):
    """
    Obtem todos os clientes do Pedido Ok

    return;
        - Json


    """
    url_clientes =f"https://api.pedidook.com.br/v1/clientes/?pagina={pagina}"
    headers = {
        'Content-Type': 'application/json',
        'token_pedidook': token_pedido_ok,
        'token_parceiro': token_parceiro ,
    }
    
    try:
        response = request(method='GET', url=url_clientes, headers=headers)
    except Exception as error:
        raise Exception(f'Erro ao Listar Clientes Pedido OK - {error}')  
    
    if response.status_code == 200:
        return response.json()
    else:
        pass




def get_vendedores_pedido_ok():

    headers = {
        'Content-Type': 'application/json',
        'token_pedidook': token_pedido_ok,
        'token_parceiro': token_parceiro ,
    }
    
    try:
        response = request(method='GET', url=url_vendedores, headers=headers)
    except Exception as error:
        raise Exception(f'Erro ao Listar Vendedores do Pedido OK - {error}')
    
   
    
    if response.status_code == 200:
        return response.json()
    else:
        pass


def get_vendedores_omie(pagina):

    payload = json.dumps({
    'call': 'ListarVendedores',
    'app_key': app_key,
    'app_secret': app_secret,
    'param': [
        {
            "pagina": pagina,
            "registros_por_pagina": 500,
            "apenas_importado_api": "N",
            
              

        }
    ]
    })
    headers = {
        'Content-Type': 'application/json'
    }

    try:
        response = request(method='POST', url=endpoint_vendedores, headers=headers, data=payload)
    except Exception as error:
        raise Exception(f'Erro ao Listar vendedores Omie - {error}')
    
    if response.status_code == 200:
        return response.json()
    else:
        pass


def dic_produtos_pedido_ok():

    try:
        dados_produtos = lista_produtos_pedido_ok()

        produtos_pedido_ok = dados_produtos["produtos"]

        dicionario_produtos_pedido_ok = {}

        

        for produtos in produtos_pedido_ok:
            id = produtos.get("id", None)        
            dicionario_produtos_pedido_ok[id] = produtos.get("codigo", None)
            
        # print(dicionario_produtos_pedido_ok)
        

        return dicionario_produtos_pedido_ok
    except Exception as error:
        raise Exception(f'Erro ao criar dicionario dos produtos do Pedido Ok - {error}')




def dic_produtos_omie():

    try:
        pagina = 1
        total_de_paginas = 1
        
        while pagina <= total_de_paginas:

        
            dados_produtos_omie = listar_produtos_omie(pagina=pagina)        
            produtos_omie = dados_produtos_omie["produto_servico_cadastro"]   


            dicionario_produtos_omie = {}

            for produtos in produtos_omie:
                itens = {}
                itens["valor_unitario"] = produtos.get("valor_unitario")        
                itens["codigo_produto"] = produtos.get("codigo_produto")                
                itens["cfop"] = "6.101"
                codigo = produtos.get("codigo")

                dicionario_produtos_omie[codigo] = itens

            total_de_paginas = int(dados_produtos_omie["total_de_paginas"])
            
            pagina += 1

        return dicionario_produtos_omie 
    except Exception as error:
        raise Exception(f'Erro ao Criar dicionario de produtos Omie - {error}')




def dic_clientes_omie():
    try:
        pagina = 1
        total_de_paginas = 1
    
        

        while pagina <= total_de_paginas:

            dados = listar_cliente_omie(pagina=pagina)
            lista_cliente = dados["clientes_cadastro"]

            dic_codigo_cliente_omie = {}
            itens = {}

            for clientes in lista_cliente:
                
                cnpj_completo = clientes.get("cnpj_cpf") 
                cnpj = cnpj_completo.replace(".","").replace("/","").replace("-","")
                dic_codigo_cliente_omie[cnpj] = itens
                itens[cnpj] = clientes.get("codigo_cliente_omie")
            
            total_de_paginas = int(dados["total_de_paginas"])
            
            pagina += 1
        
        
        return itens
    except Exception as error:
        raise Exception(f'Erro ao criar Dicionario de clientes Omie - {error}')



def dic_clientes_pedido_ok():
    try:
        pagina = 1
        dicionario_clientes_pedido_ok = {}
        while pagina <= 20000:
            
            dados = get_dados_clientes_pedido_ok(pagina=pagina)
            total_pagina = dados["href_proxima_pagina"]
            if total_pagina == None:
                break
            else:
                clientes_pedido = dados["clientes"]

                
                    
                for clientes in clientes_pedido:
                
                    id = clientes.get("id", None)       
                    
                    dicionario_clientes_pedido_ok[id] = clientes.get("cnpj_cpf", None)
                
                pagina += 1            
                
            
        return dicionario_clientes_pedido_ok
    except Exception as error:
        raise Exception(f'Erro ao criar dicionario de clientes Pedido OK - {error}')




def dic_vendedores_pedido_ok():
    
    try:
        dados = get_vendedores_pedido_ok()
        vendedores_pedido = dados["vendedores"]

        dicionario_vendedores_pedido_ok = {}

        for vendedores in vendedores_pedido:
            id_vendedor_pedido = vendedores.get("id", None)
            dicionario_vendedores_pedido_ok[id_vendedor_pedido] = vendedores["nome"]

        return dicionario_vendedores_pedido_ok
    except Exception as error:
        raise Exception(f'Erro ao criar dicionario de vendedores do Pedido OK - {error}')
        




def dic_vendedores_omie():
    
    try:
        pagina = 1
        total_de_paginas = 1

        while pagina <= total_de_paginas:
        
            dados = get_vendedores_omie(pagina)
            vendedores_omie = dados["cadastro"]

            dicionario_vendedores_omie = {}

            for vendedores in vendedores_omie:
                nome_vendedor = vendedores["nome"]
                dicionario_vendedores_omie[nome_vendedor] = vendedores["codigo"]
        
        
            total_de_paginas = int(dados["total_de_paginas"])
            pagina += 1
        
        return dicionario_vendedores_omie
    except Exception as error:
        raise Exception(f'Erro ao criar dicionario de vendedores Omie - {error}')



def lista_cod_parcelas_omie(pagina:int):
    payload = json.dumps({
    'call': 'ListarParcelas',
    'app_key': app_key,
    'app_secret': app_secret,
    'param': [
        {
            "pagina": pagina,
            "registros_por_pagina": 500,                      
              

        }
    ]
    })
    headers = {
        'Content-Type': 'application/json'
    }

    try:
        response = request(method='POST', url=endpoint_parcelas, headers=headers, data=payload)
    except Exception as error:
        raise Exception(f'Erro ao Listar codigo de Parcelas Omie - {error}')
    
    if response.status_code == 200:
        return response.json()
    else:
        pass



def lista_clientes_pedido_ok():
    '''
    - Cria um Json com dados dos clientes do Pedido OK
    - return
        Json
    '''
    try:
        pagina = 1
        json_clientes_pedido_ok = {}
        while pagina <= 20000:
            dados_clientes_pedido_ok = get_dados_clientes_pedido_ok(pagina=pagina)
            total_pagina = dados_clientes_pedido_ok["href_proxima_pagina"]
            if total_pagina == None:
                break
            else:
                clientes_pedido_ok = dados_clientes_pedido_ok["clientes"]

                
                

                for clientes in clientes_pedido_ok:
                    dicionario_clientes = {}
                    cnpj = clientes.get("cnpj_cpf", None)
                    dicionario_clientes["email"] = clientes.get("email_copia_pedido", None)
                    dicionario_clientes["razao_social"] = clientes.get("razao_social", None)
                    dicionario_clientes["cnpj_cpf"] = clientes.get("cnpj_cpf", None)
                    dicionario_clientes["id"] = clientes.get("id", None)
                    endereco_entrega = clientes["endereco_entrega"]

                
                    dicionario_clientes["uf"] = endereco_entrega.get("uf", None) 
                    dicionario_clientes["cidade"] = endereco_entrega.get("cidade", None) 
                    dicionario_clientes["numero"] = endereco_entrega.get("numero", None) 
                    dicionario_clientes["rua"] = endereco_entrega.get("logradouro", None) 
                    dicionario_clientes["bairro"] = endereco_entrega.get("bairro", None) 
                    dicionario_clientes["cep"] = endereco_entrega.get("cep", None)
                
                    json_clientes_pedido_ok[cnpj] = dicionario_clientes
                pagina += 1  
        
            
        return json_clientes_pedido_ok
    except Exception as error:
        raise Exception(f'Erro ao criar Json com informacoes dos clientes do Pedido Ok - {error}')


def descobrir_cod_pagamento():
    '''
    - Descrobrir qual o codigo do parcelamento do pedido
    - recebe como parametro uma lista do pedido Ok que já foi tratato e trasnformado em uma Str
    - Chave do dicionario é a quantidade de meses do parcelamento. ex: 30/60/90
    '''

    try:
        pagina = 1
        total_de_paginas = 1 
        
        dicionario_parcelas_omie = {}
        while pagina <= total_de_paginas:
            dados_parcelas =lista_cod_parcelas_omie(pagina)
            parcelas_omie = dados_parcelas["cadastros"]

            

            for parcelas in parcelas_omie:
                descricao = parcelas["cDescricao"]
        
                dicionario_parcelas_omie[descricao] = parcelas["nCodigo"]
            
            total_de_paginas = int(dados_parcelas["total_de_paginas"])
            
            pagina += 1  

        return  dicionario_parcelas_omie
    except Exception as error:
        raise Exception(f'Error ao Verificar codigo do Parcelamento do Pedido de Venda - {error}')



def config_forma_pagamento(forma_pag):
    forma_pag_modificado = ''
    if forma_pag == '0':        
        forma_pag_modificado = 'À Vista'
        return forma_pag_modificado
    if forma_pag == '1':        
        forma_pag_modificado = '1 Parcela'
        return forma_pag_modificado
    if forma_pag == '2':
        forma_pag_modificado = '2 Parcelas'
        return forma_pag_modificado
    if forma_pag == '3':
        forma_pag_modificado = '3 Parcelas'
        return forma_pag_modificado
    if forma_pag == '4':
        forma_pag_modificado = '4 Parcelas'
        return forma_pag_modificado
    if forma_pag == '5':
        forma_pag_modificado = '5 Parcelas'
        return forma_pag_modificado
    if forma_pag == '6':
        forma_pag_modificado = '6 Parcelas'
        return forma_pag_modificado
    if forma_pag == '7':
        forma_pag_modificado = '7 Parcelas'
        return forma_pag_modificado
    if forma_pag == '8':
        forma_pag_modificado = '8 Parcelas'
        return forma_pag_modificado
    if forma_pag == '9':
        forma_pag_modificado = '9 Parcelas'
        return forma_pag_modificado
    if forma_pag == '10':
        forma_pag_modificado = '10 Parcelas'
        return forma_pag_modificado
    if forma_pag == '11':
        forma_pag_modificado = '11 Parcelas'
        return forma_pag_modificado
    if forma_pag == '12':
        forma_pag_modificado = '12 Parcelas'
        return forma_pag_modificado
    if forma_pag == '13':
        forma_pag_modificado = '13 Parcelas'
        return forma_pag_modificado
    if forma_pag == '14':        
        forma_pag_modificado = '14 Parcelas'
        return forma_pag_modificado
    if forma_pag == '15':
        forma_pag_modificado = '15 Parcelas'
        return forma_pag_modificado
    if forma_pag == '16':
        forma_pag_modificado = '16 Parcelas'
        return forma_pag_modificado
    if forma_pag == '17':
        forma_pag_modificado = '17 Parcelas'
        return forma_pag_modificado
    if forma_pag == '18':
        forma_pag_modificado = '18 Parcelas'
        return forma_pag_modificado
    if forma_pag == '19':
        forma_pag_modificado = '19 Parcelas'
        return forma_pag_modificado
    if forma_pag == '20':
        forma_pag_modificado = '20 Parcelas'
        return forma_pag_modificado

    if forma_pag == '21':
        forma_pag_modificado = '21 Parcelas'
        return forma_pag_modificado

#SECTION - Chamando funções

dicionario_clientes_pedido_ok= dic_clientes_pedido_ok()

dic_codigo_cliente_omie = dic_clientes_omie()

dicionario_produtos_pedido_ok = dic_produtos_pedido_ok()

dicionario_produtos_omie = dic_produtos_omie()

dicionario_vendedores_pedido_ok = dic_vendedores_pedido_ok()

dicionario_vendedores_omie = dic_vendedores_omie()

dicionario_parcelas_omie = descobrir_cod_pagamento()

json_clientes_pedido_ok = lista_clientes_pedido_ok()




try:
    dados_pedidos = get_pedidos_ok()
    pedidos = dados_pedidos["pedidos"]

    
    lista_dicionario_pedidos = []
    
    #SECTION -  - Adicionando dados do pedido no Dicionário 
    for dados_pedidos in pedidos:
        situacao = dados_pedidos["situacao"]
        emissao = dados_pedidos["emissao"]
        
        if situacao == 'Pendente':
            dicionario_pedido = {}
            


            #NOTE - Adicionando codgo cliente omie no dicionário
            id_cliente_pedido_ok = dados_pedidos.get("id_cliente", None) 
            cnpj_cliente_pedido = dicionario_clientes_pedido_ok.get(id_cliente_pedido_ok)
            codigo_cliente_omie = dic_codigo_cliente_omie.get(cnpj_cliente_pedido, None)
            dicionario_pedido["codigo_cliente_omie"] = codigo_cliente_omie

        
            

            #NOTE - Obtendo dados do cliente PEDIDO OK
            dados_cliente_pedido_ok = json_clientes_pedido_ok.get(cnpj_cliente_pedido, None)
            
            
            #NOTE - Verificar se cliente Pedido Ok já está cadastrado no Omie. Caso não esteja cliente será cadasrado 
            if codigo_cliente_omie == None:            
                
                codigo_cliente_pedido = cadastrar_clientes(dados_cliente_pedido_ok)
                
                dicionario_pedido["codigo_cliente_omie"] = codigo_cliente_pedido



            #NOTE - Adicionando dados no dicionário para criar o pedido        
        
            dicionario_pedido["id_pedido"] = random.randint(10**13, 10**14 - 1)  
            dicionario_pedido["id_cliente"] = dados_pedidos.get("id_cliente", None)      
            dicionario_pedido["base_vencimento"] = dados_pedidos.get("base_vencimento", None)
            dicionario_pedido["numero"] = dados_pedidos.get("numero", None)
            dicionario_pedido["tipo_desconto_acrescimo"] = dados_pedidos.get("tipo_desconto_acrescimo", None)           
            dicionario_pedido["forma_pagamento"] = dados_pedidos.get("forma_pagamento", None)
            dicionario_pedido["emissao"] = dados_pedidos.get("emissao", None)
            dicionario_pedido["id_tabela_preco"] = dados_pedidos.get("id_tabela_preco", None)
            dicionario_pedido["condicao_pagamento"] = dados_pedidos.get("condicao_pagamento", None)
            dicionario_pedido["valor_desconto_acrescimo"] = dados_pedidos.get("valor_desconto_acrescimo", None)

            #NOTE - Adicionar codigo de parcelas no dicionario
            lista_cod_pagamento_original = dicionario_pedido["condicao_pagamento"]                 
            lista_cod_pagamento = '/'.join(str(item) for item in lista_cod_pagamento_original)
            condicao_pagamento = config_forma_pagamento(lista_cod_pagamento)
            cod_pagamento = dicionario_parcelas_omie.get(condicao_pagamento, None)
            dicionario_pedido["codigo_parcela"] = cod_pagamento


                
            #NOTE - Adicionar vendedores ao dicionario
            id_vendedor = dados_pedidos.get("id_vendedor", None)
            nome_vendedor_pedido_ok = dicionario_vendedores_pedido_ok.get(id_vendedor, None)
            codigo_vendedor = dicionario_vendedores_omie.get(nome_vendedor_pedido_ok, None)
            dicionario_pedido["cod_vendedor"] = codigo_vendedor
            
            

            dados_itens = dados_pedidos["itens"]
            if len(dados_itens) == 0:
                id_pedido = dicionario_pedido["id_pedido"]
                print(f'Lista de itens está vazia!, Não foi possivel gerar o pedido com ID:{id_pedido}')
                
            else:
            
                itens = []
                
                #NOTE - Adicionar codigo do produto no dicionario
                for itens_pedidos in dados_itens:
                    item = {}
                    id = itens_pedidos.get("id_produto", None)
                    cod_produto_pedido_ok = dicionario_produtos_pedido_ok.get(id, None)
                    try:
                        cod_produto_omie = dicionario_produtos_omie[cod_produto_pedido_ok].get("codigo_produto", None)            
                        cfop = dicionario_produtos_omie[cod_produto_pedido_ok].get("cfop", None)
                        item["valor_unitario"] = itens_pedidos.get("preco_liquido", None)
                        item["percentual_desconto"] = itens_pedidos.get("percentual_desconto_acrescimo", None)
                        item["tipo_desconto"] = "P"
                        item["quantidade"] = itens_pedidos.get("quantidade", None)
                        item["codigo_produto"] = cod_produto_omie
                    except Exception as error:
                        raise Exception (f'Produto não cadastrado no Omie - {error}')          
                    
                    item["cfop"] = cfop

                    itens.append(item)
                
                    dicionario_pedido["itens"] = itens

                    lista_dicionario_pedidos.append(dicionario_pedido)
            
     
except Exception as error:
    raise Exception (f'Erro ao Criar Dicionario para incluir no Pedido de Venda Omie - {error}')


for pedidos in lista_dicionario_pedidos:
    incluir_pedido(pedidos)