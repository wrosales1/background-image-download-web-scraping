## Revisión HTML de la página
- URL principal de la categoría: https://www.xtrafondos.com/categorias/animales/horizontal/
- Categorías:
    - Obtenemos los nombres en el panel lateral de la página
    ```html
        <ul>
            <li><a href="https://www.xtrafondos.com/categorias/animales/horizontal/1"> </a></li>
            <li><a href="https://www.xtrafondos.com/categorias/anime-comics-caricaturas/horizontal/1"> </a></li>
            ...
        </ul>
    ```
    - Extraemos los nombres del `href` y creamos la variable: `categorias=["animales","anime-comics-caricaturas",...]`. Estos nombres nos
       servirán también crear los directorios de descarga.
- URL en 1era paginación: https://www.xtrafondos.com/categorias/animales/horizontal/1
- Elemento de cada imagen en miniatura:
    ```html
        <article class="rndm horizontal" id="wall-12176"></article>
        <article class="rndm horizontal" id="wall-12175"> </article>
        ...
    ```
- Links de la paginación de la categoría:
    ```html
        <div class="content-links-pagination btn-normal g-btn-pages"> 
            <a class="active" href="https://www.xtrafondos.com/categorias/animales/horizontal/1">1</a>
            <a href="https://www.xtrafondos.com/categorias/animales/horizontal/2">2</a>
            <a href="https://www.xtrafondos.com/categorias/animales/horizontal/3">3</a>
            <a href="https://www.xtrafondos.com/categorias/animales/horizontal/4">4</a>
            <a href="https://www.xtrafondos.com/categorias/animales/horizontal/5">5</a>
            <a href="https://www.xtrafondos.com/categorias/animales/horizontal/15">15</a> 
        </div>
    ```
- URL de la imagen a descargar: https://www.xtrafondos.com/wallpapers/pelicano-australiano-12176.jpg
    - Se obtiene esa URL ingresando al link de cada miniatura: https://www.xtrafondos.com/wallpaper/horizontal/12176-pelicano-australiano.html
    - En los elementos tendrá la forma:
        ```html
            <a href="https://www.xtrafondos.com/wallpapers/pelicano-australiano-12176.jpg" itemprop="contentUrl" data-size="3840x2160"> </a>
        ```
        
## Otras notas
### Usar Chrome webDriver en Selenium para descargar un archivo
- Al entrar al link: https://www.xtrafondos.com/descargar.php?id=12176&resolucion=1920x1080 se abrirá un dialog del sistema guardar el archivo.
```py
    from selenium import webdriver
    from selenium.webdriver.chrome.options import Options
    
    options = Options()
    options.add_experimental_option("prefs", {
    "download.default_directory": r"C:\Users\xxxx\Downloads",
    "download.prompt_for_download": False,
    "download.directory_upgrade": True,
    "safebrowsing.enabled": True
    })
    driver = webdriver.Chrome(options)
    driver.get("https://www.xtrafondos.com/descargar.php?id=12176&resolucion=1920x1080")
    sleep(2)
    driver.close()
```
