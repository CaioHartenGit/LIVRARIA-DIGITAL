from apps.database.conexao import Conectar
from psycopg.rows import dict_row

class ProgressoRepository:

    def cadastrar_progresso(self,usuario_id:int, livro_id:int, pagina_atual:int = 0, concluido:bool = False):
        conn = Conectar.conectar()
        cursor = conn.cursor(row_factory = dict_row)

        try:
            cursor.execute(
                '''
                INSERT INTO progresso (usuario_id, livro_id, pagina_atual, concluido)
                VALUES (%s, %s, %s, %s)
                RETURNING id, usuario_id, livro_id, pagina_atual, concluido, atualizado_em
                ''',(usuario_id, livro_id, pagina_atual, concluido)
            )
            progresso = cursor.fetchone()
            conn.commit()
            return progresso
        
        except Exception:
            conn.rollback()
            raise
        finally:
            cursor.close()
            conn.close()
    
    def atualizar_pagina(self, usuario_id, livro_id, pagina_atual, concluido):
        conn = Conectar.conectar()
        cursor = conn.cursor(row_factory = dict_row)

        try:
            cursor.execute(
                '''
                UPDATE progresso
                SET pagina_atual = %s,
                    concluido = %s,
                    atualizado_em = CURRENT_TIMESTAMP
                WHERE usuario_id = %s AND livro_id = %s
                RETURNING id, usuario_id, livro_id, pagina_atual, concluido, atualizado_em
                ''',(pagina_atual, concluido, usuario_id, livro_id)
            )
            progresso = cursor.fetchone()
            conn.commit()
            return progresso
        
        except Exception:
            conn.rollback()
            raise
        finally:
            cursor.close()
            conn.close()

    def buscar_por_usuario_e_livro(self,usuario_id,livro_id):
        conn = Conectar.conectar()
        cursor = conn.cursor(row_factory = dict_row)

        try:
            cursor.execute(
                '''
                SELECT id, usuario_id, livro_id, pagina_atual, concluido, atualizado_em
                FROM progresso
                WHERE usuario_id = %s AND livro_id = %s
                ''',(usuario_id,livro_id)
            )
            progresso = cursor.fetchone()
            return progresso
        
        except Exception:
            conn.rollback()
            raise
        finally:
            cursor.close()
            conn.close()
    
    def listar_por_usuario(self, usuario_id):
        conn = Conectar.conectar()
        cursor = conn.cursor(row_factory = dict_row)

        try:
            cursor.execute(
                '''
                SELECT id, usuario_id, livro_id, pagina_atual, concluido, atualizado_em
                FROM progresso
                WHERE usuario_id = %s
                ''',(usuario_id,)
            )
            progresso = cursor.fetchall()
            return progresso
        
        except Exception:
            conn.rollback()
            raise
        finally:
            cursor.close()
            conn.close()

    def deletar_progresso(self,id):
        conn = Conectar.conectar()
        cursor = conn.cursor(row_factory = dict_row)

        try:
            cursor.execute(
                '''
                DELETE FROM progresso
                WHERE id = %s
                RETURNING id, usuario_id, livro_id, pagina_atual, concluido, atualizado_em
                ''',(id,)
            )
            progresso = cursor.fetchone()
            conn.commit()
            return progresso
        
        except Exception:
            conn.rollback()
            raise
        finally:
            cursor.close()
            conn.close()