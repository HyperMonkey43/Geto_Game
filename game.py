import pygame
import button


# PROBLEMA E VUV SAMIQ RUN BUTTON PROBAI RUN CODE

class Game:
    resolution = pygame.Vector2(1200, 680) # (1800, 950)
    clock = pygame.time.Clock()
    screen = pygame.display.set_mode(resolution)
    startMenu = False
    PlayBtn = None
    ControlsBtn = None
    QuitBtn = None

    def __init__(self):
        pygame.init()  
        pygame.display.set_caption("game")

        self.PlayBtn = button.Button(image=None, pos=(self.resolution.x / 2, 400), text_input="Play", font=self.get_font(75), base_color="#da5e53", hover_color="#683b4c")           
        self.ControlsBtn = button.Button(image=None, pos=(self.resolution.x / 2, 500), text_input="Controls", font=self.get_font(75), base_color="#da5e53", hover_color="#683b4c")       
        self.QuitBtn = button.Button(image=None, pos=(self.resolution.x / 2, 600), text_input="Quit", font=self.get_font(75), base_color="#da5e53", hover_color="#683b4c")

    def get_font(self, size):
        return pygame.font.Font("Font/retro_computer_personal_use.ttf", size)        
        
    def getEvent(self): # This is how you get keyboard input
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()

    def startMenu(self):

        MenuMousePosition = pygame.mouse.get_pos()
        MenuText = self.get_font(100).render("main menu", True, "#ffffff")
        MenuRect = MenuText.get_rect(center = (self.resolution.x / 2, 300))

                
        self.screen.blit(MenuText, MenuRect)

        for button in [self.PlayBtn, self.ControlsBtn, self.QuitBtn]:
            button.changeColor(MenuMousePosition)
            button.update(self.screen)



        self.startMenu = 0 # AUTOMATICALY STARTS



        for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if self.PlayBtn.checkForInput(MenuMousePosition):
                        self.startMenu = 0
                        pygame.time.delay(200)
                    if self.ControlsBtn.checkForInput(MenuMousePosition):
                        pass
                    if self.QuitBtn.checkForInput(MenuMousePosition):
                        pygame.quit()
                        exit()

        pygame.display.update()         

    def offloadDeadEnemies(self, enemyList):
        for i in enemyList:
            if i.delete:
                enemyList.remove(i) 

    def drawMultiple(self, listOfTextures, offset):
        if len(listOfTextures) > 0:
            for i in listOfTextures:
                self.screen.blit(i.texture, (i.rect.x - offset[0], i.rect.y - offset[1]))   

    def update(self):
        pygame.display.update()
