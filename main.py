#Configs

import pygame
import random

pygame.init()
pygame.display.set_caption('Jogo da cobrona')
largura, altura = 800, 600
tela = pygame.display.set_mode((largura, altura))
relogio = pygame.time.Clock()
fonte_gameover = pygame.font.Font("8bitwonder.TTF", 60)
fonte_opcoes = pygame.font.Font("8bitwonder.TTF", 20)

#Cores
preto = (0, 0, 0)
branco = (255, 255, 255)
vermelha = (255, 0, 0)
verde = (0, 255, 0)
azul = (0, 0, 255)
amarelo = (255, 255, 0)
rosa = (255, 105, 180)
ciano = (0, 255, 255)
laranja = (255, 165, 0)

skin_cores = [verde, azul, amarelo, rosa, ciano, laranja]
skin_nomes = ["Verde", "Azul", "Amarelo", "Rosa", "Ciano", "Laranja"]

#Parametros da cobra
tamanho_quadrado = 10
velocidade_jogo = 20

def gerar_comida():
    comida_x = round(random.randrange(0, largura - tamanho_quadrado) / 20.0) * 20.0
    comida_y = round(random.randrange(0, altura - tamanho_quadrado) / 20.0) * 20.0

    return comida_x, comida_y

def desenhar_comida(tamanho, comida_x, comida_y):
    pygame.draw.rect(tela, vermelha, [comida_x, comida_y, tamanho, tamanho])

def desenhar_cobra(tamanho, pixels, cor):
    for pixel in pixels:
        pygame.draw.rect(tela, cor, [pixel[0], pixel[1], tamanho, tamanho])

def desenhar_pontuacao(pontuacao):
    fonte = pygame.font.SysFont("Sans", 40)
    texto = fonte.render(f"Pontos: {pontuacao}", True, branco)
    tela.blit(texto, [1, 1])

#Tela pra selecionar skin
def tela_selecao_cor():
    fonte_titulo = pygame.font.SysFont("Sans", 50)
    fonte_info = pygame.font.SysFont("Sans", 32)
    opcoes = {
        pygame.K_1: 0, pygame.K_2: 1, pygame.K_3: 2,
        pygame.K_4: 3, pygame.K_5: 4, pygame.K_6: 5,
        pygame.K_KP1: 0, pygame.K_KP2: 1, pygame.K_KP3: 2,
        pygame.K_KP4: 3, pygame.K_KP5: 4, pygame.K_KP6: 5,
    }

    selecionado = None
    while selecionado is None:
        tela.fill(preto)

        titulo = fonte_titulo.render("Escolha a cor da cobrinha", True, branco)
        tela.blit(titulo, [largura / 2 - titulo.get_width() / 2, 40])

        info = fonte_info.render("Pressione 1-6 para selecionar", True, branco)
        tela.blit(info, [largura / 2 - info.get_width() / 2, 110])

        y_inicial = 180
        for idx, cor in enumerate(skin_cores):
            y = y_inicial + idx * 90
            for i in range(5):
                pygame.draw.rect(
                    tela,
                    cor,
                    [200 + i * (tamanho_quadrado + 6), y, tamanho_quadrado, tamanho_quadrado],
                )

            numero = fonte_info.render(f"{idx + 1}", True, branco)
            tela.blit(numero, [200 + 5 * (tamanho_quadrado + 6) + 20, y - 2])

            nome = fonte_info.render(skin_nomes[idx], True, branco)
            tela.blit(nome, [200 + 5 * (tamanho_quadrado + 6) + 60, y - 2])

        pygame.display.update()

        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                exit()
            elif evento.type == pygame.KEYDOWN and evento.key in opcoes:
                selecionado = opcoes[evento.key]

        relogio.tick(15)

    return skin_cores[selecionado]

