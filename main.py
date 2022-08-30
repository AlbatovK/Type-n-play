from game_cycle.game_cycle import GameCycle
from util.api_service import init_api_service

if __name__ == "__main__":
    init_api_service('https://kotserver.herokuapp.com/')
    game_cycle = GameCycle()
    game_cycle.start_game_cycle()
