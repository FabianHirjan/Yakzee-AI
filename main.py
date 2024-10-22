import random
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


def update_screen(game, labels=[], player_formation_labels=[], bob_formation_labels=[]):
    """Actualizează ecranul cu jocul și etichetele pentru jucător și Bob."""
    screen.fill((0, 0, 0))  # Curățăm ecranul
    game.draw(screen)  # Desenăm zarurile jucătorului
    game.draw_bob_dices(screen)  # Desenăm zarurile lui Bob

    # Desenăm etichetele generale (de ex., indicatoare de rundă)
    for label in labels:
        label.draw(screen)

    # Desenăm etichetele de formație ale jucătorului
    for label in player_formation_labels:
        label.draw(screen)

    # Desenăm etichetele de formație ale lui Bob
    for label in bob_formation_labels:
        label.draw(screen)

    pygame.display.update()  # Actualizăm ecranul


def player_turn(game, scoresheet):
    """Funcție pentru runda unui jucător."""
    available_rolls = 3
    label = Label("Player's turn", (315, 255), FONT, (255, 255, 255))
    rollsLabel = Label(
        f"Rolls left {available_rolls}", (325, 400), FONT, (255, 255, 255))

    while available_rolls > 0:
        update_screen(game, [label, rollsLabel], scoresheet.get_labels())

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if game.roll_button.is_clicked(event.pos):
                    game.roll_dices()
                    available_rolls -= 1
                    rollsLabel = Label(
                        f"Rolls left {available_rolls}", (325, 400), FONT, (255, 255, 255))
                else:
                    for dice in game.dices:
                        if dice.rect.collidepoint(event.pos):
                            if dice.isKept:
                                dice.unkeep()
                            else:
                                dice.keep()
                            break
    selected_formation = choose_formation(game, scoresheet)
    print("End of turn")
    return selected_formation


def bob_turn(game, scoresheet_bob):
    """Funcția care gestionează runda lui Bob."""
    game.roll_bob_dices()  # Rulează zarurile lui Bob
    # Modificarea aici!
    update_screen(game, bob_formation_labels=scoresheet_bob.get_labels())

    eligible_formations = []

    # Determină formațiile disponibile pentru Bob
    for formation in formations:
        if not scoresheet_bob.is_formation_used(formation):
            score = formations_check(game.bob_dices, formation)
            eligible_formations.append((formation, score))

    if eligible_formations:
        # Alege o formație aleatorie din cele disponibile
        chosen_formation, score = random.choice(eligible_formations)
        scoresheet_bob.add_score(chosen_formation, score)
        print(f"Bob has chosen {chosen_formation} with score {score}")
    else:
        print("Bob has no available formations.")


def choose_formation(game, scoresheet):
    """Permite jucătorului să aleagă o formație validă după rulare sau să aleagă o formație cu 0 puncte."""
    eligible_formations = []
    formation_labels = []

    # Afișează toate formațiile, inclusiv cele care nu sunt eligibile (cu 0 puncte)
    for i, formation in enumerate(formations):
        if not scoresheet.is_formation_used(formation):
            score = formations_check(game.dices, formation)
            color = (0, 255, 0) if score > 0 else (255, 0, 0)
            formation_label = Label(
                f"{i+1}. {formation} - {score}", (675, 200 + i * 25), SMALL_FONT, color)

            # Adaugă toate formațiile în lista de selecție, indiferent de punctaj
            eligible_formations.append((formation_label, formation, score))
            formation_labels.append(formation_label)

    selected_formation = None
    while selected_formation is None:
        update_screen(game, [], formation_labels + scoresheet.get_labels())
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                # Permite selectarea oricărei formații
                for formation_label, formation, score in eligible_formations:
                    if formation_label.is_clicked(event.pos):
                        # Dacă formația are scor 0, adaugă formația fără puncte
                        if score == 0:
                            selected_formation = formation
                            scoresheet.add_score(formation, 0)
                        else:
                            selected_formation = formation
                            scoresheet.add_score(formation, score)
                        print(f"Selected formation: {selected_formation}")
                        break

    return selected_formation


def main():
    from scoresheet import ScoreSheet
    game = Game()
    scoresheet_player = ScoreSheet(600, 150)  # Tabela de scoruri a jucătorului
    scoresheet_bob = ScoreSheet(150, 150)  # Tabela de scoruri a lui Bob
    running = True
    round = 0

    while running:
        update_screen(game, [], scoresheet_player.get_labels(),
                      scoresheet_bob.get_labels())

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            game.handle_event(event)

        if round < 13:
            for dice in game.dices:
                dice.unkeep()

            # Tura jucătorului
            # Transmitem scoresheet_player corect
            player_turn(game, scoresheet_player)

            # Tura lui Bob
            bob_turn(game, scoresheet_bob)

            round += 1
        else:
            print("Game Over")
            print("Total score (Player):", scoresheet_player.get_total_score())
            print("Total score (Bob):", scoresheet_bob.get_total_score())

    pygame.quit()


if __name__ == '__main__':
    main()
