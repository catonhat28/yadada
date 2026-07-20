# yadada

import streamlit as st
import random
from datetime import date, timedelta

# =========================================
# 기본 설정
# =========================================

st.set_page_config(
    page_title="야다의 모험",
    page_icon="🎓",
    layout="wide"
)

# =========================================
# 게임 데이터
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


def grade_text(grade):
    return f"{grade}등급"


# =========================================
# 초기화
# =========================================

def initialize_game():
    st.session_state.day = START_DATE
    st.session_state.ticks = 10
    st.session_state.scores = {
        subject: 0 for subject in SUBJECTS
    }

    # 각 과목별 공부 횟수
    st.session_state.study_count = {
        subject: 0 for subject in SUBJECTS
    }

    st.session_state.current_buttons = []
    st.session_state.game_over = False
    st.session_state.exam_started = False
    st.session_state.ending = None

    # 게임 이벤트
    st.session_state.message = (
        "야다의 마지막 수험생활이 시작되었다..."
    )

    generate_buttons()


def generate_buttons():
    """
    매 틱마다 4~5개의 랜덤 과목 버튼 생성
    """
    button_count = random.choice([4, 5])
    st.session_state.current_buttons = random.sample(
        SUBJECTS,
        button_count
    )


# =========================================
# 하루 진행
# =========================================

def use_tick(subject):
    if st.session_state.game_over:
        return

    # 현재 과목의 공부 횟수
    count = st.session_state.study_count[subject]

    # 첫 공부: 50점
    # 두 번째: 60점
    # 세 번째: 70점 ...
    gain = 50 + count * 10

    st.session_state.scores[subject] += gain
    st.session_state.study_count[subject] += 1

    st.session_state.ticks -= 1

    st.session_state.message = (
        f"📚 {subject} 공부 성공! "
        f"+{gain}점 획득!"
    )

    # 10틱 모두 사용
    if st.session_state.ticks <= 0:
        st.session_state.day += timedelta(days=1)
        st.session_state.ticks = 10

        st.session_state.message = (
            f"🌅 새로운 하루가 시작되었다!\n"
            f"{st.session_state.day.strftime('%m/%d')}"
        )

    # 수능 당일
    if st.session_state.day >= EXAM_DATE:
        st.session_state.exam_started = True
        st.session_state.current_buttons = []


# =========================================
# 수능 결과
# =========================================

def take_exam():
    st.session_state.exam_started = False
    st.session_state.game_over = True

    grades = {
        subject: get_grade(score)
        for subject, score in st.session_state.scores.items()
    }

    # 서울대 엔딩
    # 모든 과목 1등급
    if all(grade == 1 for grade in grades.values()):
        st.session_state.ending = "서울대 엔딩"

    # 연세대 엔딩
    # 1등급이 3개 이상이고 나머지는 2등급
    elif (
        sum(grade == 1 for grade in grades.values()) >= 3
        and all(grade in [1, 2] for grade in grades.values())
    ):
        st.session_state.ending = "연세대 엔딩"

    # 조건 미달 시 1:1 랜덤
    else:
        st.session_state.ending = random.choice(
            ["한양대 엔딩", "지방대 엔딩"]
        )


# =========================================
# UI
# =========================================

if "day" not in st.session_state:
    initialize_game()


# =========================================
# 타이틀
# =========================================

st.title("🎓 야다의 모험")
st.subheader("대한민국 고3의 마지막 사투")

st.markdown(
    """
    **유다윤**, 일명 **야차다윤**, 줄여서 **야다**.

    대학 진학을 위한 마지막 전투가 시작되었다.

    과연 야다는 휘몰아치는 공부 지옥과 수많은 빌런들을 뚫고
    **서울대학교**에 진학할 수 있을 것인가?
    """
)

st.divider()


# =========================================
# 엔딩 화면
# =========================================

