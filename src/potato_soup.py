import re
from urllib.request import urlopen
from bs4 import BeautifulSoup
from src.FormatHtml import HtmlFormat
import webbrowser
import os
import shutil
from pathlib import Path


class PotatoSoup:
    # on class initialization pass list of images and path for writing
    
    def __init__(self, path, soup, absolute_path):
        self.path = path
        self.absolute = absolute_path
        self.html = """
        <!DOCTYPE html>

        <html lang="en">
        <head>
            <link rel="stylesheet" href="style.css" />
        </head>
        <header>{header} Soup</header>
        <body>
        """.format(header=path.capitalize())
        self.images = []
        self.error = False
        
        #initialize the soup
        
        self.soup = soup
        self.initialize_soup()

    def initialize_soup(self):
        
            # attempt load of desired site
        print("Initializing!")

        images = self.soup.findAll('img')
        possible_images = self.soup.findAll('a')

        #self.images = [image for image in images if  image.has_attr('src')]
        for possible_image in possible_images:
            if possible_image.has_attr('href'):
                
                if possible_image['href'] is not None and ('.png' in str(possible_image['href']) or '.jpg' in str(possible_image['href'])):
                    
                    self.images.append(possible_image['href'])
                    
        for image in images:
            if image.has_attr('src'):
                if image['src'] is not None and 'award' not in str(image['src']) and 'renderTimingPixel.png' not in str(image['src']):
                    
                    self.images.append(image['src'])

        directory = './output/' + self.path

        # if directory exists remove folder
        if os.path.exists(directory):
            shutil.rmtree(directory)
        
        os.mkdir(directory)
        

    def clean_image_elements(self):

        print("Cleaning Image elements!")
        
        if len(self.images) == 0:
            return []
        else:
            #cleaned = [re.sub(r'(onload|alt|role|class|id|style|onerror)=\".*\"\s', '', str(element)) for element in self.images]
            cleaned = ['<img id="{id}" src="{image}" />'.format(image=str(self.images[image]), id=str(image)) for image in range(len(self.images))]
            
            self.images = cleaned
    
    def add_container(self):
        # wrap image elements in a div container for even scaling
        print("Boxing Up images!")
        boxedup = []
        
        for image in range(len(self.images)):
            boxedup.append(
                """
            <div class="image-container">
                {image}
                <svg onclick="download({id})" width="44" height="42" viewBox="0 0 44 42" fill="none" xmlns="http://www.w3.org/2000/svg">
                <path d="M21.6309 29.7305C21.6747 29.7865 21.7307 29.8318 21.7947 29.863C21.8586 29.8941 21.9289 29.9103 22 29.9103C22.0711 29.9103 22.1414 29.8941 22.2053 29.863C22.2693 29.8318 22.3253 29.7865 22.3691 29.7305L28.9316 21.4277C29.1719 21.123 28.9551 20.6719 28.5625 20.6719H24.2207V0.84375C24.2207 0.585937 24.0098 0.375 23.752 0.375H20.2363C19.9785 0.375 19.7676 0.585937 19.7676 0.84375V20.666H15.4375C15.0449 20.666 14.8281 21.1172 15.0684 21.4219L21.6309 29.7305ZM43.4453 27.6797H39.9297C39.6719 27.6797 39.4609 27.8906 39.4609 28.1484V37.1719H4.53906V28.1484C4.53906 27.8906 4.32813 27.6797 4.07031 27.6797H0.554688C0.296875 27.6797 0.0859375 27.8906 0.0859375 28.1484V39.75C0.0859375 40.7871 0.923828 41.625 1.96094 41.625H42.0391C43.0762 41.625 43.9141 40.7871 43.9141 39.75V28.1484C43.9141 27.8906 43.7031 27.6797 43.4453 27.6797Z" fill="black"/>
                </svg>
            </div>
                """.format(image=str(self.images[image]), id=str(image))
            )
        
        self.images = boxedup

    def write_images_to_html(self):
        #write images to the dedicated html state
        for img in self.images:
            self.html += str(img)
        

    def generate_css(self):
        print("Generating CSS")
        # generate css from outside method
        self.css = """

body {
    display: flex;
    flex-wrap: wrap;
   justify-content: space-evenly;
    top: 0;
    left: 0;
    width: 100%;
    overflow-x: hidden;
    margin: 0;
    height: 100%;
    background-color: rgb(173, 173, 173);
    font-family: sans-serif;
}
header {
    position: sticky;
    z-index: 999;
    width: 100%;
    height: 80px;
    color:  white;
    background-color: rgba(55, 71, 114, 0.788);
    backdrop-filter: blur(20px);
    margin: 0;
    border: solid black 2px;
    top: 0;
    left: 0;
    text-align: center;
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 3rem;
}
.image-container {
    width: 300px;
    height: 300px;
    margin: 1rem 0;
    flex-shrink: 0;
    background-color: rgb(197, 197, 197);
    border: solid black 2px;
    position: relative;
}
.image-container img {
    object-fit: contain;
    width: 100%;
    height: 100%;
}
.image-container svg {
    position: absolute;
    bottom: 5px;
    right: 5px;
    cursor: pointer;
    padding: 3px;
    border: solid 3px black;
    background-color: rgba(255, 255, 255, 0.336);
}

.image-container svg:hover {
    background-color: rgba(255, 255, 255, 0.801);
}

        """

    def finalize_html_gen(self):
        #finalize html gen
        print("Finalizing HTML Generation")
        self.clean_image_elements()
        self.add_container()
        self.write_images_to_html()
        self.html += """
        </body>
        <script type="text/javascript">
                function download(e) {
                    console.log(e)
                    image = document.getElementById(e).src;
                    link = document.createElement('a')
                    link.href = image
                    link.download = image
                    link.target = "_blank"
                    document.body.appendChild(link)
                    link.click()
                    document.body.removeChild(link)
                }    
            </script>
        </html>"""
        

    def render(self):
        #generate css 
        self.generate_css()
        # build css file
        with open('./output/' + self.path + '/style.css', 'w', encoding='utf8') as css:
            css.write(self.css)

        #generate html for rendering

        self.finalize_html_gen()

        print("Making Potato Soup")
        # prepare potato soup
        potato_soup = BeautifulSoup(self.html, 'html.parser').prettify()

        with open('./output/' + self.path + '/index.html', 'w', encoding='utf8') as html:
            html.write(potato_soup)
    
    def launch(self):
        self.render()
        print("Serving The Soup")
        webbrowser.open(str(self.absolute) + '/output/' + self.path + '/index.html')

        
        