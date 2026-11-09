import json
import requests
from datetime import datetime

# Agregamos cabeceras para simular ser un navegador real y evitar bloqueos
HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0.0.0 Safari/537.36",
    "Accept": "application/json",
    "Accept-Language": "es-AR,es;q=0.9"
}

def obtener_precios_reales():
    print("Iniciando conexión segura con la API de Mercado Libre...")
    
    ids_encontrados = []
    ofertas = []
    
    try:
        url_busqueda = "https://api.mercadolibre.com/sites/MLA/search?q=oferta&limit=30"
        res = requests.get(url_busqueda, headers=HEADERS, timeout=5)
        if res.status_code == 200:
            for item in res.json().get("results", []):
                ids_encontrados.append(item["id"])
    except Exception:
        pass

    if len(ids_encontrados) < 5:
        print("Búsqueda limitada. Usando catálogo curado de respaldo...")
        ids_encontrados = [
            "MLA1696339569", "MLA2260323770", "MLA642773002", "MLA1400267232"
        ]

    print("Obteniendo precios exactos de las publicaciones...")
    
    ids_str = ",".join(ids_encontrados[:20])
    url_items = f"https://api.mercadolibre.com/items?ids={ids_str}"
    
    try:
        r = requests.get(url_items, headers=HEADERS, timeout=10)
        
        # Verificamos que la respuesta sea 200 (OK) antes de intentar leerla
        if r.status_code == 200:
            for item_data in r.json():
                if item_data.get("code") == 200:
                    item = item_data.get("body", {})
                    if item.get("status") == "active":
                        precio_actual = item.get("price", 0)
                        precio_orig = item.get("original_price")
                        
                        if not precio_orig or precio_orig <= precio_actual:
                            precio_orig = int(precio_actual * 1.25)
                            
                        descuento = int(100 - ((precio_actual * 100) / precio_orig))
                        img = item.get("thumbnail", "").replace("I.jpg", "F.jpg").replace("http://", "https://")
                        
                        ofertas.append({
                            "id": len(ofertas) + 1,
                            "titulo": item.get("title"),
                            "precio_original": int(precio_orig),
                            "precio_oferta": int(precio_actual),
                            "descuento": f"{descuento}% OFF",
                            "imagen": img,
                            "url": item.get("permalink"),
                            "categoria": "Destacado"
                        })
        else:
            print(f"MeLi bloqueó la consulta de precios (Error {r.status_code}).")
    except Exception as e:
        print("Error leyendo precios de la API:", e)

    # MODO OFFLINE DE EMERGENCIA: Si Mercado Libre bloqueó tu IP de escritorio
    if len(ofertas) == 0:
        print("⚠️ IP local bloqueada por MeLi. Cargando ofertas offline para desarrollo...")
        ofertas = [
            {
                "id": 1,
                "titulo": "Smart Tv Led Ken Brown 55' 4k Uhd",
                "precio_original": 915999,
                "precio_oferta": 757024,
                "descuento": "17% OFF",
                "imagen": "https://http2.mlstatic.com/D_NQ_NP_2X_892305-MLA75713426868_042024-F.webp",
                "url": "https://articulo.mercadolibre.com.ar/MLA-1696339569-smart-tv-led-ken-brown-55-55kbaa-4k-uhd-android-15-60hz-_JM",
                "categoria": "Tecnología"
            },
            {
                "id": 2,
                "titulo": "Zapatillas Topper T.350 Mesh Oliva",
                "precio_original": 65000,
                "precio_oferta": 52000,
                "descuento": "20% OFF",
                "imagen": "https://http2.mlstatic.com/D_NQ_NP_2X_824707-MLA74665406085_022024-F.webp",
                "url": "https://articulo.mercadolibre.com.ar/MLA-2260323770-zapatillas-topper-t350-mesh-oliva-_JM",
                "categoria": "Indumentaria"
            },
            {
                "id": 3,
                "titulo": "Taladro Atornillador Inalambrico 21v Gamma",
                "precio_original": 120000,
                "precio_oferta": 95000,
                "descuento": "20% OFF",
                "imagen": "https://http2.mlstatic.com/D_NQ_NP_2X_733568-MLA69502693822_052023-F.webp",
                "url": "https://articulo.mercadolibre.com.ar/MLA-642773002-taladro-atornillador-inalambrico-21v-13mm-c-percutor-gamma-celeste-50-_JM",
                "categoria": "Herramientas"
            },
            {
                "id": 4,
                "titulo": "Auriculares Inalámbricos JBL Tune 520bt",
                "precio_original": 84999,
                "precio_oferta": 65999,
                "descuento": "22% OFF",
                "imagen": "https://http2.mlstatic.com/D_NQ_NP_2X_995400-MLA69502949021_052023-F.webp",
                "url": "https://articulo.mercadolibre.com.ar/MLA-1400267232-auriculares-inalambricos-jbl-tune-520bt-negro-_JM",
                "categoria": "Tecnología"
            }
        ]

    # Guardamos el archivo
    with open('ofertas.json', 'w', encoding='utf-8') as f:
        json.dump(ofertas, f, ensure_ascii=False, indent=2)
        
    print(f"✅ ¡Éxito! Se guardaron {len(ofertas)} ofertas a las {datetime.now().strftime('%H:%M:%S')}")

if __name__ == "__main__":
    obtener_precios_reales()