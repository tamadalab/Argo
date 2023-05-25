# 🐝 Argo
# 概要
GitHubは1000万以上の膨大なリポジトリ数を誇り、ソフトウェアリポジトリのマイニングに興味を持つ研究者を惹きつけています。GitHubのリポジトリを分析・調査することで、ソフトウェア開発活動を改善するための貴重な知見を得ることができます。しかし、ソースコードの変更履歴やコミュニケーション履歴にアクセスするための標準的な方法は、現在のところ存在しない。

本論文では、GitHubからコミュニケーション履歴を取得することを目的とした「argo」というツールの実装を紹介します。Argoは、ユーザのGraphQLクエリを受け付けてGitHubに記録されたコミュニケーション履歴を取得し、その遷移を可視化するためのラインチャートを生成する。事例として、3種類のGraphQLクエリを実装し、GitHubにホストされている有名プログラミング言語の11のリポジトリから、スターゲイザー、イシュー、プルリクエストのデータをフェッチしました。

Argo を使用すると、驚くべき速度でデータをフェッチすることができました。スターゲイザー、イシュー、プルリクエストの1秒あたりのエントリ数は、それぞれ145.19、81.27、139.90でした。このうち、リポジトリ「golang/go」のスターゲイザーのデータ取得は最も時間がかかり、96,425件、716秒を要した。

以上、本ツールArgoは、GitHubからデータを取得し、取得した情報をもとに折れ線グラフを作成できることを実証しました。

## 個人アクセストークンの設定
queryディレクトリにあるStar.py, Issue.py, PullRequest.pyの個人アクセストークンを設定しないと動かない．
user側からコマンドラインで設定できるようにする．

# About
## License
[GNU General Public License version 3 (GPLv3)](https://www.gnu.org/licenses/gpl-3.0.ja.html)

## Logo  
![Honey_Bee_logo__4_-removebg-preview](https://github.com/tamadalab/Argo/assets/69036517/12077eb5-883c-4d53-af1f-6045486985c1)

https://www.canva.com/ より引用



## Project name comes from?
Auto Repository Graph Outputの略称である．<br>
"Argo"のロゴは，Argogorytes（アワフキバチ）から蜂のアイコンにする. 

# 入出力仕様
## Usage

```sh
argo [GLOBAL_OPTIONS] <COMMAND> [<ARGS>]
GLOBAL_OPTIONS
    -c, --config <CONFIG>    specify configuration file path.
    -h, --help               print this message.
COMMANDs
    help          print help message.
    fetch         fetch data from GitHub.
    draw          draw line chart from fetched data.
    list          list available queries and metrics.
    fetch-draw    fetch data and draw line chart.
```

### `argo fetch`

```sh
argo fetch [OPTIONS] <ARGS...>
OPTIONS
    -q, --query <QUERY>           specify the query. This option is mandatory.

    -c, --cache-dir <DIR>         specify the cache directory path.
        --ignore-cache            ignore the stored cache data.
        --no-cache                no cache the fetched data.
    -Q, --queries-dir <DIR>       specify the directory contains GraphQL queries.
ARGS
    specify GitHub repository by owner/name format.
```

### `argo draw`

```sh
argo draw [OPTIONS] <ARGS...>
    -m, --metric <METRIC>      specify the metric (chart script). This option is mandatory.

    -c, --cache-dir <DIR>      specify the cache directory path.
        --ignore-cache         ignore the stored cache data.
        --no-cache             no cache the fetched data.
    -d, --write-data <DEST>    set file name of graph data destination. if this option is absent, argo outputs no graph data.
    -f, --format <FORMAT>      specify the output image format. available: pdf, svg, and png. default: svg.
    -M, --metrics-dir <DIR>    specify the directory contains chart scripts.
    -u, --unit <UNIT>          specify the unit time. Default is 1M.
                               Available: nD, nW, nM, and nY. n is the integer number,
                                          D, W, M, Y means day, week, month, and year, respectively.
ARGS
    specify GitHub repository by owner/name format.
```

### `argo list`

```sh
argo list
    -M, --metrics-dir <DIR>    specify the directory contains chart scripts.
    -Q, --queries-dir <DIR>    specify the directory contains GraphQL queries.
```


### structure of `~/.config/argo` directories.

```sh
.config/argo
├── caches
│   ├── microsoft
│   │   └── vscode
│   │       ├── issues
│   │       ├── pullrequests
│   │       └── stargazers
│   └── ruby
│       └── ruby
├── config
│   └── default.json
├── metrics
│   ├── microsoft
│   │   └── vscode
│   │       ├── N-STAR
│   │       └── R-RIS
│   └── ruby
│       └── ruby
├── scripts
│   ├── LT-CIS.awk
│   ├── LT-RP.py
│   ├── N-RIS.rb
│   ├── N-STAR.py
│   ├── R-MGPR.py
│   ├── R-PRLP.py
│   └── R-RIS.py
└── queries
    ├── issues.graphql
    ├── pullrequests.graphql
    └── stargazers.graphql
```

## 出力
### fetch data
```
First Survey
200it [00:00, 1835581.62it/s, 2]                                                

200it [00:00, 1536375.09it/s, 2]                                                

Data acquisition completed! : 1.4907136
```
### draw chart
- GitHubで公開されている11のプログラミング言語を対象に８つのメトリクスを描画した．

<img src = "https://user-images.githubusercontent.com/69036517/172577380-d8397972-693c-40a3-b460-7d4c8f3ccafb.png" width = "320px"> <img src = "https://user-images.githubusercontent.com/69036517/172577395-17243e2b-1b8c-4109-a405-afec7275a636.png" width = "320px">
<img src = "https://user-images.githubusercontent.com/69036517/172577273-31b4ee49-9f78-44ba-837d-fa293f417d36.png" width = "320px">
<img src = "https://user-images.githubusercontent.com/69036517/172577456-dca4392f-6149-4c07-b031-f6442bc68a7f.png" width = "320px">
<img src = "https://user-images.githubusercontent.com/69036517/172577369-112cd315-dc87-4f2d-8573-61416714478f.png" width = "320px">
<img src = "https://user-images.githubusercontent.com/69036517/172580845-a21aa26d-28d0-4f49-9205-2d59f04ed5a7.png" width = "320px">
<img src = "https://user-images.githubusercontent.com/69036517/172577424-2e8cd21a-803a-47da-a59b-9639ba2f2a4a.png" width = "320px">
<img src = "https://user-images.githubusercontent.com/69036517/172581269-4924a22b-3c83-4405-92bc-5301a8ee3932.png" width = "320px">
