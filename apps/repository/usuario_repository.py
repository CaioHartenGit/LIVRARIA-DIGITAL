from apps.database.conexao import Conectar
from psycopg.rows import dict_row

class UsuarioRepository:
    def cadastrar(self,nome,email,senha):
        conn = Conectar.conectar()
        cursor = conn.cursor(row_factory = dict_row)

        try:
            cursor.execute(
                '''
                INSERT INTO usuario(nome, email, senha)
                VALUES (%s,%s,%s)
                RETURNING id, nome, email, senha, ativo, tipo_usuario
                
                ''',(nome,email,senha)
            )
            usuario = cursor.fetchone()
            conn.commit()
            return usuario
        
        except Exception:
            conn.rollback()
            raise
        finally:
            cursor.close()
            conn.close()

    def atualizar_usuario(self,nome,email,senha):
        conn = Conectar.conectar()
        cursor = conn.cursor(row_factory = dict_row)

        try:
            cursor.execute(
                '''
                UPDATE usuario
                SET nome = %s, 
                    email = %s, 
                    senha = %s
                WHERE id = %s
                RETURNING id, nome, email, senha, ativo, tipo_usuario
                ''',(nome,email,senha)
            )
            usuario = cursor.fetchone()
            conn.commit()
            return usuario
        
        except Exception:
            conn.rollback()
            raise
        finally:
            cursor.close()
            conn.close()

    def listar_tudo_admin(self):
        conn = Conectar.conectar()
        cursor = conn.cursor(row_factory = dict_row)

        try:
            cursor.execute(
                '''
                SELECT id, nome, email, ativo, senha, tipo_usuario
                FROM usuario
                
                '''
            )
            usuarios = cursor.fetchall()
            return usuarios
        except Exception:
            conn.rollback()
            raise
        finally:
            cursor.close()
            conn.close()

    def deletar_usuario(self,id):
        conn = Conectar.conectar()
        cursor = conn.cursor(row_factory = dict_row)

        try:
            cursor.execute(
                '''
                DELETE FROM usuario
                WHERE id = %s
                RETURNING id, nome, email, ativo, senha, tipo_usuario
                ''',(id,)
            )
            usuario = cursor.fetchone()
            conn.commit()
            return usuario
        
        except Exception:
            conn.rollback()
            raise
        finally:
            cursor.close()
            conn.close()