1. リポジトリをフォークする。
   https://github.com/anuraghazra/github-readme-stats
2. Github APIのアクセストークンを発行する。
	1. 画面右上のアイコンから「Settings」→「Developer settings」
	2. 「Personal access tokens」→「Tokens(classic)」→「Generate new token」
	3. Token name, Expirationを設定
	4. Select scopesは「repo」「user」を選択
	5. 「Generate token」を押下
3. Vercelにログイン
4. 「Add New...」→「Project」を押下
5. Git Providerを選択→github readme statsの「Import」を押下
   (選択欄にない場合は画面に従ってVercelのインストールを行う。対象はgithub readme statsのみでよい)
6. Configure Project画面のEnviroment VariablesにGithub APIのアクセストークンを追加する
   Name: PAT_1
   Value: アクセストークン
7. Deploy実行
8. Dashboard画面のDEPLOYMENTに記載のドメインでgithub readme statsのリンクを書き換える

書き換え前
<img height="200px" src="https://github-readme-stats.vercel.app/api?username=iwbc-mzk&count_private=true&show_icons=true&theme=darcula" />
書き換え後
<img height="200px" src="https://github-readme-stats-8fbvjo0t0-iwbc-mzk.vercel.app/api?username=iwbc-mzk&count_private=true&show_icons=true&theme=darcula" />

