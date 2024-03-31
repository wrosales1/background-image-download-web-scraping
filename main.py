from selenium import webdriver
from bs4 import BeautifulSoup
import requests
import os
import time

PATH_DOWNLOAD ="./download"

def get_html(url):
    
    # Cargamos la url
    driver = webdriver.Chrome() # A partir de Selenium  v4.6.0 no es necesario configurar el driver.exe, selenium maneja el navegador y controlador por sí solo
    driver.get(url)
    #time.sleep(3) #3 segundos de carga 
           
    # Obtenemos la página    
    html = BeautifulSoup(driver.page_source,'html.parser')
    driver.close()
    return html    

def get_images(category):

    images = []

    # Obtenemos el html de la página principal de la categoría
    mainCategoryURL=f"https://www.xtrafondos.com/categorias/{category}/horizontal/"
    print(f"Revisando en categoría: {category}...".upper())
    
    htmlPageMainCategory = get_html(mainCategoryURL)
    
    # Extraemos los extremos de las paginaciones para modificar la URL
    linksPagination = htmlPageMainCategory.find("div",{"class":"content-links-pagination"}).find_all('a') # enlaces de la paginacion
    paginationStart = int(linksPagination[0].text)
    paginationEnd = int(linksPagination[-1].text)
    print(f"La categoría tiene {paginationEnd} páginas")
    # Recorremos la pagina desde el inicio hasta el final de la paginacion    
    for pagination in range(paginationStart,paginationEnd+1):
    
        categoryURL = f"{mainCategoryURL}{pagination}"
        print(f"Extrayendo datos de '{categoryURL}'...")
        htmlPageCategory = get_html(categoryURL)        
        pictures= htmlPageCategory.findAll('article',attrs={'class':'rndm horizontal'})
        # Recorremos cada imagen en miniatura
        for picture in pictures:    
            # Construimos la URL de la imagen a descargar
            idImage = picture.attrs['id'].split("-").pop() # wall-12176 -> 12176        
            urlDetailPicture = picture.find('a').attrs['href'] # https://www.xtrafondos.com/wallpaper/horizontal/12176-pelicano-australiano.html
            nameImage =  urlDetailPicture.split(idImage+"-").pop().split(".")[0]  # pelicano-australiano
            urlImage = f"https://www.xtrafondos.com/wallpapers/{nameImage}-{idImage}.jpg"
            
            # Agregamos los datos de la imagen en un array
            imageObject = {
                "name":nameImage,
                "url": urlImage
            }
            images.append(imageObject)            
    
    return images

def create_directory_root_download():
    # Crea el directorio raiz de descarga si no existe
    if not os.path.exists(f'{PATH_DOWNLOAD}'):
        os.mkdir(f'{PATH_DOWNLOAD}')       
    
def create_category_download(category):
    pathCategoryDownload = os.path.join(PATH_DOWNLOAD,category)
    
    # Creamos el directorio de descarga de la categoria si no existe
    if not os.path.exists(f'{pathCategoryDownload}'):
        os.mkdir(f'{PATH_DOWNLOAD}/{category}')
    
    return pathCategoryDownload

def download_image(allLinksURL):
    
    for imageByCategory in allLinksURL:
        # Creamos los directorios que guardarán las imágenes
        pathDirectory = create_category_download(imageByCategory['name_category'])
        print(f"Downloading in category: {imageByCategory['name_category']}...".upper())
        # Descargamos las imágenes
        for image in imageByCategory["images"]:
            print((f"Downloading {image['url']}"))
            try:                     
                with requests.get(image["url"]) as r:
                    if r.status_code ==200:
                        with open(f"{pathDirectory}/{image['name']}.jpg", "wb") as file:
                            file.write(r.content)
            except Exception as err:
                print(f"Error en descargar {image['url']} tipo: {err}")
                pass #ignora el error y continua el bucle

def init():
    # Categorías de las imágenes    
    categories = ["animales","anime-comics-caricaturas",
                  "arte-y-diseno","deportes","famosos-y-modelos",
                  "festividades","flores",
                  "juegos","paisajes","peliculas-y-series",
                  "universo","variadas","vehiculos"]
    
    allLinksURL = []
    for category in categories:

        # Obtenemos los datos de las imágenes de cada categoria y almacenamos en un array
        linkImagesDownload = get_images(category)
        linksByCategory = {
            "name_category": category,
            "images": linkImagesDownload
        }       
        allLinksURL.append(linksByCategory)

    create_directory_root_download()
    download_image(allLinksURL)
  
if __name__=='__main__':    
    start_time = time.perf_counter()
    init()
    end_time = time.perf_counter()
    elapsed_time = end_time - start_time    
    #print(f"{'Tarea terminada'.upper():=^40}")
    print("{:=^40}".format('Tarea terminada'.upper()))
    print(f"El proceso duró {elapsed_time} segundos")
    