#Direçao da cobra
def selecionar_velocidade(tecla, vel_x_atual, vel_y_atual):
    if tecla == pygame.K_DOWN:
        vel_x = 0
        vel_y = 0 + tamanho_quadrado
    elif tecla == pygame.K_UP:
        vel_x = 0
        vel_y = 0 - tamanho_quadrado
    elif tecla == pygame.K_RIGHT:
        vel_x = 0 + tamanho_quadrado
        vel_y = 0
    elif tecla == pygame.K_LEFT:
        vel_x = 0 - tamanho_quadrado
        vel_y = 0
    else:
        return vel_x_atual, vel_y_atual

    # Impedir que a cobra se mova na direção oposta
    if tecla == pygame.K_DOWN and vel_y_atual == -tamanho_quadrado:
        return vel_x_atual, vel_y_atual
    elif tecla == pygame.K_UP and vel_y_atual == tamanho_quadrado:
        return vel_x_atual, vel_y_atual
    elif tecla == pygame.K_RIGHT and vel_x_atual == -tamanho_quadrado:
        return vel_x_atual, vel_y_atual
    elif tecla == pygame.K_LEFT and vel_x_atual == tamanho_quadrado:
        return vel_x_atual, vel_y_atual

    return vel_x, vel_y

#Tela de gameover
def tela_gameover():
    opcoes = ["Reiniciar", "Sair"]
    selecionado = 0 #0 reinicia 1 sai

    while True:
        tela.fill(preto)

        texto_go = fonte_gameover.render("Game Over", True, branco)
        tela.blit(texto_go, [
            largura / 2 - texto_go.get_width() / 2,
            altura / 2 - 120
        ])

        #Desenha as opçoes
        for i, opcao in enumerate(opcoes):
            #Deixa a opçao selecionada em amarelo
            cor = amarelo if i == selecionado else branco
            texto_opcao = fonte_opcoes.render(opcao, True, cor)
            tela.blit(texto_opcao, [
                largura / 2 - texto_opcao.get_width() / 2 - 120 + i * 240,
                altura / 2
            ])

        pygame.display.update()
        relogio.tick(15)

        #Pega teclas
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                exit()
            elif evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_LEFT:
                    selecionado = 0 #Reiniciar
                elif evento.key == pygame.K_RIGHT:
                    selecionado = 1 #Sair
                elif evento.key == pygame.K_RETURN:
                    return selecionado #o que tiver selecionado

#Loop infinito
def rodar_jogo():
    gameover = False

    x = largura / 2
    y = altura / 2

    vel_x = 0
    vel_y = 0

    tamanho_cobra = 1
    pixels = []

    comida_x, comida_y = gerar_comida()


    cor_cobra = tela_selecao_cor()

#Loop do jogo
    while True:
        tela.fill(preto)

        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                gameover = True
            elif evento.type == pygame.KEYDOWN:
                vel_x, vel_y = selecionar_velocidade(evento.key, vel_x, vel_y)

        #Desenhar comida
        desenhar_comida(tamanho_quadrado, comida_x, comida_y)

        #Atualizar posicao da cobra
        if x < 0 or x >= largura or y < 0 or y >= altura:
            gameover = True

        x += vel_x
        y += vel_y

        #Desenhar cobra
        pixels.append([x, y])
        if len(pixels) > tamanho_cobra:
            del pixels[0]

        #Regra de colisao de corpo
        for pixel in pixels[:-1]:
            if pixel == [x, y]:
                gameover = True

        desenhar_cobra(tamanho_quadrado, pixels, cor_cobra)
        desenhar_pontuacao(tamanho_cobra - 1)

        #Atualizar tela
        pygame.display.update()
        relogio.tick(velocidade_jogo)

        #Criar nova comida
        if x == comida_x and y == comida_y:
            tamanho_cobra += 1
            comida_x, comida_y = gerar_comida()

        if gameover:
            escolha = tela_gameover()
            if escolha == 0:
                rodar_jogo() #Reiniciar
                return 
            else:
                pygame.quit()
                exit()

rodar_jogo()               
