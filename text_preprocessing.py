import re
import emoji

emoticon_to_word = {
    ":)": "happy",
    ":]": "happy",
    "=)": "happy",
    ":v": "happy",
    ':")': "huhu",
    ":D": "laugh",
    ":(": "sad",
    ":<": "sad",
    ";)": "wink",
    ":|": "neutral",
    ":P": "tongue",
    ":'(": "cry",
    ":O": "surprise",  
    "^^": "happy",
    "<3": "love",
    "-.-": "annoyance",
    ":-)": "happy",
    "@@": "confusion",
    "-_-": "bored",
    ":>": "smirking",
    ":3": "cuteness",
    ":'<": "sad",
    "^^": "happy",
    "=]": "friendly",
    "=.=": "disbelief",
    ":x": "secrecy",
    "0 . 0": "shock",
    ":#": "quiet",
    ">.<": "frustration",
    
}

english_to_vietnamese = {
    "happy": "vui vẻ ",
    "laugh": "cười ",
    "sad": "buồn ",
    "wink": "nháy mắt ",
    "neutral": "trung lập ",
    "tongue": "nói năng ",
    "cry": "khóc ",
    "surprise": "ngạc nhiên ",
    "love": "yêu",
    "annoyance": "tức giận",
    "confusion": "bối rối",
    "bored": "chán nản",
    "smirking": "nhếch môi",
    "cuteness": "đáng yêu",
    "friendly": "thân thiện",
    "disbelief": "hoài nghi",
    "secrecy": "bí mật",
    "shock": "shock",
    "quiet": "im lặng",
    "frustration": "thất vọng"
}

ttranslate_emoticons_to_Vietnamese = {
    ":pouting_face:": " tức giận ",
    ":disappointed_face:": "buồn " ,
    ":face_with_tears_of_joy:": "haha ",
    ":beaming_face_with_smiling_eyes:": "vui nhỉ ",
    ":smiling_face_with_smiling_eyes:": "vui ghê ",
    ":loudly_crying_face:": "buồn quá ",
    ":expressionless_face:": "cạn lời ",
    ":hot_face:": "mệt thật ",
    ":rolling_on_the_floor_laughing:": "vui quá ",
    ":smiling_face_with_sunglasses:": "chất đó ",
    ":face_blowing_a_kiss:": "đáng yêu ",
    ":face_with_rolling_eyes:": "kinh ",
    ":grinning_face_with_sweat:": "ngại nhỉ ",
    ":grinning_face:": "hớn hở ",
    ":smiling_face_with_heart-eyes:": "đáng yêu ",
    ":red_heart:": "yêu yêu ",
    ":slightly_frowning_face:": "buồn quá ",
    ":pensive_face:": "chán nhỉ ",
    ":weary_face:": "mệt mỏi ",
    ":face_with_raised_eyebrow:": "khó nhỉ ",
    ":grinning_squinting_face:": "haha ",
    ":sleepy_face:": "thôi mệt ",
    ":crying_face:": "huhu buồn quá ",
    "surpriseK_hand:": "tốt ",
    ":smirking_face:": "khinh bỉ ",
    ":relieved_face:":"hihi ",
    ":face_vomiting:": "kinh tởm ",
    ":smiling_face_with_horns:":"kinh tởm",
    ":face_with_steam_from_nose:": "bực bội",
    ":face_with_monocle:": "nghi ngờ quá đi",
    ":angry_face:": "bực bội quá đi",
    ":smiling_face:": "vui quá",
    ":kissing_face_with_closed_eyes:": "yêu",
    ":smiling_face_with_hearts:": "hạnh phúc quá",
    ":face_savoring_food:": "ngon quá đi",
    ":confused_face:": "bối rối quá",
    ":thumbs_down:": "phản đối",
    ":money-mouth_face:": "tiền nhiều quá",
    ":cherry_blossom:": "hoa anh đào",
    ":grimacing_face:": "nhăn mặt",
    ":spider_web:": "mạng nhện",
    ":dog:": "chó",
    ":fearful_face:": "sợ hãi",
    ":grinning_face_with_smiling_eyes:": "cười toét mắt",
    ":downcast_face_with_sweat:": "mệt mỏi",
    ":star-struck:": "thích thú",
    ":folded_hands:": "cầu nguyện",
    ":face_with_head-bandage:": "đầu băng",
    ":pile_of_poo:": "đống phân",
    ":sleeping_face:": "ngủ",
    ":smiling_cat_with_heart-eyes:": "yêu mến",
    ":shushing_face:": "im lặng",
    ":tired_face:": "mệt mỏi",
    ":face_with_hand_over_mouth:": "ngại quá",
    ":new_moon_face:": "lạc quan",
    ":frowning_face:": "buồn",
    ":thumbs_up:": "được đó",
    ":flexed_biceps:": "Cơ bắp",
    ":full_moon_face:": "hihi",
    ":sad_but_relieved_face:": "Buồn mà nhẹ lòng",
    ":clapping_hands:": "Vỗ tay",
    ":ghost:": "Ma",
    ":person_facepalming:": "bất cứ điều gì",
    ":light_skin_tone:": "Da nhạt",
    ":anxious_face_with_sweat:": "Lo lắng đến nổi toát mồ hôi",
    ":woman_dancing:": "Người phụ nữ nhảy múa",
    "happyictory_hand:": "sự hạnh phúc chiến thắng",
    ":index_pointing_up:": "ở trên",
    ":persevering_face:": "Kiên trì",
    ":winking_face:": "Nháy mắt",
    ":female_sign:": "Biểu tượng nữ",
    ":male_sign:": "Biểu tượng nam",
    ":face_without_mouth:": "cạn lời",
    ":unamused_face:": "không vui",
    ":face_with_open_mouth:": "ngạc nhiên quá",
    ":winking_face_with_tongue:": "đùa giỡn",
    ":slightly_smiling_face:": "dễ thương",
    ":neutral_face:": "khó chịu",
    ":person_pouting:": "khinh thường",
    ":kissing_face:": "Hôn",
    ":face_screaming_in_fear:": "kinh hãi",
    ":drooling_face:": "ghiền quá",
    ":squinting_face_with_tongue:": "mĩa mai",
    ":kiss_mark:": "Dấu hôn",
    ":two_hearts:": "Hai trái tim",
    ":sneezing_face:": "hắt hơi",
    ":grinning_face_with_big_eyes:": "quá đã",
    ":upside-down_face:": "ngớ ngẫn ",
    ":anguished_face:": "Đau đớn",
    ":beating_heart:": "rung động",
    ":confounded_face:": "Hoang mang",
    ":cat_with_tears_of_joy:": "quá vui luôn",
    ":smiling_face_with_open_hands:": "hạnh phúc quá đi"

}

