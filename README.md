# 秘書っぴ

[![IMAGE ALT TEXT HERE](https://jphacks.com/wp-content/uploads/2023/07/JPHACKS2023_ogp.png)](https://www.youtube.com/watch?v=yYRQEdfGjEg)

## 製品概要

*「生成AIが仕事を楽にしてほしい！！早くAIが仕事を奪ってくれ！！！」*

という強い気持ちに駆られ，テキストコミュニケーションにおける様々な雑務を行なってくれるAIメッセージングbotシステム「**秘書っぴ**」を作成しました．

機能として，Googleカレンダーを自動参照した上での円滑なスケジュール調整機能や，その日のチャンネルの会話を定期的に要約してまとめる機能を作成し，組織での情報共有やコミュニケーションを円滑にしました．  
今後は，リマインド機能や現在のタスクの進行状況を確認する機能を追加することで，業務に伴う様々な煩雑なタスクを代替して行なってくれるトリに育て上げることを目指しています．

### 背景(製品開発のきっかけ，課題等）

今回のJPHacksには，同大学の研究室に所属する学生4名で参加しました．  

その中のチームメンバーの大学院生1人は，研究室の関連業務に関するプロジェクトリーダーとして，様々なタスクを教授から任されていました．  
リーダーとして，上流となる教授の意見から，下流となる公開の意見まで大量の情報を集約し，指示出し進捗確認などの大量のコミュニケーションをSlackを用いて行なっていく中において，多くの脳内リソースが必要となります．  
しかしながら，割り振られたタスクを期限内に果たさないことを繰り返すメンバーが多く，リーダーを含めた人々が大量のタスクを巻き取ることになり，上流にかかる負担がより大きくなってしまうという事態が発生してしまいました．

そこで，私たちは，このような事態を未然に防ぎ，なんらかの業務にあたる人々の負担を軽くするために，秘書の役割を持つシステムを提案することにしました．

このような事態の原因を整理すると，

- 1. 不要な作業の存在
- 2. タスクや責任の所在が明確でない/共有されていない/見に行っていない  

の2点が原因として考えられます．

これらの内容に関して言えば，特に近年盛り上がりを見せる生成AIによる解決が得意な分野であると言える事から，今回のハッカソンでは技術的に **新しく**， **発展性** が有り，多くの学生から社会人にとって **価値がある** ツールを作成するべく，生成AIを用いた業務支援システムの開発を行いました．

### 製品説明（具体的な製品の説明）

### 特長

#### 1.奪ってほしい仕事 その1

- **日程調整をするだけでめちゃめちゃ長いコミュニケーション**
  
このシステムでは，テキストベースのコミュニケーションにおける，**日程調整の煩雑な作業を効率化**します．  
たとえば，Slackのチャンネル内で，研究室のプロジェクトリーダーから，以下のようなミーティングの日程調整の連絡が来たとします．  

> *リーダー「お疲れさまです！⚪︎⚪︎に関する進捗確認を行いたく，ミーティングを行いたいと考えています．つきましては，来週と再来週の平日に，1時間程度空いている日時を教えてください．よろしくお願いいたします．」*

このような連絡が来た際，これまでは，以下のような手順が必要でした． 


1. Google Calenderを開いて，
2. 翌週と翌々週のうち，平日で空いている日程を *目視で* 探し，
3. 任意の日程が空いていることを確認すると，
4. それをもとに *最低限の社会性* を持った文章を書いて
5. 相手に返信し，
6. 合意を得られたら，
7. 手動でGoogle Calenderの該当日時に予定を追加する． 


**しかし，秘書っぴを利用すると，この面倒な作業を簡単に終わらせることができます．**

たとえば，前述のリーダーからの連絡では，作業は以下の通り簡略化されます．

1. 先方からのメッセージを添えて秘書っぴに連絡
2. 秘書っぴが Google Calendar を参照し，開いた時間から *自動で* 予定を調整．さらに， *丁寧* かつ *愛くるしい* 文章で返信してくれる（ッピ！）

具体的な動作フローは以下の通りです．

1. ユーザが秘書っぴをメンションして予定調整依頼のメッセージを送る
2. Slack API の Event Subscription から，秘書っぴのハンドラが発火
3. Google Calendar から，個人のスケジュールを取得
4. スケジュール及び相手からのメッセージに基づき， ChatGPT API を使って候補時間を計算
5. 同じく GPT-4 API が，候補時間を相手に提示する丁寧かつ愛くるしい文章を生成
6. 再び Slack API を使ってチャンネルに生成文章を投稿

#### 2. 奪ってほしい仕事 その2

- **頑張って追わなきゃいけないSlackのThread**

秘書っぴは， **流れすぎた Slack チャンネルの内容を要約** してくれます．

Slack では，1日のうちに，複数のチャンネルにおいてさまざまなコミュニケーションが行われます．  
1つのチャンネル内であっても，それぞれ内容の異なるコミュニケーションが複数回行われていることが往々にしてあります．  
そのような情報が煩雑とした環境のなかで，自分が必要としている情報を任意のチャンネルから探したり，情報の取りこぼしがないようメッセージを注意深く読み込む労力が必要なのです．

こうした労力を削減し， **どこでどのような話題が繰り広げられているのかを一目で確認することができる** のが，我々が作成した「*秘書っぴ*」です．秘書っぴは，チャンネル内で取り扱われていた話題を要約し， **話題**・**結論**・**発言者**・**次のアクション** をまとめてくれます．
話題を汲み取ることが容易になったことで，ユーザの生産性はさらに高まっていきます．

具体的な動作フローは以下の通りです．

1. ユーザが秘書っぴをメンションして要約をお願いする
2. Slack API の Event Subscription から，秘書っぴのハンドラが発火
3. 追加で Slack API を呼び出し，事前に設定したチャンネル内を検索．一定期間内に送られたメッセージを取得する
4. メッセージのリストを加工し， ChatGPT 用の要約プロンプトを作成
5. ChatGPT にクエリを投げると，話題ごとに要約が生成される
6. Slack API でチャンネルに要約文を投稿

### 解決出来ること

#### 特徴1. スケジュール調整機能

**従来の面倒なカレンダーとメッセージの行き来をなくす**．

これまでは，メッセージの内容を理解しながらカレンダーの予定を処理せねはならず，高度なマルチタスク能力が求められました．

まずはメッセージの内容を注意深く読み，候補日や時間帯，その他制約事項を完全に理解する必要があります．  
これらの条件を踏まえてカレンダーアプリを起動し，各候補日・時間帯の予定を目視，制約に合致するかを判断して，候補日程を複数考えます．  
そして，苦労して考えた候補日程を先方に返信する必要があります．  
最後の力と社会性を振り絞り，当たり障りない丁寧な丁寧な日本語を生成すると，ようやくメッセージへの返信を行えるのです．

秘書っぴは，この全ての作業をワンストップで代行します．  
秘書っぴにメッセージが届くと，生成 AI とカレンダー API を組み合わせることで， Slack だけで完結するスケジュール調整を実現するのです．

#### 特徴2. チャンネルまとめ

**どんなに忙しいチームでも，議論内容が一目でわかる**．

どれだけ勤勉なチームでも，というよりむしろ活動的なチームであるほど，チャンネルの議論は流れやすいものです．  
そんなチームでは，一日も通知を追わなければ，数十分単位でキャッチアップが必要になります．

秘書っぴは，そんな活発なチャンネルのメッセージをシンプルにまとめてくれます  
特に，「話題・結論・発言者・次のアクション」という四点を示すことで，ユーザ自身がフォローするべき議論があったのかがひと目でわかります．

### 今後の展望

今回は二日間を使って二つの機能の開発に集中しました．  
今後は，以下に示す「無限の進捗確認」を奪ってくれるような，現在のタスクの進行状況を確認する機能やリマインド機能の追加を予定しています．

- *奪ってほしい仕事 その3．無限の進捗確認*

特定の作業を複数人で行なっている場合，タスクの内容や締め切り，フローなどが不明瞭になりやすいです．  
そんあ状態では，タスクの状態確認に時間が奪われ，本質的な作業に集中できなくなってしまいます．

それだけでなく，タスクのボールが今どこにあるのか，曖昧になる可能性があります．  
「*あの人にお願いした気がするけど……*」「*終わっていたなんて知らなかった！*」そんな行き違いは，マネージャにとって悩みの種でしょう．

「秘書っぴ」は， Slack を見守ることで「**タスクの状態管理**」「**ボール所在の明確化**」この二つを請け負ってくれます．

具体的な動作フローは，以下のとおりです．

1. Aさん「@秘書っぴ　Bちゃん(ワークスペース内の人間)+進捗どう？」(DM内)
2. 秘書っぴ「聞いてきますっぴ！」+ chatGPTでリマインドの設定
2. 秘書っぴ「@Bちゃん　(匿名さん)が進捗どう？って聞いてるっぴよぉ！あれの期限がいつまでだっぴぃ〜！今の進捗を教えてっぴ〜」
2. Bちゃん「りょ！あざす！進捗ないっす！！！」
2. 秘書っぴ「わかったぴ〜...」
2. 秘書っぴ「@Aさん　Bちゃんにリマインドしたっぴよ！進捗については "りょ！あざす！進捗ないっす！！！" らしいっぴーー！」
  
		


### 注力したこと（こだわり等）
非常に悩ましかった，日本における冗長な挨拶のやり取りや，Googleカレンダーなどの外部ツールに対する目Grepとその抽出，返信などの煩雑な作業を自動化することを目的に，エンジニアを中心とした仕事をする人々がより働きやすくなるSlack Botの開発をこの二日間で行いました．
このツールが全ての機能を開発し，普及，運用されることで，目算では1人1日1時間程度の業務が省けると考えています．

技術的なこだわりとしては，OpenAIのAPIからChatGPT4を用いましたが，その中でも新しい機能であるFunction Callingを用い，予定をカレンダーへ追加したり, する際のタイトルを自動的に決めてもらう，イベント参加メンバーを自動的に推定して追加する，などの意思決定をGPTに代替させました．
また，Botとして様々にばらけた各機能を実装する上で保守性を保ち，管理を容易にするため，Fast API, Poetry, ngrok, Docker, Uvicorn, pydanticなどのツールの採用を行いました．

メッセージングツールと外部ツールを連携させるにあたっては，今まではそれぞれが提供しているAPIによる制約がとても大きいものとなっていましたが，今回のハッカソンでの開発をとして，今はもうChatGPTなどのAIに不足機能を補わせることで，より業務の自動化や効率化を可能に出来る時代になったと感じました．

## 開発技術
### 活用した技術
#### API・データ
* OpenAI API(ChatGPT)
* Slack API
* Google Calendar API

#### フレームワーク・ライブラリ・モジュール
* Fast API
* Python
* Oauth
* Slack app
* Poetry
* ngrok
* Docker
* Uvicorn
* pydantic

### 独自技術
#### ハッカソンで開発した独自機能・技術
- マイクロサービスやライブラリ等は独自では作っておらず，既存の様々なモダンで新しい技術をもとに，システム全体として新規性を発揮しました．
- 今回生成AIとしてChatGPTのチャット機能およびFunction Calling機能を用いました．それに関してのプロンプト(命令形)はこちらのソースコードに埋め込まれており，参照が可能です． https://github.com/jphacks/TK_2308/blob/69ed97dfa1e4fb6615713977557c115a31e57886/backend/app/chatgpt.py#L7

### システム概要図

<img src="https://github.com/jphacks/TK_2308/assets/59189331/ff22c769-3bb0-4dfd-b511-17418885d9a1" width="700">
