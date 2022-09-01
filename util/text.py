from util.asset_manager import play_sound

text_player_one = "You are alien species whose main\ngoal is to stop anything\n" \
                  "from approaching your home\nplanet. Use your technologies to\npull meteors towards\n" \
                  "unlucky space explorer\nby executing terminal code."

text_player_two = "You are lonely space explorer that\nwas caught in meteor storm.\nYou must " \
                  "avoid\nhitting rocks by\ntyping commands in order\nfor your ship to shoot them."


def validate(text: str):
    play_sound("select.wav")
    return (text.isdigit() and len(text) <= 6) or not text
