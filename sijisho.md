1. インターン基礎の目標
Mining Software Repository のプロセスを理解する
主要なマイニング（データ収集）ツールを使えるようになる
研究ネタをやってみる

2. Mining Software Repository のプロセス
Mining Software Repositoryとは，ソフトウェア開発リポジトリからデータを収集・利用し，ソフトウェア開発に役立つ知見や手法を生む研究の総称を指す．MSR研究は大きく，「分析」と「手法開発」研究の２種類に分かれる．


「分析」研究では，設定したリサーチクエスチョン（疑問や仮説）を回答するために，データを収集し，統計手法を用いながら新しい知見を生み出す．
Research Questionの設定
データ収集
データ処理
可視化・統計処理
まとめ

「手法開発」研究では，解決するべき問題を設定し，その問題を解決するための手法を構築・評価する研究である．
問題・目標の設定
手法開発
評価
まとめ

3. 主要ツールを使ってみよう
ISSUEやPull Requestを取得しよう（GitHubからデータをとってくる）
セットアップ
Pycharm or VScodeをインストール


venv or Dockerで実行環境構築
pip でpyGitHub（https://github.com/PyGithub/PyGithub）をインストール
各リポジトリのコミット数な自身のリポジトリのデータを取得できるかをやってみよう
どを取得
参考：https://pygithub.readthedocs.io/en/latest/introduction.html
他人の公開リポジトリからデータを取得
GitHubリポジトリで，Javaとpythonでそれぞれ人気（スター数）上位10位を調査しよう
Issueデータの取得
以下のいずれかのリポジトリからIssueデータを取得しよう
https://github.com/spring-projects/spring-framework
https://github.com/opensearch-project/OpenSearch
https://github.com/apache/lucene
直近1週間のIssue報告数を日毎に集計・可視化しよう
pythonならmatplotlibなどを使う 
Pull Requestデータの取得
Issueデータの取得方法と同様にPull Requestのデータを取得
どれぐらいのPull RequestがRejectされているか調べよう
GitHub Action（Continuous Integration）データの取得
ビルド結果を取得し，どの程度のビルドが失敗しているか調べよう


コミット情報を取得しよう（ローカルにクローンしたリポジトリからデータを取得する）
どちらかのツールをインストールしよう
Java：jGit
Python：GitPython
上記ツールで以下のリポジトリをクローンするプログラムを書こう
https://github.com/apache/commons-math
すべてのコミット情報を取得しよう
コミットメッセージ
コミット作成日
変更ファイル
変更行数


テストデータを取得しよう
（上の続き）
各リビジョン（全部はしなくてよい）をチェックアウトしてみよう
以下のコマンドでテストを実行してみよう．
mvn test
テスト結果をプログラムで読み取って何件テストに成功しているかを出力しよう
target/surefire-reportの中にあるxmlファイルを読み取るで


リファクタリングを検出しよう
リファクタリングとは何かを調べよう
リファクタリングの種類を見てみよう
https://refactoring.guru/ja/refactoring/catalog
RefactoringMiner（https://github.com/tsantalis/RefactoringMiner）でコミットに含まれるリファクタリングを検出しよう．以下のどちらかを実施
方法1（初級）：コマンドラインから実行
参考：https://github.com/tsantalis/RefactoringMiner?tab=readme-ov-file#how-to-run-refactoringminer-from-the-command-line
方法2（上級）：APIを叩いて実行（Javaのみ）
https://mvnrepository.com/artifact/com.github.tsantalis/refactoring-miner/2.0

Self-Admitted Technical Debtを検出しよう 
技術的負債とは何かを調べよう
Self-Admitted Technical Debt（SATD）とは何かを調べてみよう
SATDツールを使ってみよう
https://github.com/Tbabm/SATDDetector-Core
		注意：
			・ツールのJavaバージョンが古い
			・初期ツールなので精度が低い
