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
    screen.fill((0, 0, 0))

    game.draw(screen)
    game.draw_bob_dices(screen)

    print(f"Drawing {len(labels)} labels")

    for label in labels:
        print(f"Drawing label: {label.text}")
        label.draw(screen)

    for label in player_formation_labels:
        label.draw(screen)

    for label in bob_formation_labels:
        label.draw(screen)

    pygame.display.update()


def player_turn(game, scoresheet_player, scoresheet_bob):
    """Funcție pentru runda unui jucător."""
    available_rolls = 3
    label = Label("Player's turn", (315, 255), FONT, (255, 255, 255))
    rollsLabel = Label(
        f"Remaining Rolls: {available_rolls}", (325, 150), FONT, (255, 255, 255))
    update_screen(game, [label, rollsLabel], scoresheet_player.get_labels(),
                  bob_formation_labels=scoresheet_bob.get_labels())
    print(f"Initial remaining rolls: {available_rolls}")
    while available_rolls > 0:
        update_screen(game, [label, rollsLabel], scoresheet_player.get_labels(),
                      bob_formation_labels=scoresheet_bob.get_labels())

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if game.roll_button.is_clicked(event.pos):
                    game.roll_dices()
                    available_rolls -= 1
                    print(
                        f"Roll button clicked, remaining rolls: {available_rolls}")
                    rollsLabel = Label(
                        f"Remaining Rolls: {available_rolls}", (265, 400), FONT, (0, 0, 0))
                else:
                    for dice in game.dices:
                        if dice.rect.collidepoint(event.pos):
                            if dice.isKept:
                                dice.unkeep()
                            else:
                                dice.keep()
                            break

    selected_formation = choose_formation(game, scoresheet_player)
    print("End of turn")
    return selected_formation


def bob_turn(game, scoresheet_player, scoresheet_bob):
    """Funcția care gestionează runda lui Bob."""
    game.roll_bob_dices()
    update_screen(game, player_formation_labels=scoresheet_player.get_labels(
    ), bob_formation_labels=scoresheet_bob.get_labels())

    eligible_formations = []

    for formation in formations:
        if not scoresheet_bob.is_formation_used(formation):
            score = formations_check(game.bob_dices, formation)
            eligible_formations.append((formation, score))

    if eligible_formations:
        chosen_formation, score = random.choice(eligible_formations)
        scoresheet_bob.add_score(chosen_formation, score)
        print(f"Bob has chosen {chosen_formation} with score {score}")
    else:
        print("Bob has no available formations.")


def choose_formation(game, scoresheet):
    """Permite jucătorului să aleagă o formație validă după rulare sau să aleagă o formație cu 0 puncte."""
    eligible_formations = []
    formation_labels = []

    for i, formation in enumerate(formations):
        if not scoresheet.is_formation_used(formation):
            score = formations_check(game.dices, formation)
            color = (0, 255, 0) if score > 0 else (255, 0, 0)
            formation_label = Label(
                f"{i+1}. {formation} - {score}", (675, 200 + i * 25), SMALL_FONT, color)
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
                for formation_label, formation, score in eligible_formations:
                    if formation_label.is_clicked(event.pos):
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
    scoresheet_player = ScoreSheet(600, 150)
    scoresheet_bob = ScoreSheet(150, 150)
    running = True
    round = 0

    while running:
        update_screen(game, [], scoresheet_player.get_labels(),
                      scoresheet_bob.get_labels())

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            game.handle_event(event)

        if round < 9:
            for dice in game.dices:
                dice.unkeep()

            player_turn(game, scoresheet_player, scoresheet_bob)
            for dice in game.dices:
                dice.value = 0
            bob_turn(game, scoresheet_player, scoresheet_bob)

            round += 1
        else:

            player_score = scoresheet_player.get_total_score()
            bob_score = scoresheet_bob.get_total_score()
            winner = "Player" if player_score > bob_score else "Bob" if bob_score > player_score else "No one, it's a tie!"

            game_over_label = Label(
                "Game Over", (SCREEN_WIDTH // 2 - 50, SCREEN_HEIGHT // 2 - 40), FONT, (255, 0, 0))
            winner_label = Label(
                f"Winner: {winner}", (SCREEN_WIDTH // 2 - 50, SCREEN_HEIGHT // 2), FONT, (255, 0, 0))

            update_screen(game, [game_over_label, winner_label],
                          scoresheet_player.get_labels(), scoresheet_bob.get_labels())
            pygame.display.update()

            waiting = True
            while waiting:
                for event in pygame.event.get():
                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_r:
                            waiting = False
                            round = 0
                            scoresheet_player.clear_scores()
                            scoresheet_bob.clear_scores()
                        elif event.key == pygame.K_q:
                            waiting = False
                            running = False
    pygame.quit()


if __name__ == '__main__':
    main()