if st.session_state.game_over:

    st.header("🏁 수능 결과")

    st.success(
        f"## {st.session_state.ending}"
    )

    st.write(
        "야다는 마침내 긴 수험생활의 끝에 도달했다."
    )

    st.divider()

    st.subheader("📄 성적표")

    result_data = []

    for subject in SUBJECTS:
        score = st.session_state.scores[subject]
        grade = get_grade(score)

        result_data.append({
            "과목": subject,
            "점수": score,
            "등급": grade_text(grade)
        })

    st.table(result_data)

    st.divider()

    if st.session_state.ending == "서울대 엔딩":
        st.balloons()
        st.success(
            "🏛️ 전 과목 1등급!\n\n"
            "야다는 정시로 서울대학교에 합격했다!"
        )

    elif st.session_state.ending == "연세대 엔딩":
        st.info(
            "🔵 수능에서 훌륭한 성적을 거두었다!\n\n"
            "야다는 연세대학교에 합격했다!"
        )

    elif st.session_state.ending == "한양대 엔딩":
        st.warning(
            "🔷 수능에서 원하는 결과를 얻지는 못했다.\n\n"
            "하지만 수시 합격으로 한양대학교에 진학하게 되었다!"
        )

    elif st.session_state.ending == "지방대 엔딩":
        st.error(
            "🔥 수능도, 수시도 쉽지 않았다.\n\n"
            "야다는 지방대학교에 진학하게 되었다."
        )

    if st.button("🔄 다시 시작하기"):
        initialize_game()
        st.rerun()

    st.stop()


# =========================================
# 현재 날짜와 틱
# =========================================

col1, col2, col3 = st.columns(3)

with col1:
    st.metric(
        "📅 현재 날짜",
        st.session_state.day.strftime("%m/%d")
    )

with col2:
    st.metric(
        "⏳ 남은 틱",
        st.session_state.ticks
    )

with col3:
    st.metric(
        "🎯 수능까지",
        max(
            0,
            (EXAM_DATE - st.session_state.day).days
        )
    )


st.divider()


# =========================================
# 틱 아이콘
# =========================================

st.subheader("⏱️ 오늘의 행동력")

tick_display = ""

for i in range(10):
    if i < st.session_state.ticks:
        tick_display += "🟩 "
    else:
        tick_display += "⬜ "

st.markdown(
    f"### {tick_display}"
)

st.caption(
    "공부 버튼을 한 번 누를 때마다 틱이 1개 감소합니다."
)


# =========================================
# 메시지
# =========================================

st.info(st.session_state.message)


# =========================================
# 수능 당일
# =========================================

if st.session_state.day >= EXAM_DATE:

    st.warning(
        "📢 11월 19일.\n\n"
        "드디어 수능 당일이다."
    )

    st.subheader("⚔️ 마지막 전투")

    if st.button(
        "📝 수능 보러 가기",
        use_container_width=True
    ):
        take_exam()
        st.rerun()

    st.stop()


# =========================================
# 공부 버튼
# =========================================

st.subheader("📚 무엇을 공부할까?")

st.write(
    "랜덤하게 등장한 과목 중 하나를 선택해 공부하세요."
)

buttons = st.session_state.current_buttons

columns = st.columns(len(buttons))

for i, subject in enumerate(buttons):

    with columns[i]:

        current_count = st.session_state.study_count[subject]
        next_gain = 50 + current_count * 10

        if st.button(
            f"{subject}\n+{next_gain}점",
            key=f"{subject}_{random.random()}",
            use_container_width=True
        ):
            use_tick(subject)
            generate_buttons()
            st.rerun()


# =========================================
# 현재 성적
# =========================================

st.divider()

st.subheader("📊 현재 공부 현황")

for subject in SUBJECTS:

    score = st.session_state.scores[subject]
    grade = get_grade(score)

    st.write(
        f"**{subject}** — "
        f"{score}점 / 현재 예상 {grade}등급"
    )

    st.progress(
        min(score / 6500, 1.0)
    )


# =========================================
# 스토리 설명
# =========================================

st.divider()

with st.expander("📖 야다의 모험 스토리"):

    st.write(
        """
        대한민국의 고등학교 3학년 학생 유다윤.

        별명은 야차다윤.
        줄여서 야다.

        11월 19일 수능이라는 최종 보스를 향해
        야다는 오늘도 공부 버튼을 누른다.

        하지만 수험생활은 쉽지 않다.

        하루 10틱.

        매 순간 선택.

        국어를 공부할 것인가?
        수학을 공부할 것인가?
        영어를 공부할 것인가?
        사문을 공부할 것인가?
        생윤을 공부할 것인가?

        모든 선택이 야다의 미래를 바꾼다.

        과연 야다는 서울대 엔딩을 볼 수 있을까?
        """
    )
