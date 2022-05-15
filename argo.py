from sre_parse import Verbose
import click
from cli import cli1, cli2, cli3


@click.command(
            cls = click.CommandCollection, 
            sources = [cli1.cli1, cli2.cli2, cli3.cli3]
)
#optionを追加すると以下のエラーが発生する
#Traceback (most recent call last):
#  File "argo.py", line 16, in <module>
#    cli()
#  File "/Users/kyoji0603/.anyenv/envs/pyenv/versions/anaconda3-2020.02/lib/python3.7/site-packages/click/core.py", line 764, in __call__
#    return self.main(*args, **kwargs)
#  File "/Users/kyoji0603/.anyenv/envs/pyenv/versions/anaconda3-2020.02/lib/python3.7/site-packages/click/core.py", line 717, in main
#    rv = self.invoke(ctx)
#  File "/Users/kyoji0603/.anyenv/envs/pyenv/versions/anaconda3-2020.02/lib/python3.7/site-packages/click/core.py", line 1134, in invoke
#    Command.invoke(self, ctx)
#  File "/Users/kyoji0603/.anyenv/envs/pyenv/versions/anaconda3-2020.02/lib/python3.7/site-packages/click/core.py", line 956, in invoke
#    return ctx.invoke(self.callback, **ctx.params)
#  File "/Users/kyoji0603/.anyenv/envs/pyenv/versions/anaconda3-2020.02/lib/python3.7/site-packages/click/core.py", line 555, in invoke
#    return callback(*args, **kwargs)
#TypeError: cli() got an unexpected keyword argument 'config'

def cli():
    pass

if __name__ == '__main__':
    cli()