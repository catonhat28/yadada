# yadada
import streamlit as st
import random
from datetime import date, timedelta

# =========================================

# 페이지 설정

# =========================================

st.set_page_config(
page_title="야다의 모험",
page_icon="🎓",
layout="wide"
)

# =========================================

# 게임 설정

# =========================================

SUBJECTS = ["국어", "수학", "영어", "사문", "생윤"]

START_DATE = date(2026, 10, 1)
EXAM_DATE = date(2026, 11, 19)

# =========================================

# 등급 계산

# =========================================

def get_grade(score):
if score >= 6500:
return 1
elif score >= 5000:
return 2
elif score >= 3500:
return 3
elif score >= 2000:
return 4
elif score >= 1500:
return 5
elif score >= 1200:
return 6
elif score >= 1000:
return 7
elif score >= 500:
return 8
else:
return 9

# =========================================

# 버튼 생성

# =========================================

def generate_buttons():
button_count = random.choice([4, 5])

```
st.session_state.current_buttons = random.sample(
    SUBJECTS,
    button_count
)
```

# =========================================

# 게임 초기화

# =========================================

def initialize_game():

```
st.session_state.day = START_DATE

st.session_state.ticks = 10

st.session_state.scores = {
    subject: 0
    for subject in SUBJECTS
}

st.session_state.study_count = {
    subject: 0
    for subject in SUBJECTS
}

st.session_state.current_buttons = []

st.session_state.message = (
    "야다의 마지막 수험생활이 시작되었다!"
)

st.session_state.game_over = False

st.session_state.exam_started = False

st.session_state.ending = None

generate_buttons()
```

# =========================================

# 공부 버튼 클릭

# =========================================

def study(subject):

```
# 현재 과목의 누적 공부 횟수
count = st.session_state.study_count[subject]

# 첫 번째: 50점
# 두 번째: 60점
# 세 번째: 70점
gain = 50 + (count * 10)

# 점수 추가
st.session_state.scores[subject] += gain

# 공부 횟수 증가
st.session_state.study_count[subject] += 1

# 틱 감소
st.session_state.ticks -= 1

# 메시지 변경
st.session_state.message = (
    f"📚 {subject} 공부 성공! "
    f"+{gain}점 획득!"
)

# 버튼을 새롭게 랜덤 생성
generate_buttons()

# 틱을 모두 사용했으면 다음 날
if st.session_state.ticks == 0:

    st.session_state.day += timedelta(days=1)

    st.session_state.ticks = 10

    st.session_state.message = (
        f"🌅 새로운 하루가 시작되었다!\n\n"
        f"현재 날짜: {st.session_state.day.strftime('%m/%d')}"
    )

# 수능 날짜가 되면 수능 화면으로 이동
if st.session_state.day >= EXAM_DATE:

    st.session_state.exam_started = True

    st.session_state.current_buttons = []
```

# =========================================

# 수능 보기

# =========================================

def take_exam():

```
grades = {
    subject: get_grade(score)
    for subject, score in st.session_state.scores.items()
}

# 서울대 엔딩
if all(grade == 1 for grade in grades.values()):

    st.session_state.ending = "서울대 엔딩"

# 연세대 엔딩
elif (
    sum(grade == 1 for grade in grades.values()) >= 3
    and all(grade in [1, 2] for grade in grades.values())
):

    st.session_state.ending = "연세대 엔딩"

# 나머지는 1:1 랜덤
else:

    st.session_state.ending = random.choice(
        [
            "한양대 엔딩",
            "지방대 엔딩"
        ]
    )

st.session_state.game_over = True
```

# =========================================

# 최초 실행

# =========================================

if "day" not in st.session_state:

```
initialize_game()
```

# =========================================

# 제목

# =========================================

st.title("🎓 야다의 모험")

st.subheader(
"대한민국 고3의 마지막 사투"
)

