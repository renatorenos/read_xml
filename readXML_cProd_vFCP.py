from lxml import etree
import re

def search_cProd_vFCP(root : etree._Element) -> None:
    # Definir o namespace
    namespace = {'nfe': 'http://www.portalfiscal.inf.br/nfe'}

    # Encontrar todas as ocorrências da tag <det>
    dets = root.xpath('//nfe:det', namespaces=namespace)

    # Iterar sobre as ocorrências de <det>
    for det in dets:
        # Encontrar a tag <prod><cprod> dentro de <det>
        cprod_element = det.find('.//nfe:prod/nfe:cProd', namespaces=namespace)
        
        # Se a tag <cProd> for encontrada dentro de <cProd>, obter seu valor
        if cprod_element is not None:
            cprod_valor = cprod_element.text
        else:
            cprod_valor = "N/A" 

        # Encontrar a tag <imposto><ICMS><ICMS00><vFCP> dentro de <det>
        vfcp_element = det.find('.//nfe:imposto/nfe:ICMS/nfe:ICMS00/nfe:vFCP', namespaces=namespace)

        # Se a tag <vfcp> for encontrada dentro de <icms00>, obter seu valor
        if vfcp_element is not None:
            vfcp_valor = vfcp_element.text
        else:
            vfcp_valor = "N/A"  

        # Imprimir os valores
        print(f'Value of <cProd>: {cprod_valor}, Value of <vFCP>: {vfcp_valor}')

def search_cProd_and_vFCP_optimization(root : etree._Element) -> list:
    lista_inf = []
    namespace = {'nfe': 'http://www.portalfiscal.inf.br/nfe'}

    dets = root.xpath('//nfe:det', namespaces=namespace)
    for det in dets:
        vfcp_element = det.find('.//nfe:imposto/nfe:ICMS/nfe:ICMS00/nfe:vFCP', namespaces=namespace)
        if vfcp_element is not None:
            vfcp_valor = vfcp_element.text

            cprod_element = det.find('.//nfe:prod/nfe:cProd', namespaces=namespace)  
            if cprod_element is not None:
                cprod_valor = cprod_element.text
        
            lista_inf.append((int(cprod_valor), float(vfcp_valor)))
    return lista_inf

def get_accesskeyNFe(root : etree._Element) -> str:
    namespace = {'nfe': 'http://www.portalfiscal.inf.br/nfe'}
    infNFe_element = root.find('.//nfe:infNFe', namespaces=namespace)

    if infNFe_element is not None:
        id_valor = infNFe_element.get('Id')
        return re.sub(r'\D', '', id_valor)

def load_xml(file : str) -> etree._Element:    
    try:
        # Carregar o arquivo XML
        tree = etree.parse(file)
        return tree.getroot()

    except etree.XMLSyntaxError as e:
            print(f'Error processing {file} file: {e}')