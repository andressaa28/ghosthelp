import pygame as pg
import random

def tela_inicial():
    pg.init()
    pg.joystick.init()
    
    if pg.joystick.get_count() > 0:
        joystick = pg.joystick.Joystick(0)
        joystick.init()
    else:
        joystick = None

    scale = 23
    window_width = 740
    window_height = 620
    window = pg.display.set_mode((window_width, window_height))
    pg.display.set_caption("Ghost Grind")

    # Carregar imagem do título
    titulo_img = pg.image.load('img/titulo.png').convert_alpha()

    # pega tamanho original
    orig_w, orig_h = titulo_img.get_size()

    # reduz para 70% (ajuste o fator como quiser: 0.5, 0.8, etc.)
    novo_w = int(orig_w * 0.6)
    novo_h = int(orig_h * 0.6)

    titulo_img = pg.transform.scale(titulo_img, (novo_w, novo_h))
    titulo_rect = titulo_img.get_rect(center=(window_width // 2, window_height // 2.1))

    # Fonte
    font_sub = pg.font.SysFont("Courier New", int(scale * 1.2), bold=True)
    font_help = pg.font.SysFont("Courier New", int(scale * 0.8), bold=True)
    
    clock = pg.time.Clock()
    rodando = True
    frame = 0

    while rodando:
        clock.tick(30)
        frame += 1

        # Fundo animado (cor piscando levemente)
        cor = (46, 139 + (frame % 20), 87)
        window.fill(cor)

        # Efeito de "pulsar" no título
        scale_factor = 1 + 0.02 * (pg.time.get_ticks() // 200 % 2 * 2 - 1)
        titulo_anim = pg.transform.scale(titulo_img, (int(titulo_rect.width * scale_factor), int(titulo_rect.height * scale_factor)))
        titulo_anim_rect = titulo_anim.get_rect(center=titulo_rect.center)
        window.blit(titulo_anim, titulo_anim_rect)

        # Texto instrução
        sub = font_sub.render("Pressione ENTER para iniciar", True, (255, 255, 255))
        sub_rect = sub.get_rect(center=(window_width // 2, window_height // 1.2))  
        # antes estava window_height // 1.5 → agora vai ficar mais para baixo
        window.blit(sub, sub_rect)

        # texto ajuda
        help_text = font_help.render("Pressione H para ajuda", True, (180, 180, 180))  # cinza
        help_rect = help_text.get_rect(center=(window_width // 2, window_height - 20))
        window.blit(help_text, help_rect)
        
        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()
                quit()
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_RETURN:  # Enter
                    rodando = False
                elif event.key == pg.K_h:  # tecla H abre ajuda
                    tela_ajuda()
                elif event.key == pg.K_ESCAPE:
                    pg.quit()
                    quit()
            if event.type == pg.JOYBUTTONDOWN:
                if event.button == 0:  # Botão A
                    rodando = False
                elif event.button == 1:  # Botão B
                    tela_ajuda()
                elif event.button == 7:  # Start
                    rodando = False
                elif event.button == 6:  # Back
                    pg.quit()
                    quit()

        pg.display.update()

    return escolher_personagem()

def escolher_personagem():
    pg.init()
    pg.joystick.init()

    if pg.joystick.get_count() > 0:
        joystick = pg.joystick.Joystick(0)
        joystick.init()
    else:
        joystick = None
    
    scale = 23
    window_width = 740
    window_height = 620
    window = pg.display.set_mode((window_width, window_height))
    font = pg.font.SysFont("Courier New", int(scale * 1.4), bold=True)
    small_font = pg.font.SysFont("Courier New", int(scale * 0.8), bold=True)

    # Carregando prévias dos personagens
    personagens = [
        pg.image.load('img/prin1.png'),
        pg.image.load('img/personagem1/prin1.png'),
        pg.image.load('img/personagem2/prin1.png'),
        pg.image.load('img/personagem3/prin1.png'),]

    # Dobrar o tamanho das imagens
    largura_img = scale * 4
    altura_img = scale * 4
    personagens = [pg.transform.scale(p, (largura_img, altura_img)) for p in personagens]

    selecao = 0
    clock = pg.time.Clock()
    escolhendo = True

    # Configurações da grade
    cols = 2
    espacamento_x = scale * 3
    espacamento_y = scale * 5

    # Calcular a largura total da grade para centralizar
    total_largura = cols * largura_img + (cols - 1) * espacamento_x
    inicio_x = (window_width - total_largura) // 2
    inicio_y = scale * 7

    while escolhendo:
        clock.tick(30)
        window.fill((46, 139, 87))  # fundo azul escuro

        # título centralizado
        titulo = font.render("Escolha seu personagem", True, (255, 255, 255))
        window.blit(titulo, ((window_width - titulo.get_width()) // 2, scale))

        # Exibir personagens em grade centralizada
        for i, img in enumerate(personagens):
            col = i % cols
            row = i // cols
            x = inicio_x + col * (largura_img + espacamento_x)
            y = inicio_y + row * (altura_img + espacamento_y)

            if i == selecao:
                pg.draw.rect(window, (255, 255, 255),
                             (x - 5, y - 5, img.get_width() + 10, img.get_height() + 10), 2)
            window.blit(img, (x, y))

        # instruções no rodapé
        instrucoes = small_font.render("Use ← → ou ↑ ↓ para escolher, ENTER para confirmar", True, (255, 255, 255))
        window.blit(instrucoes, ((window_width - instrucoes.get_width()) // 2, window_height - scale * 2))

        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()
                quit()
            # teclado
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_LEFT:
                    selecao = (selecao - 1) % len(personagens)
                elif event.key == pg.K_RIGHT:
                    selecao = (selecao + 1) % len(personagens)
                elif event.key == pg.K_UP:
                    selecao = (selecao - cols) % len(personagens)
                elif event.key == pg.K_DOWN:
                    selecao = (selecao + cols) % len(personagens)
                elif event.key == pg.K_RETURN:
                    escolhendo = False
                elif event.key == pg.K_h:  # tecla H abre ajuda
                    tela_ajuda()

            # Joystick - Botões
            if event.type == pg.JOYBUTTONDOWN:
                if event.button == 0:  # A
                    escolhendo = False
                elif event.button == 7:  # Start
                    escolhendo = False
                elif event.button == 1:  # B
                    tela_ajuda()
                
            # Joystick - D-Pad
            if event.type == pg.JOYHATMOTION:
                x, y = event.value
                if x == -1:
                    selecao = (selecao - 1) % len(personagens)
                elif x == 1:
                    selecao = (selecao + 1) % len(personagens)
                elif y == 1:
                    selecao = (selecao - cols) % len(personagens)
                elif y == -1:
                    selecao = (selecao + cols) % len(personagens)

            # Joystick - Analógico
            if event.type == pg.JOYAXISMOTION:
                if event.axis == 0:  # Eixo X
                    if event.value < -0.5:
                        selecao = (selecao - 1) % len(personagens)
                    elif event.value > 0.5:
                        selecao = (selecao + 1) % len(personagens)
                elif event.axis == 1:  # Eixo Y
                    if event.value < -0.5:
                        selecao = (selecao - cols) % len(personagens)
                    elif event.value > 0.5:
                        selecao = (selecao + cols) % len(personagens)

        pg.display.update()

    return selecao

def tela_game_over(score):
    pg.init()
    pg.joystick.init()

    if pg.joystick.get_count() > 0:
        joystick = pg.joystick.Joystick(0)
        joystick.init()
    else:
        joystick = None

    window = pg.display.set_mode((740, 620))
    pg.display.set_caption("Game Over")

    # Fonte principal
    font = pg.font.SysFont("Courier New", 60, bold=True)
    # Fonte média (pontuação)
    small_font = pg.font.SysFont("Courier New", 25, bold=True)
    # Fonte menor (instruções)
    tiny_font = pg.font.SysFont("Courier New", 18, bold=True)

    rodando = True
    while rodando:
        largura, altura = window.get_size()
        window.fill((0, 0, 0))

        # Texto principal
        texto = font.render("GAME OVER", True, (255, 0, 0))
        window.blit(texto, texto.get_rect(center=(largura // 2, altura // 4)))

        # Pontuação
        pontos = small_font.render(f"Sua pontuação: {score}", True, (255, 255, 255))
        window.blit(pontos, pontos.get_rect(center=(largura // 2, altura // 2)))

        # Instruções menores
        instrucoes = [
            "Pressione ENTER para jogar novamente",
            #"Pressione R para voltar ao início",
            #"Pressione ESC para sair"
        ]

        start_y = 350      # ponto inicial
        spacing = 40       # espaçamento entre linhas (um pouco menor porque a fonte é menor)

        for i, txt in enumerate(instrucoes):
            line = tiny_font.render(txt, True, (200, 200, 200))
            rect = line.get_rect(center=(370, start_y + i * spacing))
            window.blit(line, rect)

        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()
                quit()
            # teclado
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_RETURN:  # Vai para os créditos
                    tela_creditos()  # Mostra créditos
                    tela_inicial()   # Depois volta ao início
                    return    
                elif event.key == pg.K_r:  # Voltar para a tela inicial
                    tela_inicial()
                    selecao = escolher_personagem()  # se quiser reaparecer seleção
                    rodando = False
                elif event.key == pg.K_ESCAPE:  # Sai
                    pg.quit()
                    quit()
                elif event.key == pg.K_h:  # tecla H abre ajuda
                    tela_ajuda()

            # Joystick - Botões
            if event.type == pg.JOYBUTTONDOWN:
                if event.button == 0:  # A
                    tela_creditos()
                    tela_inicial()
                    return
                elif event.button == 7:  # Start
                    tela_creditos()
                    tela_inicial()
                    return
                elif event.button == 1:  # B
                    tela_ajuda()
                elif event.button == 6:  # Back
                    pg.quit()
                    quit()

        pg.display.update()

def tela_transicao(level):
    pg.init()
    window = pg.display.set_mode((740, 620))
    pg.display.set_caption("Próxima Fase")

    # Fonte principal
    font = pg.font.SysFont("Courier New", 60, bold=True)
    # Fonte menor
    small_font = pg.font.SysFont("Courier New", 25, bold=True)

    rodando = True
    tempo = pg.time.get_ticks()
    while rodando:
        largura, altura = window.get_size()
        window.fill((0, 0, 0))

        # Texto principal
        texto = font.render(f"Fase {level}", True, (255, 255, 0))
        window.blit(texto, texto.get_rect(center=(largura // 2, altura // 3)))

        # Texto menor (centralizado)
        sub = small_font.render("Prepare-se!", True, (255, 255, 255))
        window.blit(sub, sub.get_rect(center=(largura // 2, altura // 2)))

        # Espera 3 segundos
        if pg.time.get_ticks() - tempo > 3000:
            rodando = False

        pg.display.update()

def tela_transicao_fase3():
    pg.init()
    window = pg.display.set_mode((740, 620))
    pg.display.set_caption("Chegou a Fase 3!")

    font = pg.font.SysFont("Courier New", 50, bold=True)
    small_font = pg.font.SysFont("Courier New", 25, bold=True)

    rodando = True
    tempo = pg.time.get_ticks()
    while rodando:
        largura, altura = window.get_size()
        window.fill((10, 10, 40))  # fundo diferente (azul escuro)

        # Texto principal em destaque
        titulo = font.render(" FASE 3 ", True, (255, 100, 0))
        window.blit(titulo, titulo.get_rect(center=(largura // 2, altura // 3)))

        # Subtexto
        sub = small_font.render("Prepare-se para o desafio final!", True, (255, 255, 255))
        window.blit(sub, sub.get_rect(center=(largura // 2, altura // 1.8)))

        # Espera 3 segundos
        if pg.time.get_ticks() - tempo > 3000:
            rodando = False

        pg.display.update()

def tela_vitoria(score):
    pg.init()
    pg.joystick.init()

    if pg.joystick.get_count() > 0:
        joystick = pg.joystick.Joystick(0)
        joystick.init()
    else:
        joystick = None

    window = pg.display.set_mode((740, 620))
    pg.display.set_caption("Vitória!")

    font = pg.font.SysFont("Courier New", 60, bold=True)
    small_font = pg.font.SysFont("Courier New", 25, bold=True)

    rodando = True
    while rodando:
        window.fill((0, 0, 0))

        largura, altura = window.get_size()

        # Título principal
        texto = font.render("VOCÊ VENCEU!", True, (0, 255, 0))
        window.blit(texto, texto.get_rect(center=(largura // 2, altura // 3)))

        # Pontuação logo abaixo
        pontos = small_font.render(f"Sua pontuação: {score}", True, (255, 255, 255))
        window.blit(pontos, pontos.get_rect(center=(largura // 2, altura // 2)))

        # Instrução
        restart = small_font.render("Pressione ENTER para continuar", True, (200, 200, 200))
        window.blit(restart, restart.get_rect(center=(largura // 2, altura // 1.5)))

        #voltar = small_font.render("Pressione R para voltar ao início", True, (200, 200, 200))
        #window.blit(voltar, voltar.get_rect(center=(400, 410)))

        #sair = small_font.render("Pressione ESC para sair", True, (200, 200, 200))
        #window.blit(sair, sair.get_rect(center=(400, 460)))

        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()
                quit()
            # teclado
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_RETURN:  # Vai para os créditos
                    tela_creditos()  # Mostra créditos
                    tela_inicial()   # Depois volta ao início
                    return    
                elif event.key == pg.K_r:  # Voltar para a tela inicial
                    tela_inicial()
                    selecao = escolher_personagem()  # se quiser reaparecer seleção
                    rodando = False
                elif event.key == pg.K_ESCAPE:  # Sai
                    pg.quit()
                    quit()

            # Joystick - Botões
            if event.type == pg.JOYBUTTONDOWN:
                if event.button == 0:  # A
                    tela_creditos()
                    tela_inicial()
                    return
                elif event.button == 7:  # Start
                    tela_creditos()
                    tela_inicial()
                    return
                elif event.button == 1:  # B
                    tela_ajuda()
                elif event.button == 6:  # Back
                    pg.quit()
                    quit()

        pg.display.update()

def tela_creditos():
    pg.init()
    window = pg.display.set_mode((740, 620))
    pg.display.set_caption("Créditos")

    font_titulo = pg.font.SysFont("Courier New", 48, bold=True)
    font = pg.font.SysFont("Courier New", 26, bold=True)
    tiny_font = pg.font.SysFont("Courier New", 18, bold=True)

    linhas = [
        "Programação: Andressa",
        "Arte visual: Amanda, Bárbara e Giovana"
    ]

    instrucoes = [
        "Turma STEAM 23/M1",
        "Professora Ana Laura"
    ]

    spacing = 25  # espaçamento menor porque vai ficar no rodapé

    inicio = pg.time.get_ticks()
    rodando = True
    while rodando:
        largura, altura = window.get_size()
        window.fill((0, 0, 0))

        # título
        titulo = font_titulo.render("CRÉDITOS", True, (255, 255, 0))
        window.blit(titulo, titulo.get_rect(center=(largura // 2, altura // 4)))

        # linhas principais (meio da tela)
        for i, texto in enumerate(linhas):
            surf = font.render(texto, True, (255, 255, 255))
            window.blit(surf, surf.get_rect(center=(largura // 2, altura // 2 + i * 40)))

        # instruções (rodapé centralizado)
        for i, txt in enumerate(instrucoes):
            line = tiny_font.render(txt, True, (200, 200, 200))
            rect = line.get_rect(center=(largura // 2, altura - 60 + i * spacing))
            window.blit(line, rect)

        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit(); quit()

        # fecha sozinho depois de 60s
        if pg.time.get_ticks() - inicio >= 6000:
            rodando = False
            return

        pg.display.update()

def tela_ajuda():
    pg.init()
    pg.joystick.init()

    if pg.joystick.get_count() > 0:
        joystick = pg.joystick.Joystick(0)
        joystick.init()
    else:
        joystick = None

    window = pg.display.set_mode((740, 620))
    pg.display.set_caption("Ajuda")

    font_titulo = pg.font.SysFont("Courier New", 48, bold=True)
    font = pg.font.SysFont("Courier New", 26, bold=True)
    small_font = pg.font.SysFont("Courier New", 20, bold=True)

    # Carregar imagens usadas no jogo
    img_pocao = pg.image.load("img/pocao.png")
    img_coracao = pg.image.load("img/coracao.png")
    img_turbo = pg.image.load("img/turbo.png")
    img_freeze = pg.image.load("img/freeze.png")

    rodando = True
    while rodando:
        window.fill((0, 0, 0))

        # Título
        titulo = font_titulo.render("AJUDA", True, (255, 255, 0))
        window.blit(titulo, titulo.get_rect(center=(370, 60)))

        # Controles
        controles = [
            "Movimento: ↑ ↓ ← → ou W A S D",
            "Pause: P",
            "Reiniciar: R",
            "Sair: ESC"
        ]
        for i, txt in enumerate(controles):
            line = font.render(txt, True, (255, 255, 255))
            window.blit(line, (80, 140 + i * 40))

        # Legenda dos itens
        window.blit(img_pocao, (100, 320))
        window.blit(small_font.render("Poção: deixa os fantasmas vulneráveis", True, (255, 255, 255)), (160, 330))

        window.blit(img_coracao, (100, 380))
        window.blit(small_font.render("Coração: ganha uma vida extra", True, (255, 255, 255)), (160, 390))

        window.blit(img_turbo, (100, 440))
        window.blit(small_font.render("Turbo: aumenta a velocidade do Pac-Man", True, (255, 255, 255)), (160, 450))

        window.blit(img_freeze, (100, 500))
        window.blit(small_font.render("Freeze: congela os fantasmas por alguns segundos", True, (255, 255, 255)), (160, 510))

        # Instrução para sair
        sair = small_font.render("Pressione ENTER para voltar", True, (200, 200, 200))
        window.blit(sair, sair.get_rect(center=(370, 580)))

        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()
                quit()
            # teclado
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_RETURN:  # Voltar
                    rodando = False
            # Joystick - Botões
            if event.type == pg.JOYBUTTONDOWN:
                if event.button == 0:  # A
                    rodando = False
                elif event.button == 7:  # Start
                    rodando = False
                elif event.button == 6:  # Back
                    pg.quit()
                    quit()


        pg.display.update()

class FloatingText:
    def __init__(self, text, x, y, font, color=(255, 255, 0)):
        self.text = text
        self.x = x
        self.y = y
        self.font = font
        self.color = color
        self.timer = 60  # ~1 segundo a 60fps

    def update(self):
        self.y -= 1   # sobe devagar
        self.timer -= 1

    def draw(self, surface):
        img = self.font.render(self.text, True, self.color)
        surface.blit(img, (self.x, self.y))

class PacMan:
    def __init__(self, scale, selected_character=0):
        self.scale = scale
        self.selected_character = selected_character
        self.level = 1  # Começa no nível 1
        
        # Pac-Man
        char_folder = [
            "img",  # personagem 0 -> arquivos direto na pasta "img"
            "img/personagem1",
            "img/personagem2",
            "img/personagem3",
        ][self.selected_character]

        self.white = (255, 255, 255)
        self.black = (46, 139, 87)
        self.blue  = (32, 96, 64)
        scale = 20
        self.ghost_speed_factor = 1.0  # começa normal

        self.window = pg.display.set_mode((scale * 37, scale * 31))
        pg.font.init()
        self.font = pg.font.SysFont("Courier New", scale * 1, bold=True)
        self.clock = pg.time.Clock()
        self.scale = scale
        self.sprite_frame = 0
        self.sprite_speed = 2

        self.score = 0
        self.lives = 5
        self.end_game = False
        self.harmless_mode = False
        self.harmless_mode_timer = 0
        self.harmless_mode_ghost_blue   = False
        self.harmless_mode_ghost_orange = False
        self.harmless_mode_ghost_pink   = False
        self.harmless_mode_ghost_red    = False

        self.pac_man_pos            = [self.scale * 13.1, self.scale * 22.6]
        self.pac_man_direction      = [self.scale/16, 0]
        self.pac_man_next_direction = [self.scale/16, 0]

        self.ghost_blue_pos   = [self.scale * 12, self.scale * 13]
        self.ghost_orange_pos = [self.scale * 12, self.scale * 14.5]
        self.ghost_pink_pos   = [self.scale * 14, self.scale * 13]
        self.ghost_red_pos    = [self.scale * 14, self.scale * 14.5]
        self.ghost_blue_direction   = [0, 0]
        self.ghost_orange_direction = [0, 0]
        self.ghost_pink_direction   = [0, 0]
        self.ghost_red_direction    = [0, 0]
        self.ghost_blue_next_direction   = [0, 0]
        self.ghost_orange_next_direction = [0, 0]
        self.ghost_pink_next_direction   = [0, 0]
        self.ghost_red_next_direction    = [0, 0]
        self.distance_ghost_blue_to_pac_man   = self.distance_ghost_to_pac_man(self.ghost_blue_pos)
        self.distance_ghost_orange_to_pac_man = self.distance_ghost_to_pac_man(self.ghost_orange_pos)
        self.distance_ghost_pink_to_pac_man   = self.distance_ghost_to_pac_man(self.ghost_pink_pos)
        self.distance_ghost_red_to_pac_man    = self.distance_ghost_to_pac_man(self.ghost_red_pos) 

        pac_man_1 = pg.image.load(f'{char_folder}/prin1.png')
        pac_man_2 = pg.image.load(f'{char_folder}/prin2.png')
        pac_man_3 = pg.image.load(f'{char_folder}/prin3.png')
        pac_man_4 = pg.image.load(f'{char_folder}/prin4.png')
        pac_man_5 = pg.image.load(f'{char_folder}/prin5.png')
        pac_man_6 = pg.image.load(f'{char_folder}/prin6.png')
        pac_man_7 = pg.image.load(f'{char_folder}/prin7.png')
        pac_man_8 = pg.image.load(f'{char_folder}/prin8.png')
        pac_man_9 = pg.image.load(f'{char_folder}/prin9.png')
        pac_man_10 = pg.image.load(f'{char_folder}/prin10.png')
        pac_man_11 = pg.image.load(f'{char_folder}/prin11.png')

        self.pac_man_1 = pg.transform.scale(pac_man_1, (self.scale * 1.3, self.scale * 1.3))
        self.pac_man_2 = pg.transform.scale(pac_man_2, (self.scale * 1.3, self.scale * 1.3))
        self.pac_man_3 = pg.transform.scale(pac_man_3, (self.scale * 1.3, self.scale * 1.3))
        self.pac_man_4 = pg.transform.scale(pac_man_4, (self.scale * 1.3, self.scale * 1.3))
        self.pac_man_5 = pg.transform.scale(pac_man_5, (self.scale * 1.3, self.scale * 1.3))
        self.pac_man_6 = pg.transform.scale(pac_man_6, (self.scale * 1.3, self.scale * 1.3))
        self.pac_man_7 = pg.transform.scale(pac_man_7, (self.scale * 1.3, self.scale * 1.3))
        self.pac_man_8 = pg.transform.scale(pac_man_8, (self.scale * 1.3, self.scale * 1.3))
        self.pac_man_9 = pg.transform.scale(pac_man_9, (self.scale * 1.3, self.scale * 1.3))
        self.pac_man_10 = pg.transform.scale(pac_man_10, (self.scale * 1.3, self.scale * 1.3))
        self.pac_man_11 = pg.transform.scale(pac_man_11, (self.scale * 1.3, self.scale * 1.3))

        # Blue Ghost
        ghost_blue_down_right_0 = pg.image.load('img/fan_marshmallow1.png')
        ghost_blue_down_right_1 = pg.image.load('img/fan_marshmallow2.png')
        self.ghost_blue_down_right_0 = pg.transform.scale(ghost_blue_down_right_0, (self.scale * 1.3, self.scale * 1.3))
        self.ghost_blue_down_right_1 = pg.transform.scale(ghost_blue_down_right_1, (self.scale * 1.3, self.scale * 1.3))

        # Orange Ghost
        ghost_orange_down_right_0 = pg.image.load('img/fan_roxo1.png')
        ghost_orange_down_right_1 = pg.image.load('img/fan_roxo2.png')
        self.ghost_orange_down_right_0 = pg.transform.scale(ghost_orange_down_right_0, (self.scale * 1.3, self.scale * 1.3))
        self.ghost_orange_down_right_1 = pg.transform.scale(ghost_orange_down_right_1, (self.scale * 1.3, self.scale * 1.3))

        # Pink Ghost
        ghost_pink_down_right_0 = pg.image.load('img/fan_verde1.png')
        ghost_pink_down_right_1 = pg.image.load('img/fan_verde2.png')
        self.ghost_pink_down_right_0 = pg.transform.scale(ghost_pink_down_right_0, (self.scale * 1.3, self.scale * 1.3))
        self.ghost_pink_down_right_1 = pg.transform.scale(ghost_pink_down_right_1, (self.scale * 1.3, self.scale * 1.3))

        # Red Ghost
        ghost_red_down_right_0 = pg.image.load('img/dog1.png')
        ghost_red_down_right_1 = pg.image.load('img/dog2.png')
        self.ghost_red_down_right_0 = pg.transform.scale(ghost_red_down_right_0, (self.scale * 1.3, self.scale * 1.3))
        self.ghost_red_down_right_1 = pg.transform.scale(ghost_red_down_right_1, (self.scale * 1.3, self.scale * 1.3))

        # Harmless Ghost
        ghost_harmless_0       = pg.image.load('img/fan_marshmallow7.png')
        ghost_harmless_1       = pg.image.load('img/fan_roxo8.png')
        self.ghost_harmless_0 = pg.transform.scale(ghost_harmless_0, (self.scale * 1.3, self.scale * 1.3))
        self.ghost_harmless_1 = pg.transform.scale(ghost_harmless_1, (self.scale * 1.3, self.scale * 1.3))

        # Carregar imagem para o ponto de poder
        self.img_power = pg.image.load('img/pocao.png').convert_alpha()
        self.img_power = pg.transform.scale(self.img_power, (int(self.scale * 2), int(self.scale * 2)))

        # imagem coração 
        self.img_life = pg.image.load('img/coracao.png').convert_alpha()
        self.img_life = pg.transform.scale(self.img_life, (int(self.scale * 1.5), int(self.scale * 1.5)))
        self.floating_texts = []

        # imagem turbo
        self.img_turbo = pg.image.load('img/turbo.png').convert_alpha()
        self.img_turbo = pg.transform.scale(self.img_turbo, (int(self.scale * 2), int(self.scale * 2)))

        # imagem freeze
        self.img_freeze = pg.image.load('img/freeze.png').convert_alpha()
        self.img_freeze = pg.transform.scale(self.img_freeze, (int(self.scale * 2), int(self.scale * 2)))

        # atributos do turbo
        self.turbo_mode = False
        self.turbo_timer = 0
        self.turbo_duration = 420  # ~7 segundos a 60fps
        self.normal_speed = self.scale / 16
        self.turbo_speed = self.scale / 8
        self.score_turbo = 50

        # Freeze (congelar fantasmas)
        self.freeze_mode = False
        self.freeze_timer = 0
        self.freeze_duration = 360  # 6 segundos a 60fps
        self.score_freeze = 100

        # mapa original
        self.map = [
            ['#','#','#','#','#','#','#','#','#','#','#','#','#','#','#','#','#','#','#','#','#','#','#','#','#','#','#','#'],
            ['#','.','.','.','.','.','.','.','.','.','.','.','.','#','#','.','.','.','.','.','.','.','.','.','.','.','.','#'],
            ['#','.','#','#','#','#','.','#','#','#','#','#','.','#','#','.','#','#','#','#','#','.','#','#','#','#','.','#'],
            ['#','o','#','#','#','#','.','#','#','#','#','#','.','#','#','.','#','#','#','#','#','.','#','#','#','#','o','#'],
            ['#','.','#','#','#','#','.','#','#','#','#','#','.','#','#','.','#','#','#','#','#','.','#','#','#','#','.','#'],
            ['#','.','.','.','.','.','.','.','.','.','.','.','.','.','.','.','.','.','.','.','.','.','.','.','.','.','.','#'],
            ['#','.','#','#','#','#','.','#','#','.','#','#','#','#','#','#','#','#','.','#','#','.','#','#','#','#','.','#'],
            ['#','.','#','#','#','#','.','#','#','.','#','#','#','#','#','#','#','#','.','#','#','.','#','#','#','#','.','#'],
            ['#','.','.','.','.','.','.','#','#','.','.','.','.','#','#','.','.','.','.','#','#','.','.','.','.','.','.','#'],
            ['#','#','#','#','#','#','.','#','#','#','#','#',' ','#','#',' ','#','#','#','#','#','.','#','#','#','#','#','#'],
            [' ',' ',' ',' ',' ','#','.','#','#','#','#','#',' ','#','#',' ','#','#','#','#','#','.','#',' ',' ',' ',' ',' '],
            [' ',' ',' ',' ',' ','#','.','#','#',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ','#','#','.','#',' ',' ',' ',' ',' '],
            [' ',' ',' ',' ',' ','#','.','#','#',' ','#','#','#','-','-','#','#','#',' ','#','#','.','#',' ',' ',' ',' ',' '],
            ['#','#','#','#','#','#','.','#','#',' ','#',' ',' ',' ',' ',' ',' ','#',' ','#','#','.','#','#','#','#','#','#'],
            [' ',' ',' ',' ',' ',' ','.',' ',' ',' ','#',' ',' ',' ',' ',' ',' ','#',' ',' ',' ','.',' ',' ',' ',' ',' ',' '],
            ['#','#','#','#','#','#','.','#','#',' ','#',' ',' ',' ',' ',' ',' ','#',' ','#','#','.','#','#','#','#','#','#'],
            [' ',' ',' ',' ',' ','#','.','#','#',' ','#','#','#','#','#','#','#','#',' ','#','#','.','#',' ',' ',' ',' ',' '],
            [' ',' ',' ',' ',' ','#','.','#','#',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ','#','#','.','#',' ',' ',' ',' ',' '],
            [' ',' ',' ',' ',' ','#','.','#','#',' ','#','#','#','#','#','#','#','#',' ','#','#','.','#',' ',' ',' ',' ',' '],
            ['#','#','#','#','#','#','.','#','#',' ','#','#','#','#','#','#','#','#',' ','#','#','.','#','#','#','#','#','#'],
            ['#','.','.','.','.','.','.','.','.','.','.','.','.','#','#','.','.','.','.','.','.','.','.','.','.','.','.','#'],
            ['#','.','#','#','#','#','.','#','#','#','#','#','.','#','#','.','#','#','#','#','#','.','#','#','#','#','.','#'],
            ['#','.','#','#','#','#','.','#','#','#','#','#','.','#','#','.','#','#','#','#','#','.','#','#','#','#','.','#'],
            ['#','o','.','.','#','#','.','.','.','.','.','.','.',' ',' ','.','.','.','.','.','.','.','#','#','.','.','o','#'],
            ['#','#','#','.','#','#','.','#','#','.','#','#','#','#','#','#','#','#','.','#','#','.','#','#','.','#','#','#'],
            ['#','#','#','.','#','#','.','#','#','.','#','#','#','#','#','#','#','#','.','#','#','.','#','#','.','#','#','#'],
            ['#','.','.','.','.','.','v','#','#','f','.','.','.','#','#','.','.','.','.','#','#','.','.','.','.','.','.','#'],
            ['#','.','#','#','#','#','#','#','#','#','#','#','.','#','#','.','#','#','#','#','#','#','#','#','#','#','.','#'],
            ['#','.','#','#','#','#','#','#','#','#','#','#','.','#','#','.','#','#','#','#','#','#','#','#','#','#','.','#'],
            ['#','.','.','.','.','.','t','.','.','.','.','.','.','.','.','.','.','.','.','.','.','.','.','.','.','.','.','#'],
            ['#','#','#','#','#','#','#','#','#','#','#','#','#','#','#','#','#','#','#','#','#','#','#','#','#','#','#','#']]
        
        self.map2 = [
            ['#','#','#','#','#','#','#','#','#','#','#','#','#','#','#','#','#','#','#','#','#','#','#','#','#','#','#','#'],
            ['#','.','.','o','.','.','.','#','#','.','.','.','.','#','#','.','.','.','.','#','#','.','.','.','.','.','.','#'],
            ['#','.','#','#','#','#','.','#','#','.','#','#','.','#','#','.','#','#','.','#','#','.','#','#','#','#','.','#'],
            ['#','.','#','#','#','#','.','#','#','.','#','#','.','#','#','.','#','#','.','#','#','.','#','#','#','#','.','#'],
            ['#','.','.','#','#','.','t','#','#','.','#','#','.','.','.','.','#','#','.','#','#','.','o','#','#','.','.','#'],
            ['#','#','.','#','#','.','#','#','#','.','#','#','#','#','#','#','#','#','.','#','#','#','.','#','#','.','#','#'],
            ['#','#','.','.','.','.','.','.','.','.','#','#','#','#','#','#','#','#','.','.','.','.','.','.','.','.','#','#'],
            ['#','#','.','#','#','.','#','#','#','.','.','.','.','#','#','.','.','.','.','#','#','#','.','#','#','.','#','#'],
            ['#','#','.','#','#','.','.','#','#','.','#','#','.','#','#','.','#','#','.','#','#','.','.','#','#','.','#','#'],
            ['#','.','.','#','#','#','.','#','#','.','#','#','.','#','#','.','#','#','.','#','#','.','#','#','#','.','.','#'],
            ['#','.','#','#','#','#','.','#','#','.','#','#','.','#','#','.','#','#','.','#','#','.','#','#','#','#','.','#'],
            ['#','v','#','#','#','#','.','#','#','.','.','.','.','.','.','.','.','.','.','#','#','t','#','#','#','#','.','#'],
            ['#','.','.','.','.','.','.','#','#','.','#','#','#','-','-','#','#','#','.','#','#','.','.','.','.','.','.','#'],
            ['#','#','#','#','#','#','.','.','.','.','#',' ',' ',' ',' ',' ',' ','#','.','.','.','.','#','#','#','#','#','#'],
            ['#','#','#','#','#','#','.','#','#','.','#',' ',' ',' ',' ',' ',' ','#','.','#','#','.','#','#','#','#','#','#'],
            [' ',' ',' ',' ',' ',' ','.','#','#','.','#',' ',' ',' ',' ',' ',' ','#','.','#','#','.',' ',' ',' ',' ',' ',' '],
            ['#','#','#','#','#','#','.','#','#','.','#','#','#','#','#','#','#','#','.','#','#','.','#','#','#','#','#','#'],
            ['#','#','#','#','#','#','.','.','.','.','#','#',' ',' ',' ',' ','#','#','.','.','.','.','#','#','#','#','#','#'],
            ['#','.','.','.','.','.','.','#','#','.','#','#',' ','#','#',' ','#','#','.','#','#','.','.','.','.','.','.','#'],
            ['#','.','#','#','#','#','.','#','#','.',' ',' ',' ','#','#',' ',' ',' ','.','#','#','.','#','#','#','#','.','#'],
            ['#','.','#','#','#','#','.','#','#','#','#','#',' ','#','#',' ','#','#','#','#','#','.','#','#','#','#','.','#'],
            ['#','.','#','#','#','#','.','#','#','#','#','#',' ','#','#',' ','#','#','#','#','#','.','#','#','#','#','.','#'],
            ['#','.','#','#','#','#','.','#','#','#','#','#',' ','#','#',' ','#','#','#','#','#','.','#','#','#','#','.','#'],
            ['#','o','.','.','#','#','.','.','.','.','.','.','.',' ',' ','.','.','.','.','.','.','.','#','#','.','.','o','#'],
            ['#','#','#','.','#','#','.','#','#','.','#','#','#','#','#','#','#','#','.','#','#','.','#','#','.','#','#','#'],
            ['#','#','#','.','#','#','.','#','#','.','#','#','#','#','#','#','#','#','.','#','#','.','#','#','.','#','#','#'],
            ['#','.','.','.','.','.','f','#','#','.','.','.','.','#','#','.','.','.','.','#','#','.','.','.','.','.','.','#'],
            ['#','.','#','#','#','#','#','#','#','#','#','#','.','#','#','.','#','#','#','#','#','#','#','#','#','#','.','#'],
            ['#','.','#','#','#','#','#','#','#','#','#','#','.','#','#','.','#','#','#','#','#','#','#','#','#','#','.','#'],
            ['#','.','.','.','.','.','.','.','.','.','.','.','.','.','.','v','.','.','.','.','.','.','.','.','.','.','.','#'],
            ['#','#','#','#','#','#','#','#','#','#','#','#','#','#','#','#','#','#','#','#','#','#','#','#','#','#','#','#']]

        self.map3 = [
            ['#','#','#','#','#','#','#','#','#','#','#','#','#','#','#','#','#','#','#','#','#','#','#','#','#','#','#','#'],
            ['#','#','v','#','.','.','.','.','.','.','.','.','.','.','.','.','.','.','.','.','#','#','#','#','#','#','.','#'],
            ['#','#','.','#','#','#','.','#','#','#','#','#','o','#','#','#','#','#','#','.','#','#','#','#','.','.','.','#'],
            ['#','#','.','#','#','#','.','#','#','#','#','#','.','.','.','.','.','#','.','.','#','#','.','.','.','#','.','#'],
            ['#','#','.','#','.','.','.','.','.','.','.','.','.','#','#','#','.','.','.','#','#','#','.','#','#','#','.','#'],
            ['#','#','.','#','.','#','.','#','#','#','.','#','#','#','.','.','.','#','.','.','.','.','f','.','.','.','.','#'],
            ['#','#','.','#','.','#','.','#','#','#','.','.','#','#','#','.','#','#','#','#','#','#','#','#','.','#','#','#'],
            ['#','#','.','.','.','#','.','.','.','#','#','.','.','#','#','.','#','#','#','.','.','.','.','.','.','#','#','#'],
            ['#','#','.','#','#','#','#','#','.','#','#','#','.','#','#','.','#','#','.','.','#','.','#','#','#','#','#','#'],
            [' ','.','.','#','#','#','#','#','.','.','.','.','.','.','.','.','.','.','.','#','#','.','.','.','.','.','.',' '],
            ['#','#','.','#','#','#','#','#','.','#','#','#','#','#','#','#','#','#','#','#','#','.','#','.','#','#','#','#'],
            ['#','#','.','#','#','.','.','.','.','.','.','.','.','.','.','.','.','.','.','.','.','.','#','.','#','#','#','#'],
            ['#','#','.','#','.','.','#','#','#','.','#','#','#','-','-','#','#','#','.','#','#','#','#','.','.','.','#','#'],
            ['#','#','.','.','.','#','#','#','#','.','#',' ',' ',' ',' ',' ',' ','#','.','#','.','#','#','.','#','.','.','#'],
            ['#','#','.','#','.','.','#','#','#','.','#',' ',' ',' ',' ',' ',' ','#','.','#','.','#','#','.','#','#','.','#'],
            ['#','#','.','#','#','.','.','#','#','.','#',' ',' ',' ',' ',' ',' ','#','.','#','.','.','.','.','.','.','.','#'],
            ['#','#','.','#','#','#','.','.','#','.','#','#','#','#','#','#','#','#','.','#','#','#','.','#','#','#','.','#'],
            ['#','#','.','#','#','#','#','.','.','.','.','.','.','.','.','.','.','.','.','.','#','#','.','.','#','#','.','#'],
            ['#','#','.','.','.','.','.','.','#','#','#','#','#','#','.','#','#','#','#','.','#','#','#','.','#','#','.','#'],
            ['#','#','#','#','.','#','#','.','#','#','#','#','#','#','.','#','#','#','#','.','#','#','#','.','#','#','.','#'],
            ['#','#','#','#','.','#','#','.','.','.','.','.','.','.','t','.','.','#','#','.','.','.','.','.','.','.','o','#'],
            ['#','.','.','.','.','#','#','.','#','#','#','.','#','#','#','#','.','#','#','.','#','#','#','#','.','#','#','#'],
            ['#','.','#','#','.','#','#','.','#','#','#','.','#','#','#','#','.','#','#','.','#','#','#','.','.','#','#','#'],
            ['#','.','#','#','.','#','#','.','.','.','.','.','.',' ',' ','.','.','.','.','.','#','#','#','.','#','#','#','#'],
            ['#','.','#','#','.','.','.','.','#','#','#','#','#','#','#','#','#','#','#','.','#','#','.','.','#','#','#','#'],
            ['#','.','#','#','#','#','#','.','#','#','#','#','#','#','#','#','#','#','#','.','#','#','.','#','#','#','#','#'],
            ['#','.','.','.','#','#','#','.','.','.','.','.','.','.','.','.','.','.','.','.','.','.','.','.','.','.','.','#'],
            ['#','o','#','.','.','.','.','.','#','#','.','#','#','.','#','#','#','#','.','#','.','#','#','#','#','#','.','#'],
            ['#','#','#','.','#','#','#','.','.','.','f','#','#','.','.','#','.','.','.','#','.','.','#','#','.','.','.','#'],
            ['#','.','.','.','.','.','.','.','#','#','#','#','#','#','.','v','.','#','#','#','#','.','.','.','.','#','.','#'],
            ['#','#','#','#','#','#','#','#','#','#','#','#','#','#','#','#','#','#','#','#','#','#','#','#','#','#','#','#']]

    def clear_window(self):
        pg.draw.rect(self.window, self.black, (0, 0, self.window.get_width(), self.window.get_height()))

    def get_speed(self):
        return self.turbo_speed if self.turbo_mode else self.normal_speed

    def move(self, key):
        if key == 'r':
            self.restart()
        if key == 'w' or key == 'up':
            if self.pac_man_direction[0] == 0 and self.pac_man_direction[1] > 0:
                self.pac_man_direction[0] = 0
                self.pac_man_direction[1] = -self.get_speed()
                self.pac_man_next_direction[0] = 0
                self.pac_man_next_direction[1] = -self.get_speed()
            elif self.pac_man_direction[0] != 0 and self.pac_man_direction[1] == 0:
                self.pac_man_next_direction[0] = 0
                self.pac_man_next_direction[1] = -self.get_speed()
        elif key == 'a' or key == 'left':
            if self.pac_man_direction[0] > 0 and self.pac_man_direction[1] == 0:
                self.pac_man_direction[0] = -self.get_speed()
                self.pac_man_direction[1] = 0
                self.pac_man_next_direction[0] = -self.get_speed()
                self.pac_man_next_direction[1] = 0
            elif self.pac_man_direction[0] == 0 and self.pac_man_direction[1] != 0:
                self.pac_man_next_direction[0] = -self.get_speed()
                self.pac_man_next_direction[1] = 0
        elif key == 's' or key == 'down':
            if self.pac_man_direction[0] == 0 and self.pac_man_direction[1] < 0:
                self.pac_man_direction[0] = 0
                self.pac_man_direction[1] = self.get_speed()
                self.pac_man_next_direction[0] = 0
                self.pac_man_next_direction[1] = self.get_speed()
            elif self.pac_man_direction[0] != 0 and self.pac_man_direction[1] == 0:
                self.pac_man_next_direction[0] = 0
                self.pac_man_next_direction[1] = self.get_speed()
        elif key == 'd' or key == 'right':
            if self.pac_man_direction[0] < 0 and self.pac_man_direction[1] == 0:
                self.pac_man_direction[0] = self.get_speed()
                self.pac_man_direction[1] = 0
                self.pac_man_next_direction[0] = self.get_speed()
                self.pac_man_next_direction[1] = 0
            elif self.pac_man_direction[0] == 0 and self.pac_man_direction[1] != 0:
                self.pac_man_next_direction[0] = self.get_speed()
                self.pac_man_next_direction[1] = 0
            
    def board(self):
        for y in range(len(self.map)):
            for x in range(len(self.map[0])):
                cell = self.map[y][x]
            
                # paredes
                if cell == '#':
                    pg.draw.rect(self.window, self.blue, (x * self.scale, y * self.scale, self.scale, self.scale))
            
                # portas
                elif cell == '-':
                    pg.draw.rect(self.window, self.white, (x * self.scale, y * self.scale, self.scale, self.scale))
            
                # fundo para espaços, pontos e power-ups
                elif cell in (' ', '.', 'o', 'f', 't', 'v'):
                    pg.draw.rect(self.window, self.black,
                                 ((x * self.scale) - (self.scale / 2),
                                  (y * self.scale) - (self.scale / 2),
                                  self.scale * 1.5, self.scale * 1.5))

        for y in range(len(self.map)):
            for x in range(len(self.map[0])):
                cell = self.map[y][x]

               # bolinhas pequenas
                if cell == '.':
                    pg.draw.circle(self.window, self.white,
                                   ((x * self.scale) + (self.scale / 4),
                                    (y * self.scale) + (self.scale / 4)),
                                    self.scale / 5)

                # power-up normal (o)
                elif cell == 'o':
                    cx = (x * self.scale) + (self.scale / 4)
                    cy = (y * self.scale) + (self.scale / 4)
                    pw, ph = self.img_power.get_size()
                    pos_x = int(cx - pw / 2)
                    pos_y = int(cy - ph / 2) - 7
                    self.window.blit(self.img_power, (pos_x, pos_y))

                # freeze (f)
                elif cell == 'f' and self.score >= self.score_freeze:
                    cx = (x * self.scale) + (self.scale / 4)
                    cy = (y * self.scale) + (self.scale / 4)
                    pw, ph = self.img_freeze.get_size()
                    pos_x = int(cx - pw / 2)
                    pos_y = int(cy - ph / 2) 
                    self.window.blit(self.img_freeze, (pos_x, pos_y))

                # turbo (t)
                elif cell == 't' and self.score >= self.score_turbo:
                    cx = (x * self.scale) + (self.scale / 2)
                    cy = (y * self.scale) + (self.scale / 2)
                    pw, ph = self.img_turbo.get_size()
                    pos_x = int(cx - pw / 2)
                    pos_y = int(cy - ph / 2)
                    self.window.blit(self.img_turbo, (pos_x, pos_y))

                # vida extra (v)
                elif cell == 'v' and self.lives < 3 :
                    cx = (x * self.scale) + (self.scale / 4)
                    cy = (y * self.scale) + (self.scale / 4)
                    pw, ph = self.img_life.get_size()
                    pos_x = int(cx - pw / 2)
                    pos_y = int(cy - ph / 2)
                    self.window.blit(self.img_life, (pos_x, pos_y))

        # textos flutuantes
        for text in self.floating_texts[:]:
            text.update()
            text.draw(self.window)
            if text.timer <= 0:
                self.floating_texts.remove(text)

    def animation_step(self):
        if self.sprite_frame == 60:
            self.sprite_frame = 0
        else:
            self.sprite_frame += self.sprite_speed

    def player_rotation(self, image):
        x_dir = self.pac_man_direction[0]
        y_dir = self.pac_man_direction[1]
        if x_dir > 0 and y_dir == 0:
            return image
        elif x_dir == 0 and y_dir > 0:
            return pg.transform.rotate(image, -90)
        elif x_dir < 0 and y_dir == 0:
            return pg.transform.flip(image, True, False)
        elif x_dir == 0 and y_dir < 0:
            return pg.transform.rotate(image, 90)

    def collider(self, position, direction):
        if self.end_game == False:
            position[0] += direction[0]
            position[1] += direction[1]
            for y in range(len(self.map)):
                for x in range(len(self.map[0])):
                    if self.map[y][x] == '#' or self.map[y][x] == '-':
                        x_wall = (x * self.scale) - (self.scale * 0.65)
                        y_wall = (y * self.scale) - (self.scale * 0.65)
                        wall_size = self.scale * 1.85
                        x_agent = position[0] + (self.scale * 0.65)
                        y_agent = position[1] + (self.scale * 0.65)


                        if x_agent >= x_wall and x_agent <= x_wall + wall_size and y_agent >= y_wall and y_agent <= y_wall + wall_size:
                            position[0] -= direction[0]
                            position[1] -= direction[1]

        return position

    def turning_corner(self, position, direction, next_direction):
        turned_corner = True
        position[0] += next_direction[0] * 16
        position[1] += next_direction[1] * 16
        for y in range(len(self.map)):
            for x in range(len(self.map[0])):
                if self.map[y][x] == '#' or self.map[y][x] == '-':
                    x_wall = (x * self.scale) - (self.scale * 0.65)
                    y_wall = (y * self.scale) - (self.scale * 0.65)
                    wall_size = self.scale * 1.85
                    x_agent = position[0] + (self.scale * 0.65)
                    y_agent = position[1] + (self.scale * 0.65)
                    if x_agent >= x_wall and x_agent <= x_wall + wall_size and y_agent >= y_wall and y_agent <= y_wall + wall_size:
                        turned_corner = False
        position[0] -= next_direction[0] * 16
        position[1] -= next_direction[1] * 16
        if turned_corner:
            direction[0] = next_direction[0]
            direction[1] = next_direction[1]

        return direction, next_direction

    def draw_item(self, x, y, image, offset_y=-7):
        """
        Desenha uma imagem centralizada no tile do mapa.
        offset_y: ajusta a posição vertical (padrão -7 para alinhar com as bolinhas grandes).
        """
        cx = (x * self.scale) + (self.scale / 4)  # centro horizontal
        cy = (y * self.scale) + (self.scale / 4)  # centro vertical

        pw, ph = image.get_size()
        pos_x = int(cx - pw / 2)
        pos_y = int(cy - ph / 2) + offset_y

        self.window.blit(image, (pos_x, pos_y))

    def update_pacman_speed(self):
        # Atualiza a velocidade da direção atual com base no turbo
        if self.pac_man_direction[0] != 0:
            self.pac_man_direction[0] = (1 if self.pac_man_direction[0] > 0 else -1) * self.get_speed()
        if self.pac_man_direction[1] != 0:
            self.pac_man_direction[1] = (1 if self.pac_man_direction[1] > 0 else -1) * self.get_speed()

        # Também atualiza a próxima direção se estiver definida
        if self.pac_man_next_direction[0] != 0:
            self.pac_man_next_direction[0] = (1 if self.pac_man_next_direction[0] > 0 else -1) * self.get_speed()
        if self.pac_man_next_direction[1] != 0:
            self.pac_man_next_direction[1] = (1 if self.pac_man_next_direction[1] > 0 else -1) * self.get_speed()

    def collect_dots(self):
        x_pac_man = self.pac_man_pos[0] + (self.scale * 0.65)
        y_pac_man = self.pac_man_pos[1] + (self.scale * 0.65)
        for y in range(len(self.map)):
            for x in range(len(self.map[0])):
                if self.map[y][x] == '.':
                    x_dot = (x * self.scale) + (self.scale / 4)
                    y_dot = (y * self.scale) + (self.scale / 4)
                    radius = self.scale / 5
                    if x_pac_man >= x_dot - radius and x_pac_man <= x_dot + radius and y_pac_man >= y_dot - radius and y_pac_man <= y_dot + radius:
                        self.map[y][x] = ' '
                        self.score += 1
                if self.map[y][x] == 'o':
                    x_dot = (x * self.scale) + (self.scale / 4)
                    y_dot = (y * self.scale) + (self.scale / 4)
                    radius = self.scale / 2
                    if x_pac_man >= x_dot - radius and x_pac_man <= x_dot + radius and y_pac_man >= y_dot - radius and y_pac_man <= y_dot + radius:
                        self.map[y][x] = ' '
                        self.score += 10
                        self.harmless_mode = True
                        self.harmless_mode_ghost_blue   = True
                        self.harmless_mode_ghost_orange = True
                        self.harmless_mode_ghost_pink   = True
                        self.harmless_mode_ghost_red    = True
                if self.map[y][x] == 'v':
                    x_dot = (x * self.scale) + (self.scale / 4)
                    y_dot = (y * self.scale) + (self.scale / 4)
                    radius = self.scale / 2

                    # colisão com o coração
                    if (x_pac_man >= x_dot - radius and x_pac_man <= x_dot + radius and
                        y_pac_man >= y_dot - radius and y_pac_man <= y_dot + radius):

                    # só coleta se tiver 2 vidas ou menos
                        if self.lives <= 2:
                            if self.lives < 5:  # limite de vidas (opcional)
                                self.lives += 1
                            self.map[y][x] = ' '  # remove só quando ganhou vida
                if self.map[y][x] == 't' and self.score >= self.score_turbo:
                    x_dot = (x * self.scale) + (self.scale / 4)
                    y_dot = (y * self.scale) + (self.scale / 4)
                    radius = self.scale / 2
                    if (x_pac_man >= x_dot - radius and x_pac_man <= x_dot + radius and
                            y_pac_man >= y_dot - radius and y_pac_man <= y_dot + radius):
                        self.map[y][x] = ' '  # remove do mapa
                        self.turbo_mode = True
                        self.turbo_timer = 0
                        self.update_pacman_speed()
                if self.map[y][x] == 'f' and self.score >= self.score_freeze:
                    x_dot = (x * self.scale) + (self.scale / 4)
                    y_dot = (y * self.scale) + (self.scale / 4)
                    radius = self.scale / 2

                    if (x_pac_man >= x_dot - radius and x_pac_man <= x_dot + radius and
                        y_pac_man >= y_dot - radius and y_pac_man <= y_dot + radius):

                        self.map[y][x] = ' '  # remove do mapa
                        self.freeze_mode = True
                        self.freeze_timer = 0

    def pacman_tunnel(self, position):
        x_pos = position[0]
        y_pos = position[1]
        if position[0] >= self.scale * 27.5:
            x_pos = 0 - (self.scale * 1.3)
        elif position[0] <= -(self.scale * 1.3):
            x_pos = self.scale * 27.5
        return [x_pos, y_pos]

    def player(self):
        self.pac_man_direction, self.pac_man_next_direction = self.turning_corner(self.pac_man_pos, self.pac_man_direction, self.pac_man_next_direction)
        self.pac_man_pos = self.collider(self.pac_man_pos, self.pac_man_direction)
        self.pac_man_pos = self.pacman_tunnel(self.pac_man_pos)
        x = self.pac_man_pos[0]
        y = self.pac_man_pos[1]

        if self.end_game:
            if self.sprite_frame <= 5:
                self.window.blit(self.player_rotation(self.pac_man_4), (x, y))
            elif self.sprite_frame <= 10:
                self.window.blit(self.player_rotation(self.pac_man_5), (x, y))
            elif self.sprite_frame <= 15:
                self.window.blit(self.player_rotation(self.pac_man_6), (x, y))
            elif self.sprite_frame <= 20:
                self.window.blit(self.player_rotation(self.pac_man_4), (x, y))
            elif self.sprite_frame <= 25:
                self.window.blit(self.player_rotation(self.pac_man_5), (x, y))
            elif self.sprite_frame <= 30:
                self.window.blit(self.player_rotation(self.pac_man_6), (x, y))
        else:
            if self.sprite_frame <= 6:
                self.window.blit(self.player_rotation(self.pac_man_1), (x, y))
            elif self.sprite_frame <= 12:
                self.window.blit(self.player_rotation(self.pac_man_1), (x, y))
            elif self.sprite_frame <= 18:
                self.window.blit(self.player_rotation(self.pac_man_2), (x, y))
            elif self.sprite_frame <= 24:
                self.window.blit(self.player_rotation(self.pac_man_3), (x, y))
            elif self.sprite_frame <= 48:
                self.window.blit(self.player_rotation(self.pac_man_3), (x, y))
            elif self.sprite_frame <= 54:
                self.window.blit(self.player_rotation(self.pac_man_2), (x, y))
            elif self.sprite_frame <= 60:
                self.window.blit(self.player_rotation(self.pac_man_1), (x, y))
        
        if self.turbo_mode:
            self.turbo_timer += 1
            if self.turbo_timer >= self.turbo_duration:
                self.turbo_mode = False
                self.update_pacman_speed()
        if self.freeze_mode:
            self.freeze_timer += 1
            if self.freeze_timer >= self.freeze_duration:
                self.freeze_mode = False

    def aumentar_dificuldade(self):
        self.level += 1
        self.ghost_speed_factor += 0.5  # aumenta 50% a cada fase

    def ghost_render(self, color, position):
        x = position[0]
        y = position[1]
        if color == 'blue':
            if self.sprite_frame <= 15:
                self.window.blit(self.ghost_blue_down_right_0, (x, y))
            elif self.sprite_frame <= 30:
                self.window.blit(self.ghost_blue_down_right_1, (x, y))
            elif self.sprite_frame <= 45:
                self.window.blit(self.ghost_blue_down_right_0, (x, y))
            elif self.sprite_frame <= 60:
                self.window.blit(self.ghost_blue_down_right_1, (x, y))
        elif color == 'orange':
            if self.sprite_frame <= 15:
                self.window.blit(self.ghost_orange_down_right_0, (x, y))
            elif self.sprite_frame <= 30:
                self.window.blit(self.ghost_orange_down_right_1, (x, y))
            elif self.sprite_frame <= 45:
                self.window.blit(self.ghost_orange_down_right_0, (x, y))
            elif self.sprite_frame <= 60:
                self.window.blit(self.ghost_orange_down_right_1, (x, y))
        elif color == 'pink':
            if self.sprite_frame <= 15:
                self.window.blit(self.ghost_pink_down_right_0, (x, y))
            elif self.sprite_frame <= 30:
                self.window.blit(self.ghost_pink_down_right_1, (x, y))
            elif self.sprite_frame <= 45:
                self.window.blit(self.ghost_pink_down_right_0, (x, y))
            elif self.sprite_frame <= 60:
                self.window.blit(self.ghost_pink_down_right_1, (x, y))
        elif color == 'red':
            if self.sprite_frame <= 15:
                self.window.blit(self.ghost_red_down_right_0, (x, y))
            elif self.sprite_frame <= 30:
                self.window.blit(self.ghost_red_down_right_1, (x, y))
            elif self.sprite_frame <= 45:
                self.window.blit(self.ghost_red_down_right_0, (x, y))
            elif self.sprite_frame <= 60:
                self.window.blit(self.ghost_red_down_right_1, (x, y))
        elif color == 'harmless':
            if self.sprite_frame <= 15:
                self.window.blit(self.ghost_harmless_0, (x, y))
            elif self.sprite_frame <= 30:
                self.window.blit(self.ghost_harmless_1, (x, y))
            elif self.sprite_frame <= 45:
                self.window.blit(self.ghost_harmless_0, (x, y))
            elif self.sprite_frame <= 60:
                self.window.blit(self.ghost_harmless_1, (x, y))

    def random_direction_for_ghost(self):
        move_up_or_sideways = random.randint(0, 1)
        x_direction = random.randint(0, 1)
        y_direction = random.randint(0, 1)
        direction = []
        if move_up_or_sideways == 0:
            if x_direction == 0:
                direction = [-self.scale/16, 0]
            else:
                direction = [self.scale/16, 0]
        else:
            if y_direction == 0:
                direction = [0, -self.scale/16]
            else:
                direction = [0, self.scale/16]

        return direction

    def random_next_direction_for_ghost(self, direction):
        new_direction = [0, 0]
        if direction[0] != 0:
            if random.randint(0, 1) == 0:
                new_direction[1] = -self.scale/16
            else:
                new_direction[1] = self.scale/16
        elif direction[1] != 0:
            if random.randint(0, 1) == 0:
                new_direction[0] = -self.scale/16
            else:
                new_direction[0] = self.scale/16

        return new_direction

    def distance_ghost_to_pac_man(self, ghost_pos):
        ghost_x = ghost_pos[0] + (self.scale * 0.65)
        ghost_y = ghost_pos[1] + (self.scale * 0.65)
        pac_man_x = self.pac_man_pos[0] + (self.scale * 0.65)
        pac_man_y = self.pac_man_pos[1] + (self.scale * 0.65)
        delta_x = (ghost_x - pac_man_x) ** 2
        delta_y = (ghost_y - pac_man_y) ** 2
        distance = (delta_x + delta_y) ** (1 / 2)

        return distance

    def direction_ghost_to_pac_man(self, position, direction):
        new_direction = [0, 0]
        ghost_x = position[0]
        ghost_y = position[1]
        pac_man_x = self.pac_man_pos[0]
        pac_man_y = self.pac_man_pos[1]
        delta_x = ghost_x - pac_man_x
        delta_y = ghost_y - pac_man_y
        if direction[1] != 0:
            if delta_x <= 0:
                new_direction[0] = self.scale/16
            else:
                new_direction[0] = -self.scale/16
        if direction[0] != 0:
            if delta_y <= 0:
                new_direction[1] = self.scale/16
            else:
                new_direction[1] = -self.scale/16

        return new_direction

    def direction_harmless_ghost_to_pac_man(self, position, direction):
        new_direction = [0, 0]
        ghost_x = position[0]
        ghost_y = position[1]
        pac_man_x = self.pac_man_pos[0]
        pac_man_y = self.pac_man_pos[1]
        delta_x = ghost_x - pac_man_x
        delta_y = ghost_y - pac_man_y
        if direction[1] != 0:
            if delta_x <= 0:
                new_direction[0] = -self.scale/16
            else:
                new_direction[0] = self.scale/16
        if direction[0] != 0:
            if delta_y <= 0:
                new_direction[1] = -self.scale/16
            else:
                new_direction[1] = self.scale/16

        return new_direction

    def new_random_direction_for_ghost(self, position, direction):
        new_direction = [0, 0]
        pos = [0, 0]
        pos[0] = position[0]
        pos[1] = position[1]

        if direction[0] != 0:
            if random.randint(0, 1) == 0:
                new_direction[1] = -self.scale/8
            else:
                new_direction[1] = self.scale/8
        elif direction[1] != 0:
            if random.randint(0, 1) == 0:
                new_direction[0] = -self.scale/8
            else:
                new_direction[0] = self.scale/8

        new_position = self.collider(pos, new_direction)

        if position == new_position:
            new_direction[0] *= -1
            new_direction[1] *= -1
            new_position = self.collider(pos, new_direction)

        new_direction[0] /= 2
        new_direction[1] /= 2

        return new_position, new_direction
    
    def ghost_intelligence(self, ghost_pos, ghost_direction, ghost_next_direction, distance_ghost_to_pac_man, harmless_ghost_mode):
        ghost_blue_pos = [0, 0]
        ghost_blue_pos[0] = ghost_pos[0]
        ghost_blue_pos[1] = ghost_pos[1]
        distance_ghost_to_pac_man = self.distance_ghost_to_pac_man(ghost_pos)
        if distance_ghost_to_pac_man <= self.scale * 10:
            if harmless_ghost_mode:
                ghost_next_direction = self.direction_harmless_ghost_to_pac_man(ghost_pos, ghost_direction)
            else:
                ghost_next_direction = self.direction_ghost_to_pac_man(ghost_pos, ghost_direction)
            ghost_direction, ghost_next_direction = self.turning_corner(ghost_pos, ghost_direction, ghost_next_direction)
        if ghost_direction == ghost_next_direction:
            if harmless_ghost_mode:
                ghost_next_direction = self.direction_harmless_ghost_to_pac_man(ghost_pos, ghost_direction)
            else:
                ghost_next_direction = self.direction_ghost_to_pac_man(ghost_pos, ghost_direction)
            ghost_pos = self.collider(ghost_pos, ghost_direction)
        ghost_pos = self.pacman_tunnel(ghost_pos)
        ghost_pos = self.collider(ghost_pos, ghost_direction)
        if ghost_blue_pos == ghost_pos:
            ghost_pos, ghost_direction = self.new_random_direction_for_ghost(ghost_pos, ghost_direction)
        return ghost_pos, ghost_direction, ghost_next_direction, distance_ghost_to_pac_man

    def ghost(self):
        if self.freeze_mode:
            self.distance_ghost_red_to_pac_man = self.distance_ghost_to_pac_man(self.ghost_red_pos)
            self.distance_ghost_blue_to_pac_man = self.distance_ghost_to_pac_man(self.ghost_blue_pos)
            self.distance_ghost_orange_to_pac_man = self.distance_ghost_to_pac_man(self.ghost_orange_pos)
            self.distance_ghost_pink_to_pac_man = self.distance_ghost_to_pac_man(self.ghost_pink_pos)
            return  # 👈 se congelados, não se movem
        if self.ghost_blue_pos != [self.scale * 12, self.scale * 13]:
            input_1 = self.ghost_blue_pos
            input_2 = self.ghost_blue_direction
            input_3 = self.ghost_blue_next_direction
            input_4 = self.distance_ghost_blue_to_pac_man
            input_5 = self.harmless_mode_ghost_blue
            output_1, output_2, output_3, output_4 = self.ghost_intelligence(input_1, input_2, input_3, input_4, input_5)
            self.ghost_blue_pos = output_1
            self.ghost_blue_direction = output_2
            self.ghost_blue_next_direction = output_3
            self.distance_ghost_blue_to_pac_man = output_4
        if self.ghost_orange_pos != [self.scale * 12, self.scale * 14.5]:
            input_1 = self.ghost_orange_pos
            input_2 = self.ghost_orange_direction
            input_3 = self.ghost_orange_next_direction
            input_4 = self.distance_ghost_orange_to_pac_man
            input_5 = self.harmless_mode_ghost_orange
            output_1, output_2, output_3, output_4 = self.ghost_intelligence(input_1, input_2, input_3, input_4, input_5)
            self.ghost_orange_pos = output_1
            self.ghost_orange_direction = output_2
            self.ghost_orange_next_direction = output_3
            self.distance_ghost_orange_to_pac_man = output_4
        if self.ghost_pink_pos != [self.scale * 14, self.scale * 13]:
            input_1 = self.ghost_pink_pos
            input_2 = self.ghost_pink_direction
            input_3 = self.ghost_pink_next_direction
            input_4 = self.distance_ghost_pink_to_pac_man
            input_5 = self.harmless_mode_ghost_pink
            output_1, output_2, output_3, output_4 = self.ghost_intelligence(input_1, input_2, input_3, input_4, input_5)
            self.ghost_pink_pos = output_1
            self.ghost_pink_direction = output_2
            self.ghost_pink_next_direction = output_3
            self.distance_ghost_pink_to_pac_man = output_4
        if self.ghost_red_pos != [self.scale * 14, self.scale * 14.5]:
            input_1 = self.ghost_red_pos
            input_2 = self.ghost_red_direction
            input_3 = self.ghost_red_next_direction
            input_4 = self.distance_ghost_red_to_pac_man
            input_5 = self.harmless_mode_ghost_red
            output_1, output_2, output_3, output_4 = self.ghost_intelligence(input_1, input_2, input_3, input_4, input_5)
            self.ghost_red_pos = output_1
            self.ghost_red_direction = output_2
            self.ghost_red_next_direction = output_3
            self.distance_ghost_red_to_pac_man = output_4

    def moving_ghost_into_the_game(self, color):
        if color == 'blue':
            self.ghost_blue_pos = [self.scale * 13.1, self.scale * 10.6]
            self.ghost_blue_direction = self.random_direction_for_ghost()
            self.ghost_blue_next_direction = self.random_next_direction_for_ghost(self.ghost_blue_direction)
        elif color == 'orange':
            self.ghost_orange_pos = [self.scale * 13.1, self.scale * 10.6]
            self.ghost_orange_direction = self.random_direction_for_ghost()
            self.ghost_orange_next_direction = self.random_next_direction_for_ghost(self.ghost_orange_direction)
        elif color == 'pink':
            self.ghost_pink_pos = [self.scale * 13.1, self.scale * 10.6]
            self.ghost_pink_direction = self.random_direction_for_ghost()
            self.ghost_pink_next_direction = self.random_next_direction_for_ghost(self.ghost_pink_direction)
        elif color == 'red':
            self.ghost_red_pos = [self.scale * 13.1, self.scale * 10.6]
            self.ghost_red_direction = self.random_direction_for_ghost()
            self.ghost_red_next_direction = self.random_next_direction_for_ghost(self.ghost_red_direction)

    def ghost_manager(self):
        if self.harmless_mode:
            if self.sprite_frame == 60:
                self.harmless_mode_timer += 1
            if self.harmless_mode_timer == 16:
                self.harmless_mode = False
                self.harmless_mode_ghost_blue   = False
                self.harmless_mode_ghost_orange = False
                self.harmless_mode_ghost_pink   = False
                self.harmless_mode_ghost_red    = False
                self.harmless_mode_timer = 0
        if self.harmless_mode_ghost_blue:
            self.ghost_render('harmless', self.ghost_blue_pos)
        else:
            self.ghost_render('blue',   self.ghost_blue_pos)
        if self.harmless_mode_ghost_orange:
            self.ghost_render('harmless', self.ghost_orange_pos)
        else:
            self.ghost_render('orange', self.ghost_orange_pos)
        if self.harmless_mode_ghost_pink:
            self.ghost_render('harmless', self.ghost_pink_pos)
        else:
            self.ghost_render('pink',   self.ghost_pink_pos)
        if self.harmless_mode_ghost_red:
            self.ghost_render('harmless', self.ghost_red_pos)
        else:
            self.ghost_render('red',    self.ghost_red_pos)

        if self.sprite_frame == 60:
            if self.ghost_blue_pos == [self.scale * 12, self.scale * 13]:
                self.moving_ghost_into_the_game('blue')
            elif self.ghost_orange_pos == [self.scale * 12, self.scale * 14.5]:
                self.moving_ghost_into_the_game('orange')
            elif self.ghost_pink_pos == [self.scale * 14, self.scale * 13]:
                self.moving_ghost_into_the_game('pink')
            elif self.ghost_red_pos == [self.scale * 14, self.scale * 14.5]:
                self.moving_ghost_into_the_game('red')

    def ghost_and_pacman_collider(self):
        if self.distance_ghost_blue_to_pac_man <= (self.scale * 1.1):
            if self.harmless_mode_ghost_blue:
                self.ghost_blue_pos = [self.scale * 12, self.scale * 13]
                self.harmless_mode_ghost_blue = False
                self.distance_ghost_blue_to_pac_man = self.distance_ghost_to_pac_man(self.ghost_blue_pos)
                self.score += 20
                self.floating_texts.append(
                    FloatingText("+20", int(self.pac_man_pos[0]), int(self.pac_man_pos[1]), self.font))
            else:
                if self.end_game == False:
                    self.sprite_frame = 0
                    self.sprite_speed = 1
                    self.lives -= 1
                self.end_game = True
                if self.freeze_mode:         # 👈 se estava congelado, cancela
                    self.freeze_mode = False
                    self.freeze_timer = 0
        elif self.distance_ghost_orange_to_pac_man <= (self.scale * 1.1):
            if self.harmless_mode_ghost_orange:
                self.ghost_orange_pos = [self.scale * 12, self.scale * 14.5]
                self.harmless_mode_ghost_orange = False
                self.distance_ghost_orange_to_pac_man = self.distance_ghost_to_pac_man(self.ghost_orange_pos)
                self.score += 30
                self.floating_texts.append(
                    FloatingText("+30", int(self.pac_man_pos[0]), int(self.pac_man_pos[1]), self.font))
            else:
                if self.end_game == False:
                    self.sprite_frame = 0
                    self.sprite_speed = 1
                    self.lives -= 1
                self.end_game = True                
                if self.freeze_mode:         # 👈 se estava congelado, cancela
                    self.freeze_mode = False
                    self.freeze_timer = 0
        elif self.distance_ghost_pink_to_pac_man <= (self.scale * 1.1):
            if self.harmless_mode_ghost_pink:
                self.ghost_pink_pos = [self.scale * 14, self.scale * 13]
                self.harmless_mode_ghost_pink = False
                self.distance_ghost_pink_to_pac_man = self.distance_ghost_to_pac_man(self.ghost_pink_pos)
                self.score += 40
                self.floating_texts.append(
                    FloatingText("+40", int(self.pac_man_pos[0]), int(self.pac_man_pos[1]), self.font))
            else:
                if self.end_game == False:
                    self.sprite_frame = 0
                    self.sprite_speed = 1
                    self.lives -= 1
                self.end_game = True                
                if self.freeze_mode:         # 👈 se estava congelado, cancela
                    self.freeze_mode = False
                    self.freeze_timer = 0
        elif self.distance_ghost_red_to_pac_man <= (self.scale * 1.1):
            if self.harmless_mode_ghost_red:
                self.ghost_red_pos = [self.scale * 14, self.scale * 14.5]
                self.harmless_mode_ghost_red = False
                self.distance_ghost_red_to_pac_man = self.distance_ghost_to_pac_man(self.ghost_red_pos)
                self.score += 50
                self.floating_texts.append(
                    FloatingText("+50", int(self.pac_man_pos[0]), int(self.pac_man_pos[1]), self.font))
            else:
                if self.end_game == False:
                    self.sprite_frame = 0
                    self.sprite_speed = 1
                    self.lives -= 1
                self.end_game = True                
                if self.freeze_mode:         # 👈 se estava congelado, cancela
                    self.freeze_mode = False
                    self.freeze_timer = 0

    def restart(self):
        self.sprite_frame = 0
        self.sprite_speed = 2
        self.score = 0
        self.lives = 5
        self.end_game = False
        self.harmless_mode = False
        self.harmless_mode_timer = 0
        self.harmless_mode_ghost_blue   = False
        self.harmless_mode_ghost_orange = False
        self.harmless_mode_ghost_pink   = False
        self.harmless_mode_ghost_red    = False
        self.pac_man_pos            = [self.scale * 13.1, self.scale * 22.6]
        self.pac_man_direction      = [self.scale/16, 0]
        self.pac_man_next_direction = [self.scale/16, 0]
        self.ghost_blue_pos   = [self.scale * 12, self.scale * 13]
        self.ghost_orange_pos = [self.scale * 12, self.scale * 14.5]
        self.ghost_pink_pos   = [self.scale * 14, self.scale * 13]
        self.ghost_red_pos    = [self.scale * 14, self.scale * 14.5]
        self.ghost_blue_direction   = [0, 0]
        self.ghost_orange_direction = [0, 0]
        self.ghost_pink_direction   = [0, 0]
        self.ghost_red_direction    = [0, 0]
        self.ghost_blue_next_direction   = [0, 0]
        self.ghost_orange_next_direction = [0, 0]
        self.ghost_pink_next_direction   = [0, 0]
        self.ghost_red_next_direction    = [0, 0]
        self.distance_ghost_blue_to_pac_man   = self.distance_ghost_to_pac_man(self.ghost_blue_pos)
        self.distance_ghost_orange_to_pac_man = self.distance_ghost_to_pac_man(self.ghost_orange_pos)
        self.distance_ghost_pink_to_pac_man   = self.distance_ghost_to_pac_man(self.ghost_pink_pos)
        self.distance_ghost_red_to_pac_man    = self.distance_ghost_to_pac_man(self.ghost_red_pos)
        self.map = [['#','#','#','#','#','#','#','#','#','#','#','#','#','#','#','#','#','#','#','#','#','#','#','#','#','#','#','#'],
                    ['#','.','.','.','.','.','.','.','.','.','.','.','.','#','#','.','.','.','.','.','.','.','.','.','.','.','.','#'],
                    ['#','.','#','#','#','#','.','#','#','#','#','#','.','#','#','.','#','#','#','#','#','.','#','#','#','#','.','#'],
                    ['#','o','#','#','#','#','.','#','#','#','#','#','.','#','#','.','#','#','#','#','#','.','#','#','#','#','o','#'],
                    ['#','.','#','#','#','#','.','#','#','#','#','#','.','#','#','.','#','#','#','#','#','.','#','#','#','#','.','#'],
                    ['#','.','.','.','.','.','.','.','.','.','.','.','.','.','.','.','.','.','.','.','.','.','.','.','.','.','.','#'],
                    ['#','.','#','#','#','#','.','#','#','.','#','#','#','#','#','#','#','#','.','#','#','.','#','#','#','#','.','#'],
                    ['#','.','#','#','#','#','.','#','#','.','#','#','#','#','#','#','#','#','.','#','#','.','#','#','#','#','.','#'],
                    ['#','.','.','.','.','.','.','#','#','.','.','.','.','#','#','.','.','.','.','#','#','.','.','.','.','.','.','#'],
                    ['#','#','#','#','#','#','.','#','#','#','#','#',' ','#','#',' ','#','#','#','#','#','.','#','#','#','#','#','#'],
                    [' ',' ',' ',' ',' ','#','.','#','#','#','#','#',' ','#','#',' ','#','#','#','#','#','.','#',' ',' ',' ',' ',' '],
                    [' ',' ',' ',' ',' ','#','.','#','#',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ','#','#','.','#',' ',' ',' ',' ',' '],
                    [' ',' ',' ',' ',' ','#','.','#','#',' ','#','#','#','-','-','#','#','#',' ','#','#','.','#',' ',' ',' ',' ',' '],
                    ['#','#','#','#','#','#','.','#','#',' ','#',' ',' ',' ',' ',' ',' ','#',' ','#','#','.','#','#','#','#','#','#'],
                    [' ',' ',' ',' ',' ',' ','.',' ',' ',' ','#',' ',' ',' ',' ',' ',' ','#',' ',' ',' ','.',' ',' ',' ',' ',' ',' '],
                    ['#','#','#','#','#','#','.','#','#',' ','#',' ',' ',' ',' ',' ',' ','#',' ','#','#','.','#','#','#','#','#','#'],
                    [' ',' ',' ',' ',' ','#','.','#','#',' ','#','#','#','#','#','#','#','#',' ','#','#','.','#',' ',' ',' ',' ',' '],
                    [' ',' ',' ',' ',' ','#','.','#','#',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ','#','#','.','#',' ',' ',' ',' ',' '],
                    [' ',' ',' ',' ',' ','#','.','#','#',' ','#','#','#','#','#','#','#','#',' ','#','#','.','#',' ',' ',' ',' ',' '],
                    ['#','#','#','#','#','#','.','#','#',' ','#','#','#','#','#','#','#','#',' ','#','#','.','#','#','#','#','#','#'],
                    ['#','.','.','.','.','.','.','.','.','.','.','.','.','#','#','.','.','.','.','.','.','.','.','.','.','.','.','#'],
                    ['#','.','#','#','#','#','.','#','#','#','#','#','.','#','#','.','#','#','#','#','#','.','#','#','#','#','.','#'],
                    ['#','.','#','#','#','#','.','#','#','#','#','#','.','#','#','.','#','#','#','#','#','.','#','#','#','#','.','#'],
                    ['#','o','.','.','#','#','.','.','.','.','.','.','.',' ',' ','.','.','.','.','.','.','.','#','#','.','.','o','#'],
                    ['#','#','#','.','#','#','.','#','#','.','#','#','#','#','#','#','#','#','.','#','#','.','#','#','.','#','#','#'],
                    ['#','#','#','.','#','#','.','#','#','.','#','#','#','#','#','#','#','#','.','#','#','.','#','#','.','#','#','#'],
                    ['#','.','.','.','.','.','.','#','#','.','.','.','.','#','#','.','.','.','.','#','#','.','.','.','.','.','.','#'],
                    ['#','.','#','#','#','#','#','#','#','#','#','#','.','#','#','.','#','#','#','#','#','#','#','#','#','#','.','#'],
                    ['#','.','#','#','#','#','#','#','#','#','#','#','.','#','#','.','#','#','#','#','#','#','#','#','#','#','.','#'],
                    ['#','.','.','.','.','.','.','.','.','.','.','.','.','.','.','.','.','.','.','.','.','.','.','.','.','.','.','#'],
                    ['#','#','#','#','#','#','#','#','#','#','#','#','#','#','#','#','#','#','#','#','#','#','#','#','#','#','#','#']]

    def restart_ghost_collision(self):
        if self.sprite_frame == 60 and self.end_game == True and self.lives > 0:
            self.end_game = False
            self.harmless_mode = False
            self.harmless_mode_timer = 0
            self.harmless_mode_ghost_blue   = False
            self.harmless_mode_ghost_orange = False
            self.harmless_mode_ghost_pink   = False
            self.harmless_mode_ghost_red    = False
            self.pac_man_pos            = [self.scale * 13.1, self.scale * 22.6]
            self.pac_man_direction      = [self.scale/16, 0]
            self.pac_man_next_direction = [self.scale/16, 0]
            self.ghost_blue_pos   = [self.scale * 12, self.scale * 13]
            self.ghost_orange_pos = [self.scale * 12, self.scale * 14.5]
            self.ghost_pink_pos   = [self.scale * 14, self.scale * 13]
            self.ghost_red_pos    = [self.scale * 14, self.scale * 14.5]
            self.distance_ghost_blue_to_pac_man   = self.distance_ghost_to_pac_man(self.ghost_blue_pos)
            self.distance_ghost_orange_to_pac_man = self.distance_ghost_to_pac_man(self.ghost_orange_pos)
            self.distance_ghost_pink_to_pac_man   = self.distance_ghost_to_pac_man(self.ghost_pink_pos)
            self.distance_ghost_red_to_pac_man    = self.distance_ghost_to_pac_man(self.ghost_red_pos)
            self.sprite_speed = 2
            self.end_game = False

    def colect_all_dots(self):
        count = 0
        for y in range(len(self.map)):
            for x in range(len(self.map[0])):
                if self.map[y][x] == '.' or self.map[y][x] == 'o':
                    count += 1
        if count == 0:
            self.end_game = False
            self.harmless_mode = False
            self.harmless_mode_timer = 0
            self.harmless_mode_ghost_blue   = False
            self.harmless_mode_ghost_orange = False
            self.harmless_mode_ghost_pink   = False
            self.harmless_mode_ghost_red    = False
            self.pac_man_pos            = [self.scale * 13.1, self.scale * 22.6]
            self.pac_man_direction      = [self.scale/16, 0]
            self.pac_man_next_direction = [self.scale/16, 0]
            self.ghost_blue_pos   = [self.scale * 12, self.scale * 13]
            self.ghost_orange_pos = [self.scale * 12, self.scale * 14.5]
            self.ghost_pink_pos   = [self.scale * 14, self.scale * 13]
            self.ghost_red_pos    = [self.scale * 14, self.scale * 14.5]
            self.distance_ghost_blue_to_pac_man   = self.distance_ghost_to_pac_man(self.ghost_blue_pos)
            self.distance_ghost_orange_to_pac_man = self.distance_ghost_to_pac_man(self.ghost_orange_pos)
            self.distance_ghost_pink_to_pac_man   = self.distance_ghost_to_pac_man(self.ghost_pink_pos)
            self.distance_ghost_red_to_pac_man    = self.distance_ghost_to_pac_man(self.ghost_red_pos)
            self.sprite_speed = 2
            
        if not any('.' in row or 'o' in row for row in self.map):
            # terminou a fase
            self.aumentar_dificuldade()
            if self.level == 2:
                self.map = self.map2
                tela_transicao(self.level)
            elif self.level == 3:
                self.map = self.map3
                tela_transicao_fase3()
            else: 
                    ret = tela_vitoria(self.score)  # mostra tela de vitória + créditos
                    if ret == 'menu':
                    # sinal para o loop principal voltar ao menu
                        self.back_to_menu = True

    def scoreboard(self):

        max_vidas = 5

        # Posição inicial (canto superior direito)
        x_base = len(self.map[0]) * self.scale + self.scale
        y_base = self.scale

        # Carregar a imagem do coração
        coracao_img = pg.image.load('img/coracao.png')  # coloque seu coração
        coracao_img = pg.transform.scale(coracao_img, (self.scale * 2, self.scale * 2))

        # Desenha um coração para cada vida restante
        for i in range(self.lives):
            y = y_base + (coracao_img.get_height() + 5) * i  # 5px de espaço entre corações
            self.window.blit(coracao_img, (x_base, y))

        coracao_vazio = pg.image.load('img/coracao_vazio.png')  # imagem cinza/transparente
        coracao_vazio = pg.transform.scale(coracao_vazio, (self.scale * 2, self.scale * 2))
        for i in range(self.lives, max_vidas):
            y = y_base + (coracao_vazio.get_height() + 5) * i
            self.window.blit(coracao_vazio, (x_base, y))

        # Calcula posição da pontuação (logo abaixo dos corações)
        altura_total = (coracao_img.get_height() + 5) * max_vidas
        y_pontuacao = y_base + altura_total + 10  # 10px de espaço abaixo dos corações

        # Renderiza e desenha a pontuação
        texto_pontuacao = self.font.render(f"Score: {self.score}", True, (255, 255, 255))
        self.window.blit(texto_pontuacao, (x_base, y_pontuacao))

        # Fonte menor para instruções
        instrucoes_font = pg.font.SysFont("Courier New", int(self.scale * 0.6), bold=True)

        texto_instrucao_esc = instrucoes_font.render("ESC: Sair do jogo", True, (255, 255, 255))
        texto_instrucao_r = instrucoes_font.render("R: Voltar ao inicio", True, (255, 255, 255))
        texto_instrucao_pause = instrucoes_font.render("P: Pausa o jogo", True, (255, 255, 255))
        texto_instrucao_ajuda = instrucoes_font.render("H: Tela de ajuda", True, (255, 255, 255))

        # Posição no canto inferior (direito)
        margem = 10
        y_instrucao_r = self.window.get_height() - texto_instrucao_r.get_height() - margem
        y_instrucao_esc = y_instrucao_r - texto_instrucao_esc.get_height() - 5
        y_instrucao_pause = y_instrucao_esc - texto_instrucao_pause.get_height() - 5
        y_instrucao_ajuda = y_instrucao_pause - texto_instrucao_ajuda.get_height() - 5
        x_pos = self.window.get_width() - max(texto_instrucao_r.get_width(), texto_instrucao_esc.get_width(), texto_instrucao_pause.get_width(), texto_instrucao_ajuda.get_width()) - margem

        self.window.blit(texto_instrucao_esc, (x_pos, y_instrucao_esc))
        self.window.blit(texto_instrucao_r, (x_pos, y_instrucao_r))
        self.window.blit(texto_instrucao_pause, (x_pos, y_instrucao_pause))
        self.window.blit(texto_instrucao_ajuda, (x_pos, y_instrucao_ajuda))

# ajuste fino do analógico
DEADZONE = 0.30

while True:  # Loop principal (menu -> jogo -> menu)
    selecao = tela_inicial()
    jogo = PacMan(26, selecao)
    paused = False

    # --- Inicializar joystick ---
    pg.joystick.init()
    joystick = None
    if pg.joystick.get_count() > 0:
        joystick = pg.joystick.Joystick(0)
        joystick.init()
        print('HATs:', joystick.get_numhats(), 'Axes:', joystick.get_numaxes(), 'Buttons:', joystick.get_numbuttons())
        print("Joystick conectado:", joystick.get_name())
    else:
        print("Nenhum joystick encontrado")

    sair_para_menu = False
    clock = pg.time.Clock()

    while True:  # Loop da partida
        # ====== EVENTOS ======
        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()
                quit()

            # --- Teclado ---
            if event.type == pg.KEYDOWN:
                tecla = pg.key.name(event.key)
                if tecla == 'escape':
                    pg.quit()
                    quit()
                elif tecla == 'r':
                    sair_para_menu = True
                elif event.key == pg.K_h:  # tecla H abre ajuda
                    tela_ajuda()
                else:
                    jogo.move(tecla)  # aceita 'w','a','s','d' e 'up','down','left','right'
                if event.type == pg.KEYDOWN:
                    if event.key == pg.K_p:  # Tecla P para pausar
                        paused = not paused

            # --- Joystick: D-Pad (HAT) ---
            if event.type == pg.JOYHATMOTION and joystick is not None:
                hat_x, hat_y = event.value  # tuple (x, y)
                # eixo X do HAT
                if hat_x == -1:
                    jogo.move('left')
                elif hat_x == 1:
                    jogo.move('right')
                # eixo Y do HAT (OBS: up = +1, down = -1)
                if hat_y == 1:
                    jogo.move('up')
                elif hat_y == -1:
                    jogo.move('down')

            # --- Joystick: Analógico (opcional) ---
            if event.type == pg.JOYAXISMOTION and joystick is not None:
                if event.axis == 0:  # X
                    if event.value < -DEADZONE:
                        jogo.move('left')
                    elif event.value > DEADZONE:
                        jogo.move('right')
                elif event.axis == 1:  # Y
                    if event.value < -DEADZONE:
                        jogo.move('up')
                    elif event.value > DEADZONE:
                        jogo.move('down')

            # --- Joystick: Botões ---
            if event.type == pg.JOYBUTTONDOWN and joystick is not None:
                if event.button == 0:   # Botão A -> Enter
                    pg.event.post(pg.event.Event(pg.KEYDOWN, key=pg.K_RETURN))
                    pg.event.post(pg.event.Event(pg.KEYUP,   key=pg.K_RETURN))
                elif event.button == 1: # Botão B -> sair para menu
                    sair_para_menu = True
                elif event.button == 2: # Botão X -> ajuda (tecla 'h')
                    tela_ajuda()
                elif event.button == 3: # Botão Y -> pausar (tecla 'p')
                    paused = not paused
                elif event.button == 6: # Botão Select -> sair do jogo (ESC)
                    pg.quit()
                    quit()

        # ====== POLL POR FRAME (garante que o D-Pad funcione mesmo sem evento contínuo) ======
        if joystick is not None:
            # 1) HAT (D-Pad) tem prioridade
            if joystick.get_numhats() > 0:
                hat_x, hat_y = joystick.get_hat(0)
                if hat_x != 0 or hat_y != 0:
                    if hat_x == -1: jogo.move('left')
                    elif hat_x == 1: jogo.move('right')
                    if hat_y == 1: jogo.move('up')
                    elif hat_y == -1: jogo.move('down')
            # 2) Analógicos (se existirem)
            if joystick.get_numaxes() >= 2:
                x_axis = joystick.get_axis(0)
                y_axis = joystick.get_axis(1)
                if abs(x_axis) > DEADZONE:
                    jogo.move('left' if x_axis < 0 else 'right')
                if abs(y_axis) > DEADZONE:
                    jogo.move('up' if y_axis < 0 else 'down')

        # ====== ATUALIZA / DESENHA SEU JOGO AQUI ======
        # Exemplo (ajuste para o que você já usa):
        # jogo.player()        # lógica do pac-man/ghosts/timers
        # jogo.board()         # desenha o mapa/itens
        # pg.display.flip()

        # sair da partida
        if getattr(jogo, "back_to_menu", False) or sair_para_menu:
            break

        clock.tick(60)

        if paused:
            font = pg.font.SysFont("Courier New", 50, bold=True)
            pause_text = font.render("PAUSADO", True, (255, 255, 0))
            jogo.window.blit(pause_text, pause_text.get_rect(center=(jogo.window.get_width()//2, jogo.window.get_height()//2)))

            instr = pg.font.SysFont("Courier New", 25, bold=True).render("Pressione P para continuar", True, (200, 200, 200))
            jogo.window.blit(instr, instr.get_rect(center=(jogo.window.get_width()//2, jogo.window.get_height()//2 + 60)))

            pg.display.update()
            continue  # Pula o resto do loop enquanto pausado

        # Game logic
        jogo.clock.tick(60)
        jogo.clear_window()
        jogo.board()
        jogo.animation_step()
        jogo.player()
        jogo.ghost()
        jogo.collect_dots()
        jogo.ghost_manager()
        jogo.ghost_and_pacman_collider()
        jogo.scoreboard()
        jogo.restart_ghost_collision()
        jogo.colect_all_dots()

        if jogo.lives <= 0:
            tela_game_over(jogo.score)   # mostra tela
            jogo.restart() 

        pg.display.update()