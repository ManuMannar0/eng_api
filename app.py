from flask import Flask, request, jsonify
import psycopg2
from psycopg2 import sql

app = Flask(__name__)

# Connessione al database PostgreSQL
def connect_db():
    return psycopg2.connect(
        host="localhost",
        database="gpt",
        user="postgres",
        password="1458"
    )

# Funzione per eseguire query sul database
def queryToDb_query(query, params=()):
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute(query, params)
    conn.commit()
    
    # Controlla se la query è un SELECT
    if query.strip().lower().startswith('select'):
        result = cursor.fetchall()  # Fetch dei risultati per SELECT
    else:
        result = None  # Nessun risultato per query come INSERT/UPDATE/DELETE
    
    cursor.close()
    conn.close()
    return result

@app.route('/', methods=['POST'])
def queryToDb():
    data = request.json
    queries = data.get('queries', [])
    
    results = []
    try:
        for item in queries:
            query = item.get('query')
            params = item.get('params', ())
            result = queryToDb_query(query, params)
            results.append({"query": query, "result": result})
        
        return jsonify({"success": True, "results": results})
    
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 400

if __name__ == '__main__':
    app.run(debug=True)
