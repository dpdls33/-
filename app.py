import streamlit as st

# ------------------ 자모 정의 ------------------ #

CHOSUNG_LIST  = ['ㄱ','ㄲ','ㄴ','ㄷ','ㄸ','ㄹ','ㅁ','ㅂ','ㅃ','ㅅ','ㅆ','ㅇ','ㅈ','ㅉ','ㅊ','ㅋ','ㅌ','ㅍ','ㅎ']
JUNGSUNG_LIST = ['ㅏ','ㅐ','ㅑ','ㅒ','ㅓ','ㅔ','ㅕ','ㅖ','ㅗ','ㅘ','ㅙ','ㅚ','ㅛ','ㅜ','ㅝ','ㅞ','ㅟ','ㅠ','ㅡ','ㅢ','ㅣ']
JONGSUNG_LIST = ["",'ㄱ','ㄲ','ㄳ','ㄴ','ㄵ','ㄶ','ㄷ','ㄹ','ㄺ','ㄻ','ㄼ','ㄽ','ㄾ','ㄿ','ㅀ','ㅁ','ㅂ','ㅄ','ㅅ',
                 'ㅆ','ㅇ','ㅈ','ㅊ','ㅋ','ㅌ','ㅍ','ㅎ']

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

# ------------------ 영타 → 자모 ------------------ #

def eng_to_jamo(text):
    result = []
    i = 0
    while i < len(text):
        if i+1 < len(text) and text[i:i+2] in ENG2KOR:
            result.append(ENG2KOR[text[i:i+2]])
            i += 2
        elif text[i] in ENG2KOR:
            result.append(ENG2KOR[text[i]])
            i += 1
        else:
            result.append(text[i])
            i += 1
    return result

# ------------------ 완전 조합(실제 입력기 방식) ------------------ #

def combine(jamo_list):
    result = ""
    cho = jung = jong = None

    def flush():
        nonlocal cho, jung, jong, result
        if cho and jung:
            code = 0xAC00 + (CHOSUNG_LIST.index(cho)*21*28) + (JUNGSUNG_LIST.index(jung)*28) + (JONGSUNG_LIST.index(jong) if jong else 0)
            result += chr(code)
        else:
            if cho: result += cho
            if jung: result += jung
        cho = jung = jong = None

    for j in jamo_list:
        # 모음
        if j in JUNGSUNG_LIST:
            if cho and not jung:           # 초성 + 중성
                jung = j
            elif cho and jung and jong:    # 종성이 있는데 모음 → 종성 분리
                prev_jong = jong
                jong = None
                flush()
                cho = prev_jong
                jung = j
            elif not cho:
                result += j
            else:
                flush()
                jung = j

        # 자음
        elif j in CHOSUNG_LIST:
            if cho and jung and not jong:  # 종성 넣기
                jong = j
            elif cho and jung and jong:    # 종성 끝났는데 또 자음 → 새 글자
                flush()
                cho = j
            else:
                if cho and not jung:       # 초성 충돌 → 이전 초성 출력
                    result += cho
                cho = j

        # 기타 문자
        else:
            flush()
            result += j

    flush()
    return result


def convert(text):
    return combine(eng_to_jamo(text))

# ------------------ Streamlit UI ------------------ #

st.title("영타 → 한글 자동 변환기")
st.write("영타가 실제 한글처럼 조합되는 변환기입니다.")

txt = st.text_area("영타 입력", placeholder="예: dkssud → 안녕")

if st.button("변환"):
    st.success(convert(txt))
