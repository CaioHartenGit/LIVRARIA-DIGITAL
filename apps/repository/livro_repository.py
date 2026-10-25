from apps.database.conexao import Conectar
from psycopg.rows import dict_row

class LivroRepository:
    def cadastrar(self,titulo,autor,total_paginas,arquivo_path):
        conn = Conectar.conectar()
        cursor = conn.cursor(row_factory = dict_row)

        try:
            cursor.execute(
                '''
                INSERT INTO livro(titulo, autor, total_paginas, arquivo_path)
                VALUES (%s,%s,%s,%s)
                RETURNING id, titulo, autor, total_paginas, arquivo_path, ativo
                
                ''',(titulo,autor, total_paginas,arquivo_path)
            )
            livro = cursor.fetchone()
            conn.commit()
            return livro
        
        except Exception:
            conn.rollback()
            raise
        finally:
            cursor.close()
            conn.close()

    def listar_livros(self):
        conn = Conectar.conectar()
        cursor = conn.cursor(row_factory = dict_row)

        try:
            cursor.execute(
            '''
            SELECT id, titulo, autor, total_paginas, arquivo_path, ativo
            FROM livro
            '''
            )
            livro = cursor.fetchall()
            return livro
        
        except Exception:
            conn.rollback()
            raise

        finally:
            cursor.close()
            conn.close()

    def buscar_livro_por_id(self,id):
        conn = Conectar.conectar()
        cursor = conn.cursor(row_factory = dict_row)
        try:
            cursor.execute(
                '''
                SELECT id, titulo, autor, total_paginas, arquivo_path, ativo
                FROM livro
                WHERE id = %s
                ''',(id,)
            )
            livro = cursor.fetchone()
            return livro
        except Exception:
            conn.rollback()
            raise
        finally:
            cursor.close()
            conn.close()

    def buscar_por_nome(self,titulo):
        conn = Conectar.conectar()
        cursor = conn.cursor(row_factory = dict_row)
        try:
            cursor.execute(
            '''
                SELECT id, titulo, autor, total_paginas,arquivo_path, ativo
                FROM livro
                WHERE titulo ILIKE %s

            ''',(f"%{titulo}%",)
            )
            buscar_livro_nome = cursor.fetchall()
            return buscar_livro_nome
        except Exception:
            conn.rollback()
            raise
        finally:
            cursor.close()
            conn.close()

    def deletar_livro(self,id):
        conn = Conectar.conectar()
        cursor = conn.cursor(row_factory = dict_row)
        try:
            cursor.execute(
                '''
                DELETE FROM livro
                WHERE id = %s
                RETURNING id, titulo, autor, total_paginas, arquivo_path, ativo
                ''',(id,)
            )
            livro_deletado = cursor.fetchone()
            if livro_deletado is None:
                conn.rollback()
                return None
            conn.commit()
            return livro_deletado
        except Exception:
            conn.rollback()
            raise
        finally:
            cursor.close()
            conn.close()
