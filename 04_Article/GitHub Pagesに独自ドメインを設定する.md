参考: [GitHub Pages サイトのカスタムドメインを管理する - GitHub Docs](https://docs.github.com/ja/pages/configuring-a-custom-domain-for-your-github-pages-site/managing-a-custom-domain-for-your-github-pages-site#configuring-a-subdomain)

## 1. GitHub のリポジトリに独自ドメインを設定する

1. リポジトリの「Setting」→「Code and automation」の「Pages」を開く
2. Custom domain に独自ドメインを入力し、「Save」を押下する  
   ![[Pasted image 20240302143028.png]]

ブランチから直接サイトを公開している場合は、自動で `CNAME` ファイルを追加するコミットが作成される。  
カスタムのGitHub Actionsワークフローを使用してサイトを公開している場合は、自動で作成されないため手動で追加を行う。

- ファイル名: CNAME
- 記載内容: <利用したい独自ドメイン>

>[!Warning]  
> CNAME ファイルが存在しない場合、GitHub Pages のデプロイ毎に独自ドメインの設定がリセットされてしまう。

## 2. DNS にレコードを登録する

### サブドメインを利用しない場合

apex ドメインが GitHub Pages の IP アドレスを指すように設定する。  
2024 年 3 月時点では以下の通り。

```shell
185.199.108.153
185.199.109.153
185.199.110.153
185.199.111.153
```

IPv6 を利用したい場合は AAAA レコードを作成する。

```shell
2606:50c0:8000::153
2606:50c0:8001::153
2606:50c0:8002::153
2606:50c0:8003::153
```

試していないので不明だが、サブドメイン利用の場合と同じように CNAME 設定でも OK かも。

以下のコマンドで DNS レコードが正しく構成されたことを確認する。

```shell
$ dig WWW.EXAMPLE.COM +nostats +nocomments +nocmd
> ;WWW.EXAMPLE.COM.                    IN      A
> WWW.EXAMPLE.COM.             3592    IN      CNAME   YOUR-USERNAME.github.io.
> YOUR-USERNAME.github.io.      43192   IN      CNAME   GITHUB-PAGES-SERVER .
> GITHUB-PAGES-SERVER .         22      IN      A       192.0.2.1
```

### サブドメインを利用する場合

ホスト名に利用したいサブドメイン、指定先に `<username>.github.io` を指定した CNAME レコードを登録する。  
![[Pasted image 20240302143936.png]]

正しく DNS レコードが設定できたことを `dig <your domain> +nostats +nocomments +nocmd` で確認する。  
![[Pasted image 20240302144357.png]]
