import readXML_cProd_vFCP as xml
import os
import connectDB
import sys
from loguru import logger

def find_XMLfiles_recursively_directories(root_dir: str) -> list:
    xml_files = []
    for current_dir, subdirs, files in os.walk(root_dir):
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

def calc_sum(l: list, sum: float) -> float:
    if l:
        for t in l:
            sum += t[1]
    return round(sum, 4)
            
def main():
    #configura o que irá mostar no console
    logger.configure(handlers=[{"sink": sys.stderr, "level": "WARNING"}])
    # Configuração para salvar todos os níveis de log em um arquivo
    logger.add("log/log.log", level="DEBUG", rotation="500 MB")

    xml_list = find_XMLfiles_recursively_directories('xml') 
    
    total_xml = 0.0
    total_fiscal = 0.0
    for xml_file in xml_list:
        if xml_file.endswith('.xml') and os.path.isfile(xml_file):
            logger.info(xml_file)
            root_xml = xml.load_xml(xml_file)
            dict_prod_vfcf = xml.search_cProd_and_vFCP_optimization(root_xml)
            
            if dict_prod_vfcf:
                keyNFe = xml.get_accesskeyNFe(root_xml)                
                
                # teste para verificar se o cupom foi cancelado
                querySelect = 'select n.CODSITDOC from rf_notamestre n where n.nfechaveacesso = '+ keyNFe +' and n.CODSITDOC NOT IN (2,3,4,5)'
                if connectDB.sql_query(querySelect):
                    prod_vfcf_db = connectDB.select_valores_db(keyNFe)
                
                    logger.debug(f'chave: {keyNFe}')
                    logger.debug(f'xml = {dict_prod_vfcf}')
                    logger.debug(f'nfc = {prod_vfcf_db}')

                    # calculo do valor total dos campos
                    total_xml = calc_sum(dict_prod_vfcf, total_xml)
                    total_fiscal = calc_sum(prod_vfcf_db, total_fiscal)

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
    
    logger.debug(f'Total xml = {total_xml}')
    logger.debug(f'Total fiscal = {total_fiscal}')
    print(f'Total xml = {total_xml}')
    print(f'Total fiscal = {total_fiscal}')


if __name__ == "__main__":
    main()
exit()