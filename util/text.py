from util.asset_manager import play_sound

intro_player_one = "You are alien species whose main\ngoal is to stop anything\n" \
                   "from approaching your home\nplanet. Use your technologies to\npull meteors towards\n" \
                   "unlucky space explorer\nby executing terminal code. You\nhave 120 seconds to\n" \
                   "eliminate intruder."

intro_player_two = "You are lonely space explorer that\nwas caught in meteor storm\nlasting for 120 seconds.\n" \
                   "You must avoid\nhitting rocks by\ntyping commands in order\nfor your ship to shoot them."

outro_player_two_won = "You were able to successfully\ntransfer meteors and\nreach safety\nYou won!"

outro_player_two_lost = "Unfortunately, you were\nhit by meteor and was lost\nin immense darkness of space."

outro_player_one_won = "You managed to hit\nstranger rocket with big rock.\nNow you're not going to\n" \
                       "be annoyed by those dumb ships.\nYou won!"

outro_player_one_lost = "You missed several times\nand secrets of your home world\nare spread all over\n" \
                        "the galaxy. What a shame!"


def validate(text: str):
    play_sound("select.wav")
    return (text.isdigit() and len(text) <= 6) or not text
