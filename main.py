from game.game_cycle import GameCycle
from util.api_service import init_api_service
from util.text import load_words

if __name__ == "__main__":
    init_api_service('https://kotserver-production.up.railway.app/')
    load_words()
    game_cycle = GameCycle()
    game_cycle.start_game_cycle()
