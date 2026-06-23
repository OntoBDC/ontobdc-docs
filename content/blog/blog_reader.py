
import js
import sys
import json
import requests
import pyodide_http


# Habilita o requests para funcionar no navegador
pyodide_http.patch_all()

class DOMOutput:
    def write(self, txt):
        if txt.strip():
            js.updateOutput(txt.rstrip("\n"))
    def flush(self): pass

sys.stdout = DOMOutput()
sys.stderr = DOMOutput()

def load_blog_container():
    print("Buscando metadados do RO-Crate...")
    
    # Em produção no GitHub Pages, a URL relativa funciona.
    # Usamos URL base do próprio host
    base_url = js.window.location.href.rsplit('/', 1)[0]
    crate_url = f"{base_url}/.__ontobdc__/ro-crate-metadata.json"
    
    try:
        response = requests.get(crate_url)
        response.raise_for_status()
        crate_data = response.json()
        
        posts = []
        
        # Lógica simplificada: Buscar todas as entidades que não são o próprio dataset
        # Em um cenário real, você buscaria por @type = "Article" ou similar
        for item in crate_data.get('@graph', []):
            type_ = item.get('@type', '')
            id_ = item.get('@id', '')
            
            # Pula a raiz e o próprio arquivo de metadados
            if id_ in ['./', 'ro-crate-metadata.json']:
                continue
                
            # Se for um markdown, consideramos como post
            if id_.endswith('.md'):
                # Tenta extrair o título (se não tiver, usa o nome do arquivo)
                title = item.get('name', id_.replace('.md', '').replace('-', ' ').title())
                
                # Monta a URL de visualização (aqui você apontaria pro seu leitor de MD)
                # Por enquanto, apenas aponta pro arquivo estático
                post_url = f"{base_url}/{id_}"
                
                posts.append({
                    "id": id_,
                    "title": title,
                    "date": item.get('datePublished', 'Recente'),
                    "excerpt": item.get('description', f"Conteúdo do arquivo {id_}")[:100] + "...",
                    "url": post_url
                })
        
        print(f"✅ {len(posts)} posts encontrados no contêiner.")
        
        # Envia a lista JSON de volta para o JavaScript renderizar o HTML
        js.renderBlogPosts(json.dumps(posts))
        
    except Exception as e:
        print(f"❌ Erro ao ler contêiner remoto: {str(e)}")

load_blog_container()