def remove_repeated_sequences(text):
    # Define a regex pattern to find sequences of repeated characters (including punctuation)
    pattern = r'(\S)\1+'
    
    # Replace the repeated sequences with a single instance of the character
    text = re.sub(pattern, r'\1', text, flags=re.IGNORECASE)
    
    return text


def transform_emoticons(text):
    for emoticon, word in emoticon_to_word.items():
        text = text.replace(emoticon, word)
    return text

def transform_emojis_and_emoticons(text):
    text_with_emojis = emoji.demojize(text)
    text = transform_emoticons(text_with_emojis)
    return text

def translate_english_to_vietnamese(text):
    for english, vietnamese in english_to_vietnamese.items():
        text = text.replace(english, vietnamese)
    return text
def translate_english_to_vietnamese_emoticon(text):
    for word_form, vietnamese in english_to_vietnamese.items():
        text = text.replace(word_form, vietnamese)
    return text
def replace_words(text):
    correct_words = {
        "cóa": "có",
        "coá": "có",
        "ngta": "người ta",
        "nta": "người ta",
        "cf": "cà phê",
        "coffee": "cà phê",
        "cafe": "cà phê ",
        "caphe": "cà phê",
        "coffe": "cà phê",
        "hk": "không",
        "cũnh": "cũng",
        "cungc": "cũng",
        "cungz": "cũng",
        "pik": "biết",
        "pk": "biết",
        "bik": "biết",
        "bjt": "biết",
        "nge": "nghe",
        "t": "tui",
        "uh": "ừm",
        "uhm": "ừm",
        "ah": "à",
        "v": "vậy",
        "thậc": "thật",
        "e":"em",
        "a": "anh",
        "dụng": "rụng",
        "thixx": "thích",
        "nhuwnh": "nhưng",
        "mợt": "mệt",
        "tnao": "thế nào",
        "thik": "thích",
        "k": "không",
        "truất": "chất",
        "fa": "Forever Alone",
        "h": "giờ",
        "chời": "trời",
        "lun": "luôn",
        "trym": "chim",
        "dume": "đụ mẹ",
        "cmm": "con mẹ mày",
        "lol": "lồn",
        "loz": "lồn",
        "mừ": "mà",
        "cmnl": "con mẹ nó luôn",
        "đm": "đụ mẹ",
        "ml": "mặt lồn",
        "đcm": "địt cụ mày",
        "zai": "trai",
        "vkl": "vãi cả lồn",
        "thoii": "thôi",
        "mọe": "mẹ",
        "âu kề": "ok",
        "gét": "ghét",
        "ah": "à",
        "vailon": "vãi lồn",
        "đựu": "đụ",
        "lìn": "lồn",
        "gê": "ghê",
        "douma": "đụ má",
        "lòn":"lồn",
        "tềnh": "tình",
        "nthe": "như thế", 
        "bều": "bèo",
        "chụy": "chị",
        "mòa": "mà",
        "th": "thôi",
        "v": "vậy",
        "b": "bạn",
        "ny": "người yêu",
        "đbh": "đéo bao giờ",
        "wtf": "what the fuck",
        "rùi": "rồi",
        "gvcn": "giáo viên chủ nhiệm",
        "ròi": "rồi",
        "z": "vậy",
        "àh": "à",
        "rụg": "rụng",
        "vạy": "vậy",
        "nv": "nhân viên",
        "ròi": "rồi",
        "đóa": "đó",
        "vid": "video",
        "hk": "không",
        "clm": "cái lồn má",
        "vlon": "vãi lồn",
        "mềnh": "mình",
        "cmt": "bình luận" ,
        "hỏg": "hỏng",
        "ẻ": "ỉa",
        "dồi": "rồi",
        "dth": "dễ thương",
        "nge": "nghe",
        "ak": "á",
        "iêu": "yêu",
        "thíu": "thiếu",
        "m": "mày",
        "cíu": "cứu",
        "n": "nó",
        "móa": "má",
        "thặc": "thật",
        "tks": "cảm ơn",
        "c": "chị",
        "mé": "má",
        "pê": "bê",
        "cóa": "có",
        "coá": "có",
        "ngta": "người ta",
        "nta": "người ta",
        "cf": "cà phê",
        "coffee": "cà phê",
        "cafe": "cà phê ",
        "caphe": "cà phê",
        "coffe": "cà phê",
        "hk": "không",
        "cũnh": "cũng",
        "cungc": "cũng",
        "cungz": "cũng",
        "pik": "biết",
        "pk": "biết",
        "bik": "biết",
        "bjt": "biết",
        "nge": "nghe",
        "t": "tui",
        "uh": "ừm",
        "uhm": "ừm",
        "ah": "à",
        "v": "vậy",
        "thậc": "thật",
        "e":"em",
        "a": "anh",
        }
    words = text.split()
    replaced_words = [correct_words.get(word, word) for word in words]
    text = ' '.join(replaced_words)
    return text

def remove_stopwords(text, stopword_file='stopword_1.txt'):
    # Read stopwords from the file with utf-8 encoding
    with open(stopword_file, 'r', encoding='utf-8') as file:
        stopwords = set(word.strip() for word in file)

    # Tokenize the input sentence into words
    words = text.split()

    # Remove the stopwords from the list of words
    filtered_words = [word for word in words if word.lower() not in stopwords]

    # Reconstruct the sentence without the stopwords
    text = ' '.join(filtered_words)

    return text

def process_text(input_text):
    # Applying all transformations in order
    text = remove_repeated_sequences(input_text)
    text = transform_emojis_and_emoticons(text)
    text = translate_english_to_vietnamese_emoticon(text)
    text = translate_english_to_vietnamese(text)
    text = replace_words(text)
    text = remove_stopwords(text)

    return text



input_sentence = "người buồn cảnh có vui đâu bao giờ"
result =process_text(input_sentence)
print(result)