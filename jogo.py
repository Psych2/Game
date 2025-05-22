import pygame
import sys

pygame.init()

# Desenhando a tela / Draw the window
tdt = (1920, 1080)
tela = pygame.display.set_mode(tdt, pygame.FULLSCREEN)
pygame.display.set_caption("Meu Jogo")

# Carregar imagem de fundo / Load background image
imagem_fundo = pygame.image.load("fundo.png").convert()
imagem_fundo = pygame.transform.scale(imagem_fundo, tdt)


# Carregar sons / Load sounds
som_colisao = pygame.mixer.Sound("som_colisao.wav")
som_vitoria = pygame.mixer.Sound("som_vitoria.wav")
som_derrota = pygame.mixer.Sound("som_derrota.wav")
pygame.mixer.music.load("musica_fundo.mp3")
pygame.mixer.music.play(-1)  # Reproduz em loop

# Criando a Bola / Creating the ball
ball = 15
bola = pygame.Rect(100, 500, ball, ball)
tam_jogador = 100
jogador = pygame.Rect(0, 1050, tam_jogador, 15)
# Criando os quadrados / Creating the Squares
qntd_blocos_linhas = 5
qntd_linhas_blocos = 4
qntd_total_blocos = qntd_blocos_linhas * qntd_linhas_blocos

# Definindo cores / The Colors
cores = {
    "branca": [255, 255, 255],
    "preta": [0, 0, 0],
    "amarela": [255, 255, 0],
    "azul": [0, 0, 255],
    "verde": [0, 255, 0]
}

# Variáveis iniciais / Initial Variable
vel_bola = [4, -4]
pontos = 0
fim = False

# Criando a função para desenhar os blocos / Create the function do draw the "blocos"
def criar_blocos(qntd_blocos_linhas, qntd_linhas_blocos):
    largura_tela = tdt[0]
    distancia_entre_blocos = 5
    largura_bloco = largura_tela / qntd_blocos_linhas - distancia_entre_blocos
    altura_bloco = 15
    distancia_entre_linhas = altura_bloco + 10
    blocos = []
    for j in range(qntd_linhas_blocos):
        for i in range(qntd_blocos_linhas):
            bloco = pygame.Rect(i * (largura_bloco + distancia_entre_blocos), j * distancia_entre_linhas, largura_bloco, altura_bloco)
            blocos.append(bloco)
    return blocos

# Criando e Desenvolvendo o Movimento do Jogador / Creating and devevolping the movement of player
def mov_jogador_tecla():
    keys = pygame.key.get_pressed()
    if keys[pygame.K_RIGHT] and jogador.x + tam_jogador < tdt[0]:
        jogador.x += 7
    if keys[pygame.K_LEFT] and jogador.x > 0:
        jogador.x -= 7

# Criando e Desenvolvendo o movimento da Bola / Creating and devevolping the movement of the ball
def mov_bola(bola, vel_bola, blocos, jogador, pontos):
    bola.x += vel_bola[0]
    bola.y += vel_bola[1]

    if bola.x <= 0:
        vel_bola[0] = - vel_bola[0]
    if bola.y <= 0:
        vel_bola[1] = - vel_bola[1]
    if bola.x + ball >= tdt[0]:
        vel_bola[0] = - vel_bola[0]
    if bola.y + ball >= tdt[1]:  # Correção: usar altura da tela
        return None, vel_bola, blocos, pontos  # A bola saiu da tela, fim do jogo / The ball go away of window, end game

    # Criando Colisão / Creating the colission
    if jogador.collidepoint(bola.x, bola.y):
        vel_bola[1] = - vel_bola[1]
        som_colisao.play()

    for bloco in blocos[:]:
        if bloco.collidepoint(bola.x, bola.y):
            blocos.remove(bloco)
            vel_bola[1] = - vel_bola[1]
            pontos += 1
            som_colisao.play()

    return bola, vel_bola, blocos, pontos

# Criando a tabela de pontos / creating the points table 
def atualizar_pontos(pontos):
    fonte = pygame.font.Font(None, 30)
    texto = fonte.render(f"Pontos: {pontos}", 1, cores["azul"])
    tela.blit(texto, (0, 780))

# Definindo as cores e desenhando os aspectos na tela / Give the window colors and drawing the aspects
def desenhar_inicio_jogo():
    tela.blit(imagem_fundo, (0, 0))
    pygame.draw.rect(tela, cores["azul"], jogador)
    pygame.draw.ellipse(tela, cores["branca"], bola)

# Desenhando os blocos / Draw the Blocos
def desenhar_blocos(blocos):
    for bloco in blocos:
        pygame.draw.rect(tela, cores["verde"], bloco)

blocos = criar_blocos(qntd_blocos_linhas, qntd_linhas_blocos)

# Loop para o jogo não fechar automático / Loop for the game dont close automatically
while not fim:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            fim = True

    mov_jogador_tecla()

    # Desenha tudo / Draw all
    desenhar_inicio_jogo()
    desenhar_blocos(blocos)
    atualizar_pontos(pontos)

    # Move a bola / Move the ball
    bola, vel_bola, blocos, pontos = mov_bola(bola, vel_bola, blocos, jogador, pontos)

    # Verifica se o jogo acabou / Check if the game ends
    if bola is None or len(blocos) == 0:
        pygame.mixer.music.stop()
        fonte = pygame.font.Font(None, 50)
        if len(blocos) == 0:
            msg = "Você venceu!"
            som_vitoria.play()
        else:
            msg = "Game Over"
            som_derrota.play()
        texto = fonte.render(msg, True, cores["amarela"])
        tela.blit(texto, (tdt[0]//2 - 100, tdt[1]//2))
        pygame.display.flip()
        pygame.time.wait(3000)
        fim = True

    # Atualiza a tela / Update the window
    pygame.display.flip()
    pygame.time.delay(10)

pygame.quit()
