import requests
from bs4 import BeautifulSoup
import json
import time
import random
import pandas as pd
import sys

if sys.stdout.encoding != 'utf-8':
    sys.stdout.reconfigure(encoding='utf-8')

def minerar_tudo_vivareal(cidade, max_paginas=400):
    print(f"🚀 [MODO MARATONA] Iniciando mineração completa para: {cidade}")
    
    url_base = "https://www.vivareal.com.br/venda/rio-grande-do-sul/novo-hamburgo/?onde=%2CRio+Grande+do+Sul%2CNovo+Hamburgo%2C%2C%2C%2C%2Ccity%2CBR%3ERio+Grande+do+Sul%3ENULL%3ENovo+Hamburgo%2C-29.683463%2C-51.133747%2C&pagina={}"
    
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8",
        "Accept-Language": "pt-BR,pt;q=0.9,en-US;q=0.8",
        "Referer": "https://www.google.com/",
        "Connection": "keep-alive"
    }
    
    imoveis_coletados = []
    pagina_atual = 1
    
    try:
        for pagina in range(1, max_paginas + 1):
            pagina_atual = pagina
            url = url_base.format(pagina)
            print(f"⏳ Minerando Página {pagina}/{max_paginas}... ", end="", flush=True)
            
            resposta = requests.get(url, headers=headers, timeout=15)
            
            if resposta.status_code == 403:
                print("❌ Bloqueado (403). Salvando dados obtidos até aqui...")
                break
            elif resposta.status_code != 200:
                print(f"❌ Status {resposta.status_code}. Interrompendo...")
                break
                
            soup = BeautifulSoup(resposta.text, 'html.parser')
            todas_tags = soup.find_all('script', type='application/ld+json')
            script_tag_correto = None
            
            for tag in todas_tags:
                if tag.string and 'itemListElement' in tag.string:
                    script_tag_correto = tag
                    break
            
            if not script_tag_correto:
                print("🏁 Fim dos anúncios (Tag não encontrada).")
                break
                
            dados_pagina = json.loads(script_tag_correto.string)
            elementos = dados_pagina.get('itemListElement', [])
            
            if not elementos:
                print("🏁 Fim das páginas disponíveis.")
                break
                
            for el in elementos:
                imovel = el.get('item', {})
                id_anuncio = imovel.get('@id')
                
                if id_anuncio and imovel.get('offers', {}).get('price'):
                    rua_bairro = imovel.get('address', {}).get('streetAddress', 'Não Informado')
                    bairro = rua_bairro.split(',')[-1].strip() if ',' in rua_bairro else rua_bairro
                    
                    imoveis_coletados.append({
                        "ID_Imovel": id_anuncio,
                        "Tipo": imovel.get('@type'),
                        "Bairro": bairro,
                        "Preco": imovel.get('offers', {}).get('price'),
                        "Condominio": imovel.get('offers', {}).get('propertyValue', {}).get('value', 0),
                        "Area_m2": imovel.get('floorSize', {}).get('value'),
                        "Quartos": imovel.get('numberOfBedrooms'),
                        "Banheiros": imovel.get('numberOfBathroomsTotal'),
                        "Titulo": imovel.get('name'),
                        "Link": imovel.get('url')
                    })
            
            print(f"✅ {len(elementos)} imóveis processados. (Total acumulado: {len(imoveis_coletados)})")
            
            # Pausa aleatória entre 3 e 5 segundos para quebrar o padrão do bot
            time.sleep(random.uniform(3.0, 5.0))
            
    except KeyboardInterrupt:
        print("\n🛑 Mineração interrompida manualmente pelo usuário.")
    except Exception as e:
        print(f"\n❌ Erro inesperado na página {pagina_atual}: {e}")
        
    finally:
        # O bloco 'finally' roda OBRIGATORIAMENTE, aconteça o que acontecer acima
        if imoveis_coletados:
            print("\n💾 Salvando base de dados de segurança...")
            df = pd.DataFrame(imoveis_coletados)
            df.drop_duplicates(subset=['ID_Imovel'], inplace=True)
            
            df.to_csv("base_dados_vivareal.csv", index=False, encoding="utf-8-sig")
            df.to_excel("base_dados_vivareal.xlsx", index=False)
            
            print("="*60)
            print(f"🎉 Amostra final consolidada: {len(df)} imóveis salvos!")
            print("="*60)
        else:
            print("\n❌ Nenhuma informação foi extraída para salvar.")

if __name__ == '__main__':
    minerar_tudo_vivareal("Novo Hamburgo", max_paginas=370)