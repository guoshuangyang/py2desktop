# 使用须知

使用venv虚拟环境， 使用py2app打包

## 创建虚拟环境
```shell
python3 -m venv venv
```

## 激活虚拟环境
```shell
source venv/bin/activate
```

## 虚拟环境下安装依赖

```shell
pip install -r requirements.txt
python setup.py py2app
```

## 运行（开发）
```shell
python main.py
```

## 打包
```shell
python setup.py py2app
```

## 打包（调试）
```shell
# python setup.py py2app -A
# pyinstaller Scanner.spec
```

## 生成requirements.txt
```shell
pipreqs . --force --ignore venv,dist,build,.eggs
```