import pygame
import random
from os import path
import sqlite3

from sqlite3 import Error


def main():

            # Ορισμός μεγέθους παραθύρου
            WIDTH = 700
            HEIGHT = 550
            FPS = 60

            # Ορισμός χρωμάτων
            WHITE = (255, 255, 255)
            BLACK = (0, 0, 0)
            RED = (255, 0, 0)
            GREEN = (0, 255, 0)
            BLUE = (0, 0, 255)
            YELLOW = (255, 255, 0)
            
        #**********************Δημιουργία πίνακα για την βάση sqlite************************
            create_users_table="""
            CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            score INTEGER
            ); 

            """
            create_users="""
            INSERT INTO users(score)
            values
            (?)
            ;
            """

                    
        
        #**********************#
        


            # Αρχικοποίηση pygame και δημιουργία παραθύρου

            pygame.init()
            screen = pygame.display.set_mode((WIDTH, HEIGHT))
            pygame.display.set_caption("MyGame")

            # Εισαγωγή ήχου
            pygame.mixer.init()
            fire_sound = pygame.mixer.Sound("sound/shot.ogg")

            # Ορισμός διαδρομής φόρτωσης εικόνας
            img_dir = path.join(path.dirname(__file__), 'img')

            # Αρχικοποίηση μεταβλητής
            clock = pygame.time.Clock()


            # Φόρτωση των game graphics
            background = pygame.image.load(path.join(img_dir, "background.jpg")).convert()
            background_rect = background.get_rect()
            background=pygame.transform.scale(background,[700,550])
            player_img = pygame.image.load(path.join(img_dir, "spaceship.png")).convert()
            comet_img = pygame.image.load(path.join(img_dir, "comet.png")).convert()
            bullet_img = pygame.image.load(path.join(img_dir, "rock.png")).convert()
            star_img = pygame.image.load(path.join(img_dir, "star.png"))

            # Ορισμός γραμματοσειράς
            font_score=pygame.font.match_font('arial')

            #Ορισμός παραθύρου score
            def draw_score(surf, text, size, x,y):
                font = pygame.font.Font(font_score, size)
                text_surface = font.render(text, True, GREEN)
                #Το score εμφανίζεται με πράσινο χρώμα στην μέση στον άξονα των x και πάνω
                text_rect=text_surface.get_rect()
                text_rect.midtop = (x,y)
                surf.blit(text_surface,text_rect)


            #αποθήκευση του  score  σε  txt  αρχείο    
            def save_highest_score(score):
                        record = 0

                        try:
                            with open("score.txt", "r") as score_file:
                               record_line = score_file.read()
                            if record_line:
                                record = int(record_line)
                                record1 = record
                                record2 = str(record1)
                                draw_score(screen,'High score Score: ' + str(record1), 30, WIDTH/2, 50)
                            
                        except FileNotFoundError:
                            print("There was no champion")

                        if score > record:
                            print("You are the new champion!")
                            with open("score.txt", "w") as score_file:
                              score_file.write(str(score)) 
                              
                        #**********************#

        
        #******************** DATABASE******#
        #Εγκαθιδρύει την σύνδεση με μία βάση δεδομένων
            def create_connection(path):
                connection=None
                try:
                    connection=sqlite3.connect(path)
                    print("Connection to Database Succesful")
                except Error as e:
                   print(f"The error '{e}' occured")
                return connection

         #Συνάρτηση εκτέλεσης ερωτημάτων 
            def execute_query(connection,query):
                #Κανάλι επικοινωνίας cursor
                cursor=connection.cursor()
                try:
                   cursor.execute(query)
                   connection.commit()
                   print(f"Query '{query}' executed succesfully")
                except Error as e:
                   print(f"The error '{e}' occured")

            #Συνάρτηση  ανάγνωσης στηλών
            def execute_query_read(connection,query):
                cursor=connection.cursor()
                try:
                    cursor.execute(query)
                    result=cursor.fetchall()
                    column_names=[description[0] for description in cursor.description]
                    return column_names,result
                except Error as e:
                    print(f"The error '{e}' occured")
            
        
        
        #**********FINISH DATABASE****************#                  


            # Κλάση του player
            class Player(pygame.sprite.Sprite):
                def __init__(self):
                    pygame.sprite.Sprite.__init__(self)
                    self.image = pygame.transform.scale(player_img, (80, 90))
                    self.image.set_colorkey(BLACK)
                    self.rect = self.image.get_rect()
                    # Δημιουργώ κύκλο ώστε το collision να είναι πιο πετυχημένο οπτικά
                    self.radius= 38 
                    self.rect.centerx = WIDTH / 2
                    self.rect.bottom = HEIGHT - 10  
                    self.speedx = 0

                def update(self):
                    self.speedx = 0
                    keystate = pygame.key.get_pressed()
                    if keystate[pygame.K_LEFT]:
                        self.speedx = -8
                    if keystate[pygame.K_RIGHT]:
                        self.speedx = 8
                    self.rect.x += self.speedx
                    if self.rect.right > WIDTH:
                        self.rect.right = WIDTH
                    if self.rect.left < 0:
                        self.rect.left = 0

                def shoot(self):
                    bullet = Bullet(self.rect.centerx, self.rect.top)
                    all_sprites.add(bullet)
                    bullets.add(bullet)

                
            # Κλάση των bullet του παίκτη
            class Bullet(pygame.sprite.Sprite):
                def __init__(self, x, y):
                    pygame.sprite.Sprite.__init__(self)
                    self.image = bullet_img
                    self.image.set_colorkey(BLACK)
                    self.rect = self.image.get_rect()
                    # Δημιουργώ κύκλο ώστε το collision να είναι πιο πετυχημένο οπτικά
                    self.radius= int(self.rect.width  /2)
                    self.rect.bottom = y
                    self.rect.centerx = x
                    self.speedy = -10

                def update(self):
                    self.rect.y += self.speedy
                    # kill if it moves off the top of the screen
                    if self.rect.bottom < 0:
                        self.kill()
                        
            # Κλάση του comet            
            class Comet(pygame.sprite.Sprite):
                def __init__(self):
                    pygame.sprite.Sprite.__init__(self)
                    self.image = pygame.transform.scale(comet_img, (70, 70))
                    self.image.set_colorkey(BLACK)
                    self.rect = self.image.get_rect()
                    # Δημιουργώ κύκλο ώστε το collision να είναι πιο πετυχημένο οπτικά
                    self.radius= int(self.rect.width *  .5/2)
                    self.rect.x = random.randrange(WIDTH - self.rect.width)
                    self.rect.y = random.randrange(-100, -40)
                    self.speedy = random.randrange(1, 8)
                    self.speedx = random.randrange(-3, 3)

                def update(self):
                    self.rect.x += self.speedx
                    self.rect.y += self.speedy
                    if self.rect.top > HEIGHT + 10 or self.rect.left < -25 or self.rect.right > WIDTH + 20:
                        self.rect.x = random.randrange(WIDTH - self.rect.width)
                        self.rect.y = random.randrange(-100, -40)
                        self.speedy = random.randrange(1, 5)
                                        
                        if score >  80:
                                self.speedy = random.randrange(3, 8 )  
                        if score >  120:
                                self.speedy = 15     
                        
            # Κλάση των star
            class Star(pygame.sprite.Sprite):
                def __init__(self):
                    pygame.sprite.Sprite.__init__(self)
                    self.image = pygame.transform.scale(star_img, (60, 50))
                    self.image.set_colorkey(BLACK)
                    self.rect = self.image.get_rect()
                    # Δημιουργώ κύκλο ώστε το collision να είναι πιο πετυχημένο οπτικά
                    self.radius= int(self.rect.width *  .5/2)
                    self.rect.x = random.randrange(WIDTH - self.rect.width)
                    self.rect.y = random.randrange(-100, -40)
                    self.speedy = random.randrange(1, 8)
                    self.speedx = random.randrange(-3, 3)

                def update(self):
                    self.rect.x += self.speedx
                    self.rect.y += self.speedy
                    if self.rect.top > HEIGHT + 10 or self.rect.left < -25 or self.rect.right > WIDTH + 20:
                        self.rect.x = random.randrange(WIDTH - self.rect.width)
                        self.rect.y = random.randrange(-100, -40)
                        self.speedy = random.randrange(1, 8)
                        
                        


            all_sprites = pygame.sprite.Group() 
            bullets = pygame.sprite.Group()
            comets = pygame.sprite.Group() 
            stars = pygame.sprite.Group() 

            # Δημιουργία του 'player'
            player = Player()
            all_sprites.add(player)

            # Επαναλαμβανόμενη δημιουργία comet  
            for i in range(8):
                m = Comet()
                all_sprites.add(m)
                comets.add(m)

            # Επαναλαμβανόμενη δημιουργία  star    
            for i in range(1):
                n=Star()
                all_sprites.add(n)
                stars.add(n)  
                
            # Ορισμός του score
            score=0
            life = 3
            gethealth=0 
            newscore=0

            # Game loop
            running = True
            while running:
                # keep loop running at the right speed
                clock.tick(FPS)
                # Process input (events)
                for event in pygame.event.get():
                    # check for closing window
                    if event.type == pygame.QUIT:
                        running = False
                    elif event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_SPACE:
                            player.shoot()
                            fire_sound.play()
                

                # Update
                all_sprites.update()
                # Check αν η bullet χτυπάει το comet
                hits_comet = pygame.sprite.groupcollide(comets,bullets, True, True,pygame.sprite.collide_circle)
                # Έλεγχος αν το bullet χτυπάει το comet, το score αυξάνεται κατά 2
                if hits_comet:
                    score=score+2
                # Check αν η bullet χτυπάει το star
                hits_star = pygame.sprite.groupcollide(stars,bullets, True, True,pygame.sprite.collide_circle)
                # Έλεγχος αν το bullet χτυπάει το star, το life αυξάνεται κατά 1 για κάθε 6 star,
                for hit in hits_star:
                    gethealth += 1
                    if (gethealth>=6):
                        life = life+1
                        gethealth=0
                    else:
                        gethealth = gethealth   
                            
                            




                # Για να εμφανίζονται πάλι commets και stars, αφού τα χτυπήσουμε
                for hit in hits_comet:
                    m = Comet()
                    all_sprites.add(m)
                    comets.add(m)

                for hit in hits_star:
                    n=Star()
                    all_sprites.add(n)
                    stars.add(n)



                # Check αν το comet χτυπάει τον player
                # Η λίστα hits αποθηκεύει τους comets που χτυπάνε τον player
                hits = pygame.sprite.spritecollide(player,comets, True, pygame.sprite.collide_circle)
                # Έλεγχος αν το comet χτυπάει τον player, το  life μειώνεται κατά 1
                if hits:
                    life=life-1

                # Ελέγχει αν το life είναι μικρότερο από το 0, ο παίκτης χάνει και τελειώνει το παιχνίδι
                if  (life<=0):
                    running = False
                    #Δημιουργία βάσης με τα σκορ που πετυχαίνει ο παίκτης
                    f=open('myscore.dat', '+a')
                    data=score 
                    f=open('myscore.dat', '+a')
                    f.write(str(data) + '\n')
                    f.close()
                    
                # Draw / render
                screen.fill(BLACK)
                screen.blit(background, background_rect)
                all_sprites.draw(screen)     
                save_highest_score(score)  
                draw_score(screen, 'Score: ' + str(score), 40, WIDTH/2, 10)
                draw_score(screen, 'Life: '+str(life), 30, WIDTH/6, 10)
                draw_score(screen, 'gethealth: '+str(gethealth), 30, WIDTH-80 , 10)
               
                
 #********************Aποθήκευση στην βάση mydatabase.sqlite**************************#
   
                if(life<=0):
                    conn=create_connection("mydatabase.sqlite")   
                    execute_query(conn,create_users_table)  
                    execute_query(conn,create_users)
                    newscore=score
                    #Αποθηκεύουμε το τελικό  score
                    update_users=f'UPDATE users SET score="{newscore}" where id="{1}";'
                    execute_query(conn,update_users) 


        
#**********************************************#

            # *after* drawing everything, flip the display
                pygame.display.flip()
                

def main_menu():
    pygame.init()
    pygame.mixer.init()
    WIDTH = 700
    HEIGHT = 550
    title_font = pygame.font.SysFont("comicsans", 20)
   
      
      
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("MyGame")

      
    BLACK = (0, 0, 0)
        
    run = True
    
    while run:

        screen.fill(BLACK)
        title_label = title_font.render("Πίεσε το πλήκτρο από το  mouse για να ξεκινήσεις", 1, (0,255,255))
        screen.blit(title_label, (WIDTH/2 - title_label.get_width()/2, 250))
        
        pygame.display.update()
        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                main()
                
    pygame.quit()
   
main_menu()              
            