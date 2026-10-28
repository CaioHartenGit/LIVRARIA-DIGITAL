from apps.database.conexao import Conectar
from psycopg.rows import dict_row

class LivroRepository:
    def __init__(self):
        self.garantir_coluna_usuario_id()

    def garantir_coluna_usuario_id(self):
        conn = Conectar.conectar()
        cursor = conn.cursor()
        try:
            cursor.execute(
                '''
                ALTER TABLE livro
                ADD COLUMN IF NOT EXISTS usuario_id INTEGER REFERENCES usuario(id) ON DELETE CASCADE;

                UPDATE livro
                SET usuario_id = (SELECT id FROM usuario WHERE tipo_usuario = 'admin' ORDER BY id ASC LIMIT 1)
                WHERE usuario_id IS NULL;
                '''
            )
            conn.commit()
        except Exception:
            conn.rollback()
        finally:
            cursor.close()
            conn.close()

    def cadastrar(self,titulo,autor,total_paginas,arquivo_path,usuario_id):
        conn = Conectar.conectar()
        cursor = conn.cursor(row_factory = dict_row)

        try:
            cursor.execute(
                '''
                INSERT INTO livro(titulo, autor, total_paginas, arquivo_path, usuario_id)
                VALUES (%s,%s,%s,%s,%s)
                RETURNING id, titulo, autor, total_paginas, arquivo_path, ativo, usuario_id
                
                ''',(titulo,autor, total_paginas,arquivo_path,usuario_id)
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
            SELECT id, titulo, autor, total_paginas, arquivo_path, ativo, usuario_id
            FROM livro
            ORDER BY id DESC
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

    def listar_livros_por_usuario(self, usuario_id):
        conn = Conectar.conectar()
        cursor = conn.cursor(row_factory = dict_row)

        try:
            cursor.execute(
            '''
            SELECT id, titulo, autor, total_paginas, arquivo_path, ativo, usuario_id
            FROM livro
            WHERE usuario_id = %s
            ORDER BY id DESC
            ''',(usuario_id,)
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
                SELECT id, titulo, autor, total_paginas, arquivo_path, ativo, usuario_id
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
                SELECT id, titulo, autor, total_paginas, arquivo_path, ativo, usuario_id
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

    def buscar_por_nome_e_usuario(self, titulo, usuario_id):
        conn = Conectar.conectar()
        cursor = conn.cursor(row_factory = dict_row)
        try:
            cursor.execute(
            '''
                SELECT id, titulo, autor, total_paginas, arquivo_path, ativo, usuario_id
                FROM livro
                WHERE titulo ILIKE %s AND usuario_id = %s

            ''',(f"%{titulo}%", usuario_id)
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
                RETURNING id, titulo, autor, total_paginas, arquivo_path, ativo, usuario_id
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
