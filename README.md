# Python + VSCodeのポータブル環境構築
## 必要なファイルのダウンロード
[ここ](https://winpython.github.io/) から *Winpython64-X.X.X.X `dot` .exe* をダウンロードする．<br>
> dotはpythonポータブルのみを含んだもの<br>

<br>

[ここ](https://code.visualstudio.com/download) から *VSCode-Win32-x64-X.X.X.*  `zip` をダウンロードする．<br>
> インストーラではなくzip版を落とす<br>

## ファイルの展開，配置
任意の場所（Cドライブの直下など）に環境やソースコードを格納するためのディレクトリを作成する（以下の例では *svlab22* ）．<br>
作成したディレクトリの中に *Winpython* と *VSCode* を展開する．その際，展開したディレクトリ名からバージョン番号等を削除しておくと便利．<br>
さらにソースコードを格納するための空ディレクトリを作成しておく<br>

```
svlab
 ∟ WPy64-XXXXX
 ∟ VScode
 ∟ SourceCode
```

## 環境設定(1)
WPy64-XXXXX / scripts フォルダ内の *winvscode.bat* を編集する．5行目～6行目の code.exe へのパスを展開した場所への相対パスに変更する．<br>

> - original
>  ```
>  if exist "%WINPYDIR%\..\t\vscode\code.exe" (
>      "%WINPYDIR%\..\t\vscode\code.exe" %*
>  ) else (
>  ```
> 
>  - rewrite
>  ```
>  if exist "%WINPYDIR%\..\..\vscode\code.exe" (
>      "%WINPYDIR%\..\..\vscode\code.exe" %*
>  ) else (
> ```

```
@echo off
rem launcher for VScode
call "%~dp0env_for_icons.bat" %*
rem cd/D "%WINPYWORKDIR1%"
if exist "%WINPYDIR%\..\..\vscode\code.exe" (
    "%WINPYDIR%\..\..\vscode\code.exe" %*
) else (
if exist "%LOCALAPPDATA%\Programs\Microsoft VS Code\code.exe" (
    "%LOCALAPPDATA%\Programs\Microsoft VS Code\code.exe"  %*
) else (
    "code.exe" %*
))
```

WPy64-XXXXX / scripts フォルダ内の *env.bat* を編集する．環境変数 *pythonpath* を追加して，メニュー，ボタンからの実行に適応させる．<br>

```
set PYTHONPATH=%WINPYDIRBASE%\..\SourceCode\mylibs\;%WINPYDIR%\Lib\site-packages
```

VSCode フォルダの直下に *data* フォルダ（空）を作成する．<br>

## 環境設定(2)
WPy64-XXXXX フォルダ直下の *VS Code.exe* をダブルクリックする．<br>
> 環境設定(1)が正しく設定されていれば VS Code が起動する．<br>
> 日本語パッケージのインストールのポップアップが上がるので，同意して VS Code を再起動する．<br>
> 外観，テーマを任意で選択する．<br>

<br>

エクスプローラ メニューから *フォルダーを開く* ボタンをクリックし，環境設定(1)で作成した SourceCode フォルダを選択する．<br>
> 作成者に関する質問のポップアップは *信頼する* にチェックを入れる．<br>

<br>

左のメニューアイコンから *拡張機能* ボタンを押し，*python* 拡張機能を検索してインストールする．<br>
 *python* 拡張機能のページにある *管理* （歯車）ボタンをクリックし， *拡張機能の設定* を選択する．タブ内にある *settings.jsonで編集* を選択する．<br>
settings.json を以下のように編集し，VS Codeを再起動する．<br>
> *update.mode* は VS Code の自動アップデートの設定
> *mylibs* へのパスは自作ライブラリへの参照と補完用．

```
{
    "workbench.colorTheme": "選択したテーマ",
    "update.mode": "none",
    "python.defaultInterpreterPath": "${workspaceFolder}\\..\\WPy64-310111\\python-3.10.11.amd64\\python.exe",
    "python.autoComplete.extraPaths": [
        "${workspaceFolder}\\..\\sourcecode\\mylibs",
        "${workspaceFolder}\\..\\WPy64-39100\\python-3.9.10.amd64\\Lib\\site-packages",
    ],
    "python.analysis.extraPaths": [
        "${workspaceFolder}\\..\\sourcecode\\mylibs",
        "${workspaceFolder}\\..\\WPy64-39100\\python-3.9.10.amd64\\Lib\\site-packages",
    ],
}
```

*settigs.json* に実行環境に読み込ませるライブラリパスを追記する．<br>
> 下記はWindows11の場合（powershellがデフォルトでインストールされている環境）．Windows10用にCommand Prompt使用時のライブラリも追記しておく．
> *env* は自作ライブラリへのパス．

```

"terminal.integrated.defaultProfile.windows": "Windows PowerShell",
"terminal.integrated.profiles.windows": {
    "PowerShell": {
        "source": "PowerShell",
        "icon": "terminal-powershell",
        "env": {
            "PYTHONPATH": "${workspaceFolder}\\..\\sourcecode\\mylibs; ${workspaceFolder}\\..\\WPy64-310111\\python-3.10.11.amd64\\Lib\\site-packages"
        },
    },
    "Windows PowerShell": {
        "source": "PowerShell",
        "icon": "terminal-powershell",
        "env": {
            "PYTHONPATH": "${workspaceFolder}\\..\\sourcecode\\mylibs; ${workspaceFolder}\\..\\WPy64-310111\\python-3.10.11.amd64\\Lib\\site-packages"
        },
    },
    "Command Prompt": {
        "path": [
            "${env:windir}\\Sysnative\\cmd.exe",
            "${env:windir}\\System32\\cmd.exe"
        ],
        "env": {
            "PYTHONPATH": "${workspaceFolder}\\..\\sourcecode\\mylibs"
        },
        "args": [],
        "icon": "terminal-cmd"
    },
},
```
## 環境設定(3)
WPy64-XXXXX の VS Code.exe を実行するための起動用 *.bat* ファイルを作成する<br>
> 作成環境のルート直下に作成する

```
svlab
 ∟ WPy64-XXXXX
 ∟ VScode
 ∟ SourceCode
 ∟ svlab_start.bat
```
*.bat* ファイルの内容は以下の通り． *--locale en* を指定すると英語モードで起動する
```
start "" ".\WPy64-XXXXX\VS Code.exe" ..\..\SourceCode --locale ja
exit/b
```

## Pythonライブラリのインストール
WPy64-XXXXX フォルダ直下の *VS Code.exe* からVSCodeを起動する．<br>
*ターミナル* メニューからターミナルウィンドウを開く．
1. pythonのバージョン確認
```
% python -V
Python X.X.X
```
2. インストールされたライブラリの確認
```
% pip list
Package               Version
--------------------- ------------
```
3. 必要なライブラリのインストール

```
% pip install opencv-python
% pip install opencv-contrib-python
% pip install mediapipe
% pip install scipy
% pip install pyqt5
% pip install pyqtgraph
% pip install cmake
% pip install imutils

% pip install scikit-learns

% pip install pywin32       #スクリーンキャプチャ用(win32gui)
% pip install pyautogui     #スクリーンキャプチャ用

% pip install pydirectinput #エミュレーション用
```

***

 - dlibはpipでインストール可能だが， *setup.py* が走るので，Cコンパイラ環境とcmakeが必要．<br>
[Visual Studio Community (無償版)](https://visualstudio.microsoft.com/ja/free-developer-offers/) のVisual C++アプリケーションのインストールを事前に行っておく．

```
% pip insatll cmake
% pip install dlib
```

 - [OpenCVのHaar Cascadeの学習済みサンプルへのリンク](https://github.com/opencv/opencv/tree/master/data/haarcascades)
 - [dlibの学習済みサンプル等へのリンク](http://dlib.net/files/)
 - [OpenCV FaceMark APIの説明へのリンク](https://docs.opencv.org/4.x/d7/dec/tutorial_facemark_usage.html)


4. 自作ライブラリの追加

*mylibs* 自作ライブラリの中に， *myCapture* というパッケージ， *camera_selector.py* というクラスを構成する場合，<br>
*myCapture* 内に，下記のような内容の *\_\_init\_\_.py* を作成する必要がある．<br>

- フォルダ構成
 ```
 mylibs
 ∟ myCapture
   ∟ camera_selector.py
   ∟ __init__.py 
 ```

 - \_\_init\_\_.py の内容
```
from myCapture.camera_selector import *
```

> 上記の *settings.json* の設定が正しければ，ライブラリのインポートは，
> ```
> from myCapture import camera_selector
> ```
