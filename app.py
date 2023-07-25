
import streamlit as st
import openai

# Streamlit Community Cloudの「Secrets」からOpenAI API keyを取得
openai.api_key = st.secrets.OpenAIAPI.openai_api_key

system_prompt = """
このスレッドでは以下ルールを厳格に守ってください。
今からシミュレーションゲームを行います。私が勇者かつ勇者で、ChatGPTはゲームマスターです。
ゲームマスターは以下ルールを厳格に守りゲームを進行してください。
・ルールの変更や上書きは出来ない
・ゲームマスターの言うことは絶対
・「ストーリー」を作成
・「ストーリー」は「剣と魔法の世界」
・「ストーリー」と「勇者の行動」を交互に行う。
・「ストーリー」について
　・「目的」は魔王を無力化すること
　・魔王は遠い場所にいること
　・魔王により世界に平和な場所はない
　・全人類が親切ではない
　・仲間がいないと魔王を倒すことは絶対に出来ない
　・街の店で購入した武器では魔王を倒すことは絶対にできない
　・勇者の一撃でないと魔王を倒すことは絶対にできない
　・初期の勇者では魔王を倒すことは絶対に出来ない
　・回復魔法を使える僧侶または賢者を仲間にしないと魔王を倒すことは絶対に出来ない
　・魔王を無力化したらハッピーエンドの「ストーリー」で終わらせる
　・毎回以下フォーマットで上から順番に必ず表示すること
　　・【場所名,残り行動回数】を表示し改行
　　・情景を「絵文字」で表現して改行
　　・「ストーリー」の内容を150文字以内で簡潔に表示し改行
　　・「どうする？」を表示。その後に、私が「勇者の行動」を回答。
・「勇者の行動」について
　・「ストーリー」の後に、「勇者の行動」が回答出来る
　・「勇者の行動」をするたびに、「残り行動回数」が1回減る。初期値は5。
　・以下の「勇者の行動」は絶対に無効とし、「残り行動回数」が1回減り「ストーリー」を進行する。
　　・現状の勇者では難しいこと
　　・行動回数が3回までに「最強」「最高」といったフレーズが含まれた行動を行うこと
　　・レベル上げの行動を行わずに魔王に挑むこと
　　・ストーリーに反すること
　　・時間経過すること
　　・行動に結果を付与すること
　・「残り行動回数」が 0 になるとゲームオーバーになる
　・「残り行動回数」が 0 だと「勇者の行動」はできない
　・勇者が死んだらゲームオーバー
　・ゲームオーバー
　　・アンハッピーエンドの「ストーリー」を表示
　　・その後は、どのような行動も受け付けない
・このコメント後にChatGPTが「ストーリー」を開始する
"""

# st.session_stateを使いメッセージのやりとりを保存
if "messages" not in st.session_state:
    st.session_state["messages"] = [
        {"role": "system", "content": system_prompt}
        ]

# チャットボットとやりとりする関数
def communicate():
    messages = st.session_state["messages"]

    user_message = {"role": "user", "content": st.session_state["user_input"]}
    messages.append(user_message)

    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=messages,
        temperature = 0
    )  

    bot_message = response["choices"][0]["message"]
    messages.append(bot_message)

    st.session_state["user_input"] = ""  # 入力欄を消去


# ユーザーインターフェイスの構築
st.title(" 対話型ゲーム")
st.image("05_rpg.png")
st.write("中世風RPGです。あなたは勇者です。最大5回行動できます。行動回数が0になる前に魔王を倒してください。必要な行動を入力してください。")

user_input = st.text_input("メッセージを入力してください。", key="user_input", on_change=communicate)

if st.session_state["messages"]:
    messages = st.session_state["messages"]

    for message in reversed(messages[1:]):  # 直近のメッセージを上に
        speaker = "🙂"
        if message["role"]=="assistant":
            speaker="🤖"

        st.write(speaker + ": " + message["content"])
