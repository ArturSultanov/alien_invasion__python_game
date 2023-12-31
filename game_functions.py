import sys
from time import sleep
import pygame
from bullet import Bullet
from alien import Alien


def check_keydown_events(event, ai_settings, screen, ship, bullets):
    if event.key == pygame.K_RIGHT:
        ship.moving_right = True
    elif event.key == pygame.K_LEFT:
        ship.moving_left = True
    elif event.key == pygame.K_SPACE:
        new_bullet = Bullet(ai_settings, screen, ship)
        bullets.add(new_bullet)
    elif event.key == pygame.K_q:
        sys.exit()


def check_play_button(stats, play_button, mouse_x, mouse_y):
    """Starts a new game when the Play button is pressed."""
    if play_button.rect.collidepoint(mouse_x, mouse_y):
        stats.game_active = True


def check_keyup_events(event, ship):
    if event.key == pygame.K_RIGHT:
        ship.moving_right = False
    elif event.key == pygame.K_LEFT:
        ship.moving_left = False


def check_events(ai_settings, screen,stats, play_button, ship, bullets):
    """Handles keystrokes and mouse events."""
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()

        elif event.type == pygame.KEYDOWN:
            check_keydown_events(event, ai_settings, screen, ship, bullets)
            # if event.key == pygame.K_RIGHT:
            #     ship.moving_right = True
            # if event.key == pygame.K_LEFT:
            #     ship.moving_left = True

        elif event.type == pygame.KEYUP:
            check_keyup_events(event, ship)
            # if event.key == pygame.K_RIGHT:
            #     ship.moving_right = False
            # if event.key == pygame.K_LEFT:
            #     ship.moving_left = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            mouse_x, mouse_y = pygame.mouse.get_pos()
            check_play_button(stats, play_button, mouse_x, mouse_y)


def update_screen(ai_settings, screen, stats, ship, aliens, bullets, play_button):
    """Updates the images on the screen and displays a new screen."""
    # The screen is redrawn every time the loop passes.
    screen.fill(ai_settings.bg_color)
    ship.blitme()
    aliens.draw(screen)
    if not stats.game_active:
        play_button.draw_button()
    for bullet in bullets:
        bullet.draw_bullet()
    pygame.display.flip()


def get_number_aliens_x(ai_settings, alien_width):
    """Calculates the number of aliens in a row."""
    available_space_x = ai_settings.screen_width - 2 * alien_width
    number_alien_x = int(available_space_x / (2 * alien_width))
    return number_alien_x


def get_number_row(ai_settings, ship_height, alien_height):
    """Determines the number of rows that fit on the screen."""
    available_space_y = (ai_settings.screen_height - (3 * alien_height) - ship_height)
    number_row = int(available_space_y / (2 * alien_height))
    return number_row


def create_aline(ai_settings, screen, aliens, alien_number, row_number):
    alien = Alien(ai_settings, screen)
    alien_width = alien.rect.width
    alien.x = alien_width + 2 * alien_number * alien_width
    alien.rect.x = alien.x
    alien.rect.y = alien.rect.height + 2 * alien.rect.height * row_number
    aliens.add(alien)


def create_fleet(ai_settings, screen, ship, aliens):
    """Create aliens fleet"""
    # Creating an alien and calculating the number of aliens in a row.
    # The interval between adjacent aliens is equal to one width of the alien.

    alien = Alien(ai_settings, screen)
    aliens_number_x = get_number_aliens_x(ai_settings, alien.rect.width)
    aliens_number_row = get_number_row(ai_settings, ship.rect.height,
                                       alien.rect.height)
    for row_number in range(aliens_number_row):
        for alien_number in range(aliens_number_x):
            # Creating an alien and placing it in a row.
            create_aline(ai_settings, screen, aliens, alien_number, row_number)


def check_fleet_edges(ai_settings, aliens):
    """Reacts to the alien reaching the edge of the screen."""
    for alien in aliens.sprites():
        if alien.check_edges():
            change_fleet_direction(ai_settings, aliens)
            break


def change_fleet_direction(ai_settings, aliens):
    """Drops the entire fleet and changes the direction of the fleet."""
    for alien in aliens.sprites():
        alien.rect.y += ai_settings.fleet_drop_speed
    ai_settings.fleet_direction *= -1


def check_bullet_alien_collisions(ai_settings, screen, ship, aliens, bullets):
    # Check if bullets have collisions with aliens
    # If they have - delete bullet and alien
    collisions = pygame.sprite.groupcollide(bullets, aliens, True, True)


def update_bullets(ai_settings, screen, ship, bullets, aliens):
    # Update bullets position and remove bullets
    for bullet in bullets.copy():
        bullet.update()
        if bullet.rect.bottom <= 0:
            bullets.remove(bullet)
        # print(len(bullets))

    check_bullet_alien_collisions(ai_settings, screen, ship, aliens, bullets)

    if len(aliens) == 0:
        bullets.empty()
        create_fleet(ai_settings, screen, ship, aliens)


def update_aliens(ai_settings, stats, screen, ship, aliens, bullets):
    """Checks if the fleet has reached the edge of the screen,
       then updates the positions of all aliens in the fleet."""
    check_fleet_edges(ai_settings, aliens)
    aliens.update()

    # Check alien-ship collision
    if pygame.sprite.spritecollideany(ship, aliens):
        ship_hit(ai_settings, stats, screen, ship, aliens, bullets)
        # print("Ship hit!!!")


def ship_hit(ai_settings, stats, screen, ship, aliens, bullets):
    """Detect alien and ship collision"""
    if stats.ships_lives_left > 0:
        # Reduce ship lives by 1 if collision is detected
        stats.ships_lives_left -= 1

        # Clear lists of aliens and bullets
        aliens.empty()
        bullets.empty()

        # Create new fleet and place ship at the center point
        create_fleet(ai_settings, screen, ship, aliens)
        ship.center_ship()

        # Pause
        sleep(0.5)
    else:
        stats.game_active = False


def check_aliens_bottom(ai_settings, stats, screen, ship, aliens, bullets):
    """Check if there is alien at the bottom of the screen"""
    screen_rect = screen.get_rect()
    for alien in aliens.sprites():
        if alien.rect.bottom >= screen_rect.bottom:
            ship_hit(ai_settings, stats, screen, ship, aliens, bullets)
            break
