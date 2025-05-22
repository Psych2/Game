import pygame
import sys


pygame.init()

# Desenhando a tela / Draw the window
tdt = (800, 800)
tela = pygame.display.set_mode(tdt)
pygame.display.set_caption("Meu Jogo")

# Criando a Bola / Creating the ball
ball = 15
bola = pygame.Rect(100, 500, ball, ball)
tam_jogador = 100
jogador = pygame.Rect(0, 750, tam_jogador, 15)

# Criando os quadrados / Creating the Squares
qntd_blocos_linhas = 8
qntd_linhas_blocos = 5
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
vel_bola = [2, -2]
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
def mov_jogador(event):
    if event.type == pygame.KEYDOWN:
        if event.key == pygame.K_RIGHT and jogador.x + tam_jogador < tdt[0]:
            jogador.x += 5
        if event.key == pygame.K_LEFT and jogador.x > 0:
            jogador.x -= 5

# Criando e Desenvolvendo o movimento da Bola / Creating and devevolping the movement of the ball
def mov_bola(bola, vel_bola):
    bola.x += vel_bola[0]
    bola.y += vel_bola[1]
   
    if bola.x <= 0:
        vel_bola[0] = - vel_bola[0]
    if bola.y <= 0:
        vel_bola[1] = - vel_bola[1]
    if bola.x + ball >= tdt[0]:
        vel_bola[0] = - vel_bola[0]
    if bola.y + ball >= tdt[0]:
        return None, vel_bola  # A bola saiu da tela, fim do jogo / The ball go away of window, end game
   
   # Criando Colisão / Creating the colission
    if jogador.collidepoint(bola.x, bola.y):
        vel_bola[1] = - vel_bola[1]
    for bloco in blocos[:]:
        if bloco.collidepoint(bola.x, bola.y):
            blocos.remove(bloco)
            vel_bola[1] = - vel_bola[1]
            global pontos
            pontos += 1
       
    return bola, vel_bola
 
 # Criando a tabela de pontos / creating the points table 
def atualizar_pontos():
    fonte = pygame.font.Font(None, 30)
    texto = fonte.render(f"Pontos: {pontos}", 1, cores["azul"])
    tela.blit(texto, (0, 780))

# Definindo as cores e desenhando os aspectos na tela / Give the window colors and drawing the aspects
def desenhar_inicio_jogo():
    tela.fill(cores["preta"])
    pygame.draw.rect(tela, cores["azul"], jogador)
    pygame.draw.ellipse(tela, cores["branca"], bola)

# Desenhando os blocos / Draw the Blocos
def desenhar_blocos(blocos):
    for bloco in blocos:
        pygame.draw.rect(tela, cores["verde"], bloco)


blocos = criar_blocos(qntd_blocos_linhas, qntd_linhas_blocos)

#Loop para o jogo não fechar automático / Loop for the game dont close automatically
while not fim:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            fim = True
   
    # Movimenta o jogador / Moviment the player
    mov_jogador(event)
   
    # Desenha tudo / Draw all
    desenhar_inicio_jogo()
    desenhar_blocos(blocos)
    atualizar_pontos()
   
    # Move a bola / Move the ball
    bola, vel_bola = mov_bola(bola, vel_bola)
   
    # Verifica se o jogo acabou / Check if the game ends
    if bola is None or len(blocos) == 0:
        fim = True
   
   # Atualiza a tela / Update the window
    pygame.display.flip()
    pygame.time.delay(10)


pygame.quit()