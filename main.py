import certifi
from kivy.lang import Builder
from kivy.network.urlrequest import UrlRequest
from kivymd.app import MDApp
from kivymd.uix.dialog import MDDialog
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from webdriver_manager.chrome import ChromeDriverManager

class WikiReaderApp(MDApp):

    info_dialog = None
    contact_dialog = None

    def build(self):
        self.title = "RL Insider"
        self.theme_cls.theme_style = "Light"
        self.theme_cls.primary_palette = "Gray"
        return Builder.load_file("rlinsider_style.kv")

    def search_item(self):
        query = self.root.ids["mdtext"].text
        self.get_data(title=query)

    def get_data(self, title=None):
        if (title == ""):
            self.set_textarea()
        else:
            item_url = "https://rl.insider.gg/it/psn/" + title
            driver = webdriver.Chrome(ChromeDriverManager().install())
            title = title.replace("/", " ")
            driver.get(item_url)
            result = []
            final_result = ""
            try:
                provenience = driver.find_element_by_xpath("//tr[@id='matrixRow0']/td[2]")
                ris_provenience = provenience.get_attribute('innerHTML')
                result.append(f"Tutte le provenienze : {ris_provenience}")
                project = driver.find_element_by_xpath("//tr[@id='matrixRow3']/td[2]")
                ris_project = project.get_attribute('innerHTML')
                result.append(f"Valore progetto : {ris_project}")
                construction = driver.find_element_by_xpath("//tr[@id='matrixRow4']/td[2]")
                ris_construction = construction.get_attribute('innerHTML')
                result.append(f"Costo di costruzione : {ris_construction}")
                driver.close()
                for element in result:
                    final_result += element
                    final_result += "\n\n"
                self.set_textarea(title, final_result)
            except BaseException:
                title = "Data not found!"   
                driver.close()
                self.set_textarea(title)

    def set_textarea(self, title=None, response=None):
        page_title = ""
        if title is None:
            page_title = "Per favore," 
            content = "inserire una ricerca nel campo di testo.\n\nRiprovare!"
        elif response is None:
            page_title = title
            content = "Ci spiace, ma la ricerca non ha prodotto risultati!\n\nRiprova! "
        else:
            page_title = title
            content = response
        self.root.ids["mdlab"].text = f"{page_title}\n\n{content}"


WikiReaderApp().run()
