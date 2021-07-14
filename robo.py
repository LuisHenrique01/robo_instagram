from typing import List, Optional, Any
import random
from . import BASE_URL_IG, XPATH_SALVAR_LOGIN, CSS_PATH_NOTIFICACOES
from . import XPATH_CAMPO_COMENTAR, XPATH_BOTAO_ENVIAR
from selenium import webdriver
from time import sleep


class ComentarInstagram:

    def __init__(self, login: str = '', password: str = '') -> None:
        """
        Essa classe realiza comentarios no instagram em um determinado post
        :param login: o seu login no instagram
        :param password: a sua senha do instagram

        NÃO ME RESPONSABILIZO POR BANIMENTO DO SEU
        PERFIL OU QUEBRA DE SEGURANÇA, AO USAR ESSA CLASSE VOCÊ ACEITA
        INTEIRAMENTE E LIVREMENTE OS RISCOS.

        I AM NOT RESPONSIBLE FOR BAN YOUR PROFILE OR BREACH OF SECURITY,
        BY USING THIS CLASS YOU FULLY AND FREELY ACCEPT THE RISKS.
        """
        self.navegador = webdriver.Chrome()
        self.navegador.implicitly_wait(10)
        self._login = login
        self._password = password
        self.base_url_ig = BASE_URL_IG
        self.xpath_salvar_login = XPATH_SALVAR_LOGIN
        self.css_path_notificao = CSS_PATH_NOTIFICACOES
        self.xpath_campo_comentar = XPATH_CAMPO_COMENTAR
        self.xpath_botao_enviar = XPATH_BOTAO_ENVIAR

    def get_username(self) -> str:
        return self._login

    def get_password(self) -> str:
        return self._password

    def acessar_pagina(self, url: str = None) -> None:
        if url:
            self.navegador.get(url)
        else:
            self.navegador.get(self.base_url_ig)

    def nao_salvar_login(self) -> None:
        self.navegador.find_element_by_xpath(self.xpath_salvar_login).click()
        sleep(3)  # Os sleeps é para evitar qualquer atitude suspeita

    def desativar_notificacoes(self) -> None:
        self.navegador.find_element_by_css_selector(self.css_path_notificao).click()
        sleep(2)  # Os sleeps é para evitar qualquer atitude suspeita

    def faz_login(self) -> None:
        self.acessar_pagina()
        login = self.navegador.find_element_by_name('username')
        senha = self.navegador.find_element_by_name('password')
        sleep(2)
        login.send_keys(self.get_username())
        sleep(1)
        senha.send_keys(self.get_password())
        self.navegador.find_element_by_id('loginForm').submit()
        sleep(3)  # Os sleeps é para evitar qualquer atitude suspeita
        self.nao_salvar_login()
        self.desativar_notificacoes()

    def comenta_humanamente(self, campo_comentario: Any, comentario: str, 
                            mencionar: bool, qtd_mencoes: int, amigos: list) -> None:
        sleep(1)  # Os sleeps é para evitar qualquer atitude suspeita
        for letra in list(comentario):
            sleep(random.randint(2, 5)/5)
            campo_comentario.send_keys(f'{letra}')
        if mencionar:
            if qtd_mencoes > len(amigos):
                raise ValueError("Número de amigos menor que o nescessário")
            mencoes = amigos.copy()  # Fazendo uma cópia para não modificar a original pelo ponteiro
            for _ in range(qtd_mencoes):
                sleep(random.randint(1, 2)/2)
                amigo = random.choice(mencoes)
                if '@' not in amigo:
                    amigo = '@' + amigo
                campo_comentario.send_keys(f' {amigo}')
                mencoes.remove(amigo)  # Evitar que o amigo seja marcado no mesmo comentário

    def comentar_um_post(self, url: str, comentarios: List[str],
                         qtd_comentarios: int = 20, mencionar: bool = False,
                         qtd_mencoes: int = 0, amigos: Optional[list] = ['']) -> None:
        """
        Realiza um ou varios comentários em um post com ou sem menções a terceiros
        :param url: string com o link da publicação
        :param comentarios: lista de comentarios (pode sem um texto ou uma palavra)
        :param qtd_comentarios: inteiro com a quantidade de comentarios (default: 20)
        :param mencionar: boleano, mencionar ou não um terceiro
        :param qtd_mencoes: inteiro com o número de menções por comentário
        :param amigos: lista de amigos a serem mencionados
        """
        try:
            for _ in range(qtd_comentarios):
                self.acessar_pagina(url)
                sleep(1)
                self.navegador.find_element_by_xpath(self.xpath_campo_comentar).click()
                campo_comentario = self.navegador.find_element_by_xpath(self.xpath_campo_comentar)
                self.comenta_humanamente(campo_comentario, random.choice(comentarios), mencionar, qtd_mencoes, amigos)
                sleep(1)  # Os sleeps é para evitar qualquer atitude suspeita
                self.navegador.find_element_by_xpath(self.xpath_botao_enviar).click()
        except Exception as e:
            print(e)
        finally:
            self.navegador.quit()

    def __str__(self):
        return f'Bot do {self.get_username()}'

    def quit(self) -> None:
        self.navegador.quit()