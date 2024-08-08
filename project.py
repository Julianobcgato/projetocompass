from fastapi import FastAPI, HTTPException
from fastapi.responses import HTMLResponse, RedirectResponse
import subprocess
import json
import os

app = FastAPI()

def run_trivy():
    try:
        # aqui vai executar o Trivy e salva a saída em um arquivo
        result = subprocess.run([
            "trivy", "fs", ".", 
            "--severity", "CRITICAL", 
            "--format", "json"
        ], capture_output=True, text=True, check=True)

        # Salvando uum JSON para um arquivo
        with open("trivy-results.json", "w") as file:
            file.write(result.stdout)
        
    except subprocess.CalledProcessError as e:
        raise HTTPException(status_code=500, detail=f"Erro ao executar o Trivy: {e.stderr}")

    if not os.path.exists("trivy-results.json"):
        raise HTTPException(status_code=500, detail="O arquivo de resultados do Trivy não foi encontrado.")

    with open("trivy-results.json", "r") as file:
        results = json.load(file)

    # contando as vulnerabilidades criticas
    critical_count = sum(
        len(result.get("Vulnerabilities", [])) 
        for result in results.get("Results", [])
        if any(vuln.get("Severity") == "CRITICAL" for vuln in result.get("Vulnerabilities", []))
    )
    
    return critical_count

@app.get("/", response_class=HTMLResponse)
def read_root():
    try:
        critical_count = run_trivy()
    except subprocess.CalledProcessError as e:
        raise HTTPException(status_code=500, detail=f"Erro ao executar o Trivy: {str(e)}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro: {str(e)}")

    if critical_count > 10:  # quantidade de linhas criticas
        result_message = "Danger: Muitas Vulnerabilidades Críticas!"
    else:
        result_message = "Nenhuma vulnerabilidade crítica encontrada."

    html_content = f"""
        html>
        <head>
            <title>Trivy Scan Results</title>
            <style>
                body {{
                    font-family: Arial, sans-serif;
                    background-color: #e6f0ff;
                    color: #333;
                    text-align: center;
                    padding: 50px;
                }}
                h1 {{
                    color: #ff4d4d;
                }}
                p {{
                    font-size: 1.2em;
                }}
                .container {{
                    max-width: 600px;
                    margin: 0 auto;
                    padding: 20px;
                    background: #fff;
                    border-radius: 8px;
                    box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);
                }}
                button {{
                    background-color: #007bff;
                    color: #fff;
                    border: none;
                    border-radius: 5px;
                    padding: 10px 20px;
                    font-size: 1em;
                    cursor: pointer;
                    transition: background-color 0.3s ease;
                }}
                button:hover {{
                    background-color: #0056b3;
                }}
            </style>
        </head>
        <body>
            <div class="container">
                <h1>{result_message}</h1>
                <p>Critical vulnerabilities count: {critical_count}</p>
                <form action="/mario" method="get">
                    <button type="submit">Continuar</button>
                </form>
            </div>
        </body>
    </html>
    """
    return HTMLResponse(content=html_content)

@app.get("/mario")
def mario_world():
    return {"Mario": "World"}

@app.get("/items/{item_id}")
def read_item(item_id: int, q: str = None):
    return {"item_id": item_id, "q": q}



