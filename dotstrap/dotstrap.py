import click
import subprocess, os, shutil
import pexpect, time

# https://www.atlassian.com/git/tutorials/dotfiles

# git init --bare $HOME/.cfg
# alias config='/usr/bin/git --git-dir=$HOME/.cfg/ --work-tree=$HOME'
# config config --local status.showUntrackedFiles no
# echo "alias config='/usr/bin/git --git-dir=$HOME/.cfg/ --work-tree=$HOME'" >> $HOME/.bashrc

def runccore(*args):
    p = pexpect.spawn(" ".join(args))
    lines = p.readlines()
    for l in lines:
        click.echo(click.style(' .g. ', fg='cyan'),nl=False)
        click.echo(l,nl=False)
    timeout=30
    while p.isalive() and timeout>0:
        click.echo(click.style('.', fg='cyan'))
        time.sleep(1)
        timeout-=1
    p.close()
    click.echo(click.style('', fg='cyan'),nl=True)

    return p.exitstatus

    retval = subprocess.run( list(args), check=False, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, universal_newlines=True)
    if retval.stdout != "":
        [click.echo( click.style(' .git.     ', fg='cyan') + l ) for l in retval.stdout.split("\n")]
    return retval

def run(*args):
    return runccore( 'git',"--git-dir=%s/.dotstrap" % os.environ["HOME"], "--work-tree=%s" % os.environ["HOME"], *args )

def echo(s):
    click.echo( click.style('.ds. ', fg='magenta') + s )

@click.group()
def cli():
    """Git wrapper for dotfile management via bare git repository

Inspired by
https://www.atlassian.com/git/tutorials/dotfiles
and
https://news.ycombinator.com/item?id=11071754
    """
    pass

@click.command()
@click.argument('repo')
def init( repo ):
    """Initializes dotstrap with a remote git repository"""
    runccore("git", "init", "--bare", "%s/.dotstrap" % os.environ["HOME"])
    run( "config", "--local", "status.showUntrackedFiles", "no" )
    run( "remote", "remove", "origin" )
    run( "remote", "add", "origin", repo )
    run( "pull", "--rebase", "origin", "master" )
    if run( "push", "origin", "master" ) != 0:
        echo(click.style('could not push to remote master - did you create an empty repo first?', fg="red"))
        return
    echo('initialize done')

@click.command()
def destroy():
    """WARNINIG: Destroys your local dotstrap git repo"""
    try:
        if click.confirm(click.style('.dotstrap. ',fg="magenta")+'This will destroy your local dotstrap repository, are you sure?'):
            shutil.rmtree("%s/.dotstrap" % os.environ["HOME"])
            echo(click.style('destroyed your git repo from localhost',fg="yellow"))
        else:
            echo(click.style('aborted',fg="yellow"))

    except OSError as e:
        echo(click.style('error, could not destroy your dotstrap repo - have you already destroyed it?', fg="red"))


@click.command()
@click.argument('args', nargs=-1)
def status():
    """Git status"""
    #run( "remote", "show", "origin" )
    run( "status", *args )
    echo(click.style('done', fg="green"))


@click.command()
@click.argument('args', nargs=-1)
def diff(args):
    """Git diff"""
    run( "diff", *args )
    echo(click.style('done', fg="green"))

@click.command()
def sync():
    """Git sync with remote origin"""
    run( "pull", "--rebase", "origin", "master" )
    if run( "push", "origin", "master" ) != 0:
        echo(click.style('could not push to remote master - repos out of sync?', fg="red"))
        return
    echo(click.style('repos synced', fg="green"))

@click.command()
@click.argument('args', nargs=-1)
def commit(args):
    """Git commits any pending files"""
    if len(args)==0:
        run( "commit", "-a", "-m", "Updated files" )
    else:
        run( "commit", *args )
    echo(click.style('all changes committed locally', fg="green") + click.style(' (sync if you want them remote too)',fg="blue"))

@click.command()
@click.argument('filename')
def add( filename ):
    """Adds a file from your system to your dotstrap repo"""
    if run( "add", filename ) != 0:
        return
    if run( "commit", "-m", "Added %s" % filename ) != 0:
        return
    if run( "push", "origin", "master" ) != 0:
        return
    echo(click.style('%d added locally' % fliename, fg="green") + click.style(" (don't forget to commit and sync)",fg="blue"))


@click.command()
@click.argument('args', nargs=-1)
def git( args ):
    """Manually run arbitrary git commands"""
    run( *args )

cli.add_command(init)
cli.add_command(destroy)
cli.add_command(status)
cli.add_command(diff)
cli.add_command(sync)
cli.add_command(commit)
cli.add_command(add)
cli.add_command(git)

if __name__ =="__main__":
    cli()
