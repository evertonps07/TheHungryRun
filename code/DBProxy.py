import sqlite3

class DBProxy:
    def __init__(self, db_name: str):
        self.db_name = db_name
        self.connection = sqlite3.connect(db_name)
        # Cria a tabela de dados caso ela ainda não exista no arquivo .db
        self.connection.execute('''
            CREATE TABLE IF NOT EXISTS dados(
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                score INTEGER NOT NULL,
                date TEXT NOT NULL
            )
        ''')

    def save(self, score_dict: dict):
        # Mapeia as chaves do dicionário diretamente nas colunas correspondentes do SQL
        self.connection.execute(
            'INSERT INTO dados (name, score, date) VALUES (:name, :score, :date)',
            score_dict
        )
        self.connection.commit()

    def retrieve_top10(self) -> list:
        # Ordena de forma crescente (ASC) para que o menor tempo de corrida lidere o ranking
        return self.connection.execute('SELECT * FROM dados ORDER BY score ASC LIMIT 10').fetchall()

    def close(self):
        return self.connection.close()