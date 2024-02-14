import oracledb
from dotenv import load_dotenv
import os

def select_valores_db(keyNFe: str) -> list:
    load_dotenv()

    oracledb.init_oracle_client()
    connection = oracledb.connect(  user=os.getenv("DB_USER"), 
                                password=os.getenv("DB_PASSWORD"), 
                                dsn=os.getenv("DB_DSN") )
    cursor  = connection.cursor()

    cursor.execute("select p.seqproduto, i.vlrfcpicms from rf_notamestre n, rf_notaitem i , map_produto p where n.nfechaveacesso = " + keyNFe + " and n.seqnota = i.seqnota and i.vlrfcpicms > 0 and p.seqproduto = i.seqproduto")
    result = cursor.fetchall()

    cursor.close()
    connection.close
    return result

def sql_query(query : str) -> list:
    load_dotenv()

    oracledb.init_oracle_client()
    connection = oracledb.connect(  user=os.getenv("DB_USER"), 
                                password=os.getenv("DB_PASSWORD"), 
                                dsn=os.getenv("DB_DSN") )
    cursor  = connection.cursor()

    cursor.execute(query)
    result = cursor.fetchall()

    cursor.close()
    connection.close
    return result