st.write(
"""
대한민국의 고등학교 3학년 학생 유다윤.

```
일명 야차다윤.
줄여서 야다.

수능이라는 최종 보스를 향한
야다의 마지막 모험이 시작된다.
"""
```

)

st.divider()

# =========================================

# 엔딩 화면

# =========================================

if st.session_state.game_over:

```
st.header("🏁 수능 결과")

ending = st.session_state.ending

if ending == "서울대 엔딩":

    st.balloons()

    st.success(
        "🏛️ 서울대 엔딩!\n\n"
        "전 과목 1등급을 달성했다!\n"
        "야다는 정시로 서울대학교에 합격했다!"
    )

elif ending == "연세대 엔딩":

    st.info(
        "🔵 연세대 엔딩!\n\n"
        "수능에서 뛰어난 성적을 거두었다!\n"
        "야다는 연세대학교에 합격했다!"
    )

elif ending == "한양대 엔딩":

    st.warning(
        "🔷 한양대 엔딩!\n\n"
        "수능에서 원하는 결과를 얻지는 못했지만\n"
        "수시 합격으로 한양대학교에 진학하게 되었다!"
    )

else:

    st.error(
        "🔥 지방대 엔딩!\n\n"
        "수능과 수시 모두 쉽지 않았다.\n"
        "야다는 지방대학교에 진학하게 되었다."
    )

st.divider()

st.subheader("📄 야다의 성적표")

for subject in SUBJECTS:

    score = st.session_state.scores[subject]

    grade = get_grade(score)

    st.write(
        f"**{subject}**: {score}점 — {grade}등급"
    )

st.divider()

if st.button(
    "🔄 다시 시작하기",
    use_container_width=True
):

    initialize_game()

    st.rerun()

st.stop()
```

# =========================================

# 현재 날짜

# =========================================

col1, col2, col3 = st.columns(3)

with col1:

```
st.metric(
    "📅 현재 날짜",
    st.session_state.day.strftime("%m/%d")
)
```

with col2:

```
st.metric(
    "⏳ 남은 틱",
    st.session_state.ticks
)
```

with col3:

```
days_left = (
    EXAM_DATE - st.session_state.day
).days

st.metric(
    "🎯 수능까지",
    max(0, days_left)
)
```

st.divider()

# =========================================

# 틱 표시

# =========================================

st.subheader("⏱️ 오늘의 행동력")

tick_text = ""

for i in range(10):

```
if i < st.session_state.ticks:

    tick_text += "🟩 "

else:

    tick_text += "⬜ "
```

st.markdown(
f"### {tick_text}"
)

st.info(
st.session_state.message
)

# =========================================

# 수능 당일

# =========================================

if st.session_state.day >= EXAM_DATE:

```
st.warning(
    "📢 11월 19일.\n\n"
    "드디어 수능 당일이다!"
)

if st.button(
    "📝 수능 보러 가기",
    use_container_width=True
):

    take_exam()

    st.rerun()

st.stop()
```

# =========================================

# 공부 버튼

# =========================================

st.subheader("📚 공부할 과목을 선택하세요")

buttons = st.session_state.current_buttons

columns = st.columns(len(buttons))

for index, subject in enumerate(buttons):

```
with columns[index]:

    count = st.session_state.study_count[subject]

    next_gain = 50 + (count * 10)

    # 중요:
    # random.random()을 사용하지 않고
    # 과목 이름을 고정 key로 사용
    if st.button(
        f"📖 {subject}\n+{next_gain}점",
        key=f"study_button_{subject}",
        use_container_width=True
    ):

        study(subject)

        st.rerun()
```

# =========================================

# 현재 성적

# =========================================

st.divider()

st.subheader("📊 현재 공부 현황")

for subject in SUBJECTS:

```
score = st.session_state.scores[subject]

grade = get_grade(score)

st.write(
    f"**{subject}** — "
    f"{score}점 / 현재 예상 {grade}등급"
)

progress = min(score / 6500, 1.0)

st.progress(progress)
```