以下がSATDかどうかを調べてみよう
//TODO: make a new history item
// Get the jar files in .ant/lib
// add ant properties
// we need to break apart for 1.8 ver.
4. 分析してみよう
PRが却下される原因を自分なりに仮説を立てて検証しよう
PRをしているコミットを取得(PyGitHubを使用)
多い方が結果がでやすいが，時間の都合上数十件でも良い
コミットから様々なメトリクスを収集する
メトリクス例：変更されたファイル数，行数 ，コミットメッセージ
OPEN状態のものは，今後どう変化するか（CLOSEDもしくはMERGED）になるかわからないため，フィルタリングする
受理されたPR（MERGED）と却下さ
れたPR（CLOSED）にわけて，数値を可視化（箱ひげ図で表示）
有意差があるかどうかを確認するために統計検定を適用する
Mann-whiteneyのU検定など
各PRがマージされるか予測してみよう
データセットを準備しよう	
上記で取得したメトリクスとマージされたかどうかを1データとして，100件以上準備
データセットを8:2で分割し，学習データとテストデータにわける
学習データでロジスティック回帰モデルを構築
テストデータのPRがマージされるかを予測してみよう
Accuracy, Recal, Precision, F1メトリクスを計測してモデルを評価しよう
ロジスティック回帰モデルをRandomForestアルゴリズgムに変更して，精度が上がるかを見てみよう
RandomForestアルゴリズムのImportanceを取得して，どのメトリクスが最も効果があるかを確認しよう
5. 暇を潰そう（時間があまった人むけ）
ソースコード解析してみよう
Eclipse JSTのASTParcerを使ってASTを構築
https://qiita.com/esplo/items/fa93ab6136e7697ed1d9
https://www.ne.jp/asahi/hishidama/home/tech/eclipse/plugin/develop/jdt/ast.html
コメント抽出してみよう
SATD検出ツールを実行して，SATDを見つけてみよう
カバレッジを計測してみよう
Javaリポジトリをクローン
https://github.com/jhy/jsoup.git
Jacocoを設定
https://kazuhira-r.hatenablog.com/entry/2024/08/04/181730
テストを実行
mvn test jacoco:report
カバレッジファイルを見てみよう
HTMLファイルが
カバレッジファイルをプログラムから読み取ろう
XMLファイルでも出力されるはず
ミューテーションスコアを計測しよう
ミューテーションとはなにか調べよう
リポジトリをクローンしよう（小さいプロジェクトの方が良い）
https://github.com/Yutaro-Kashiwa/TestEffortEstimationTutorial
PITESTを設定しよう
https://pitest.org/
実行してみよう
プログラムの動きを観察してみよう（動的解析を使ってみよう）
リポジトリをクローン
https://github.com/Yutaro-Kashiwa/TestEffortEstimationTutorial
動的解析ツールを使えるようにビルドファイル（pom.xml）を修正
https://github.com/takashi-ishio/selogger
動的解析ツールと共にテストを実行


Appendix. 主要ツール（作業なし）
☆は下記に課題あり
プロジェクトデータ収集 
GitHubのスター数など
PyGitHub☆
変更履歴データ収集
コミットごとの変更箇所など
GitPython (https://github.com/gitpython-developers/GitPython)☆
checkout
diff 取得

リファクタリングの検出
Refactoring Miner2 ☆
https://refactoring.guru/refactoring
不具合混入コミットの特定
OpenSZZ
https://github.com/VladyslavBondarenko/OpenSZZ
注意：Originalは品質が低く，Fork先のほうが良い
ソースコードデータ
抽象構文木 (AST：Abstract Syntax Tree)
Eclipse.core
Refactoring Miner2 
コメントアウトの抽出
SoCCMiner
技術的負債データ収集
Self-admitted Technical Debt ☆
SATD Detector
https://github.com/Tbabm/SATDDetector-Core
CodeClone (重複コード)
CodeClone detector
テストデータ収集
テスト結果
JUnit
EvoSuite
テスト品質
PIT（https://pitest.org） 
トレース
SELogger
