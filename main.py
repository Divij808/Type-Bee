import asyncio
import random
import pygame

pygame.init()

background_colour = (240, 244, 248)
(width, height) = (700, 420)

screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Type Bee - Word Practice")

clock = pygame.time.Clock()
font = pygame.font.Font(None, 28)
title_font = pygame.font.Font(None, 36)
small_font = pygame.font.Font(None, 20)


def load_words():
    words_list = []
    try:
        with open("words.txt", "r", encoding="utf-8") as f:
            for line in f:
                w = line.strip().lower()
                if len(w) >= 3 and w.isalpha():
                    words_list.append(w)
    except Exception:
        pass

    # Fallback word list if words.txt isn't in the folder yet
    if not words_list:
        words_list = [
            "apple",
            "banana",
            "computer",
            "python",
            "spelling",
            "browser",
            "developer",
            "keyboard",
            "network",
            "science",
        ]

    # Remove duplicates so words never repeat randomly
    return list(set(words_list))


words = load_words()

current_word = ""
user_text = ""
state = "MENU"
score = 0
question_count = 0

start_btn = pygame.Rect(225, 220, 250, 50)
rehear_btn = pygame.Rect(50, 310, 150, 40)
submit_btn = pygame.Rect(215, 310, 150, 40)
menu_btn = pygame.Rect(250, 300, 200, 45)
input_box = pygame.Rect(50, 230, 600, 45)


def speak_word(word_to_say):
    """Triggers browser-native speech synthesis safely inside WASM"""
    try:
        from platform import window

        window.eval(
            f"speechSynthesis.speak(new SpeechSynthesisUtterance('{word_to_say}'))"
        )
    except Exception:
        pass


def next_word():
    global current_word, question_count
    current_word = random.choice(words)
    question_count += 1


async def main():
    global user_text, state, score, question_count
    running = True
    while running:
        mouse_pos = pygame.mouse.get_pos()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if state == "MENU":
                    if start_btn.collidepoint(event.pos):
                        score = 0
                        question_count = 0
                        next_word()
                        user_text = ""
                        state = "PLAYING"
                        speak_word(current_word)
                elif state == "PLAYING":
                    if rehear_btn.collidepoint(event.pos):
                        speak_word(current_word)
                    elif submit_btn.collidepoint(event.pos):
                        if user_text.strip().lower() == current_word:
                            score += 1
                            next_word()
                            user_text = ""
                            speak_word(current_word)
                        else:
                            state = "GAME_OVER"
                elif state == "GAME_OVER":
                    if menu_btn.collidepoint(event.pos):
                        state = "MENU"
            elif event.type == pygame.KEYDOWN and state == "PLAYING":
                if event.key == pygame.K_BACKSPACE:
                    user_text = user_text[:-1]
                elif event.key == pygame.K_RETURN:
                    if user_text.strip().lower() == current_word:
                        score += 1
                        next_word()
                        user_text = ""
                        speak_word(current_word)
                    else:
                        state = "GAME_OVER"
                else:
                    user_text += event.unicode

        screen.fill(background_colour)

        if state == "MENU":
            pygame.draw.rect(screen, (30, 58, 138), pygame.Rect(0, 0, width, 90))
            header_surface = title_font.render("Type Bee | Word Practice", True, (255, 255, 255))
            screen.blit(header_surface, (30, 28))

            pygame.draw.rect(screen, (255, 255, 255), pygame.Rect(100, 150, 500, 260), border_radius=8, )
            pygame.draw.rect(screen, (203, 213, 225), pygame.Rect(100, 150, 500, 260), 1, border_radius=8, )

            start_color = ((49, 115, 250) if start_btn.collidepoint(mouse_pos) else (37, 99, 235))
            pygame.draw.rect(screen, start_color, start_btn, border_radius=6)
            start_txt = font.render("Start Game", True, (255, 255, 255))
            screen.blit(start_txt, (
                start_btn.centerx - start_txt.get_width() // 2, start_btn.centery - start_txt.get_height() // 2,), )

        elif state == "PLAYING":
            pygame.draw.rect(screen, (30, 58, 138), pygame.Rect(0, 0, width, 70))
            app_title = title_font.render("Spelling Practice", True, (255, 255, 255))
            screen.blit(app_title, (30, 20))

            pygame.draw.rect(screen, (255, 255, 255), pygame.Rect(30, 90, 640, 300), border_radius=8)

            pygame.draw.rect(screen, (203, 213, 225), pygame.Rect(30, 90, 640, 300), 1, border_radius=8, )

            q_surf = small_font.render(f"Question {question_count}   |   Score: {score}", True, (100, 116, 139), )
            screen.blit(q_surf, (50, 110))

            label_surf = title_font.render(
                "Listen carefully and type the word:", True, (15, 23, 42))
            screen.blit(label_surf, (50, 155))

            pygame.draw.rect(screen, (255, 255, 255), input_box, border_radius=6)
            pygame.draw.rect(screen, (148, 163, 184), input_box, 1, border_radius=6)

            input_surface = font.render(user_text, True, (15, 23, 42))
            screen.blit(input_surface, (input_box.x + 12, input_box.y + 10))

            rehear_color = ((255, 255, 255)
                            if rehear_btn.collidepoint(mouse_pos)
                            else (241, 245, 249))

            pygame.draw.rect(screen, rehear_color, rehear_btn, border_radius=6)
            pygame.draw.rect(screen, (203, 213, 225), rehear_btn, 1, border_radius=6)
            rehear_surface = small_font.render("🔊 Rehear Audio", True, (30, 41, 59))
            screen.blit(rehear_surface, (
                rehear_btn.centerx - rehear_surface.get_width() // 2,
                rehear_btn.centery - rehear_surface.get_height() // 2,), )

            submit_color = ((59, 113, 254) if submit_btn.collidepoint(mouse_pos) else (37, 99, 235))
            pygame.draw.rect(screen, submit_color, submit_btn, border_radius=6)
            submit_surface = small_font.render("Submit Answer", True, (255, 255, 255))
            screen.blit(submit_surface, (submit_btn.centerx - submit_surface.get_width() // 2,
                                         submit_btn.centery - submit_surface.get_height() // 2,), )

        elif state == "GAME_OVER":
            pygame.draw.rect(screen, (30, 58, 138), pygame.Rect(0, 0, width, 90))
            go_header = title_font.render(
                "Game Over - Incorrect Answer!", True, (255, 255, 255))
            screen.blit(go_header, (30, 28))

            pygame.draw.rect(screen, (255, 255, 255), pygame.Rect(100, 130, 500, 250),
                             border_radius=8, )
            pygame.draw.rect(screen, (203, 213, 225),
                             pygame.Rect(100, 130, 500, 250), 1, border_radius=8, )

            final_score_surf = title_font.render(
                f"Final Score: {score}", True, (15, 23, 42))
            screen.blit(final_score_surf, (130, 170))

            correct_word_surf = font.render(f"The correct word was: {current_word}", True, (220, 38, 38))
            screen.blit(correct_word_surf, (130, 220))

            menu_color = ((49, 115, 250) if menu_btn.collidepoint(mouse_pos) else (37, 99, 235))
            pygame.draw.rect(screen, menu_color, menu_btn, border_radius=6)
            menu_txt = font.render("Back to Menu", True, (255, 255, 255))
            screen.blit(menu_txt, (menu_btn.centerx - menu_txt.get_width() // 2,
                                   menu_btn.centery - menu_txt.get_height() // 2,), )

        pygame.display.flip()
        clock.tick(60)
        await asyncio.sleep(0)


if __name__ == "__main__":
    asyncio.run(main())
