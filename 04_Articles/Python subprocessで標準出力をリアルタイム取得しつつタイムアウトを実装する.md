---
tags:
  - article
  - Python
aliases: []
slug: 3f7e9a21-5c84-4d62-b891-6a0f2e7d4b38
created: 2026-07-16
updated: 2026-07-16 Thu 20:01
---
# Python subprocessで標準出力をリアルタイム取得しつつタイムアウトを実装する

## 概要

`subprocess.Popen` で子プロセスの標準出力をリアルタイムに取得しながら、`threading.Timer` によるタイムアウトと `psutil` によるプロセスkillを実装する方法。

`subprocess.run()`・`communicate()`・`call()` はタイムアウトをサポートするが、子プロセスが終了するまで標準出力を受け取れない。そのためリアルタイム取得には `subprocess.Popen` を直接使う必要がある。

## 標準出力のリアルタイム取得

`proc.stdout.readline` をイテレートすることでリアルタイムに標準出力を取得できる。

```python
import subprocess

def main(cmd):
    proc = subprocess.Popen(
        cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT
    )

    for line in iter(proc.stdout.readline, b""):
        line = line.rstrip().decode()
        print(line)

    proc.wait()

if __name__ == "__main__":
    cmd = "python sub.py"
    main(cmd)
```

`stderr=subprocess.STDOUT` により標準エラー出力を標準出力にマージしている。

出力テスト用スクリプト（`sub.py`）:

```python
import time

for i in range(0, 10):
    print(i, flush=True)
    time.sleep(1)
```

子プロセス側では `flush=True` を指定しないとバッファリングされてリアルタイムに出力されない。

> [!warning] `stdout=PIPE, stderr=PIPE` のデッドロック
> 標準出力と標準エラー出力を完全に分けて取得する場合、パイプバッファが詰まりデッドロックが発生する恐れがある。両方をリアルタイム取得するなら `ThreadPoolExecutor` を使うのが安全。

## threading.Timer によるタイムアウト

```python
from threading import Timer
import subprocess

def main(cmd, timeout=3):
    proc = subprocess.Popen(
        cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT
    )

    def kill_process(pid):
        pass  # killの処理をここに書く

    t = Timer(timeout, kill_process, [proc.pid])
    t.start()

    for line in iter(proc.stdout.readline, b""):
        line = line.rstrip().decode()
        print(line)

    t.cancel()
    proc.stdout.close()
    proc.wait()
```

`Timer(timeout, func, args)` は `timeout` 秒後に `func(*args)` を実行する。正常終了時は `t.cancel()` でタイマーをキャンセルする。

## psutil によるプロセスkill

`subprocess.Popen.kill()` は子孫プロセスをkillできない。`psutil` を使うと子孫プロセスも含めて確実にkillできる。

```python
import psutil

def killed(proc):
    print(f"process {proc} killed with exit code {proc.returncode}")

def kill_process(pid):
    t.cancel()
    try:
        parent = psutil.Process(pid)
    except psutil.NoSuchProcess as e:
        print(e)
        return

    procs = parent.children(recursive=True)
    procs.append(parent)
    for p in procs:
        try:
            p.kill()
        except Exception as e:
            print(e)
    gone, alive = psutil.wait_procs(procs, callback=killed)
```

| 関数 | 説明 |
|------|------|
| `psutil.Process(pid)` | PIDからプロセスオブジェクトを取得 |
| `parent.children(recursive=True)` | 全子孫プロセスのリストを取得 |
| `psutil.wait_procs(procs, callback=f)` | 全プロセスの終了を待機、終了済みに `callback` を実行 |

OSごとのkill動作:
- UNIX: `os.kill(pid, signal.SIGKILL)`
- Windows: `TerminateProcess`（`kill()` と `terminate()` は同じ動作）

## コード全体

```python
import psutil
import subprocess
from threading import Timer

def main(cmd, timeout=3):
    proc = subprocess.Popen(
        cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT
    )

    def killed(proc):
        print(f"process {proc} killed with exit code {proc.returncode}")

    def kill_process(pid):
        t.cancel()
        try:
            parent = psutil.Process(pid)
        except psutil.NoSuchProcess as e:
            print(e)
            return

        procs = parent.children(recursive=True)
        procs.append(parent)
        for p in procs:
            try:
                p.kill()
            except Exception as e:
                print(e)
        gone, alive = psutil.wait_procs(procs, callback=killed)

    t = Timer(timeout, kill_process, [proc.pid])
    t.start()

    for line in iter(proc.stdout.readline, b""):
        line = line.rstrip().decode()
        print(line)

    t.cancel()
    proc.stdout.close()
    proc.wait()

if __name__ == "__main__":
    cmd = "python sub.py"
    timeout = 3
    main(cmd, timeout)
```

## psutil.Popen の活用

`psutil.Popen` を使うとプロセス操作がより簡潔になる。`subprocess.Popen` と互換性があり、psutil固有のメソッドも使用可能。

```python
proc = psutil.Popen(
    cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT
)
procs = proc.parent().children(recursive=True)
```

引用元: [Pythonのsubprocessで標準出力をリアルタイムに取得しつつthreading.Timerとpsutilでタイムアウトを実装してみる | 専門卒ニートのブログ](https://ryo-fujinone.net/blog/archives/1573)
