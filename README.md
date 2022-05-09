# 🐝 Argo
# 概要
近年、開発者自身が自発的に提案できるソーシャルコーディングという新たなソフトウェア開発方式に注目されている。しかしながら、現状の「自発的ソフトウェア進化」を辿っている成功プロジェクトがどのように管理され、活発なコミュニティがどのように形成されているか分からない。先行研究では、その開発方式で成功したGitHubで公開されているプロジェクトがAtom、Brackets、VSCodeを実験対象とし、GitHub GraphQL APIを用いて、どのような状態を辿ってきたかを分析することでその成功した要因を解明しています。

本研究では、より多くのプロジェクトに対して同様の調査を行い、自発的進化の良いパターン・悪いパターンを発見し、どこを改善したらより自発進化が見込めるのかを提案することを目的とする。しかし、現状ではGraphQLを用いたデータ抽出には結構な労力が必要となるため、まずデータ分析を自動化するアプリケーションを作成する。


# About
## License
[GNU General Public License version 3 (GPLv3)](https://www.gnu.org/licenses/gpl-3.0.ja.html)

## Logo  
![icon-removebg-preview](https://user-images.githubusercontent.com/69036517/122642836-6017fc80-d147-11eb-8717-5d5664b589aa.png)

pngtreeから引用.
https://ja.pngtree.com/freepng/bee-animal-icon-honey-flying-bee-insect-bugs_3641499.html

## Project name comes from?
Argogorytes（アワフキバチ）から蜂のアイコンにする. 

# 開発言語
java
 - 互換性がある事や実行環境を選ばない点から上記のプログラミング言語を使用する.
 
# 実行例
- 入力例
```sh
argo draw n_star tamadalab/argo
```
- 出力例
  - 画像は先行研究のもの
  <img width="275" alt="スクリーンショット 2021-06-21 21 04 52" src="https://user-images.githubusercontent.com/69036517/122758916-5374df00-d2d4-11eb-90ec-da32cc536810.png">

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

### 出力
  - 画像は先行研究のもの
  <img width="275" alt="スクリーンショット 2021-06-21 21 04 52" src="https://user-images.githubusercontent.com/69036517/122758916-5374df00-d2d4-11eb-90ec-da32cc536810.png">


### memo
- githubのバッヂ調査にも対応できるかも？
