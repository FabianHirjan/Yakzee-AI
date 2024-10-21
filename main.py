import pygame
from game import Game
from button import Button
from uielement import Label
from dice_logic import formations_check, formations

pygame.init()

# Setarea ferestrei
SCREEN_WIDTH, SCREEN_HEIGHT = 800, 600
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption('Dice Game')

FONT = pygame.font.Font(None, 36)
SMALL_FONT = pygame.font.Font(None, 16)


def update_screen(game, labels=[]):
    """Actualizează ecranul cu jocul și orice etichete adiționale."""
    screen.fill((0, 0, 0))  # Curăță ecranul
    game.draw(screen)  # Desenează jocul
    for label in labels:
        label.draw(screen)  # Desenează fiecare etichetă
    pygame.display.update()  # Actualizează ecranul


def player_turn(game):
    """Funcție pentru runda unui jucător."""
    available_rolls = 3
    label = Label("Player's turn", (315, 255), FONT, (0, 0, 0))
    rollsLabel = Label(
        f"Rolls left {available_rolls}", (325, 400), FONT, (0, 0, 0))

    while available_rolls > 0:
        update_screen(game, [label, rollsLabel])

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.MOUSEBUTTONDOWN and game.roll_button.is_clicked(event.pos):
                game.roll_dices()
                print([dice.value for dice in game.dices])
                available_rolls -= 1
                rollsLabel = Label(
                    f"Rolls left {available_rolls}", (325, 400), FONT, (0, 0, 0))

    selected_formation = choose_formation(game)
    print("End of turn")
    return selected_formation


def choose_formation(game):
    """Permite jucătorului să aleagă o formație validă după rulare."""
    eligible_formations = []
    formation_labels = []

    for i, formation in enumerate(formations):
        score = formations_check(game.dices, formation)
        color = (0, 255, 0) if score > 0 else (255, 0, 0)
        formation_label = Label(
            f"{i+1}. {formation} - {score}", (675, 200 + i * 25), SMALL_FONT, color)
        if score > 0:
            eligible_formations.append((formation_label, formation))
        formation_labels.append(formation_label)

    selected_formation = None
    while selected_formation is None:
        update_screen(game, formation_labels)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                for formation_label, formation in eligible_formations:
                    if formation_label.is_clicked(event.pos):
                        selected_formation = formation
                        print(f"Selected formation: {selected_formation}")
                        break

    return selected_formation


def main():
    game = Game()
    running = True
    round = 0

    while running:
        update_screen(game)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            game.handle_event(event)

        if round < 13:
            player_turn(game)
            round += 1
        else:
            print("Game Over")

    pygame.quit()


if __name__ == '__main__':
    main()
