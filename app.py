import streamlit as st

# ===================== 두벌식 자모 정의 ===================== #

CHOSUNG_LIST = ['ㄱ','ㄲ','ㄴ','ㄷ','ㄸ','ㄹ','ㅁ','ㅂ','ㅃ','ㅅ','ㅆ','ㅇ','ㅈ','ㅉ','ㅊ','ㅋ','ㅌ','ㅍ','ㅎ']
JUNGSUNG_LIST = ['ㅏ','ㅐ','ㅑ','ㅒ','ㅓ','ㅔ','ㅕ','ㅖ','ㅗ','ㅘ','ㅙ','ㅚ','ㅛ','ㅜ','ㅝ','ㅞ','ㅟ','ㅠ','ㅡ','ㅢ','ㅣ']
JONGSUNG_LIST = ["",'ㄱ','ㄲ','ㄳ','ㄴ','ㄵ','ㄶ','ㄷ','ㄹ','ㄺ','ㄻ','ㄼ','ㄽ','ㄾ','ㄿ','ㅀ','ㅁ','ㅂ','ㅄ','ㅅ',
                 'ㅆ','ㅇ','ㅈ','ㅊ','ㅋ','ㅌ','ㅍ','ㅎ']

# ===================== 영타 → 자모 매핑 ===================== #

ENG2KOR = {
    "r":"ㄱ","R":"ㄲ","rt":"ㄳ",
    "s":"ㄴ","sw":"ㄵ","sg":"ㄶ",
    "e":"ㄷ","E":"ㄸ",
    "f":"ㄹ","fr":"ㄺ","fa":"ㄻ","fq":"ㄼ","ft":"ㄽ","fx":"ㄾ","fv":"ㄿ","fg":"ㅀ",
    "a":"ㅁ",
    "q":"ㅂ","Q":"ㅃ","qt":"ㅄ",
    "t":"ㅅ","T":"ㅆ",
    "d":"ㅇ",
    "w":"ㅈ","W":"ㅉ",
    "c":"ㅊ",
    "z":"ㅋ",
    "x":"ㅌ",
    "v":"ㅍ",
    "g":"ㅎ",

    # 모음
    "k":"ㅏ","o":"ㅐ","i":"ㅑ","O":"ㅒ","j":"ㅓ","p":"ㅔ","u":"ㅕ","P":"ㅖ",
    "h":"ㅗ","hk":"ㅘ","ho":"ㅙ","hl":"ㅚ",
    "y":"ㅛ",
    "n":"ㅜ","nj":"ㅝ","np":"ㅞ","nl":"ㅟ",
    "b":"ㅠ",
    "m":"ㅡ","ml":"ㅢ",
    "l":"ㅣ"
}


# ===================== 영타 → 자모 ===================== #

def eng_to_jamo(text):
    """영타 → 자모 문자열 변환"""
    result = []
    i = 0
    while i < len(text):
        # 2글자 조합 우선
        if i + 1 < len(text) and text[i:i+2] in ENG2KOR:
            result.append(ENG2KOR[text[i:i+2]])
            i += 2
        elif text[i] in ENG2KOR:
            result.append(ENG2KOR[text[i]])
            i += 1
        else:
            result.append(text[i])
            i += 1
    return result


# ===================== 자모 → 완성형 한글 ===================== #

def jamo_to_hangul(jamo_list):
    result = ""
    cho = jung = jong = None

    def flush():
        nonlocal cho, jung, jong, result
        if cho is not None and jung is not None:
            cho_idx = CHOSUNG_LIST.index(cho)
            jung_idx = JUNGSUNG_LIST.index(jung)
            jong_idx = JONGSUNG_LIST.index(jong) if jong else 0
            code = 0xAC00 + (cho_idx * 21 * 28) + (jung_idx * 28) + jong_idx
            result += chr(code)
        else:
            if cho: result += cho
            if jung: result += jung
        cho = jung = jong = None

    for j in jamo_list:

        # 초성
        if j in CHOSUNG_LIST and jung is None:
            cho = j

        # 중성
        elif j in JUNGSUNG_LIST:
            if jung is None:
                jung = j
            else:
                flush()
                jung = j

        # 종성
        elif j in JONGSUNG_LIST and jung is not None:
            if jong is None:
                jong = j
            else:
                flush()
                cho = j if j in CHOSUNG_LIST else None

        else:
            flush()
            if j in CHOSUNG_LIST:
                cho = j
            elif j in JUNGSUNG_LIST:
                jung = j
            else:
                result += j

    flush()
    return result


# ===================== 전체 변환 함수 ===================== #

def convert(text):
    jamo = eng_to_jamo(text)
    hangul = jamo_to_hangul(jamo)
    return hangul


# ===================== Streamlit UI ===================== #

st.title("영타 → 한글 자동 변환기")
st.write("영어 자판으로 입력된 한글을 변환합니다.\n예: **dkssud → 안녕**")

text = st.text_area("영타 입력", placeholder="예: dkssud → 안녕")

if st.button("변환"):
    st.success(convert(text))
