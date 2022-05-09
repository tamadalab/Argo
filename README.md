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
## CLI
### 基本的な操作
 ```sh
argo <COMMAND> <METRICS> [OPTIONS] <REPOSITORY...>

COMMAND
    draw         Draw a graph. (Default)
    get          Get the original data for graph drawing.
    help         Print this message.

METRICS     
    N_STAR       ユーザー数　　　     
    N_RIS        残イシュー数
    R_RIS        残イシュー率
    LT_CIS       イシュー生存率
    R_MGPR       マージされたプルリクエスト数
    LT_PR        プルリクエスト生存時間
    R_PRLP       参加者が欠けているプルリクエスト率

OPTIONS (grobal)
    -h,--help    Explain the specified command
    
REPOSITORY
    （userID | organizationID /repository name）
```
<br>


### それぞれのコマンド操作
#### draw
```sh
SYNOPSIS
    argo draw [<options>] <repository...>    
    
DESCRIPITION
    Draw a graph. (If multiple repositories are specified, a compared graph will be output.)
    
OPTIONS
    -t, --type <type>
        Specify the type of graph to output.
        he default is stargazers.
        Valid values are n_star, n-code, n-ris (remaing issue), r-ris, lt_is, n-mgpr (marge pullrequst), lt_pr, r_prlt.
        
    -c, --cache-dir <cache_dir>
        Specify the cache directory.
        The default is `~/.config/argo/caches`.
        
    -o, --output <output>
        Specify the graph data of the output destination.
```

#### get
```sh
SYNOPSIS
    argo get [<options>] <repository...>    
    
DESCRIPITION
    Get the original data for graph drawing.
    
OPTIONS 
    -c, --cache-dir <cache_dir>
        Specify the cache directory.
        The default is `~/.config/argo/caches`.
        
    -o, --output <output>
        Specify the graph data of the output destination.
```

### summary
```sh
SYNOPSIS
    argo summary [<options>] <repository...>    
    
DESCRIPITION
    Extract summary data.
    The output is the project name, the number of stars, the number of commits, 
    the number of issues, the number of pull requests, and the creation date and time.
    
OPTIONS 
    -c, --cache-dir <cache_dir>
        Specify the cache directory.
        The default is `~/.config/argo/caches`.
        
    -o, --output <output>
        Specify the graph data of the output destination.
```

#### help
```sh
SYNOPSIS
    argo help [-a|--all [--verbose]]    
    
DESCRIPITION
    With no options and no COMMAND or GUIDE given,
    the synopsis of the argo command and a list of the most commonly used Git commands are printed on the standard output.

    
OPTIONS 
    -a, --all
        Prints all the available commands on the standard output. 
        This option overrides any given command or guide name.
    
    --verbose
        When used with --all print description for all recognized commands.
        This is the default.
```

### 出力
  - 画像は先行研究のもの
  <img width="275" alt="スクリーンショット 2021-06-21 21 04 52" src="https://user-images.githubusercontent.com/69036517/122758916-5374df00-d2d4-11eb-90ec-da32cc536810.png">


### memo
- githubのバッヂ調査にも対応できるかも？
