---
created: 2025-01-25 Sat 20:54
updated: 2026-02-28 Sat 10:56
---
1. リポジトリをフォークする。  
   https://github.com/anuraghazra/github-readme-stats
2. Github API のアクセストークンを発行する。
	1. 画面右上のアイコンから「Settings」→「Developer settings」
	2. 「Personal access tokens」→「Tokens(classic)」→「Generate new token」
	3. Token name, Expiration を設定
	4. Select scopes は「repo」「user」を選択
	5. 「Generate token」を押下
3. Vercel にログイン
4. 「Add New...」→「Project」を押下
5. Git Provider を選択→github readme stats の「Import」を押下  
   (選択欄にない場合は画面に従って Vercel のインストールを行う。対象は github readme stats のみでよい)
6. Configure Project 画面の Enviroment Variables に Github API のアクセストークンを追加する  
   Name: PAT_1  
   Value: アクセストークン
7. Deploy 実行
8. Dashboard 画面の DEPLOYMENT に記載のドメインで github readme stats のリンクを書き換える

書き換え前  
<img height="200px" src="https://github-readme-stats.vercel.app/api?username=iwbc-mzk&count_private=true&show_icons=true&theme=darcula" />  
書き換え後  
<img height="200px" src="https://github-readme-stats-8fbvjo0t0-iwbc-mzk.vercel.app/api?username=iwbc-mzk&count_private=true&show_icons=true&theme=darcula" />
