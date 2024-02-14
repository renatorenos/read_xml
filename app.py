import readXML_cProd_vFCP as xml
import os
import connectDB
import sys
from loguru import logger

def find_XMLfiles_recursively_directories(root_dir: str) -> list:
    xml_files = []

    print(os.walk(root_dir))

    for current_dir, files in os.walk(root_dir):
        for f in files:
            if f.endswith('.xml'):
                full_path = os.path.join(current_dir, f)
                xml_files.append(full_path)

    return xml_files

def remove_file(file : str, logger : logger) -> None:
    try:
        os.remove(file)
        logger.info(f'{file} file deleted.')
    except OSError as e:                    
        logger.error(f"Error:{ e.strerror}")

def main():
    #configura o que irá mostar no console
    logger.configure(handlers=[{"sink": sys.stderr, "level": "WARNING"}])

    # Configuração para salvar todos os níveis de log em um arquivo
    logger.add("log/log.log", level="DEBUG", rotation="500 MB")

    xml_list = find_XMLfiles_recursively_directories('xml')
    
    for xml_file in xml_list:
        if xml_file.endswith('.xml') and os.path.isfile(xml_file):
            logger.info(xml_file)
            root_xml = xml.load_xml(xml_file)
            dict_prod_vfcf = xml.search_cProd_and_vFCP_optimization(root_xml)
            
            if dict_prod_vfcf:
                keyNFe = xml.get_accesskeyNFe(root_xml)                
                
                querySelect = 'select n.CODSITDOC from rf_notamestre n where n.nfechaveacesso = '+ keyNFe +' and n.CODSITDOC NOT IN (2,3,4,5)'
                # teste para verificar se o cupom foi cancelado
                if connectDB.sql_query(querySelect):
                    prod_vfcf_db = connectDB.select_valores_db(keyNFe)
                
                    logger.debug(f'chave: {keyNFe}')
                    logger.debug(f'xml = {dict_prod_vfcf}')
                    logger.debug(f'nfc = {prod_vfcf_db}')
                    
                    if set(dict_prod_vfcf) != set(prod_vfcf_db):                    
                        print(f'chave: {keyNFe}')
                        print(f'xml = {dict_prod_vfcf}')
                        print(f'nfc = {prod_vfcf_db}')
                        print('\n-----------------------------------------------------------------------------------------------')

                        logger.info('Different information.')
                        logger.info(keyNFe)
                        logger.info(dict_prod_vfcf)
                        logger.info(prod_vfcf_db)
                    else:
                        remove_file(xml_file, logger)
                else:
                    remove_file(xml_file, logger)
            else:
                remove_file(xml_file, logger)
    
if __name__ == "__main__":
    main()
exit()