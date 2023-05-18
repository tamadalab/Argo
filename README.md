# 🐝 Argo
# 概要
近年、開発者自身が自発的に提案できるソーシャルコーディングという新たなソフトウェア開発方式に注目されている。しかしながら、現状の「自発的ソフトウェア進化」を辿っている成功プロジェクトがどのように管理され、活発なコミュニティがどのように形成されているか分からない。

本研究では、より多くのプロジェクトに対して同様の調査を行い、自発的進化の良いパターン・悪いパターンを発見し、どこを改善したらより自発進化が見込めるのかを提案することを目的とする。
しかし、現状ではGraphQLを用いたデータ抽出には結構な労力が必要となるため、まずデータ分析を自動化するアプリケーションを作成する。

## 個人アクセストークンの設定
queryディレクトリにあるStar.py, Issue.py, PullRequest.pyの個人アクセストークンを設定しないと動かない．
user側からコマンドラインで設定できるようにする．

# About
## License
[GNU General Public License version 3 (GPLv3)](https://www.gnu.org/licenses/gpl-3.0.ja.html)

## Logo  
<img src = "https://user-images.githubusercontent.com/69036517/122642836-6017fc80-d147-11eb-8717-5d5664b589aa.png"
     width = "320px">

pngtreeから引用.
https://ja.pngtree.com/freepng/bee-animal-icon-honey-flying-bee-insect-bugs_3641499.html

## Project name comes from?
Argogorytes（アワフキバチ）から蜂のアイコンにする. 

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
